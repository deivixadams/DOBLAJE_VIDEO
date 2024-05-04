import subprocess
import os
from pytube import YouTube, exceptions

class AudioVideoManager:
    def __init__(self, output_path):
        """
        Inicializa el gestor de audio y vídeo con una ruta de salida donde se guardarán los archivos.
        
        Args:
        output_path (str): Ruta donde se guardarán los archivos de vídeo y audio descargados y convertidos.
        """
        self.output_path = output_path

    def download_video_audio(self, url):
        """
        Descarga el vídeo y el audio de una URL de YouTube especificada y guarda los archivos
        en la ruta de salida configurada.
        
        Args:
        url (str): URL del vídeo de YouTube a descargar.
        
        Returns:
        bool: True si la descarga y la conversión fueron exitosas, False de lo contrario.
        """
        try:
            yt = YouTube(url)
            video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
            audio_stream = yt.streams.filter(only_audio=True).first()

            if video_stream and audio_stream:
                video_path = video_stream.download(output_path=self.output_path, filename='video_only.mp4')
                audio_path = audio_stream.download(output_path=self.output_path, filename='audio_only.mp4')
                self.convert_mp4_to_wav(audio_path, os.path.join(self.output_path, 'audio_only.wav'))
                return True
            else:
                print("No video or audio streams available.")
                return False
        except exceptions.PytubeError as e:
            print(f"Error al descargar el video/audio: {e}")
            return False

    def convert_mp4_to_wav(self, input_file, output_file):
        """
        Convierte un archivo MP4 a WAV utilizando ffmpeg para su uso en transcripciones o otros procesos.
        
        Args:
        input_file (str): Ruta al archivo MP4 de audio descargado.
        output_file (str): Ruta del archivo WAV de salida.
        """
        if os.path.exists(input_file):
            command = ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', output_file]
            subprocess.run(command, check=True)
            print(f"Audio convertido a WAV en {output_file}")
        else:
            print(f"El archivo {input_file} no existe.")
