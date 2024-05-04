from googletrans import Translator

def test_translation():
    translator = Translator()
    try:
        # Prueba de traducción del inglés al español
        result = translator.translate('Hello world', src='en', dest='es')
        print("Texto original: 'Hello world'")
        print("Texto traducido:", result.text)
    except Exception as e:
        print("Error al traducir:", e)

test_translation()
