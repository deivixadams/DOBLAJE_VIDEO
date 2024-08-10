from pytube import YouTube, exceptions
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
import subprocess
import os

def setup_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

def convert_mp4_to_wav_ffmpeg(input_file, output_file):
    if os.path.exists(input_file):
        command = ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', output_file]
        subprocess.run(command, check=True)
    else:
        print(f"El archivo {input_file} no existe.")

def download_video_audio(url, output_path):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(only_audio=True).first()
        if video_stream and audio_stream:
            video_stream.download(output_path=output_path, filename='video_only.mp4')
            audio_stream.download(output_path=output_path, filename='audio_only.mp4')
            convert_mp4_to_wav_ffmpeg(os.path.join(output_path, 'audio_only.mp4'), os.path.join(output_path, 'audio_only.wav'))
        else:
            print("No video or audio streams available.")
    except exceptions.PytubeError as e:
        print(f"Error al descargar el video/audio: {e}")

def transcribe_audio(audio_path, lang='en-US'):
    if not os.path.exists(audio_path):
        print(f"El archivo {audio_path} no existe.")
        return ""

    recognizer = sr.Recognizer()
    full_text = ""
    try:
        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while True:
                try:
                    audio_data = recognizer.record(source, duration=30)
                    text = recognizer.recognize_google(audio_data, language=lang)
                    full_text += text + " "
                except sr.WaitTimeoutError:
                    break
        print("Texto transcribido completo: ", full_text)
        return full_text
    except sr.UnknownValueError:
        print("El reconocimiento de voz no pudo entender el audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error en la solicitud de transcripción: {e}")
        return ""
    except Exception as e:
        print(f"Error inesperado durante la transcripción: {e}")
        return ""

def translate_text(text, src_lang, dest_lang):
    if text:
        translator = Translator()
        translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
        print("Texto traducido: ", translated_text)
        return translated_text
    else:
        print("No hay texto para traducir.")
        return ""

def text_to_speech(text, lang, output_path):
    if text:
        tts = gTTS(text, lang=lang)
        audio_file = os.path.join(output_path, "translated_audio.mp3")
        tts.save(audio_file)
        return audio_file
    return None

def merge_video_audio(video_path, audio_path, output_path):
    if os.path.exists(video_path) and os.path.exists(audio_path):
        command = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path]
        subprocess.run(command, check=True)

def play_video(file_path):
    if os.path.exists(file_path):
        os.system(f"start {file_path}")
    else:
        print(f"El archivo {file_path} no existe para reproducir.")

output_path = 'D:\\VIDSIGN'

# Preparar directorio
setup_directory(output_path)

# URL del video de YouTube
url = 'https://www.youtube.com/watch?v=RR5rIcK5pQ0&ab_channel=TheRoyalSociety'

# Descargar video y audio
download_video_audio(url, output_path)

# Transcribir el audio desde el archivo WAV correcto
audio_file_path = os.path.join(output_path, 'audio_only.wav')
if os.path.exists(audio_file_path):
    transcribed_text = transcribe_audio(audio_file_path, lang='en-US')

    # Traducir el texto del inglés al español
    translated_text = translate_text(transcribed_text, src_lang='en', dest_lang='es')

    # Convertir texto traducido a audio
    audio_file = text_to_speech(translated_text, lang='es', output_path=output_path)

    # Combinar video y audio si el audio traducido fue generado
    if audio_file:
        video_path = os.path.join(output_path, 'video_only.mp4')
        audio_path = audio_file
        merged_video_path = os.path.join(output_path, 'final_video.mp4')
        merge_video_audio(video_path, audio_path, merged_video_path)

        # Reproducir el vídeo combinado
        play_video(merged_video_path)
    else:
        print("No se generó el archivo de audio traducido.")
else:
    print(f"El archivo de audio {audio_file_path} no existe.")
