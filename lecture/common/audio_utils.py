import wave
from pydub import AudioSegment


def slow_down_audio(input_file, output_file, speed_factor):
    sound = AudioSegment.from_file(input_file, format="mp3")
    resampled_sound = (sound.set_frame_rate(int(sound.frame_rate * speed_factor)))
    # .set_frame_rate(sound.frame_rate))
    resampled_sound.export(output_file, format="mp3")


def wave_audio_speed_reset(input_audio: str, output_audio: str, speed_factor):
    channels = 1
    swidth = 2
    multiplier = speed_factor

    spf = wave.open(input_audio, 'rb')
    fr = spf.getframerate()  # frame rate
    signal = spf.readframes(-1)

    wf = wave.open(output_audio, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(swidth)
    wf.setframerate(fr * multiplier)
    wf.writeframes(signal)
    wf.close()
