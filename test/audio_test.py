import os

from lecture.common.audio_utils import slow_down_audio, wave_audio_speed_reset
from lecture.common.file_utils import get_resource_folder

if __name__ == '__main__':
    voice_dir = get_resource_folder("voice")
    liu_file = os.path.join(voice_dir, "liuvoice.wav")
    liu_file_out = os.path.join(voice_dir, "liuvoice_out.wav")
    # slow_down_audio(liu_file, liu_file_out, 0.78)
    wave_audio_speed_reset(liu_file, liu_file_out, 0.9)
