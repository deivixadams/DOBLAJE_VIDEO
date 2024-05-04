import subprocess
import os

class MediaMerger:
    def __init__(self, output_path):
        """
        Inicializa el objeto MediaMerger.
        
        Args:
        output_path (str): Ruta base donde se guardará el archivo de video combinado.
        """
        self.output_path = output_path

    def merge_video_audio(self, video_path, audio_path, final_output):
        """
        Combina un archivo de video y un archivo de audio en un solo archivo de video.

        Args:
        video_path (str): Ruta al archivo de video original.
        audio_path (str): Ruta al archivo de audio que se superpondrá al video.
        final_output (str): Ruta del archivo de salida donde se guardará el video combinado.

        Returns:
        bool: True si la combinación fue exitosa, False de lo contrario.
        """
        if os.path.exists(video_path) and os.path.exists(audio_path):
            try:
                # Comando ffmpeg para combinar video y audio manteniendo el video sin recodificar.
                command = [
                    'ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy',
                    '-c:a', 'aac', '-strict', 'experimental', final_output
                ]
                subprocess.run(command, check=True)
                print(f"Video combinado creado con éxito en {final_output}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error al combinar video y audio: {e}")
                return False
        else:
            if not os.path.exists(video_path):
                print(f"El archivo de video {video_path} no existe.")
            if not os.path.exists(audio_path):
                print(f"El archivo de audio {audio_path} no existe.")
            return False

    def clean_up_temp_files(self):
        """
        Limpia archivos temporales si es necesario.
        Este método puede ser extendido para realizar la limpieza según los requisitos específicos del proyecto.
        """
        # Implementación pendiente según necesidad.
        pass
