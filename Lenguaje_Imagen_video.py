import whisper
import os
import openai
import requests
from PIL import Image
from io import BytesIO

class LanguageTranscriptionService:
    """
    Clase para transcribir audio a texto utilizando el modelo Whisper de OpenAI.
    """
    def __init__(self, audio_path, lang='en'):
        self.audio_path = audio_path
        self.lang = lang
        self.model = whisper.load_model("base")

    def transcribe_audio(self):
        if not os.path.exists(self.audio_path):
            print(f"El archivo {self.audio_path} no existe.")
            return ""

        try:
            result = self.model.transcribe(self.audio_path, language=self.lang)
            transcription = result['text']
            return transcription
        except Exception as e:
            print(f"Error durante la transcripción: {e}")
            return ""

    def print_segments(self):
        transcription = self.transcribe_audio()
        segments = [transcription[i:i+15] for i in range(0, len(transcription), 15)]
        for segment in segments:
            print(segment)
            image_service = LanguageImageVideo(segment)
            image_service.generate_image()

class LanguageImageVideo:
    """
    Clase para convertir texto en imágenes de lenguaje de señas utilizando la API de DALL-E de OpenAI.
    """
    def __init__(self, text):
        self.text = text
        openai.api_key = 'tu-clave-api'  # Asegúrate de usar tu clave de API real aquí

    def generate_image(self):
        prompt = f"Una imagen de una mano con tono de piel claro mostrando lenguaje de señas para '{self.text}'. Consistencia en el tono de piel en todas las imágenes."
        try:
            response = openai.Image.create(
                model="image-dalle-2",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            self.download_and_resize_image(image_url)
        except Exception as e:
            print(f"Error al generar la imagen: {e}")

    def download_and_resize_image(self, url):
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((288, 288), Image.ANTIALIAS)  # 288x288 pixels (2x2 inches at 144 DPI)
        image_path = f"D:\\VIDSIGN\\IMG\\{self.text[:10]}_sign_language.jpg"
        image.save(image_path)
        print(f"Imagen guardada en: {image_path}")

# Ejemplo de uso
if __name__ == "__main__":
    trans_service = LanguageTranscriptionService("path_to_your_audio_file.wav", "en")
    trans_service.print_segments()
