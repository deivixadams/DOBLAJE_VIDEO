from directory_manager import DirectoryManager
from audio_video_manager import AudioVideoManager
from transcription_service import TranscriptionService
from translation_service import TranslationService
from text_to_speech_service import TextToSpeechService
from media_merger import MediaMerger

def main():
    output_path = 'D:\\VIDSIGN'
    url = 'https://www.youtube.com/watch?v=RR5rIcK5pQ0&ab_channel=TheRoyalSociety'
    
    dir_manager = DirectoryManager(output_path)
    av_manager = AudioVideoManager(output_path)
    av_manager.download_video_audio(url)
    
    audio_path = os.path.join(output_path, 'audio_only.wav')
    trans_service = TranscriptionService(audio_path)
    transcribed_text = trans_service.transcribe_audio()
    
    trans_service = TranslationService()
    translated_text = trans_service.translate_text(transcribed_text, 'en', 'es')
    
    tts_service = TextToSpeechService()
    tts_path = tts_service.text_to_speech(translated_text, 'es', output_path)
    
    media_merger = MediaMerger()
    final_video_path = os.path.join(output_path, 'final_video.mp4')
    media_merger.merge_video_audio(os.path.join(output_path, 'video_only.mp4'), tts_path, final_video_path)

if __name__ == "__main__":
    main()
