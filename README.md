
# JumpCutter GUI  - Documentation


The JumpCutter GUI is built using the Tkinter library, which is a standard Python library for creating graphical user interfaces. The GUI allows users to input parameters, select input and output files, and control the jump cutting process.

## Usage ##
To use JumpCutter, simply run the script, and the GUI will be displayed. The interface consists of several sections for different parameters and settings:

Input video: Select the input video file that you want to process.

Output video: Enter the desired output video file name.

Magnitude threshold ratio: Set the threshold for sound magnitude (volume) to determine whether a part is silent or not.

Duration threshold: Set the duration threshold to determine the minimum length of a silent part to be removed.

Failure tolerance ratio: Set the tolerance for detecting and removing silent parts.

Space on edges: Set the amount of space to leave around the edges of a cut.

Silence part speed: Set the playback speed for the silent parts (if you want to include them in the output video).

Minimum loud part duration: Set the minimum duration for a loud part to be considered as a separate segment.

Codec: Set the codec for the output video file (optional).

Bitrate: Set the bitrate for the output video file (optional).

Cut: Choose which parts to remove or include in the output video (silent, voiced, or both).

Once you have configured the desired settings, click the "Run" button to start processing the video. A progress bar will indicate the progress of the process.
![image](https://user-images.githubusercontent.com/35880258/227778348-bd7255c9-18d5-4ae4-addb-7847fea20d52.png)

## Code Explanation ##
The code consists of a main JumpCutterGUI class that handles the creation and management of the GUI components, such as labels, entries, sliders, and buttons. The __init__ method initializes the GUI components and sets up the grid layout.

The browse_input method allows the user to select an input video file using a file dialog, and the run_jump_cutter method gathers the input parameters and calls the jump_cutter_main function from the jump_cutter_main module to process the video.

The execute_jump_cutter method is a wrapper for the jump_cutter_main function, which processes the input video file based on the provided arguments and generates the output video file.

## Acknowledgements ##
We would like to extend our sincerest gratitude to Kivanc Yuksel (emkademy@gmail.com) for creating this useful tool. The original source code can be found at the following repository: https://github.com/kivancyuksel/jumpcutter.git

This software is distributed under the MIT License.

### Contact ###
If you have any questions, suggestions, or need assistance, please feel free to reach out to me at:
Email: umut.keltek@gmail.com
