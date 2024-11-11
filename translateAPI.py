import gradio as gr
import assemblyai as aai
from translate import Translator

def voice_to_voice(audio_file):
    
    transcription_response = audio_transcription(audio_input)

    if transcription_response.status == aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    else:
        text = transcription_response.text

    ja_translation, es_translation = text_Translation(text)

def audio_transcription(audio_file):
    aai.settings.api_key = ""

    transcriber = aai.Transcriber()
    transcription = transcriber.transcribe(audio_file)

    return transcription

def text_Translation(text):
    translate_ja = Translator(from_lang="en", to_lang="ja")
    ja_text = translate_ja.translate(text)

    translate_es = Translator(from_lang="en", to_lang="es")
    es_text = translate_es.translate(text)

    return ja_text, es_text

def text_to_text():
    return True

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