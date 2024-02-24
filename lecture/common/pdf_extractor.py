import os

from fitz import fitz
from pydub import AudioSegment

from lecture.common.pdf_utils import is_chinese


class PdfPage:
    def __init__(self, id: str, captions: [], total_words=0, page_number=0, total_pages=0):
        self.id = id
        self.captions = captions
        self.total_words = total_words
        self.page_number = page_number
        self.total_pages = total_pages
        self.images = []
        self.tables = []
        self.text_blocks = []

    def set_images(self, imgs: []):
        self.images = imgs

    def set_tables(self, tbs: []):
        self.tables = tbs


class PdfExtractor:
    def __init__(self, id: str, file_path: str, img_directory: str, file_name: str, zoom_x, zoom_y, rotation_angle):
        self.id = id
        self.file_path = file_path
        self.total_pages = 0
        self.img_directory = img_directory
        self.file_name = file_name
        self.zoom_x = zoom_x
        self.zoom_y = zoom_y
        self.rotation_angle = rotation_angle
        # PdfPage list
        self.pdf_pages = []
        self.pg_video_img_dirs = []
        self.extract_all()

    def save_as_image(self, pg, page_no: int):
        # 设置缩放和旋转系数
        trans = fitz.Matrix(self.zoom_x, self.zoom_y).prerotate(self.rotation_angle)
        pm = pg.get_pixmap(matrix=trans, alpha=False)
        # save to files
        file_path = os.path.join(self.img_directory, str(self.file_name) + "_" + str(page_no) + ".png")
        pm.save(file_path)
        self.pg_video_img_dirs.append(file_path)

    def extract_all(self, convert_img=True):
        if not os.path.exists(self.file_path):
            return False
        doc = fitz.open(self.file_path)
        pgs = doc.pages()
        pg_number = 0
        self.pg_video_img_dirs = []
        for pg in pgs:
            txt_blocks = pg.get_text("blocks")
            captions = []
            total_words = 0
            if convert_img:
                self.save_as_image(pg, pg_number)

            for txt_blk in txt_blocks:
                caption_temp = []
                caption_splits = []
                if len(txt_blk) > 4:
                    caption_splits = str(txt_blk[4]).split('\n')
                elif len(txt_blk) == 1:
                    caption_splits = str(txt_blk[0]).split('\n')
                for i in range(len(caption_splits)):
                    # remove the item not start with a word
                    texts = str(caption_splits[i]).split(',')
                    for t in texts:
                        str_temp = str.strip(t).replace('\'', '')
                        if len(str_temp) > 0 and (str.lower(str_temp[0]) != str_temp[0] or is_chinese(str_temp[0])):
                            caption_temp.append(str_temp)
                            total_words += len(str_temp.split(' '))
                captions.extend(caption_temp)
            pdfg = PdfPage(id=self.id, total_words=total_words, captions=captions, page_number=pg_number)
            pdfg.id = self.id
            pdfg.text_blocks = captions
            pdfg.images = pg.get_images()
            self.pdf_pages.append(pdfg)
            pg_number += 1

        doc.close()
        # set the total_pages for the pdf
        for i in range(pg_number):
            self.pdf_pages[i].total_pages = pg_number
