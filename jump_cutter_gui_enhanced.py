"""
Enhanced Jump Cutter GUI with improved UI/UX and preset system.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QFormLayout, QGroupBox, QLabel, QLineEdit, QPushButton,
    QSlider, QDoubleSpinBox, QSpinBox, QComboBox, QCheckBox, QProgressBar,
    QTextEdit, QFileDialog, QTabWidget, QListWidget, QMessageBox,
    QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont, QPixmap

try:
    from jumpcutter import main as jump_cutter_main
    from presets import PRESETS, EXPORT_PRESETS, get_preset, get_export_preset
except ImportError:
    # Fallback if imports fail
    PRESETS = {}
    EXPORT_PRESETS = {}
    def get_preset(name): return {}
    def get_export_preset(name): return {}
    def jump_cutter_main(args): print(f"Would process with args: {args}")


class ProcessingWorker(QThread):
    """Worker thread for video processing to keep UI responsive."""
    
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress_update = pyqtSignal(str)
    
    def __init__(self, args: List[str]):
        super().__init__()
        self.args = args
        
    def run(self):
        try:
            self.progress_update.emit("Starting video processing...")
            jump_cutter_main(self.args)
            self.finished.emit("Video processing completed successfully!")
        except Exception as e:
            self.error.emit(f"Error during processing: {str(e)}")


class FileListWidget(QListWidget):
    """Enhanced list widget for batch file processing with drag-and-drop."""
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        video_files = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv'))]
        
        for file_path in video_files:
            self.addItem(file_path)


class ParameterGroupBox(QGroupBox):
    """Reusable group box for parameter sections."""
    
    def __init__(self, title: str, description: str = ""):
        super().__init__(title)
        self.description = description
        self.layout = QFormLayout(self)
        self.setLayout(self.layout)
        
        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 10px;")
            self.layout.addRow(desc_label)


class EnhancedJumpCutterGUI(QMainWindow):
    """Enhanced Jump Cutter GUI with modern design and advanced features."""
    
    def __init__(self):
        super().__init__()
        self.current_preset = None
        self.batch_files = []
        self.processing_worker = None
        
        self.init_ui()
        self.setup_styles()
        self.load_default_preset()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Jump Cutter Pro - Advanced Video Silence Remover")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setMinimumSize(900, 700)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tabbed interface
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Main processing tab
        self.create_main_tab()
        
        # Batch processing tab
        self.create_batch_tab()
        
        # Settings tab
        self.create_settings_tab()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
    def create_main_tab(self):
        """Create the main processing tab."""
        main_tab = QWidget()
        self.tab_widget.addTab(main_tab, "Single Video")
        
        layout = QVBoxLayout(main_tab)
        
        # File selection section
        file_group = ParameterGroupBox("File Selection", "Select input video and output location")
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Select input video file...")
        input_browse_btn = QPushButton("Browse")
        input_browse_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(input_browse_btn)
        file_group.layout.addRow("Input Video:", input_layout)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Output will be auto-generated...")
        output_browse_btn = QPushButton("Browse")
        output_browse_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(output_browse_btn)
        file_group.layout.addRow("Output Video:", output_layout)
        
        layout.addWidget(file_group)
        
        # Preset selection section
        preset_group = ParameterGroupBox("Quick Presets", "Choose a preset for your content type")
        
        preset_layout = QHBoxLayout()
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("Custom", "")
        for preset_name, preset_data in PRESETS.items():
            self.preset_combo.addItem(preset_data["name"], preset_name)
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        
        self.preset_description = QLabel("Configure parameters manually")
        self.preset_description.setWordWrap(True)
        self.preset_description.setStyleSheet("color: #666; font-style: italic;")
        
        preset_layout.addWidget(self.preset_combo)
        preset_layout.addWidget(self.preset_description)
        preset_layout.addStretch()
        
        preset_group.layout.addRow("Content Preset:", preset_layout)
        layout.addWidget(preset_group)
        
        # Parameters section
        self.create_parameters_section(layout)
        
        # Export presets section
        export_group = ParameterGroupBox("Export Settings", "Platform-specific optimization")
        
        export_layout = QHBoxLayout()
        self.export_combo = QComboBox()
        self.export_combo.addItem("Default", "")
        for export_name, export_data in EXPORT_PRESETS.items():
            self.export_combo.addItem(export_data["name"], export_name)
        self.export_combo.currentTextChanged.connect(self.on_export_preset_changed)
        
        export_layout.addWidget(self.export_combo)
        export_layout.addStretch()
        
        export_group.layout.addRow("Platform:", export_layout)
        layout.addWidget(export_group)
        
        # Processing section
        self.create_processing_section(layout)
        
    def create_batch_tab(self):
        """Create the batch processing tab."""
        batch_tab = QWidget()
        self.tab_widget.addTab(batch_tab, "Batch Processing")
        
        layout = QVBoxLayout(batch_tab)
        
        # Instructions
        instructions = QLabel(
            "Drag and drop multiple video files or use the Add Files button. "
            "All files will be processed with the same settings from the Single Video tab."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("background: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;")
        layout.addWidget(instructions)
        
        # File list and controls
        file_section = QHBoxLayout()
        
        # File list
        file_list_layout = QVBoxLayout()
        file_list_layout.addWidget(QLabel("Files to Process:"))
        self.batch_file_list = FileListWidget()
        file_list_layout.addWidget(self.batch_file_list)
        
        # Controls
        controls_layout = QVBoxLayout()
        add_files_btn = QPushButton("Add Files")
        add_files_btn.clicked.connect(self.add_batch_files)
        remove_file_btn = QPushButton("Remove Selected")
        remove_file_btn.clicked.connect(self.remove_batch_file)
        clear_files_btn = QPushButton("Clear All")
        clear_files_btn.clicked.connect(self.clear_batch_files)
        
        controls_layout.addWidget(add_files_btn)
        controls_layout.addWidget(remove_file_btn)
        controls_layout.addWidget(clear_files_btn)
        controls_layout.addStretch()
        
        file_section.addLayout(file_list_layout, 3)
        file_section.addLayout(controls_layout, 1)
        
        layout.addLayout(file_section)
        
        # Batch processing controls
        batch_controls = QHBoxLayout()
        self.batch_process_btn = QPushButton("Process All Files")
        self.batch_process_btn.clicked.connect(self.process_batch_files)
        self.batch_process_btn.setEnabled(False)
        
        batch_controls.addStretch()
        batch_controls.addWidget(self.batch_process_btn)
        
        layout.addLayout(batch_controls)
        
    def create_settings_tab(self):
        """Create the settings/help tab."""
        settings_tab = QWidget()
        self.tab_widget.addTab(settings_tab, "Help & Settings")
        
        layout = QVBoxLayout(settings_tab)
        
        # Help section
        help_group = QGroupBox("Parameter Guide")
        help_layout = QVBoxLayout(help_group)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
        <h3>Parameter Explanations:</h3>
        <p><b>Magnitude Threshold Ratio:</b> Controls sensitivity to silence detection. Lower values detect more silence.</p>
        <p><b>Duration Threshold:</b> Minimum length of silence (in seconds) before it's considered for removal.</p>
        <p><b>Failure Tolerance Ratio:</b> Tolerance for imperfect silence detection. Higher values are more forgiving.</p>
        <p><b>Space on Edges:</b> Time (in seconds) to leave around cuts to avoid jarring transitions.</p>
        <p><b>Min Loud Part Duration:</b> Minimum length of non-silent parts to keep.</p>
        
        <h3>Presets Guide:</h3>
        <p><b>Podcast:</b> Optimized for speech content with natural pauses.</p>
        <p><b>Lecture:</b> For educational content with longer natural pauses.</p>
        <p><b>Tutorial:</b> For screen recordings and demonstrations.</p>
        <p><b>Meeting:</b> For multi-speaker content like interviews.</p>
        <p><b>Aggressive:</b> Maximum silence removal for tight editing.</p>
        <p><b>Conservative:</b> Gentle removal preserving natural flow.</p>
        """)
        
        help_layout.addWidget(help_text)
        layout.addWidget(help_group)
        
    def create_parameters_section(self, layout):
        """Create the parameters configuration section."""
        params_group = ParameterGroupBox("Processing Parameters", "Fine-tune silence detection and cutting behavior")
        params_layout = QGridLayout()
        
        # Magnitude threshold
        self.mag_slider = QSlider(Qt.Orientation.Horizontal)
        self.mag_slider.setRange(1, 100)
        self.mag_slider.setValue(20)
        self.mag_value_label = QLabel("0.020")
        self.mag_slider.valueChanged.connect(lambda v: self.mag_value_label.setText(f"{v/1000:.3f}"))
        
        mag_layout = QHBoxLayout()
        mag_layout.addWidget(self.mag_slider)
        mag_layout.addWidget(self.mag_value_label)
        params_layout.addWidget(QLabel("Magnitude Threshold:"), 0, 0)
        params_layout.addLayout(mag_layout, 0, 1)
        
        # Duration threshold
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.1, 10.0)
        self.duration_spin.setValue(0.5)
        self.duration_spin.setSingleStep(0.1)
        self.duration_spin.setSuffix(" sec")
        params_layout.addWidget(QLabel("Duration Threshold:"), 1, 0)
        params_layout.addWidget(self.duration_spin, 1, 1)
        
        # Failure tolerance
        self.tolerance_spin = QDoubleSpinBox()
        self.tolerance_spin.setRange(0.01, 0.5)
        self.tolerance_spin.setValue(0.05)
        self.tolerance_spin.setSingleStep(0.01)
        params_layout.addWidget(QLabel("Failure Tolerance:"), 2, 0)
        params_layout.addWidget(self.tolerance_spin, 2, 1)
        
        # Space on edges
        self.space_spin = QDoubleSpinBox()
        self.space_spin.setRange(0.0, 1.0)
        self.space_spin.setValue(0.1)
        self.space_spin.setSingleStep(0.05)
        self.space_spin.setSuffix(" sec")
        params_layout.addWidget(QLabel("Space on Edges:"), 3, 0)
        params_layout.addWidget(self.space_spin, 3, 1)
        
        # Min loud part duration
        self.min_loud_spin = QDoubleSpinBox()
        self.min_loud_spin.setRange(0.1, 5.0)
        self.min_loud_spin.setValue(0.3)
        self.min_loud_spin.setSingleStep(0.1)
        self.min_loud_spin.setSuffix(" sec")
        params_layout.addWidget(QLabel("Min Loud Duration:"), 4, 0)
        params_layout.addWidget(self.min_loud_spin, 4, 1)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
    def create_processing_section(self, layout):
        """Create the processing controls section."""
        process_group = QGroupBox("Processing")
        process_layout = QVBoxLayout(process_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        process_layout.addWidget(self.progress_bar)
        
        # Process button
        button_layout = QHBoxLayout()
        self.process_btn = QPushButton("Process Video")
        self.process_btn.clicked.connect(self.process_video)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.process_btn)
        button_layout.addStretch()
        
        process_layout.addLayout(button_layout)
        
        # Log output
        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(150)
        self.log_output.setReadOnly(True)
        process_layout.addWidget(QLabel("Processing Log:"))
        process_layout.addWidget(self.log_output)
        
        layout.addWidget(process_group)
        
    def setup_styles(self):
        """Apply modern styling to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 8px 15px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #007bff;
            }
        """)
        
    def load_default_preset(self):
        """Load the default preset."""
        self.preset_combo.setCurrentText("Podcast")
        
    def on_preset_changed(self):
        """Handle preset selection change."""
        preset_name = self.preset_combo.currentData()
        if preset_name:
            preset = get_preset(preset_name)
            if preset:
                self.current_preset = preset_name
                self.apply_preset(preset)
                self.preset_description.setText(preset.get("description", ""))
        else:
            self.current_preset = None
            self.preset_description.setText("Configure parameters manually")
            
    def apply_preset(self, preset: Dict[str, Any]):
        """Apply preset values to the UI controls."""
        if "magnitude_threshold_ratio" in preset:
            value = int(preset["magnitude_threshold_ratio"] * 1000)
            self.mag_slider.setValue(value)
            
        if "duration_threshold" in preset:
            self.duration_spin.setValue(preset["duration_threshold"])
            
        if "failure_tolerance_ratio" in preset:
            self.tolerance_spin.setValue(preset["failure_tolerance_ratio"])
            
        if "space_on_edges" in preset:
            self.space_spin.setValue(preset["space_on_edges"])
            
        if "min_loud_part_duration" in preset:
            self.min_loud_spin.setValue(preset["min_loud_part_duration"])
            
    def on_export_preset_changed(self):
        """Handle export preset selection change."""
        export_name = self.export_combo.currentData()
        if export_name:
            export_preset = get_export_preset(export_name)
            suggested = export_preset.get("suggested_settings", {})
            if suggested:
                # Apply suggested settings
                if "magnitude_threshold_ratio" in suggested:
                    value = int(suggested["magnitude_threshold_ratio"] * 1000)
                    self.mag_slider.setValue(value)
                if "duration_threshold" in suggested:
                    self.duration_spin.setValue(suggested["duration_threshold"])
                    
    def browse_input_file(self):
        """Browse for input video file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Input Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;All Files (*)"
        )
        
        if file_path:
            self.input_edit.setText(file_path)
            # Auto-generate output filename
            input_path = Path(file_path)
            output_path = input_path.parent / f"{input_path.stem}_processed{input_path.suffix}"
            self.output_edit.setText(str(output_path))
            
    def browse_output_file(self):
        """Browse for output video file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)"
        )
        
        if file_path:
            self.output_edit.setText(file_path)
            
    def add_batch_files(self):
        """Add files to batch processing list."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;All Files (*)"
        )
        
        for file_path in file_paths:
            self.batch_file_list.addItem(file_path)
            
        self.batch_process_btn.setEnabled(self.batch_file_list.count() > 0)
        
    def remove_batch_file(self):
        """Remove selected file from batch list."""
        current_item = self.batch_file_list.currentItem()
        if current_item:
            self.batch_file_list.takeItem(self.batch_file_list.row(current_item))
            
        self.batch_process_btn.setEnabled(self.batch_file_list.count() > 0)
        
    def clear_batch_files(self):
        """Clear all files from batch list."""
        self.batch_file_list.clear()
        self.batch_process_btn.setEnabled(False)
        
    def get_processing_args(self, input_path: str, output_path: str) -> List[str]:
        """Generate processing arguments from current UI state."""
        args = [
            "--input", input_path,
            "--output", output_path,
            "--magnitude-threshold-ratio", str(self.mag_slider.value() / 1000),
            "--duration-threshold", str(self.duration_spin.value()),
            "--failure-tolerance-ratio", str(self.tolerance_spin.value()),
            "--space-on-edges", str(self.space_spin.value()),
            "--min-loud-part-duration", str(self.min_loud_spin.value()),
            "--cut", "silent"
        ]
        
        # Add export preset settings if selected
        export_name = self.export_combo.currentData()
        if export_name:
            export_preset = get_export_preset(export_name)
            if "codec" in export_preset:
                args.extend(["--codec", export_preset["codec"]])
            if "bitrate" in export_preset:
                args.extend(["--bitrate", export_preset["bitrate"]])
                
        return args
        
    def process_video(self):
        """Process a single video."""
        input_path = self.input_edit.text().strip()
        output_path = self.output_edit.text().strip()
        
        if not input_path or not output_path:
            QMessageBox.warning(self, "Error", "Please select both input and output files.")
            return
            
        if not Path(input_path).exists():
            QMessageBox.warning(self, "Error", "Input file does not exist.")
            return
            
        self.start_processing(input_path, output_path)
        
    def process_batch_files(self):
        """Process all files in the batch list."""
        if self.batch_file_list.count() == 0:
            return
            
        # For now, process first file as example
        # In a full implementation, you'd process all files sequentially
        first_item = self.batch_file_list.item(0)
        if first_item:
            input_path = first_item.text()
            input_path_obj = Path(input_path)
            output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_processed{input_path_obj.suffix}")
            self.start_processing(input_path, output_path)
            
    def start_processing(self, input_path: str, output_path: str):
        """Start video processing in a worker thread."""
        args = self.get_processing_args(input_path, output_path)
        
        self.processing_worker = ProcessingWorker(args)
        self.processing_worker.finished.connect(self.on_processing_finished)
        self.processing_worker.error.connect(self.on_processing_error)
        self.processing_worker.progress_update.connect(self.on_progress_update)
        
        # Update UI for processing state
        self.process_btn.setEnabled(False)
        self.batch_process_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.status_bar.showMessage("Processing...")
        
        self.processing_worker.start()
        
    def on_processing_finished(self, message: str):
        """Handle successful processing completion."""
        self.log_output.append(f"✅ {message}")
        self.reset_ui_after_processing()
        QMessageBox.information(self, "Success", message)
        
    def on_processing_error(self, error_message: str):
        """Handle processing error."""
        self.log_output.append(f"❌ {error_message}")
        self.reset_ui_after_processing()
        QMessageBox.critical(self, "Error", error_message)
        
    def on_progress_update(self, message: str):
        """Handle progress updates."""
        self.log_output.append(f"ℹ️ {message}")
        self.status_bar.showMessage(message)
        
    def reset_ui_after_processing(self):
        """Reset UI to ready state after processing."""
        self.process_btn.setEnabled(True)
        self.batch_process_btn.setEnabled(self.batch_file_list.count() > 0)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Ready")


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application properties
    app.setApplicationName("Jump Cutter Pro")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Jump Cutter")
    
    window = EnhancedJumpCutterGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()