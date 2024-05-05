from PyQt5 import QtWidgets
from main_graph_base import Ui_Dialog
from directory_manager import DirectoryManager
from audio_video_manager import AudioVideoManager
from whisper_transcription_service import TranscriptionService
from text_to_speech_service import TextToSpeechService
from media_merger import MediaMerger
from translation_service import TranslationService
import os

class MainDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.customize_ui()
        self.output_path = 'D:\\VIDSIGN'

    def customize_ui(self):
        self.ui.pushButton.clicked.connect(self.on_go_clicked)
        self.ui.comboBox.addItems(["Inglés", "Francés", "Mandarín"])
        self.ui.textEdit_2.setStyleSheet("background-color: lightblue; font-size: 14pt;")
        self.ui.textEdit_3.setStyleSheet("background-color: lightgreen; font-size: 14pt;")

    def update_text_edit(self, translated_segment):
        """ Esta función será llamada desde el callback de TranslationService. """
        self.ui.textEdit_3.append(translated_segment + '\n')  # Añade el segmento traducido al textEdit_3

    def on_go_clicked(self):
        self.ui.progressBar.setValue(0)  # Reset progress bar at the start
        video_url = self.ui.textEdit_2.toPlainText()  # Extract URL from QTextEdit
        selected_language = self.ui.comboBox.currentText()
        language_map = {'Inglés': 'en', 'Francés': 'fr', 'Mandarín': 'zh'}

        if selected_language in language_map:
            selected_language_code = language_map[selected_language]

            dir_manager = DirectoryManager(self.output_path)
            dir_manager.clean_directory()
            self.ui.progressBar.setValue(10)  # Update progress bar

            av_manager = AudioVideoManager(self.output_path)
            av_manager.download_video_audio(video_url)  # Use URL provided by the user
            self.ui.progressBar.setValue(30)  # Update progress bar

            audio_path = os.path.join(self.output_path, 'audio_only.wav')
            trans_service = TranscriptionService(audio_path, selected_language_code)
            transcribed_text = trans_service.transcribe_audio()
            self.ui.progressBar.setValue(50)  # Update progress bar

            # Instantiate TranslationService with the callback update_text_edit
            trans_service = TranslationService(selected_language_code, 'es', self.update_text_edit)
            translated_text = trans_service.translate_text(transcribed_text)
            self.ui.progressBar.setValue(70)  # Update progress bar

            tts_service = TextToSpeechService(self.output_path)
            audio_file = tts_service.text_to_speech(translated_text, 'es')
            self.ui.progressBar.setValue(90)  # Update progress bar

            if audio_file:
                video_path = os.path.join(self.output_path, 'video_only.mp4')
                merged_video_path = os.path.join(self.output_path, 'final_video.mp4')
                media_merger = MediaMerger(video_path, audio_file, merged_video_path)
                media_merger.merge_media()
                self.ui.progressBar.setValue(100)  # Complete progress
                self.play_video(merged_video_path)
            else:
                print("No se generó el archivo de audio traducido.")
                self.ui.progressBar.setValue(100)  # Complete progress
        else:
            print("Invalid language selection. Exiting.")
            self.ui.progressBar.setValue(0)  # Reset progress bar on error

    def play_video(self, file_path):
        if os.path.exists(file_path):
            os.system(f"start {file_path}")
        else:
            print(f"El archivo {file_path} no existe para reproducir.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = MainDialog()
    dialog.show()
    sys.exit(app.exec_())
