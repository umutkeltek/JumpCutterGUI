import sys
from pathlib import Path
from PyQt6 import QtWidgets, QtCore, QtGui
from jumpcutter import main as jump_cutter_main

class Worker(QtCore.QThread):
    finished = QtCore.pyqtSignal(str)

    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        try:
            jump_cutter_main(self.args)
            self.finished.emit('Done!')
        except Exception as e:
            self.finished.emit(f'Error: {e}')

class JumpCutterQt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Jump Cutter Qt')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        QtWidgets.QApplication.setStyle('Fusion')
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        layout.addLayout(form)

        # Input file
        file_layout = QtWidgets.QHBoxLayout()
        self.input_edit = QtWidgets.QLineEdit()
        browse_btn = QtWidgets.QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_input)
        file_layout.addWidget(self.input_edit)
        file_layout.addWidget(browse_btn)
        form.addRow('Input video:', file_layout)

        # Output file
        self.output_edit = QtWidgets.QLineEdit()
        form.addRow('Output video:', self.output_edit)

        # Magnitude threshold
        self.mag_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.mag_slider.setRange(0, 100)
        self.mag_slider.setValue(3)
        self.mag_slider.setSingleStep(1)
        form.addRow('Magnitude threshold (%):', self.mag_slider)

        # Duration threshold
        self.duration_spin = QtWidgets.QDoubleSpinBox()
        self.duration_spin.setRange(0.0, 10.0)
        self.duration_spin.setSingleStep(0.1)
        self.duration_spin.setValue(1.5)
        form.addRow('Duration threshold:', self.duration_spin)

        # Failure tolerance
        self.fail_spin = QtWidgets.QDoubleSpinBox()
        self.fail_spin.setRange(0.0, 1.0)
        self.fail_spin.setSingleStep(0.01)
        self.fail_spin.setValue(0.07)
        form.addRow('Failure tolerance:', self.fail_spin)

        # Space on edges
        self.space_spin = QtWidgets.QDoubleSpinBox()
        self.space_spin.setRange(0.0, 2.0)
        self.space_spin.setSingleStep(0.1)
        form.addRow('Space on edges:', self.space_spin)

        # Silence part speed
        self.silence_check = QtWidgets.QCheckBox('Include silence')
        self.silence_speed_spin = QtWidgets.QDoubleSpinBox()
        self.silence_speed_spin.setRange(0.1, 5.0)
        self.silence_speed_spin.setSingleStep(0.1)
        self.silence_speed_spin.setEnabled(False)
        self.silence_check.toggled.connect(self.silence_speed_spin.setEnabled)
        sil_layout = QtWidgets.QHBoxLayout()
        sil_layout.addWidget(self.silence_check)
        sil_layout.addWidget(self.silence_speed_spin)
        form.addRow('Silence speed:', sil_layout)

        # Minimum loud part duration
        self.min_loud_check = QtWidgets.QCheckBox('Enable')
        self.min_loud_spin = QtWidgets.QDoubleSpinBox()
        self.min_loud_spin.setRange(0.0, 5.0)
        self.min_loud_spin.setSingleStep(0.1)
        self.min_loud_spin.setEnabled(False)
        self.min_loud_check.toggled.connect(self.min_loud_spin.setEnabled)
        loud_layout = QtWidgets.QHBoxLayout()
        loud_layout.addWidget(self.min_loud_check)
        loud_layout.addWidget(self.min_loud_spin)
        form.addRow('Min loud duration:', loud_layout)

        # Codec and bitrate
        self.codec_check = QtWidgets.QCheckBox('Specify codec')
        self.codec_edit = QtWidgets.QLineEdit()
        self.codec_edit.setEnabled(False)
        self.codec_check.toggled.connect(self.codec_edit.setEnabled)
        codec_layout = QtWidgets.QHBoxLayout()
        codec_layout.addWidget(self.codec_check)
        codec_layout.addWidget(self.codec_edit)
        form.addRow('Codec:', codec_layout)

        self.bitrate_check = QtWidgets.QCheckBox('Specify bitrate')
        self.bitrate_edit = QtWidgets.QLineEdit()
        self.bitrate_edit.setEnabled(False)
        self.bitrate_check.toggled.connect(self.bitrate_edit.setEnabled)
        bitrate_layout = QtWidgets.QHBoxLayout()
        bitrate_layout.addWidget(self.bitrate_check)
        bitrate_layout.addWidget(self.bitrate_edit)
        form.addRow('Bitrate:', bitrate_layout)

        # Cut option
        self.cut_check = QtWidgets.QCheckBox('Enable')
        self.cut_combo = QtWidgets.QComboBox()
        self.cut_combo.addItems(['silent', 'voiced', 'both'])
        self.cut_combo.setEnabled(False)
        self.cut_check.toggled.connect(self.cut_combo.setEnabled)
        cut_layout = QtWidgets.QHBoxLayout()
        cut_layout.addWidget(self.cut_check)
        cut_layout.addWidget(self.cut_combo)
        form.addRow('Cut parts:', cut_layout)

        # Progress and logs
        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        # Run button
        self.run_btn = QtWidgets.QPushButton('Run')
        self.run_btn.clicked.connect(self.on_run)
        layout.addWidget(self.run_btn)

    def browse_input(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select video')
        if path:
            self.input_edit.setText(path)
            output = Path(path).stem + '_autocut' + ''.join(Path(path).suffixes)
            self.output_edit.setText(output)

    def on_run(self):
        args = ['-i', self.input_edit.text(), '-o', self.output_edit.text(),
                '--magnitude-threshold-ratio', str(self.mag_slider.value()/100)]
        if self.duration_spin.value() > 0:
            args.extend(['--duration-threshold', str(self.duration_spin.value())])
        if self.fail_spin.value() > 0:
            args.extend(['--failure-tolerance-ratio', str(self.fail_spin.value())])
        if self.space_spin.value() > 0:
            args.extend(['--space-on-edges', str(self.space_spin.value())])
        if self.silence_check.isChecked():
            args.extend(['--silence-part-speed', str(self.silence_speed_spin.value())])
        if self.min_loud_check.isChecked():
            args.extend(['--min-loud-part-duration', str(self.min_loud_spin.value())])
        if self.codec_check.isChecked() and self.codec_edit.text():
            args.extend(['--codec', self.codec_edit.text()])
        if self.bitrate_check.isChecked() and self.bitrate_edit.text():
            args.extend(['--bitrate', self.bitrate_edit.text()])
        if self.cut_check.isChecked():
            args.extend(['--cut', self.cut_combo.currentText()])

        self.log.append('Processing video...')
        self.run_btn.setEnabled(False)
        self.progress.setRange(0, 0)

        self.worker = Worker(args)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, message: str):
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.run_btn.setEnabled(True)
        self.log.append(message)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = JumpCutterQt()
    gui.resize(500, 600)
    gui.show()
    sys.exit(app.exec())
