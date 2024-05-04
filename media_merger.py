from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import subprocess
import os

class MediaMerger:
    def __init__(self, video_path, audio_path, output_path):
        self.video_path = video_path
        self.audio_path = audio_path
        self.output_path = output_path

    def merge_media(self, last_seconds=10):
        video_duration = self._get_duration(self.video_path)
        audio_duration = self._get_duration(self.audio_path)

        if video_duration < audio_duration:
            self._extend_video(video_duration, audio_duration, last_seconds)
        else:
            self._simple_merge()

    def _extend_video(self, video_duration, audio_duration, last_seconds):
        video_clip = VideoFileClip(self.video_path)
        audio_clip = AudioFileClip(self.audio_path)  # Cargando el audio traducido

        if video_duration >= audio_duration:
            extended_clip = video_clip.set_audio(audio_clip)  # No need to extend, just set audio
        else:
            extra_time = audio_duration - video_duration
            number_of_repeats = int(extra_time / last_seconds) + 1

            # Tomar el último segmento del video para repetir
            last_segment = video_clip.subclip(max(0, video_duration - last_seconds), video_duration)

            # Crear una lista de clips repetidos
            clips = [video_clip] + [last_segment] * number_of_repeats
            extended_clip = concatenate_videoclips(clips)

            # Asegurarse de que el video extendido tenga la misma duración que el audio
            extended_clip = extended_clip.set_duration(audio_duration)

        # Configurar el clip de audio sobre el clip de video extendido
        final_clip = extended_clip.set_audio(audio_clip)

        final_clip.write_videofile(self.output_path, codec='libx264', audio_codec='aac')

    def _get_duration(self, file_path):
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        return float(result.stdout.strip())

    def _simple_merge(self):
        cmd = ['ffmpeg', '-i', self.video_path, '-i', self.audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', '-2', '-y', self.output_path]
        subprocess.run(cmd, check=True)
