import enum

import cv2
import moviepy.editor

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import VideoClip
from torchvision.io.video import av

from lecture.common.image_utils import frames_joint_horizontal, VideoAligment

from lecture.common.file_utils import check_lecture_path, add_filename_tail

# version 1.0
"""
function:
    step 1. explanation to create the voice_file.
    step 2. bind the lecture file video path with the voice_file.
    setp 3. check the length.
"""


class VideoEditor:
    def __init__(self, lecture_id: str, lecture_name: str, file_path: str, explanations: list, voice_file: str,
                 lecture_output: str):
        self.id = lecture_id
        self.lecture_name = lecture_name,
        self.file_path = check_lecture_path(lecture_name, lecture_id, file_path)
        self.explanations = explanations
        self.voice_file = check_lecture_path(lecture_name, lecture_id, voice_file)
        self.lecture_output = check_lecture_path(lecture_name, lecture_id, lecture_output)
        self.container = None
        self.stream = None

    def bind_voice(self, output_file, voice_file=''):

        if voice_file != "":
            self.voice_file = voice_file
        if self.voice_file == "":
            return False
        try:
            video_file_clip = VideoFileClip(self.file_path)
            audio_clip = AudioFileClip(self.voice_file)
            video_clip_with_audio = video_file_clip.set_audio(audio_clip)
            video_clip_with_audio.write_videofile(output_file, code='libx264', audio_codec='aac')
            video_clip_with_audio.close()
            audio_clip.close()
            video_file_clip.close()

        except Exception as e:
            return False

        return True

    def create_video(self, video_file, width, height, fps=24):
        if video_file == "":
            video_file = self.lecture_output
        self.container = av.open(video_file, mode='w')
        self.stream = self.container.add_stream('mpeg4', rate=fps)
        self.stream.width = width
        self.stream.height = height
        self.stream.pix_fmt = 'yuv420p'

        if width * height > 128000:
            self.stream.bit_rate = width * height * 8
        else:
            self.stream.bit_rate = 128000 * 8

    def store_frame(self, frame_array):
        frame = av.VideoFrame.from_ndarray(frame_array, format="bgr24")
        for packet in self.stream.encode(frame):
            self.container.mux(packet)

    def save_video(self):
        for packet in self.stream.encode():
            self.container.mux(packet)
        self.container.close()

    def merge_videos(self, output_path: str, alignment=VideoAligment.Center):
        # try:
        # Open video files
        if output_path == "":
            output_path = self.lecture_output
        lecture_capture = cv2.VideoCapture(self.file_path)
        audio_capture = cv2.VideoCapture(self.voice_file)

        lecture_frame_count = lecture_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        audio_frame_count = audio_capture.get(cv2.CAP_PROP_FRAME_COUNT)

        lecture_fps = lecture_capture.get(cv2.CAP_PROP_FPS)
        audio_fps = audio_capture.get(cv2.CAP_PROP_FPS)

        lecture_width = int(lecture_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        audio_width = int(audio_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        lecture_height = int(lecture_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        audio_height = int(audio_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps_output = int(max(lecture_fps, audio_fps))
        # use max fps to fill the resolution with the video
        height_output = int(max(lecture_height, audio_height))
        width_output = int(lecture_width + audio_width)
        max_fps_frame_index = 0
        lecture_frame = None
        audio_frame = None
        # video_frames = []
        to_continue = True
        audio_frame_current_index = 0
        lecture_frame_current_index = 0
        self.create_video(output_path, width_output, height_output, fps=fps_output)
        while to_continue:
            max_fps_frame_index += 1
            if fps_output == lecture_fps:
                if max_fps_frame_index < lecture_frame_count:
                    success_lecture, lecture_frame = lecture_capture.read()
                else:
                    success_lecture = 0
            else:
                current_index = max_fps_frame_index * lecture_fps / fps_output
                if lecture_frame_current_index < current_index:
                    if lecture_frame_current_index < lecture_frame_count:
                        success_lecture, lecture_frame = lecture_capture.read()
                        lecture_frame_current_index += 1
                    else:
                        success_lecture = 0
                else:
                    success_lecture = 1
            if fps_output == audio_fps:
                if max_fps_frame_index < audio_frame_count:
                    success_audio, audio_frame = audio_capture.read()
                else:
                    success_audio = 0
                # cv2.imwrite("frame_%d.jpg" % max_fps_frame_index, audio_frame)
            else:
                current_index = max_fps_frame_index * audio_fps / fps_output
                if audio_frame_current_index < current_index:
                    if audio_frame_current_index < audio_frame_count:
                        success_audio, audio_frame = audio_capture.read()
                        audio_frame_current_index += 1
                    else:
                        success_audio = 0
                else:
                    success_audio = 1
            to_continue = success_lecture or success_audio
            if to_continue:
                new_frame = frames_joint_horizontal(lecture_frame, audio_frame)
                # cv2.imwrite("frame_joint_%d.jpg" % max_fps_frame_index, new_frame)
                if new_frame is None:
                    to_continue = 0
                else:
                    # video_frames.append(new_frame)
                    self.store_frame(new_frame)
                    # print("f:" + str(max_fps_frame_index) + "-" + str(audio_frame_current_index))

        self.save_video()
        # self.save_video(output_path, video_frames, width_output, height_output, fps=audio_fps)
        lecture_capture.release()
        audio_capture.release()
        try:
            video_clip = VideoFileClip(output_path)
            audio_clip = VideoFileClip(self.voice_file)
            video_clip = video_clip.set_audio(audio_clip.audio)
            # can't use the same file other-wise it will cause conflict for the writing
            video_new = add_filename_tail(output_path, "_audio")
            video_clip.write_videofile(video_new)
            # get_audio_clip.write_videofile(filename=output_path, code='libx264', audio_codec='aac')
            video_clip.close()
            audio_clip.close()
        except Exception as e:
            print(e)
            return False

        return True
