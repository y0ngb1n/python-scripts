#!/usr/bin/env python3
#coding: utf-8
#
# 用于「七牛」批量上传文件
# 参考：https://github.com/zhaoweizheng/pythonUpload
#
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import sys
import os
import time
import subprocess
import uuid
from glob import glob
import shutil

IMG_SUFFIX = ["jpg", "jpeg", "png", "bmp", "gif"]

# --------- 七牛云配置 ---------

ACCESS_KEY  = 'ACCESS_KEY'
SECRET_KEY  = 'SECRET_KEY'
BUCKET_NAME = 'BUCKET_NAME' #空间名
BUCKET_URL  = 'BUCKET_URL'  #空间外链地址

# --------- 七牛云配置 ---------

UPLOAD_RESULT_FILE = 'qiniu/images_url.txt'

# 图片来源目录
SOURCE_DIR = 'origin_images'
TARGET_DIR = 'qiniu/upload_success'

def init():
    # 目录是否存在
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

def batch_upload(images_path):
    if images_path is None:
        print('No image specified', file=sys.stderr)
        return

    size = len(images_path)
    index = 0
    digits_len = len(str(size))

    for img_path in images_path:
        index += 1
        print("[%s/%s] Uploading %s" %('{0:{width}}'.format(index, width=digits_len), size, img_path))

        qn = Auth(ACCESS_KEY, SECRET_KEY)
        # 上传后的文件名, None 为使用服务端返回的 hash 值, 当名字一样时不覆盖不新增
        key = None #str(uuid.uuid4())
        # 生成上传 token 并指定过期时间
        token = qn.upload_token(BUCKET_NAME, key, 3600)
        ret, err = put_file(token, key, img_path)
        if ret is not None:
            assert ret['hash'] == etag(img_path)

            img_qiniu_url = BUCKET_URL + ret['hash']

            write2txt(img_qiniu_url)

            # 移动文件
            shutil.move(img_path, TARGET_DIR)

            print("[%s/%s] \033[1;37;42m%s\033[0m" %('{0:{width}}'.format(index, width=digits_len), size, 'upload success!'))
            print("\t url: %s" %img_qiniu_url)
        else:
            print("[%s/%s] \033[1;37;41m%s\033[0m, %s" %('{0:{width}}'.format(index, width=digits_len), size, 'upload fail!', err), file=sys.stderr)

def write2txt(url):
    with open(UPLOAD_RESULT_FILE, 'a+') as note:
        note.write("%s\n" %url)
        note.close()

if __name__ == '__main__':
    init()
    # 寻找指定目录下所有符合要求的文件
    file_names = glob('{}/*'.format(SOURCE_DIR))
    batch_upload(file_names)
