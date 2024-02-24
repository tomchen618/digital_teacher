from moviepy.editor import *


def video_caption(src_mp4, dst_mp4, dot_temp: list, dot_times: list,
                  mp3_file: str, positions=None, font_size=12, font_name='Arial'):
    # input:
    #   src_mp4: the path of source mp4
    #   dst_mp4: the path of destination mp4
    #   dot_temp: the screen caption list

    if positions is None:
        positions = ['bottom']
    video = VideoFileClip(src_mp4)

    start_times = []
    start_time_temp = []
    for i in range(len(dot_times)):
        start_time_temp += dot_times[i]
        start_times.append(start_time_temp)

    captions = []
    for si, sentence in enumerate(dot_temp):
        txt = (TextClip(sentence, fontsize=font_size, font=font_name,
                        size=(1900, font_size), align='center', color='red')
               .set_position(positions[si])
               .set_duration(dot_times[si])
               .set_start(start_times[si]))

        captions.append(txt)

    video = CompositeVideoClip([video, *captions])
    videos = video.set_audio(AudioFileClip(mp3_file))
    videos.write_videofile(dst_mp4, audio_condc='aac')
