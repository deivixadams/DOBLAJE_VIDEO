import ctypes
import os

# Ensure the correct C library is loaded on Windows
if os.name == 'nt':
    libc_name = 'msvcrt.dll'
else:
    import ctypes.util
    libc_name = ctypes.util.find_library('c')

if libc_name:
    libc = ctypes.CDLL(libc_name)
else:
    raise OSError("Could not find the libc library.")

import whisper

class LenguajeTranscriptionService:
    """
    Clase para transcribir audio a texto utilizando el modelo Whisper de OpenAI.
    Para instalar Whisper, puedes usar:
    pip install git+https://github.com/openai/whisper.git
    """

    def __init__(self, audio_path, lang='en'):
        """
        Inicializa la clase con la ruta del archivo de audio y el idioma para la transcripción.
        Por defecto, utiliza el modelo 'base' de Whisper, pero puedes elegir entre 'tiny', 'base', 'small', 'medium', 'large'.

        Args:
            audio_path (str): Ruta completa al archivo de audio.
            lang (str): Código de idioma para la transcripción (ISO 639-1, por ejemplo, 'en').
        """
        self.audio_path = audio_path
        self.lang = lang
        self.model = whisper.load_model("base")

    def transcribe_audio(self):
        """
        Realiza la transcripción del audio utilizando Whisper. Retorna el texto transcribido o una cadena vacía si la transcripción no es posible.

        Returns:
            str: Texto transcribido del audio.
        """
        if not os.path.exists(self.audio_path):
            print(f"El archivo {self.audio_path} no existe.")
            return ""

        try:
            result = self.model.transcribe(self.audio_path, language=self.lang)
            transcription = result['text']
            print("Texto transcribido completo: ", transcription)
            return transcription
        except Exception as e:
            print(f"Error durante la transcripción: {e}")
            return ""

# Ejemplo de uso
if __name__ == "__main__":
    trans_service = LenguajeTranscriptionService("path_to_your_audio_file.wav", "en")
    transcript = trans_service.transcribe_audio()
    print(transcript)
