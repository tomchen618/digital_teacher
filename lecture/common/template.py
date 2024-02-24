# this is the frame template for the lecture
# version : 1.0
# created : Jan, 9, 2024
# author : Tom Chen
import io

from numpy.core.defchararray import lower

import globle
import inspect
import datetime
import imgkit
import cv2 as cv
import av
import os

from lecture.common import pdf_utils
from lecture.common.file_utils import get_create_lecture_directory, get_directory_name
from lecture.common.pdf_extractor import PdfExtractor


class LectureTemplate:
    def __init__(self, id: str, frame_absolute_directory: str,
                 frames: list, frame_intervals: list, interval_between: int, total_mms_interval: int,
                 store_file: str, created_by: str):
        if id == "":
            raise ValueError("Lecture template id is empty[L:" +
                             str(inspect.getframeinfo(inspect.currentframe()).lineno) + "]")
        self.id = id
        # frame picture path
        self.frame_absolute_directory = frame_absolute_directory
        self.lecture_dir = os.path.join(self.frame_absolute_directory, self.id)
        self.frames = frames
        # frame continuing time by seconds
        self.frame_intervals = frame_intervals
        # interval between two pictures
        self.interval_between = interval_between
        # total seconds for the lecture
        self.total_mms_interval = total_mms_interval
        self.created_by = created_by
        self.modified_by = ""
        self.store_file = store_file
        self.created = datetime.datetime.now()
        self.updated = self.created

    def to_video(self):
        self.store_file = "lt_" + type(self).__name__ + "_" + self.id + ".mp4"
        ret = self.generate_video()
        return ret

    def generate_video(self, fps=24):
        cv_images = []
        try:
            for i in range(len(self.frames)):
                if os.path.exists(self.frames[i]):
                    cv_images.extend(self.frame_intervals[i] * int(fps * self.frame_intervals[i]))
                else:
                    globle.LOGGER.error("Template file is not exists[L:" +
                                        str(inspect.getframeinfo(inspect.currentframe()).lineno) + "]")
            cv_images = [cv.imread(i) for i in cv_images]
            # get the first image size
            height, width, _ = cv_images[0].shape
            container = av.open(self.store_file, mode='w')
            stream = container.add_stream('mpeg4', rate=fps)
            stream.width = width
            stream.height = height
            stream.pix_fmt = 'yuv420p'
            stream.bit_rate = width * height * 8
            for i in cv_images:
                # to pyav frame
                frame = av.VideoFrame.from_ndarray(i, format='bgr24')
                for packet in stream.encode(frame):
                    container.mux(packet)
            for packet in stream.encode():
                container.mux(packet)
            container.close()
            return True
        except Exception as e:
            globle.LOGGER.error("generate video error[L:" +
                                str(inspect.getframeinfo(inspect.currentframe()).lineno) + "]", exc_info=True)
            return False


class FrameTemplate:
    def __init__(self, id: str, content_str: str, second_interval: float, created_by: str):
        if id == "":
            raise ValueError("Lecture template id is empty[L:" +
                             str(inspect.getframeinfo(inspect.currentframe()).lineno) + "]")
        self.id = id
        # content defined by pure html format
        self.content_str = content_str
        # float value for second interval
        self.second_interval = second_interval
        self.created_by = created_by
        self.modified_by = ""
        self.created = datetime.datetime.now()
        self.updated = self.created

    def to_picture(self):
        tmp_file = "ft_" + type(self).__name__ + "_" + self.id + ".ltp"
        ret = imgkit.from_string(self.content_str, tmp_file)
        return ret

