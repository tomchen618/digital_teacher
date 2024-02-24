import asyncio
import os.path

import torch
from clickhouse_orm import Database
from torch import device

import globle
from lecture.common.file_utils import get_system_data_directory
from service.table_service import get_table_id, update_table_id, delete_table_id
from test.video_editor_test import run_video_editor_test
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"


def init_all():
    globle.config.read('config.ini')
    sections = globle.config.sections()
    if len(sections) < 1:
        return False
    if ((globle.config.get("DefaultDatabase", "db_name") == "") or
            (globle.config.get("DefaultDatabase", "db_url") == "")):
        return False
    globle.pdf_max_pages = globle.config.getint("System", "pdf_max_pages")
    globle.db = Database(db_name=globle.config.get("DefaultDatabase", "db_name"),
                                       db_url=globle.config.get("DefaultDatabase", "db_url"),
                                       username=globle.config.get("DefaultDatabase", "username"),
                                       password=globle.config.get("DefaultDatabase", "password"), timeout=100)
    if not globle.db.db_exists:
        return False

    return True


def test_tts_single():
    # tts --text "Text to speech" --vocoder_name "vocoder_models/en/ljspeech/univnet" --out_path speech.wav

    output_path = get_system_data_directory()
    output_path = os.path.join(output_path, "temp", "tts-en.wav")

    tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False).to(device)
    # tts = TTS(model_name="vocoder_models/en/ljspeech/univnet", progress_bar=False).to(device)

    # Run TTS
    txt_to_speech = "In order to pragmatically promote President Xi Jinping’s major  initiative of establishing the BRICS Partnership on New Industrial Revolution "
    # "and to implement the deliverables of the BRICS Business Council Skills "
    # "Development Working Group (hereinafter referred to as the BRICS Skills Group) "
    # "on the establishment of BRICS Academy of Skills Development and Technology Innovation, "
    # "in December 2021，BRICS Academy of Skills Development and Technology Innovation (Xiamen) "
    # "(hereinafter referred to as the Academy) was jointly established by five units "
    # "which are BRICS PartNIR Innovation Center, Administrative Commission of "
    # "Xiamen Torch Development Zone for High Technology Industries, "
    # "People's Government of Jimei District of Xiamen City, Xiamen Information Group Co., Ltd., "
    # "and Beijing ARC Xinxing Science and Technology Co., Ltd.")
    # "Ich bin eine Testnachricht."
    tts.tts_to_file(text=txt_to_speech, speaker_wav="audio-ch.wav", file_path=output_path)

    # Example voice cloning with YourTTS in English, French and Portuguese
    # tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)
    # tts.tts_to_file("This is voice cloning.", speaker_wav="audio-ch.wav", language="en", file_path="output.wav")
    # tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="audio-ch.wav", language="fr-fr",
    #                 file_path="output.wav")
    # tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="audio-ch.wav", language="pt-br",
    #                 file_path="output.wav")


def test_tts_multi():
    output_path = get_system_data_directory()
    output_path = os.path.join(output_path, "temp", "tts-en.wav")
    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # List available 🐸TTS models
    print(TTS().list_models())
    txt_to_speech = ("In order to pragmatically promote President Xi Jinping’s major "
                     "initiative of establishing the BRICS Partnership on New Industrial Revolution, "
                     "and to implement the deliverables of the BRICS Business Council Skills "
                     "Development Working Group (hereinafter referred to as the BRICS Skills Group) "
                     "on the establishment of BRICS Academy of Skills Development and Technology Innovation")
    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Run TTS
    # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
    # Text to speech list of amplitude values as output
    # wav = tts.tts(text=txt_to_speech, speaker_wav="audio-ch.wav", language="en")
    # Text to speech to a file
    tts.tts_to_file(text=txt_to_speech, speaker_wav="speech.wav", language="en", file_path=output_path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # test_tts_single()
    # test_tts_multi()
    # run_video_editor_test()
    if globle.db is None:
        print("Can not init databases from configuration!")
        exit()
    else:
        # Create an event loop
        loop = asyncio.get_event_loop()

        # Run the async function in the event loop
        # loop.run_until_complete(get_table_id(table_name="lecture"))
        # loop.run_until_complete(update_table_id(table_name="com_user"))
        loop.run_until_complete(delete_table_id(table_name="com_user"))
        # Close the loop
        loop.close()
