import inspect
import os
import re
import fitz
from pypinyin import lazy_pinyin

import globle

"""
parse pdf to text
file_path pdf file path
"""


def parsePDF(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc.pages():
            text += page.get_text()
        doc.close()
        if text:
            return text


'''
# convert pdf to picture
pdf_path pdf file path
img_directory picture file directory
zoom_x x zoom ratio
zoom_y y zoom ratio
rotation_angle rotation angle
'''


def pdf_images(pdf_path, img_directory, zoom_x, zoom_y, rotation_angle):
    try:
        pics = []
        file_name = pdf_path
        if is_chinese(pdf_path):
            file_name = convert_to_pinyin(pdf_path)

        if str.lower(pdf_path).rfind(".pdf") != len(pdf_path) - 4:
            pdf_path += ".pdf"
        else:
            file_name = dir_name = os.path.basename(pdf_path)
            if is_chinese(file_name):
                file_name = convert_to_pinyin(file_name[0:len(file_name) - 4])
            else:
                file_name = file_name[0:len(file_name) - 4]

        doc = fitz.open(pdf_path)
        pgs = doc.pages()
        i = 0
        for pg in pgs:
            # 设置缩放和旋转系数
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
            pm = pg.get_pixmap(matrix=trans, alpha=False)
            # save to files
            file_path = os.path.join(img_directory, str(file_name) + "_" + str(i) + ".png")
            pm.save(file_path)
            pics.append(file_path)
            i += 1
        doc.close()
        return pics
    except Exception as e:
        globle.LOGGER.error("convert pdf error[L:" +
                            str(inspect.getframeinfo(inspect.currentframe()).lineno) + "]", exc_info=True)
        return None


def convert_to_pinyin(text: str):
    pinyin = lazy_pinyin(text)
    # bind together from pinyin
    for i in range(len(pinyin)):
        if pinyin[i].isupper():
            pinyin[i] = pinyin[i] + "_"
        else:
            pinyin[i] = pinyin[i][0]
    return ''.join(pinyin)


def is_chinese(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    else:
        return False


def check_chinese(content: str):
    # Unicode范围内的汉字编码
    pattern = r'[\u4e00-\u9fa5]'
    if re.search(pattern, content, 0):
        return True
    else:
        return False