class PdfLecture:
    def __init__(self, id: str, lecture_name: str, frame_absolute_directory: str, pdf_file_path: str, explanation: [],
                 frame_intervals: list, interval_between: float, total_mms_interval: float,
                 store_file: str, minute_words=150, created_by=''):
        if id == "":
            raise ValueError("Lecture template id is empty[L:" +
                             str(inspect.getframeinfo(inspect.currentframe()).lineno) + "]")
        self.id = id
        # frame picture path
        if lecture_name == "":
            self.lecture_name = get_directory_name(pdf_file_path)
        else:
            self.lecture_name = lecture_name
        if self.lecture_name.rfind(".pdf") != len(pdf_file_path) - 4:
            self.lecture_name = self.lecture_name[0:len(self.lecture_name) - 4]

        if pdf_file_path != "" and pdf_file_path.rfind(".pdf") != len(pdf_file_path) - 4:
            self.pdf_file_path = pdf_file_path + ".pdf"
        else:
            self.pdf_file_path = pdf_file_path
        self.frame_absolute_directory = frame_absolute_directory
        self.lecture_dir = os.path.join(self.frame_absolute_directory, self.id)
        self.frames = []
        self.explanations = explanation
        # frame continuing time by seconds
        self.frame_intervals = frame_intervals
        # interval between two pictures
        self.interval_between = interval_between
        # total seconds for the lecture
        self.total_mms_interval = total_mms_interval
        self.created_by = created_by
        self.modified_by = ""
        self.store_file = store_file
        self.minute_words = minute_words
        self.created = datetime.datetime.now()
        self.updated = self.created
        self.video_file = self.id + ".mp4"
        self.check_directory()
        self.pdf_extractor = PdfExtractor(self.id, self.pdf_file_path,self.pdf_file_path, self.lecture_dir,
                                          1.0, 1.0, 0)

        self.frames = self.pdf_extractor.pg_video_img_dirs

    def check_directory(self):
        if self.frame_absolute_directory == "":
            if ((str.lower(self.pdf_file_path).rfind(".pdf") == len(self.pdf_file_path) - 4) or
                    (self.lecture_name == self.pdf_file_path)):
                self.frame_absolute_directory = get_create_lecture_directory(self.lecture_name, self.id)
            else:
                self.frame_absolute_directory = self.pdf_file_path[:len(self.pdf_file_path) - 4]

        self.lecture_dir = self.frame_absolute_directory
        return self.frames is not None

    def to_video(self):
        if self.store_file == "":
            self.store_file = "lt_" + type(self).__name__ + "_" + self.id + ".mp4"
        elif self.store_file.rfind(".mp4") != len(self.store_file) - 4:
            self.store_file += ".mp4"
        ret = self.generate_video()
        return ret

    def save_video(self, cv_video: list, file_index=0, fps=24):
        # cv_images = [cv.imread(j) for j in cv_images]
        # get the first image size
        height, width, _ = cv_video[0].shape
        if file_index > 0:
            temp_file = self.store_file[0:len(self.store_file) - 4] + "_" + str(file_index) + ".mp4"
            self.video_file = os.path.join(self.lecture_dir, temp_file)
        else:
            self.video_file = os.path.join(self.lecture_dir, self.store_file)

        container = av.open(self.video_file, mode='w')
        stream = container.add_stream('mpeg4', rate=fps)
        stream.width = width
        stream.height = height
        stream.pix_fmt = 'yuv420p'
        if width * height > 128000:
            stream.bit_rate = width * height * 8
        else:
            stream.bit_rate = 128000 * 8

        for i in cv_video:
            # to pyav frame
            frame = av.VideoFrame.from_ndarray(i, format='bgr24')
            for packet in stream.encode(frame):
                container.mux(packet)
        for packet in stream.encode():
            container.mux(packet)
        container.close()

    def generate_video(self, fps=25):
        cv_images = []
        try:
            c = len(self.frame_intervals)
            if len(self.frames) == 0:
                return False
            cv_video = []
            k = 0
            index = 0
            for i in range(len(self.frames)):
                if os.path.exists(self.frames[i]):
                    stream_temp = cv.imread(self.frames[i])
                    if i >= c:
                        for j in range(int(fps * self.frame_intervals[c - 1])):
                            cv_video.append(stream_temp)
                    else:
                        for j in range(int(fps * self.frame_intervals[i])):
                            cv_video.append(stream_temp)
                k += 1
                if k >= globle.pdf_max_pages:
                    k = 0
                    index += 1
                    self.save_video(cv_video, index, fps)
                    cv_video = []

            if len(cv_video) > 0:
                self.save_video(cv_video, index, fps)
            return True
        except Exception as e:
            globle.LOGGER.error("generate video error[L:" +
                                str(inspect.getframeinfo(inspect.currentframe()).lineno) + "]", exc_info=True)
            return False
