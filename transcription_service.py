import speech_recognition as sr
import os

class TranscriptionService:
    def __init__(self, audio_path, lang='en-US'):
        self.audio_path = audio_path
        self.lang = lang

    def transcribe_audio(self):
        """
        Transcribe el audio a texto utilizando Google Speech-to-Text.
        Retorna:
        - El texto transcribido o una cadena vacía si ocurre un error.
        """
        if not os.path.exists(self.audio_path):
            print(f"El archivo {self.audio_path} no existe.")
            return ""

        recognizer = sr.Recognizer()
        full_text = ""

        try:
            with sr.AudioFile(self.audio_path) as source:
                # Ajustar el reconocedor para el ruido ambiental al inicio del archivo
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Procesar el archivo de audio en bucle hasta que termine
                while True:
                    try:
                        # Leer el audio del archivo por segmentos de 30 segundos
                        audio_data = recognizer.record(source, duration=30)
                        # Intentar transcribir el audio a texto
                        text = recognizer.recognize_google(audio_data, language=self.lang)
                        full_text += text + " "
                    except sr.WaitTimeoutError:
                        # No hay más audio para procesar, salir del bucle
                        break

            print("Texto transcribido completo: ", full_text)
            return full_text

        except sr.UnknownValueError:
            print("El reconocimiento de voz no pudo entender el audio.")
            return ""
        except sr.RequestError as e:
            print(f"Error en la solicitud de transcripción: {e}")
            return ""
        except Exception as e:
            print(f"Error inesperado durante la transcripción: {e}")
            return ""

