import os

class LenguajeDirectoryManager:
    def __init__(self, path):
        """
        Inicializa el objeto DirectoryManager con una ruta de directorio.
        
        Args:
        path (str): Ruta del directorio que se administrará.
        """
        self.path = path
        self.setup_directory()

    def setup_directory(self):
        """
        Configura el directorio asegurando que esté creado y vacío. Si el directorio ya existe,
        se limpia eliminando todos los archivos que contiene.
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print(f"Directorio creado en: {self.path}")
        else:
            self.clean_directory()
            print(f"Directorio existente limpiado: {self.path}")

    def clean_directory(self):
        """
        Limpia el directorio eliminando todos los archivos en él. No elimina subdirectorios ni sus contenidos.
        """
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Archivo eliminado: {file_path}")
            except Exception as e:
                print(f"No se pudo eliminar {file_path}. Razón: {e}")
