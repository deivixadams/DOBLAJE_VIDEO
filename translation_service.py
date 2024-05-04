from googletrans import Translator, LANGUAGES

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, src_lang='en', dest_lang='es'):
        """
        Traduce el texto del idioma fuente al idioma destino utilizando Google Translate.
        Args:
        - text: Texto a traducir.
        - src_lang: Código del idioma fuente (por defecto 'en' para inglés).
        - dest_lang: Código del idioma destino (por defecto 'es' para español).
        Retorna:
        - El texto traducido o una cadena vacía si la traducción falla.
        """
        if text.strip() == "":
            print("No hay texto para traducir.")
            return ""

        try:
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
            print(f"Texto traducido de {LANGUAGES[src_lang]} a {LANGUAGES[dest_lang]}: {translated.text}")
            return translated.text
        except Exception as e:
            print(f"Error al traducir el texto: {e}")
            return ""

