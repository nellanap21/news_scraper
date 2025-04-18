from elevenlabs import ElevenLabs
from elevenlabs import play, save, stream, Voice, VoiceSettings
import s3fs
import os
from dotenv import load_dotenv
import pandas as pd
import arrow


def generate_audio(s3_folder_path):

    # load environmental variables
    load_dotenv()
    api_key = os.getenv("ELEVEN_LABS_API_KEY")

    client = ElevenLabs(
        api_key=api_key,
    )

    # get filepath with data
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY-MM-DD')
    scripts_filepath = s3_folder_path + formatted_date + '/scripts.csv'

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

        # save locally to EC2
        save(audio, 'output.mp3')

        # create S3 filepath for audio
        audio_filepath = s3_folder_path + formatted_date + '/' + str(index) + '.mp3'

        # use s3fs to save to s3 bucket
        # Note: need to have .aws cli credentials configured with profile admin
        s3 = s3fs.S3FileSystem(profile='admin')
        s3.put(lpath='./output.mp3', rpath=audio_filepath, recursive=False)

def generate_audio_cnn(s3_folder_path):

    # load environmental variables
    load_dotenv()
    api_key = os.getenv("ELEVEN_LABS_API_KEY")

    client = ElevenLabs(
        api_key=api_key,
        timeout=300
    )

    # get filepath with data
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY-MM-DD')
    scripts_filepath = s3_folder_path + formatted_date + '/cnn_summaries_script.csv'

    # create data frame
    scripts = pd.read_csv(filepath_or_buffer=scripts_filepath)

    # remove instances of "Script"
    for index, row in scripts.iterrows():
        script = scripts.at[index, 'script']
        print("generate_audio_cnn: got script")

        audio = client.text_to_speech.convert(
            voice_id="AVZoXJVV8SEUYYOn6s00",
            output_format="mp3_44100_128",
            text=script,
            model_id="eleven_multilingual_v2",
        )

        # if old mp3 exists, delete it
        if os.path.exists('output.mp3'):
            os.remove('output.mp3')

        # save locally to EC2
        save(audio, 'output.mp3')
        print("generate_audio_cnn: saved audio locally")

        # create S3 filepath for audio
        audio_filepath = s3_folder_path + formatted_date + '/' + 'summary_cnn.mp3'
        print("generate_audio_cnn: created audio filepath", audio_filepath)

        # use s3fs to save to s3 bucket
        # Note: need to have .aws cli credentials configured with profile admin
        s3 = s3fs.S3FileSystem(profile='admin')
        s3.put(lpath='./output.mp3', rpath=audio_filepath, recursive=False)
        print("generate_audio_cnn: saved audio to s3")

def generate_audio_fox(s3_folder_path):

    # load environmental variables
    load_dotenv()
    api_key = os.getenv("ELEVEN_LABS_API_KEY")

    client = ElevenLabs(
        api_key=api_key,
        timeout=300
    )

    # get filepath with data
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY-MM-DD')
    scripts_filepath = s3_folder_path + formatted_date + '/fox_summaries_script.csv'

    # create data frame
    scripts = pd.read_csv(filepath_or_buffer=scripts_filepath)

    # remove instances of "Script"
    for index, row in scripts.iterrows():
        script = scripts.at[index, 'script']
        print("generate_audio_fox: got script")

        audio = client.text_to_speech.convert(
            voice_id="AVZoXJVV8SEUYYOn6s00",
            output_format="mp3_44100_128",
            text=script,
            model_id="eleven_multilingual_v2",
        )

        # if old mp3 exists, delete it
        if os.path.exists('output.mp3'):
            os.remove('output.mp3')

        # save locally to EC2
        save(audio, 'output.mp3')
        print("generate_audio_fox: saved audio locally")

        # create S3 filepath for audio
        audio_filepath = s3_folder_path + formatted_date + '/' + 'summary_fox.mp3'
        print("generate_audio_fox: created audio filepath", audio_filepath)

        # use s3fs to save to s3 bucket
        # Note: need to have .aws cli credentials configured with profile admin
        s3 = s3fs.S3FileSystem(profile='admin')
        s3.put(lpath='./output.mp3', rpath=audio_filepath, recursive=False)
        print("generate_audio_fox: saved audio to s3")