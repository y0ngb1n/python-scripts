# coding: utf-8
# 批量压缩图片
# https://zhuanlan.zhihu.com/p/32246003

# pip install Pillow
from glob import glob
from PIL import Image
import os
import math

DEBUG = True

# 图片来源目录
SOURCE_DIR = 'origin_images'
# 压缩后图片的输出目录
TARGET_DIR = 'output'
# 压缩阈值（2M）
THRESHOLD = 2*1024*1024

'''
 @source_dir 图片源目录
 @target_dir 压缩图片输出目录
 @threshold  阈值
'''
def resize_images(source_dir, target_dir, threshold):
    # 寻找指定目录下所有符合要求的文件
    file_names = glob('{}/*'.format(SOURCE_DIR))
    # 目录是否存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for file_name in file_names:
        file_size = os.path.getsize(file_name)
        if file_size >= threshold:
            print(file_name)
            with Image.open(file_name) as img:
                width, height = img.size
                if width >= height:
                    new_width = int(math.sqrt(threshold / 2))
                    new_height = int(new_width * height * 1.0 / width)
                else:
                    new_height = int(math.sqrt(threshold / 2))
                    new_width = int(new_height * width * 1.0 / height)
                resized_img = img.resize((new_width, new_height))
                output_file_name = file_name.replace(source_dir, target_dir)
                resized_img.save(output_file_name)

if __name__ == '__main__':
    resize_images(SOURCE_DIR, TARGET_DIR, THRESHOLD)
