import gradio as gr
import assemblyai as aai
from translate import Translator
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import uuid
from pathlib import Path


def voice_to_voice(audio_file):
    
    transcription_response = audio_transcription(audio_file)

    if transcription_response.status == aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    else:
        text = transcription_response.text

    ja_translation, es_translation = text_Translation(text)

    ja_audi_path = text_to_speech(ja_translation)
    es_audi_path = text_to_speech(es_translation)

    ja_path = Path(ja_audi_path)
    es_path = Path(es_audi_path)

    return ja_path, es_path

def audio_transcription(audio_file):
    aai.settings.api_key = "4c3d1f05a6ff448dbc0f1c6f7afdad70"

    transcriber = aai.Transcriber()
    transcription = transcriber.transcribe(audio_file)

    return transcription

def text_Translation(text):
    translate_ja = Translator(from_lang="en", to_lang="ja")
    ja_text = translate_ja.translate(text)

    translate_es = Translator(from_lang="en", to_lang="es")
    es_text = translate_es.translate(text)

    return ja_text, es_text

def text_to_speech(text):
    client = ElevenLabs(
    api_key="sk_f3543aa9672a4b7b6758b5edf3a811861c9571a68c5065d3",
    )

    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

audio_input = gr.Audio(
    sources=["microphone"],
    type="filepath"
)

demo = gr.Interface(
    fn = voice_to_voice,
    inputs=audio_input,
    outputs=[gr.Audio(label="Japanese"), gr.Audio(label="Spanish")]
)

if __name__ == "__main__":
    demo.launch()