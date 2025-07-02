
# JumpCutter GUI  - Documentation

The project provides graphical interfaces to the jumpcutter tool for removing silent parts of videos.

## Tkinter Interface

`jump_cutter_gui.py` implements the original interface using Tkinter. Run the script with Python and the window will appear. All parameters can be adjusted using the form elements and pressing **Run** starts the processing.

## Qt Interface

A more polished interface built with PyQt6 is available in `jump_cutter_gui_qt.py`. To use it install the `PyQt6` package and run the script:

```bash
pip install PyQt6
python jump_cutter_gui_qt.py
```

This version groups options with modern widgets and shows progress and log output.

### Packaging for Windows and macOS

You can generate a standalone application using [PyInstaller](https://pyinstaller.org/).
After installing the dependencies run:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon icon.ico jump_cutter_gui_qt.py
```

On Windows this creates an `.exe` in the `dist` folder. On macOS the same command
produces an `.app` bundle that can be copied to the Applications folder.

## Usage Overview

Input video: Select the input file to process.

Output video: Choose the output file name.

Magnitude threshold ratio: Threshold for sound magnitude to determine silence.

Duration threshold: Minimum length of a silent part to be removed.

Failure tolerance ratio: Tolerance for detecting and removing silent parts.

Space on edges: Space to leave around the edges of a cut.

Silence part speed: Playback speed for silent parts when included.

Minimum loud part duration: Minimum duration for a loud part to be considered.

Codec: Optional codec for the output.

Bitrate: Optional bitrate for the output.

Cut: Choose which parts to remove or include (silent, voiced, or both).

Click **Run** to process the video. A progress bar indicates processing and log messages appear below.

## Code Explanation

Both GUI implementations collect the parameters and execute `jump_cutter_main` from `jumpcutter.py` in a background thread so the interface remains responsive.

## Acknowledgements
We would like to extend our sincerest gratitude to Kivanc Yuksel (emkademy@gmail.com) for creating this useful tool. The original source code can be found at the following repository: https://github.com/kivancyuksel/jumpcutter.git

This software is distributed under the MIT License.

### Contact
If you have any questions, suggestions, or need assistance, please feel free to reach out to me at:
Email: umut.keltek@gmail.com
