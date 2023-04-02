import tkinter as tk
import traceback
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import moviepy.editor as moviepy
from threading import Thread
from jumpcutter import main as jump_cutter_main
import sys
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
import logging
import subprocess
import sys
import os
from threading import Thread
from jumpcutter import main as jumpcutter_main
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
#etc.

class JumpCutterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Jump Cutter")
        self.run_button = tk.Button(master, text="Run", command=lambda: self.run_jump_cutter())
        self.min_loud_part_duration_var = tk.BooleanVar()

        self.silence_part_speed_var = tk.BooleanVar()
        self.silence_part_speed_checkbox = tk.Checkbutton(master, text="Include", variable=self.silence_part_speed_var)
        self.codec_var = tk.BooleanVar()
        self.codec_checkbox = tk.Checkbutton(master, text="Include", variable=self.codec_var)
        self.bitrate_var = tk.BooleanVar()
        self.bitrate_checkbox = tk.Checkbutton(master, text="Include", variable=self.bitrate_var)
        self.cut_var = tk.BooleanVar()
        self.cut_checkbox = tk.Checkbutton(master, text="Include", variable=self.cut_var)
        self.min_loud_part_duration_var = tk.BooleanVar()
        self.min_loud_part_duration_checkbox = tk.Checkbutton(master, text="Include", variable=self.min_loud_part_duration_var)

        # Labels, entries, sliders, and spinboxes for each argument
        self.input_label = tk.Label(master, text="Input video:")
        self.input_entry = tk.Entry(master)
        self.input_button = tk.Button(master, text="Browse", command=self.browse_input)

        self.output_label = tk.Label(master, text="Output video:")
        self.output_entry = tk.Entry(master)

        self.magnitude_threshold_ratio_label = tk.Label(master, text="Magnitude threshold ratio:")
        self.magnitude_threshold_ratio_slider = tk.Scale(master, from_=0, to_=1, resolution=0.01, orient=tk.HORIZONTAL)

        self.duration_threshold_label = tk.Label(master, text="Duration threshold:")
        self.duration_threshold_entry = tk.Entry(master)

        self.failure_tolerance_ratio_label = tk.Label(master, text="Failure tolerance ratio:")
        self.failure_tolerance_ratio_entry = tk.Entry(master)

        self.space_on_edges_label = tk.Label(master, text="Space on edges:")
        self.space_on_edges_entry = tk.Entry(master)
        # Add a new button for optimized parameters
        self.find_optimized_parameters_button = tk.Button(master, text="Find Optimized Parameters", command=self.find_optimized_parameters)
        self.find_optimized_parameters_button.grid(row=23, column=1)

        self.silence_part_speed_label = tk.Label(master, text="Silence part speed:")
        self.silence_part_speed_entry = tk.Entry(master)
        self.silence_part_speed_checkbox = tk.Checkbutton(master, text="Include", variable=self.silence_part_speed_var)

        self.min_loud_part_duration_label = tk.Label(master, text="Minimum loud part duration:")
        self.min_loud_part_duration_entry = tk.Entry(master)
        self.min_loud_part_duration_checkbox = tk.Checkbutton(master, text="Include", variable=self.min_loud_part_duration_var)

        self.codec_label = tk.Label(master, text="Codec:")
        self.codec_entry = tk.Entry(master)
        self.codec_checkbox = tk.Checkbutton(master, text="Include", variable=self.codec_var)

        self.bitrate_label = tk.Label(master, text="Bitrate:")
        self.bitrate_entry = tk.Entry(master)
        self.bitrate_checkbox = tk.Checkbutton(master, text="Include", variable=self.bitrate_var)

        self.cut_label = tk.Label(master, text="Cut:")
        self.cut_combobox = ttk.Combobox(master, values=["silent", "voiced", "both"])
        self.cut_combobox.current(0)
        self.cut_checkbox = tk.Checkbutton(master, text="Include", variable=self.cut_var)

        # ... Add more labels, entries, and checkboxes for other optional arguments ...



        # Progress bar and information text
        self.progress_bar = ttk.Progressbar(master, mode="indeterminate")
        self.info_text = tk.Text(master, height=5, width=50, wrap=tk.WORD)

        # Grid layout
        self.input_label.grid(row=0, column=0, sticky=tk.E)
        self.input_entry.grid(row=0, column=1)
        self.input_button.grid(row=0, column=2)

        self.output_label.grid(row=1, column=0, sticky=tk.E)
        self.output_entry.grid(row=1, column=1)

        self.magnitude_threshold_ratio_label.grid(row=2, column=0, sticky=tk.E)
        self.magnitude_threshold_ratio_slider.grid(row=2, column=1)

        self.duration_threshold_label.grid(row=3, column=0, sticky=tk.E)
        self.duration_threshold_entry.grid(row=3, column=1)

        self.failure_tolerance_ratio_label.grid(row=4, column=0, sticky=tk.E)
        self.failure_tolerance_ratio_entry.grid(row=4, column=1)

        self.space_on_edges_label.grid(row=5, column=0, sticky=tk.E)
        self.space_on_edges_entry.grid(row=5, column=1)

        self.silence_part_speed_label.grid(row=6, column=0, sticky=tk.E)
        self.silence_part_speed_entry.grid(row=6, column=1)
        self.silence_part_speed_checkbox.grid(row=6, column=2)

        self.min_loud_part_duration_label.grid(row=7, column=0, sticky=tk.E)
        self.min_loud_part_duration_entry.grid(row=7, column=1)
        self.min_loud_part_duration_checkbox.grid(row=7, column=2)

        self.codec_label.grid(row=8, column=0, sticky=tk.E)
        self.codec_entry.grid(row=8, column=1)
        self.codec_checkbox.grid(row=8, column=2)

        self.bitrate_label.grid(row=9, column=0, sticky=tk.E)
        self.bitrate_entry.grid(row=9, column=1)
        self.bitrate_checkbox.grid(row=9, column=2)

        self.cut_label.grid(row=10, column=0, sticky=tk.E)
        self.cut_combobox.grid(row=10, column=1)
        self.cut_checkbox.grid(row=10, column=2)

        # ... Add more grid placements for other labels, entries, and checkboxes ...

        self.run_button.grid(row=20, column=1)

        self.progress_bar.grid(row=21, column=0, columnspan=3, sticky=tk.W + tk.E)
        self.info_text.grid(row=22, column=0, columnspan=3)

        self.silence_part_speed_var.trace('w', self.update_silence_part_speed_entry_state)
        self.min_loud_part_duration_var.trace('w', self.update_min_loud_part_duration_entry_state)
        self.codec_var.trace('w', self.update_codec_entry_state)
        self.bitrate_var.trace('w', self.update_bitrate_entry_state)
        self.cut_var.trace('w', self.update_cut_combobox_state)
        self.min_loud_part_duration_var.trace('w', self.update_min_loud_part_duration_entry_state)
        # Initialize the state of the entry boxes
        self.update_silence_part_speed_entry_state()
        self.update_min_loud_part_duration_entry_state()
        self.update_codec_entry_state()
        self.update_bitrate_entry_state()
        self.update_cut_combobox_state()

    def update_silence_part_speed_entry_state(self, *args):
        if self.silence_part_speed_var.get():
            self.silence_part_speed_entry.config(state=tk.NORMAL)
        else:
            self.silence_part_speed_entry.config(state=tk.DISABLED)

    def update_min_loud_part_duration_entry_state(self, *args):
        if self.min_loud_part_duration_var.get():
            self.min_loud_part_duration_entry.config(state=tk.NORMAL)
        else:
            self.min_loud_part_duration_entry.config(state=tk.DISABLED)

    def update_codec_entry_state(self, *args):
        if self.codec_var.get():
            self.codec_entry.config(state=tk.NORMAL)
        else:
            self.codec_entry.config(state=tk.DISABLED)

    def update_bitrate_entry_state(self, *args):
        if self.bitrate_var.get():
            self.bitrate_entry.config(state=tk.NORMAL)
        else:
            self.bitrate_entry.config(state=tk.DISABLED)

    def update_cut_combobox_state(self, *args):
        if self.cut_var.get():
            self.cut_combobox.config(state=tk.NORMAL)
        else:
            self.cut_combobox.config(state=tk.DISABLED)



        # Initialize the checkbox variables

    def find_optimized_parameters(self):
        # Implement a machine learning model or heuristic-based approach to estimate the best parameters
        # This is a complex task and requires a large dataset of videos and their associated optimal parameters
        # Here, you would load the model or use the heuristic-based approach to estimate the parameters
        # For now, we will use dummy values as an example

        optimized_magnitude_threshold_ratio = 0.03
        optimized_duration_threshold = 1.45
        optimized_failure_tolerance_ratio = 0.07
        optimized_space_on_edges = 0.12

        # Update the GUI with the optimized parameters
        self.magnitude_threshold_ratio_slider.set(optimized_magnitude_threshold_ratio)
        self.duration_threshold_entry.delete(0, tk.END)
        self.duration_threshold_entry.insert(0, optimized_duration_threshold)
        self.failure_tolerance_ratio_entry.delete(0, tk.END)
        self.failure_tolerance_ratio_entry.insert(0, optimized_failure_tolerance_ratio)
        self.space_on_edges_entry.delete(0, tk.END)
        self.space_on_edges_entry.insert(0, optimized_space_on_edges)

    def execute_jump_cutter(self, args):
        try:
            jump_cutter_main(args)
        except Exception:
            traceback.print_exc()
    #def execute_jump_cutter(self):
        args = []
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()

        if self.cut_var.get():
            args.extend(['--cut', self.cut_combobox.get()])

        if self.magnitude_threshold_ratio_slider.get():
            args.extend(['--magnitude-threshold-ratio', str(self.magnitude_threshold_ratio_slider.get())])

        if self.duration_threshold_entry.get():
            args.extend(['--duration-threshold', self.duration_threshold_entry.get()])

        if self.failure_tolerance_ratio_entry.get():
            args.extend(['--failure-tolerance-ratio', self.failure_tolerance_ratio_entry.get()])

        if self.space_on_edges_entry.get():
            args.extend(['--space-on-edges', self.space_on_edges_entry.get()])

        if self.silence_part_speed_var.get() and self.silence_part_speed_entry.get():
            args.extend(['--silence-part-speed', self.silence_part_speed_entry.get()])

        if self.min_loud_part_duration_entry.get():
            args.extend(['--min-loud-part-duration', self.min_loud_part_duration_entry.get()])

        if self.codec_var.get() and self.codec_entry.get():
            args.extend(['--codec', self.codec_entry.get()])
            if self.bitrate_var.get() and self.bitrate_entry.get():
                args.extend(['--bitrate', self.bitrate_entry.get()])

        args.extend(['--input', input_path])
        args.extend(['--output', output_path])

        try:
            jump_cutter_main(args)

        except Exception:
            traceback.print_exc()

    def browse_input(self):
        if sys.platform == 'darwin':  # For macOS
            filetypes = [
                ("Video files", "public.movie"),
                ("All files", "public.item")
            ]
        else:  # For Windows and Linux
            filetypes = [
                ("Video files", "*.mp4 *.mkv *.avi *.mov *.flv *.wmv"),
                ("All files", "*.*")
            ]

        file_path = filedialog.askopenfilename(filetypes=filetypes)
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)

        # Set output file with _autocut
        output_path = Path(file_path).stem + '_autocut' + ''.join(Path(file_path).suffixes)
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, output_path)

    def run_jump_cutter(self):
        args = [
            '-i', self.input_entry.get(),
            '-o', self.output_entry.get(),
            '--magnitude-threshold-ratio', str(self.magnitude_threshold_ratio_slider.get())
        ]

        # Add optional arguments if the checkboxes are checked
        if self.duration_threshold_entry.get():
            args.extend(['--duration-threshold', self.duration_threshold_entry.get()])
        if self.failure_tolerance_ratio_entry.get():
            args.extend(['--failure-tolerance-ratio', self.failure_tolerance_ratio_entry.get()])
        if self.space_on_edges_entry.get():
            args.extend(['--space-on-edges', self.space_on_edges_entry.get()])
        if self.silence_part_speed_var.get() and self.silence_part_speed_entry.get():
            args.extend(['--silence-part-speed', self.silence_part_speed_entry.get()])
        if self.min_loud_part_duration_entry.get():
            args.extend(['--min-loud-part-duration', self.min_loud_part_duration_entry.get()])
        if self.codec_var.get() and self.codec_entry.get():
            args.extend(['--codec', self.codec_entry.get()])
            if self.bitrate_var.get() and self.bitrate_entry.get():
                args.extend(['--bitrate', self.bitrate_entry.get()])
            if self.cut_checkbox.get():
                args.extend(['--cut', self.cut_checkbox.get()])

        # Call execute_jump_cutter method to run jump_cutter_main

        try:
            self.run_main_with_progress(args)  # Pass the args to run_main_with_progress
        except Exception as e:
            #tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            tb_str = traceback.format_exception(type(e), e, e.__traceback__)

            error_str = ''.join(tb_str)
            self.info_text.insert(tk.END, f"An error occurred during processing:\n{error_str}\n")
            self.info_text.see(tk.END)

    def run_main_with_progress(self, args):  # Add 'args' as an argument
        self.run_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.info_text.insert(tk.END, "Processing the video...\n")
        self.info_text.see(tk.END)

        def thread_target():
            try:
                jump_cutter_main(args)  # Call jump_cutter_main with 'args'
                self.info_text.insert(tk.END, "Video processing completed successfully.\n")
                self.info_text.see(tk.END)
            except Exception as e:
                tb_str = traceback.format_exception(type(e), e, e.__traceback__)
                error_str = ''.join(tb_str)
                self.info_text.insert(tk.END, f"An error occurred during processing:\n{error_str}\n")
                self.info_text.see(tk.END)

            self.progress_bar.stop()
            self.run_button.config(state=tk.NORMAL)

        processing_thread = Thread(target=thread_target)
        processing_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    jump_cutter_gui = JumpCutterGUI(root)
    root.mainloop()
