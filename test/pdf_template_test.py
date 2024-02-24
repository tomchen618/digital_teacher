# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import imgkit
import av
import cv2 as cv
import globle
from lecture.common import pdf_utils
from lecture.common.template import PdfLecture

from hmmlearn import hmm
import numpy as np

if __name__ == '__main__':
    pdf_file = 'd:\\sourcecode\\Lecture\\resource\\pdf_file\\BRICS.pdf'
    explanations = ["This is the course for HTML language, which is the website programming language. " +
                    "If you want to know more about it read this book",
                    "This is the index for this course. You can find the directories for each unit.",
                    "", "Thanks for who is concerned.", "The first unit I must explain."]
    frame_intervals = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    total_mms_interval = np.sum(frame_intervals)
    pdf_lecture = PdfLecture("id_test", "", "",
                             pdf_file, explanations, frame_intervals,
                             0.5, total_mms_interval, "pdf_testing", 180, "")

    if len(pdf_lecture.frames) > 0:
        pdf_lecture.to_video()
        # step 1 is to put the lip image to the vid
        print("video is done")
