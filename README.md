
# JumpCutter Pro - Advanced Video Silence Remover

An intelligent desktop application that automatically removes silent parts from videos, making your content more engaging and saving viewers' time. Perfect for podcasts, lectures, tutorials, and any video content with natural pauses.

## ✨ Features

### 🎯 Smart Presets
- **Podcast**: Optimized for speech content with natural pauses
- **Lecture/Educational**: For educational content with longer pauses
- **Tutorial/Demo**: Perfect for screen recordings and demonstrations
- **Meeting/Interview**: Handles multi-speaker content effectively
- **Aggressive Cutting**: Maximum silence removal for tight editing
- **Conservative**: Gentle removal preserving natural flow

### 🚀 Advanced Capabilities
- **Batch Processing**: Process multiple videos with the same settings
- **Platform Optimization**: Export presets for YouTube, Instagram, TikTok, Twitter
- **Drag & Drop**: Modern file handling interface
- **Real-time Progress**: Detailed feedback during processing
- **Smart Parameter Detection**: Automatically suggests optimal settings
- **Professional UI**: Clean, modern interface built with PyQt6

### 🎛️ Precise Control
- Magnitude threshold for silence detection sensitivity
- Duration threshold for minimum silence length
- Failure tolerance for imperfect silence detection
- Edge spacing to avoid jarring transitions
- Minimum loud part duration filtering

## 🚀 Quick Start

### Enhanced Interface (Recommended)

The new enhanced interface provides the best user experience:

```bash
pip install PyQt6 moviepy tqdm numpy
python jump_cutter_gui_enhanced.py
```

### Legacy Interfaces

**Qt Interface** (original):
```bash
pip install PyQt6
python jump_cutter_gui_qt.py
```

**Tkinter Interface** (basic):
```bash
python jump_cutter_gui.py
```

## 📦 Installation

### Requirements
- Python 3.7+
- FFmpeg (for video processing)

### Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install moviepy PyQt6 tqdm numpy Pillow
```

## 🎮 Usage Guide

### 1. Single Video Processing

1. **Select Input**: Choose your video file or drag & drop
2. **Choose Preset**: Pick a preset that matches your content type
3. **Adjust Parameters**: Fine-tune settings if needed
4. **Select Platform**: Choose export optimization (optional)
5. **Process**: Click "Process Video" and wait for completion

### 2. Batch Processing

1. Switch to the "Batch Processing" tab
2. Add multiple files using "Add Files" or drag & drop
3. Configure settings in the "Single Video" tab
4. Click "Process All Files" to start batch processing

### 3. Parameter Tuning

- **Lower magnitude threshold** = detects more silence (more aggressive)
- **Higher duration threshold** = only removes longer silences
- **Higher failure tolerance** = more forgiving detection
- **More edge spacing** = smoother transitions

## 🔧 Advanced Features

### Platform-Specific Optimization

Export presets automatically configure codec and bitrate settings:

- **YouTube**: High quality for long-form content
- **Instagram**: Optimized for social media
- **TikTok**: Perfect for short-form vertical videos
- **Twitter**: Compressed for social sharing

### Custom Presets

You can modify presets in `presets.py` or create your own:

```python
my_preset = {
    "name": "My Custom Preset",
    "description": "Tailored for my specific needs",
    "magnitude_threshold_ratio": 0.025,
    "duration_threshold": 0.8,
    "failure_tolerance_ratio": 0.06,
    "space_on_edges": 0.12,
    "min_loud_part_duration": 0.3,
    "cut": "silent"
}
```

## 📦 Deployment

### Standalone Executables

Create standalone applications using PyInstaller:

```bash
pip install pyinstaller

# Enhanced GUI (recommended)
pyinstaller --onefile --windowed --icon icon.ico jump_cutter_gui_enhanced.py

# Original Qt GUI
pyinstaller --onefile --windowed --icon icon.ico jump_cutter_gui_qt.py
```

This creates executables in the `dist` folder:
- **Windows**: `.exe` file
- **macOS**: `.app` bundle
- **Linux**: Executable binary

### Distribution

The standalone executable can be distributed without requiring Python installation.

## 🧠 How It Works

JumpCutter Pro analyzes the audio track of your video to identify silent segments:

1. **Audio Analysis**: Extracts audio and analyzes magnitude levels
2. **Silence Detection**: Identifies segments below the threshold
3. **Smart Filtering**: Applies duration and tolerance filters
4. **Intelligent Cutting**: Removes silence while preserving natural flow
5. **Video Reconstruction**: Reassembles the video without silent parts

The application uses advanced algorithms to ensure smooth transitions and maintain audio-video synchronization.

## 🔍 Technical Details

### Supported Formats

**Input**: MP4, AVI, MKV, MOV, FLV, WMV, WebM, M4V, 3GP
**Output**: MP4, AVI, MKV, MOV (depends on codec selection)

### Performance

- **Processing Speed**: Typically 0.1x - 0.5x of video duration
- **Memory Usage**: Optimized for large files
- **Quality**: Lossless cutting with optional re-encoding

## 🤝 Contributing

We welcome contributions! Here are some ways to help:

### Priority Features
- [ ] Real-time preview with timeline
- [ ] AI-powered silence detection
- [ ] Cloud processing integration
- [ ] Plugin system for extensions
- [ ] Advanced audio visualization
- [ ] Team collaboration features

### Getting Started
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🏢 Commercial Use

### Business Model Opportunities

**JumpCutter Pro** has potential as a commercial product:

#### Target Markets
- **Content Creators**: YouTubers, podcasters, educators
- **Businesses**: Training videos, presentations, webinars
- **Educational Institutions**: Lecture recordings, online courses
- **Media Companies**: Post-production workflows

#### Monetization Strategies
- **Freemium Model**: Basic features free, advanced features paid
- **Subscription Tiers**: Different feature sets for different users
- **Enterprise Licensing**: Bulk processing, API access, custom integrations
- **Educational Pricing**: Special rates for schools and universities

#### Value Propositions
- **Time Savings**: Reduce editing time by 80%
- **Improved Engagement**: Shorter, more engaging content
- **Professional Quality**: Broadcast-ready output
- **Workflow Integration**: API for automation

## 🛠️ Development Roadmap

### Phase 1: Foundation ✅
- [x] Enhanced UI with presets
- [x] Batch processing capability
- [x] Platform-specific export presets
- [x] Improved documentation

### Phase 2: Intelligence (In Progress)
- [ ] Smart parameter detection
- [ ] Content type auto-detection
- [ ] Quality assurance checks
- [ ] Performance optimization

### Phase 3: Professional Features
- [ ] Real-time preview
- [ ] Manual cut point editing
- [ ] Audio waveform visualization
- [ ] Advanced export options

### Phase 4: Enterprise
- [ ] API for automation
- [ ] Cloud processing
- [ ] Team collaboration
- [ ] Analytics dashboard

## Acknowledgements
We would like to extend our sincerest gratitude to Kivanc Yuksel (emkademy@gmail.com) for creating this useful tool. The original source code can be found at the following repository: https://github.com/kivancyuksel/jumpcutter.git

This software is distributed under the MIT License.

### Contact
If you have any questions, suggestions, or need assistance, please feel free to reach out to me at:
Email: umut.keltek@gmail.com
