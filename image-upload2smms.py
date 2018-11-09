#!/usr/bin/env python3
#coding: utf-8
#
# 用于 sm.ms 批量上传文件
# 参考：https://github.com/hlx98007/smms-cli
#
import sys
import os
from glob import glob
import requests
import json
import ntpath
import shutil

IMG_SUFFIX = ["jpg", "jpeg", "png", "bmp", "gif"]

API_URL_UPLOAD = 'https://sm.ms/api/upload'

UPLOAD_RESULT_FILE = 'smms/images_url.txt'


# 图片来源目录
SOURCE_DIR = 'origin_images'
TARGET_DIR = 'smms/upload_success'

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

    for img_path in images_path:
        index += 1
        print("[%s/%s] Uploading %s" %(index, size, img_path))
        form = {'smfile': open(img_path, 'rb')}
        api_result = requests.post(API_URL_UPLOAD, files=form)
        result = json.loads(api_result.text)
        if 'success' == result['code']:
            img_smms_url = result['data']['url']
            img_smms_delete_url = result['data']['delete']

            write2txt(img_smms_url)

            # 移动文件
            shutil.move(img_path, TARGET_DIR)

            print("[%s/%s] upload success!" %(index, size))
            print("\t url: %s" %img_smms_url)
            print("\t delete url: %s" %img_smms_delete_url)
        else:
            print("[%s/%s] upload fail!" %(index, size), file=sys.stderr)

def write2txt(url):
    with open(UPLOAD_RESULT_FILE, 'a+') as note:
        note.write("%s\n" %url)
        note.close()

if __name__ == '__main__':
    init()
    # 寻找指定目录下所有符合要求的文件
    file_names = glob('{}/*'.format(SOURCE_DIR))
    batch_upload(file_names)
