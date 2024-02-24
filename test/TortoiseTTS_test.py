from tortoise import api, utils
from tortoise.utils import audio


if __name__ == '__main__':
    # clips_paths = ["audio-ch-man.wav"]
    clips_paths = [r'd:/sourcecode/lecture/audio-ch-man.wav']
    reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
    tts = api.TextToSpeech()
    txt = ("In order to pragmatically promote President Xi Jinping’s major"
           "initiative of establishing the BRICS Partnership on New Industrial Revolution, "
           "and to implement the deliverables of the BRICS Business Council Skills Development "
           "Working Group (hereinafter referred to as the BRICS Skills Group) on the establishment of BRICS "
           "Academy of Skills Development and Technology Innovation, in December 2021，"
           "BRICS Academy of Skills Development and Technology Innovation (Xiamen) "
           "(hereinafter referred to as the Academy) was jointly established by five units")
    pcm_audio = tts.tts_with_preset(txt, voice_samples=reference_clips, preset='fast')