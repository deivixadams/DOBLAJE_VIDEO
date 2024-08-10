import os
import subprocess
from LenguajeDirectoryManager import LenguajeDirectoryManager
from Lenguaje_whisper_transcription_service import LenguajeTranscriptionService
from text_to_speech_service import TextToSpeechService
from media_merger import MediaMerger
from argostranslate import translate

class LenguajeAudioVideoManager:
    def __init__(self, output_path):
        """
        Inicializa el gestor de audio y vídeo con una ruta de salida donde se guardarán los archivos.
        
        Args:
        output_path (str): Ruta donde se guardarán los archivos de vídeo y audio descargados y convertidos.
        """
        self.output_path = output_path

    def download_video_audio(self, url):
        """
        Descarga el vídeo y el audio de una URL de YouTube especificada utilizando yt-dlp y guarda los archivos
        en la ruta de salida configurada.
        
        Args:
        url (str): URL del vídeo de YouTube a descargar.
        
        Returns:
        bool: True si la descarga y la conversión fueron exitosas, False de lo contrario.
        """
        video_output = os.path.join(self.output_path, 'video_only.mp4')
        audio_output = os.path.join(self.output_path, 'audio_only.wav')

        try:
            # Descargar el video y el audio por separado utilizando yt-dlp
            video_command = [
                'yt-dlp',
                '-f', 'bestvideo',
                '-o', video_output,
                url
            ]
            audio_command = [
                'yt-dlp',
                '-f', 'bestaudio',
                '-o', audio_output,
                '--extract-audio',
                '--audio-format', 'wav',
                '--audio-quality', '0',
                url
            ]
            subprocess.run(video_command, check=True)
            subprocess.run(audio_command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al descargar el video/audio: {e}")
            return False

class ConsoleApp:
    def __init__(self):
        self.output_path = 'D:\\VIDSIGN'
        self.language_map = {'1': 'en', '2': 'fr', '3': 'zh'}  # Eliminado Español del menú
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la consola al iniciar

    def update_text_edit(self, translated_segment):
        """ Imprime segmentos traducidos en consola. """
        print(translated_segment)

    def translate_text(self, text, source_lang_code, target_lang_code='es'):
        """ Traduce el texto del idioma de origen al español utilizando Argos Translate. """
        installed_languages = translate.get_installed_languages()

        source_lang = next(lang for lang in installed_languages if lang.code == source_lang_code)
        target_lang = next(lang for lang in installed_languages if lang.code == target_lang_code)

        translation = source_lang.get_translation(target_lang)
        translated_text = translation.translate(text)
        return translated_text

    def on_go(self):
        video_url = input("Introducir el url: ")
        print("Seleccione el idioma del video: ")
        print("1 - Inglés")
        print("2 - Francés")
        print("3 - Chino")
        selected_language = input("Opción: ")

        if selected_language in self.language_map:
            selected_language_code = self.language_map[selected_language]
            dir_manager = LenguajeDirectoryManager(self.output_path)
            dir_manager.clean_directory()

            av_manager = LenguajeAudioVideoManager(self.output_path)
            success = av_manager.download_video_audio(video_url)

            if success:
                audio_path = os.path.join(self.output_path, 'audio_only.wav')
                trans_service = LenguajeTranscriptionService(audio_path, selected_language_code)
                transcribed_text = trans_service.transcribe_audio()
                self.update_text_edit(transcribed_text)  # Mostrar texto transcribido en la consola

                # Realizar la traducción al español
                translated_text = self.translate_text(transcribed_text, selected_language_code)
                print(f'Texto traducido: {translated_text}')
                
                # Convertir el texto traducido a voz
                tts_service = TextToSpeechService(self.output_path)
                translated_audio_path = tts_service.text_to_speech(translated_text, 'es')

                if translated_audio_path:
                    # Fusionar el nuevo audio con el video
                    merger = MediaMerger(video_path=os.path.join(self.output_path, 'video_only.mp4'), 
                                         audio_path=translated_audio_path,
                                         output_path=os.path.join(self.output_path, 'final_translated_video.mp4'))
                    merger.merge_media()
                    print("Video con audio traducido generado con éxito en: D:\\VIDSIGN\\final_translated_video.mp4")
                else:
                    print("Error al generar el audio traducido.")
            else:
                print("Error en la descarga de video/audio.")
        else:
            print("Selección de idioma inválida. Saliendo.")

if __name__ == "__main__":
    app = ConsoleApp()
    app.on_go()
