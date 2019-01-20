import os
from PIL import Image
import re
from flask import current_app


def image_size_off(rootDir, file_name):
    #需要什么格式的图片自己手动改改就好了
    path = os.path.join(rootDir, file_name)
    im = Image.open(path)
    box = clipimage(im.size)
    region = im.crop(box)
    size = (60, 60)
    region.thumbnail(size, Image.ANTIALIAS)
    #这里保存thumbnail以后的结果
    region.save(
        os.path.join(current_app.config['UPLOAD_FOLDER'], file_name[:-4]+'_thumb.jpg'))
    box = ()

#取宽和高的值小的那一个来生成裁剪图片用的box
#并且尽可能的裁剪出图片的中间部分,一般人摄影都会把主题放在靠中间的,个别艺术家有特殊的艺术需求我顾不上
def clipimage(size):
    width = int(size[0])
    height = int(size[1])
    box = ()
    if (width > height):
        dx = width - height
        box = (dx / 2, 0, height + dx / 2,  height)
    else:
        dx = height - width
        box = (0, dx / 2, width, width + dx / 2)
    return box