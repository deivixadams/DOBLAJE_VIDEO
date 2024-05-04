from directory_manager import DirectoryManager
from audio_video_manager import AudioVideoManager
from whisper_transcription_service import TranscriptionService
from text_to_speech_service import TextToSpeechService
from media_merger import MediaMerger
from translation_service import TranslationService
import os

def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la consola
    output_path = 'D:\\VIDSIGN'  # Define la ruta donde se guardarán los archivos

    # Instancia y uso de DirectoryManager para limpiar el directorio
    dir_manager = DirectoryManager(output_path)
    dir_manager.clean_directory()  # Corregido para usar el método existente

    # Instancia y uso de AudioVideoManager para descargar y convertir video y audio
    av_manager = AudioVideoManager(output_path)
    av_manager.download_video_audio('https://www.youtube.com/shorts/Qb1xQ0muq5Q')

    # Instancia y uso de TranscriptionService para transcribir el audio
    audio_path = os.path.join(output_path, 'audio_only.wav')
    trans_service = TranscriptionService(audio_path)
    transcribed_text = trans_service.transcribe_audio()

    # Instancia y uso de TranslationService para traducir el texto
    trans_service = TranslationService()
    translated_text = trans_service.translate_text(transcribed_text, 'en', 'es')

    # Instancia y uso de TextToSpeechService para convertir texto a voz
    tts_service = TextToSpeechService(output_path)
    audio_file = tts_service.text_to_speech(translated_text, 'es')

    # Instancia y uso de MediaMerger para combinar el video y el audio
    if audio_file:
        video_path = os.path.join(output_path, 'video_only.mp4')
        merged_video_path = os.path.join(output_path, 'final_video.mp4')
        media_merger = MediaMerger(video_path, audio_file, merged_video_path)
        media_merger.merge_media()

        # Reproducir el video combinado
        play_video(merged_video_path)
    else:
        print("No se generó el archivo de audio traducido.")

def play_video(file_path):
    if os.path.exists(file_path):
        os.system(f"start {file_path}")
    else:
        print(f"El archivo {file_path} no existe para reproducir.")

if __name__ == "__main__":
    main()
