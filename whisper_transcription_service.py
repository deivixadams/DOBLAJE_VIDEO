import whisper
import os

class TranscriptionService:
    """
    Clase para transcribir audio a texto utilizando el modelo Whisper de OpenAI.
    para instalarlo puedes usar:

    pip install git+https://github.com/openai/whisper.git

    """

    def __init__(self, audio_path, lang='en'):
        """
        Nota: estoy utilizando el modelo 'base' de Whisper para la transcripción. pero puedes elegir entre 'tiny', 'base', 'small', 'medium', 'large'.

        Inicializa la clase con la ruta del archivo de audio y el idioma para la transcripción.
        
        Args:
            audio_path (str): Ruta completa al archivo de audio.
            lang (str): Código de idioma para la transcripción (ISO 639-1, por ejemplo, 'en').
        """
        self.audio_path = audio_path
        self.lang = lang
        # para cargar el modelo Whisper de OpenAI larga duración Large puedo usar:self.model = whisper.load_model("large")
        self.model = whisper.load_model("base")  # Puedes elegir entre 'tiny', 'base', 'small', 'medium', 'large'


    def transcribe_audio(self):
        """
        Realiza la transcripción del audio utilizando Whisper.
        
        Returns:
            str: Texto transcribido del audio o una cadena vacía si la transcripción no es posible.
        """
        if not os.path.exists(self.audio_path):
            print(f"El archivo {self.audio_path} no existe.")
            return ""

        # Cargar el archivo de audio y realizar la transcripción
        result = self.model.transcribe(self.audio_path, language=self.lang)
        transcription = result['text']
        print("Texto transcribido completo: ", transcription)
        return transcription

# Ejemplo de uso (elimina esta parte si estás integrando en un sistema más grande)
if __name__ == "__main__":
    trans_service = TranscriptionService("path_to_your_audio_file.wav", "en")
    transcript = trans_service.transcribe_audio()
    print(transcript)
