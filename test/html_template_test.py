# This is a sample Python script.

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


def to_image(filepath: str, outputpath: str):
    # Use a breakpoint in the code line below to debug your script.
    return imgkit.from_file(filepath, outputpath)


def to_image_from_content(content: str, output_path: str):
    return imgkit.from_string(content, output_path)


def generate_video(frames: list, frame_intervals: list, output_path: str, fps=24) -> None:
    cv_images = []
    try:
        for i in range(len(frames)):
            cv_images.extend([frames[i]] * int(fps * frame_intervals[i]))
        cv_images = [cv.imread(i) for i in cv_images]
        # get the first image size
        height, width, _ = cv_images[0].shape
        container = av.open(output_path, mode='w')
        stream = container.add_stream('mpeg4', rate=fps)
        stream.width = width
        stream.height = height
        stream.pix_fmt = 'yuv420p'
        stream.bit_rate = width * height * 8
        for i in cv_images:
            # 转成pyav 的frame
            frame = av.VideoFrame.from_ndarray(i, format='bgr24')
            for packet in stream.encode(frame):
                container.mux(packet)
        for packet in stream.encode():
            container.mux(packet)
        container.close()

    except Exception as e:
        globle.LOGGER.error("generate video error", exc_info=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    html_content_file = "test.html"

    html_content_str = ("<h2>Hello from video creator!</h2><h2>This picture is created from String</h2><ul>" +
                        "<li>the content create from string</li>" +
                        "<li>See the View</li><li>Following is picture shown</li></ul><img src=\"pic.PNG\"" +
                        " style=\"width:50px; height:50px;\"/><img src=\"pic.PNG\"" +
                        " style=\"width:50px; height:50px;\"/>")

    output_path1 = "out1.jpg"
    output_path2 = "out2.jpg"
    img1_ret = to_image(html_content_file, output_path1)
    img2_ret = to_image_from_content(html_content_str, output_path2)
    img_paths = [output_path1, output_path2]
    intervals = [1.6, 5.8]
    generate_video(img_paths, intervals, "test_video.mp4")


