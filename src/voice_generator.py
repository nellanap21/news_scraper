from datetime import date
from elevenlabs import ElevenLabs
from elevenlabs import play, save, stream, Voice, VoiceSettings

import s3fs
import os
from dotenv import load_dotenv
import pandas as pd


def generate_audio(s3_folder_path):

    # load environmental variables
    load_dotenv()
    api_key = os.getenv("ELEVEN_LABS_API_KEY")

    client = ElevenLabs(
        api_key=api_key,
    )

    # get filepath with data
    today = date.today()
    scripts_filepath = s3_folder_path + today.strftime("%Y-%m-%d") + '/scripts.csv'

    # use this line for testing purposes
    # scripts_filepath = s3_folder_path + '2025-03-31' + '/scripts.csv'

    # create data frame
    scripts = pd.read_csv(filepath_or_buffer=scripts_filepath)

    # remove instances of "Script"
    for index, row in scripts.iterrows():
        script = scripts.at[index, 'script']
        print(script)

        audio = client.text_to_speech.convert(
            voice_id="AVZoXJVV8SEUYYOn6s00",
            output_format="mp3_44100_128",
            text=script,
            model_id="eleven_multilingual_v2",
        )

        audio_filepath = s3_folder_path + today.strftime("%Y-%m-%d") + str(index) + '.mp3'


        # try this to save to S3
        save(audio, audio_filepath)



        # also try this to save to S3
        with open(audio_filepath, "wb") as file:
            file.write(audio)

        # saves output.mp3 to s3 bucket
        # audio_filepath = s3_folder_path + today.strftime("%Y-%m-%d") + str(index) + '.mp3'

        # you may not need to reference profile='admin' on EC2 because it has access to S3
        # s3fs did not work
        # s3 = s3fs.S3FileSystem(profile='admin')
        # s3.put(lpath='./output.mp3', rpath=audio_filepath, recursive=False)
