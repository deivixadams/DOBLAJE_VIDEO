

from argostranslate import package
from argostranslate import translate

# Asegúrate de reemplazar la ruta con la ubicación del archivo que descargaste
package.install_from_path('D:\\ALL\VIDSIGN\\FUENTES_LIB\\ARGOS\MODEL\\en_es.argosmodel')

package.install_from_path('D:\\ALL\VIDSIGN\\FUENTES_LIB\\ARGOS\MODEL\\En_Chino-moderno-1_9.argosmodel')
package.install_from_path('D:\\ALL\VIDSIGN\\FUENTES_LIB\\ARGOS\MODEL\\fr_en-1_9.argosmodel')


installed_languages = translate.get_installed_languages()
for language in installed_languages:
    print(language.name)

