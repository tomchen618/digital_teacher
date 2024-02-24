import enum

import cv2
import numpy as np
from PIL import Image


class VideoAligment(enum.Enum):
    Left = 0
    Right = 1
    Top = 3
    Bottom = 4
    Center = 5


#
# def images_bind_horizontal(left_image, right_image):
#     images = [left_image, right_image]
#     widths, heights = zip(*(i.size for i in images))
#     total_width = sum(widths)
#     max_height = max(heights)
#
#     new_im = Image.new('RGB', (total_width, max_height))
#
#     x_offset = 0
#     for im in images:
#         new_im.paste(im, (x_offset, 0))
#         x_offset += im.size[0]
#     return new_im
def frames_joint_horizontal(frame_left, frame_right, differ_aligment=VideoAligment.Center):
    if frame_left is None or frame_right is None:
        return None
    height_left, width_left, _ = frame_left.shape
    height_right, width_right, _ = frame_right.shape
    if height_left > height_right:
        height_differ = int(height_left - height_right)
        if differ_aligment == VideoAligment.Center:
            half_height1 = int(height_differ / 2)
            half_height2 = int(height_differ - half_height1)
            half_blank_frame1 = np.zeros((half_height1, width_left, 3), dtype=np.uint8)
            half_blank_frame2 = np.zeros((half_height2, width_left, 3), dtype=np.uint8)
            new_f = cv2.vconcat([half_blank_frame1, frame_left, half_blank_frame2])
            new_frame = cv2.hconcat([frame_left, new_f])
            return new_frame
        elif differ_aligment == VideoAligment.Top:
            half_blank_frame = np.zeros((height_differ, width_right, 3), dtype=np.uint8)
            b_h, b_w, _ = half_blank_frame.shape
            new_f = cv2.vconcat([half_blank_frame, frame_right])
            new_frame = cv2.hconcat([frame_left, new_f])
            return new_frame
        else:
            half_blank_frame = np.zeros((height_differ, width_right, 3), dtype=np.uint8)
            new_f = cv2.vconcat([ frame_right, half_blank_frame])
            new_frame = cv2.hconcat([frame_left, new_f])
            return new_frame
    elif height_left < height_right:
        height_differ = int(height_right - height_left)
        if differ_aligment == VideoAligment.Center:
            half_height1 = int(height_differ / 2)
            half_height2 = int(height_differ - half_height1)
            half_blank_frame1 = np.zeros((half_height1, width_left, 3), dtype=np.uint8)
            half_blank_frame2 = np.zeros((half_height2, width_left, 3), dtype=np.uint8)

            new_f = cv2.vconcat([half_blank_frame1, frame_left, half_blank_frame2])
            new_frame = cv2.hconcat([new_f, frame_right])
            return new_frame
        elif differ_aligment == VideoAligment.Top:
            half_blank_frame = np.zeros((height_differ, width_left, 3), dtype=np.uint8)
            new_f = cv2.vconcat([half_blank_frame, frame_left])
            new_frame = cv2.hconcat([new_f, frame_right])
            return new_frame
        else:
            half_blank_frame = np.zeros((height_differ, width_left, 3), dtype=np.uint8)
            new_f = cv2.vconcat([frame_left, half_blank_frame])
            new_frame = cv2.hconcat([new_f, frame_right])
            return new_frame
    else:
        frame_new = cv2.hconcat([frame_left, frame_right])
        return frame_new
