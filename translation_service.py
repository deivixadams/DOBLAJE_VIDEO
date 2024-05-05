from argostranslate import translate, package

class TranslationService:
    def __init__(self, src_lang='en', dest_lang='es', callback=None):
        """
        Inicializa el servicio de traducción utilizando Argos Translate.
        Args:
        - src_lang: Código del idioma fuente (por defecto 'en' para inglés).
        - dest_lang: Código del idioma destino (por defecto 'es' para español).
        - callback: Función a llamar con cada segmento traducido (opcional).
        """
        self.src_lang_code = src_lang
        self.dest_lang_code = dest_lang
        self.callback = callback
        self.translation = None
        if not self.setup_translation(src_lang, dest_lang):
            raise ValueError("Los idiomas especificados no están disponibles o no se han instalado correctamente.")

    def setup_translation(self, src_lang, dest_lang):
        """
        Configura la traducción cargando los idiomas instalados y buscando la traducción adecuada.
        """
        try:
            installed_languages = translate.get_installed_languages()
            src_language = next((lang for lang in installed_languages if lang.code == src_lang), None)
            dest_language = next((lang for lang in installed_languages if lang.code == dest_lang), None)
            
            if src_language and dest_language:
                self.translation = src_language.get_translation(dest_language)
                return True
            else:
                print("Idiomas solicitados no disponibles. Asegúrese de haber instalado los modelos adecuados.")
                return False
        except Exception as e:
            print(f"Error al configurar los idiomas de traducción: {e}")
            return False

    def translate_text(self, text):
        """
        Traduce el texto del idioma fuente al idioma destino utilizando Argos Translate.
        Divide el texto en segmentos para manejar eficientemente textos largos.
        Args:
        - text: Texto a traducir.
        Retorna:
        - El texto traducido o una cadena vacía si la traducción falla.
        """
        if not text.strip():
            print("No hay texto para traducir.")
            return ""
        
        if not self.translation:
            print("Configuración de traducción no disponible.")
            return ""

        segments = self._split_text(text, max_length=300)
        translated_text = ""

        try:
            for segment in segments:
                if segment.strip():
                    translated_segment = self.translation.translate(segment)
                    translated_text += translated_segment + " "
                    if self.callback:
                        self.callback(translated_segment)  # Llamar al callback con el segmento traducido
            return translated_text.strip()
        except Exception as e:
            print(f"Error al traducir el texto: {e}")
            return ""

    def _split_text(self, text, max_length=300):
        """
        Divide el texto en segmentos para mantener cada segmento dentro de un límite de caracteres específico.
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
