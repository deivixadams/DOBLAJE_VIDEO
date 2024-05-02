from pytube import YouTube
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
            os.remove(os.path.join(path, file))

def convert_mp4_to_wav_ffmpeg(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1', output_file]
    subprocess.run(command, check=True)

def download_video_audio(url, output_path):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(only_audio=True).first()
        video_stream.download(output_path=output_path, filename='video_only.mp4')
        audio_stream.download(output_path=output_path, filename='audio_only.mp4')
        convert_mp4_to_wav_ffmpeg(os.path.join(output_path, 'audio_only.mp4'), os.path.join(output_path, 'audio_only.wav'))
    except Exception as e:
        print(f"Error al descargar el video/audio: {e}")

def transcribe_audio(audio_path, lang='en-US'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language=lang)
        print("Texto transcribido: ", text)
        return text
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
    except sr.RequestError as e:
        print(f"Error de la API; {e}")
    return ""

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    print("Texto traducido: ", translated_text)
    return translated_text

def text_to_speech(text, lang, output_path):
    tts = gTTS(text, lang=lang)
    audio_file = os.path.join(output_path, "translated_audio.mp3")
    tts.save(audio_file)
    return audio_file

#Este sistema depende mucho del utilitario llamado ffmpeg, que es un programa que se puede instalar en Windows y en Linux.
def merge_video_audio(video_path, audio_path, output_path):
    command = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path]
    subprocess.run(command, check=True)



def play_video(file_path):
    os.system(f"start {file_path}")

output_path = 'D:\\VIDSIGN'

# Preparar directorio
setup_directory(output_path)

# URL del video de YouTube
url = 'https://www.youtube.com/watch?v=-67hh86N42Q&ab_channel=Treehouse'

# Descargar video y audio
download_video_audio(url, output_path)

# Transcribir el audio desde el archivo WAV correcto
transcribed_text = transcribe_audio(os.path.join(output_path, 'audio_only.wav'), lang='en-US')

# Traducir el texto del inglés al español
translated_text = translate_text(transcribed_text, src_lang='en', dest_lang='es')

# Convertir texto traducido a audio
audio_file = text_to_speech(translated_text, lang='es', output_path=output_path)

# Ejemplo de uso de la función
video_path = os.path.join(output_path, 'video_only.mp4')
audio_path = os.path.join(output_path, 'translated_audio.mp3')
merged_video_path = os.path.join(output_path, 'final_video.mp4')

# Llamar a la función para combinar video y audio
merge_video_audio(video_path, audio_path, merged_video_path)

# Reproducir el vídeo combinado
play_video(merged_video_path)
