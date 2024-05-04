from gtts import gTTS
from pydub import AudioSegment
import os

class TextToSpeechService:
    def __init__(self, output_path):
        self.output_path = output_path

    def text_to_speech(self, text, lang):
        """
        Convierte texto a voz y guarda el archivo de audio en la ruta especificada.
        Args:
        - text: El texto a convertir.
        - lang: El código de idioma (por ejemplo, 'es' para español).
        """
        if text:
            try:
                # Dividir el texto en segmentos si es demasiado largo
                segments = self.split_text(text, max_length=100)  # Suponiendo un máximo de 100 caracteres por segmento
                combined_audio = None
                for segment in segments:
                    tts = gTTS(segment, lang=lang)
                    segment_file = os.path.join(self.output_path, "temp_segment.mp3")
                    tts.save(segment_file)
                    segment_audio = AudioSegment.from_mp3(segment_file)
                    combined_audio = segment_audio if combined_audio is None else combined_audio + segment_audio
                    os.remove(segment_file)  # Limpiar segmentos temporales
                final_audio_file = os.path.join(self.output_path, "translated_audio.mp3")
                if combined_audio:
                    combined_audio.export(final_audio_file, format="mp3")
                return final_audio_file
            except Exception as e:
                print(f"Error al convertir texto a voz: {e}")
                return None
        else:
            print("No hay texto para convertir a voz.")
            return None

    def split_text(self, text, max_length=100):
        """
        Divide el texto en segmentos de un máximo de 'max_length' caracteres sin cortar palabras.
        Args:
        - text: El texto a dividir.
        - max_length: La longitud máxima de cada segmento.
        """
        words = text.split()
        segments = []
        current_segment = ""
        for word in words:
            if len(current_segment) + len(word) + 1 > max_length:
                segments.append(current_segment)
                current_segment = word
            else:
                current_segment += " " + word if current_segment else word
        if current_segment:
            segments.append(current_segment)
        return segments
