from typing import Dict, List, Tuple

import numpy as np

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx import speedx
from moviepy.video.io.VideoFileClip import VideoFileClip
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.editor import *
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.resize import resize
#etc.
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize
from moviepy.video.VideoClip import VideoClip
from moviepy.video.fx.resize import resize
VideoClip.resize = resize

class Clip:
    def __init__(
        self, clip_path: str, min_loud_part_duration: int, silence_part_speed: int
    ) -> None:
        self.clip = VideoFileClip(clip_path)
        self.audio = Audio(self.clip.audio)
        self.cut_to_method = {
            "silent": self.jumpcut_silent_parts,
            "voiced": self.jumpcut_voiced_parts,
        }
        self.min_loud_part_duration = min_loud_part_duration
        self.silence_part_speed = silence_part_speed

    def jumpcut(
        self,
        cuts: List[str],
        magnitude_threshold_ratio: float,
        duration_threshold_in_seconds: float,
        failure_tolerance_ratio: float,
        space_on_edges: float,
    ) -> Dict[str, VideoFileClip]:

        intervals_to_cut = self.audio.get_intervals_to_cut(
            magnitude_threshold_ratio,
            duration_threshold_in_seconds,
            failure_tolerance_ratio,
            space_on_edges,
        )
        outputs = {}
        for cut in cuts:
            jumpcutted_clips = self.cut_to_method[cut](intervals_to_cut)
            outputs[cut] = concatenate_videoclips(jumpcutted_clips)

        return outputs

    def jumpcut_silent_parts(
        self, intervals_to_cut: List[Tuple[float, float]]
    ) -> List[VideoFileClip]:
        jumpcutted_clips = []
        previous_stop = 0
        for start, stop in tqdm(intervals_to_cut, desc="Cutting silent intervals"):
            clip_before = self.clip.subclip(previous_stop, start)

            if clip_before.duration > self.min_loud_part_duration:
                jumpcutted_clips.append(clip_before)

            if self.silence_part_speed is not None:
                silence_clip = self.clip.subclip(start, stop)
                silence_clip = speedx(
                    silence_clip, self.silence_part_speed
                ).without_audio()
                jumpcutted_clips.append(silence_clip)

            previous_stop = stop

        if previous_stop < self.clip.duration:
            last_clip = self.clip.subclip(previous_stop, self.clip.duration)
            jumpcutted_clips.append(last_clip)
        return jumpcutted_clips

    def jumpcut_voiced_parts(
        self, intervals_to_cut: List[Tuple[float, float]]
    ) -> List[VideoFileClip]:
        jumpcutted_clips = []
        for start, stop in tqdm(intervals_to_cut, desc="Cutting voiced intervals"):
            if start < stop:
                silence_clip = self.clip.subclip(start, stop)
                jumpcutted_clips.append(silence_clip)
        return jumpcutted_clips


class Audio:
    def __init__(self, audio: AudioFileClip) -> None:
        self.audio = audio
        self.fps = audio.fps

        self.signal = self.audio.to_soundarray()
        if len(self.signal.shape) == 1:
            self.signal = self.signal.reshape(-1, 1)

    def get_intervals_to_cut(
        self,
        magnitude_threshold_ratio: float,
        duration_threshold_in_seconds: float,
        failure_tolerance_ratio: float,
        space_on_edges: float,
    ) -> List[Tuple[float, float]]:
        min_magnitude = min(abs(np.min(self.signal)), np.max(self.signal))
        magnitude_threshold = min_magnitude * magnitude_threshold_ratio
        failure_tolerance = self.fps * failure_tolerance_ratio
        duration_threshold = self.fps * duration_threshold_in_seconds
        silence_counter = 0
        failure_counter = 0

        intervals_to_cut = []
        absolute_signal = np.absolute(self.signal)
        for i, values in tqdm(

            enumerate(absolute_signal),
            desc="Getting silent intervals to cut",
            total=len(absolute_signal),
            file=sys.stderr
        ):
            silence = all([value < magnitude_threshold for value in values])
            silence_counter += silence
            failure_counter += not silence
            if failure_counter >= failure_tolerance:
                if silence_counter >= duration_threshold:
                    interval_end = (i - failure_counter) / self.fps
                    interval_start = interval_end - (silence_counter / self.fps)

                    interval_start += space_on_edges
                    interval_end -= space_on_edges

                    intervals_to_cut.append(
                        (abs(interval_start), interval_end)
                    )  # in seconds
                silence_counter = 0
                failure_counter = 0
        return intervals_to_cut

#if __name__ == "__main__":
    #main()