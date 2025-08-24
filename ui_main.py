from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QVBoxLayout, QTextEdit, QSlider
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os

class RenamerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Batch Image Renamer")
        self.setGeometry(100, 100, 700, 600)
        self.setWindowIcon(QIcon("images/logo.ico"))

        # Inputs
        self.folder_input = QLineEdit()
        self.prefix_input = QLineEdit()
        self.suffix_input = QLineEdit()
        self.find_input = QLineEdit()
        self.replace_input = QLineEdit()
        self.slice_replace_input = QLineEdit()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        # Sliders
        self.start_slider = QSlider(Qt.Horizontal)
        self.end_slider = QSlider(Qt.Horizontal)
        self.start_slider.setRange(0, 100)
        self.end_slider.setRange(0, 100)
        self.slice_label = QLabel("Slice Range: [0:0]")

        self.start_slider.valueChanged.connect(self.update_preview)
        self.end_slider.valueChanged.connect(self.update_preview)

        # Buttons
        browse_btn = QPushButton("Browse Folder")
        preview_btn = QPushButton("Preview Changes")
        rename_btn = QPushButton("Rename Files")

        browse_btn.clicked.connect(self.browse_folder)
        preview_btn.clicked.connect(self.update_preview)
        rename_btn.clicked.connect(self.rename_files)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Folder:"))
        layout.addWidget(self.folder_input)
        layout.addWidget(browse_btn)
        layout.addWidget(QLabel("Prefix:"))
        layout.addWidget(self.prefix_input)
        layout.addWidget(QLabel("Suffix:"))
        layout.addWidget(self.suffix_input)
        layout.addWidget(QLabel("Find:"))
        layout.addWidget(self.find_input)
        layout.addWidget(QLabel("Replace:"))
        layout.addWidget(self.replace_input)
        layout.addWidget(QLabel("Slice Replace:"))
        layout.addWidget(self.slice_replace_input)
        layout.addWidget(self.slice_label)
        layout.addWidget(QLabel("Start Index:"))
        layout.addWidget(self.start_slider)
        layout.addWidget(QLabel("End Index:"))
        layout.addWidget(self.end_slider)
        layout.addWidget(preview_btn)
        layout.addWidget(rename_btn)
        layout.addWidget(QLabel("Live Preview:"))
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)
            self.update_slider_range(folder)
            self.update_preview()

    def update_slider_range(self, folder):
        files = os.listdir(folder)
        image_exts = (".exr", ".jpg", ".png", ".jpeg", ".tiff", ".bmp", ".exe")
        matching = [f for f in files if f.lower().endswith(image_exts)]
        if matching:
            max_len = max(len(os.path.splitext(f)[0]) for f in matching)
            self.start_slider.setMaximum(max_len)
            self.end_slider.setMaximum(max_len)

    def get_slice_replacement(self, name):
        start = self.start_slider.value()
        end = self.end_slider.value()
        replacement = self.slice_replace_input.text()

        safe_start = min(start, len(name))
        safe_end = min(end, len(name))
        if safe_start > safe_end:
            safe_start, safe_end = safe_end, safe_start

        replaced_segment = name[safe_start:safe_end]
        new_name = name[:safe_start] + replacement + name[safe_end:]
        return new_name, replaced_segment, safe_start, safe_end

    def update_preview(self):
        folder = self.folder_input.text()
        if not folder or not os.path.isdir(folder):
            self.log_output.setText("No folder selected or folder is invalid.")
            return

        start = self.start_slider.value()
        end = self.end_slider.value()
        inject_text = self.slice_replace_input.text()
        prefix = self.prefix_input.text()
        suffix = self.suffix_input.text()
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()

        self.slice_label.setText(f"Slice Range: [{start}:{end}]")
        self.log_output.clear()

        files = os.listdir(folder)
        image_exts = (".exr", ".jpg", ".png", ".jpeg", ".tiff", ".bmp", ".exe")
        matching_files = [f for f in files if f.lower().endswith(image_exts)]

        if not matching_files:
            self.log_output.setText("No matching files found.")
            return

        self.log_output.append("Live Preview:\n")
        for filename in matching_files:
            name, ext = os.path.splitext(filename)
            original_name = name

            if find_text:
                name = name.replace(find_text, replace_text or "")

            sliced_name, replaced_segment, s_start, s_end = self.get_slice_replacement(name)
            final_name = f"{prefix}{sliced_name}{suffix}{ext}"

            self.log_output.append(
                f"{filename}\n"
                f"  ↳ Replacing slice [{s_start}:{s_end}] → '{replaced_segment}' with '{inject_text}'\n"
                f"  ↳ Final name: {final_name}\n"
            )

    def rename_files(self):
        folder = self.folder_input.text()
        if not folder or not os.path.isdir(folder):
            self.log_output.setText("No folder selected or folder is invalid.")
            return

        start = self.start_slider.value()
        end = self.end_slider.value()
        inject_text = self.slice_replace_input.text()
        prefix = self.prefix_input.text()
        suffix = self.suffix_input.text()
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()

        files = os.listdir(folder)
        image_exts = (".exr", ".jpg", ".png", ".jpeg", ".tiff", ".bmp", ".exe")
        matching_files = [f for f in files if f.lower().endswith(image_exts)]

        renamed = []
        for filename in matching_files:
            name, ext = os.path.splitext(filename)

            if find_text:
                name = name.replace(find_text, replace_text or "")

            sliced_name, _, _, _ = self.get_slice_replacement(name)
            final_name = f"{prefix}{sliced_name}{suffix}{ext}"
            src = os.path.join(folder, filename)
            dst = os.path.join(folder, final_name)

            if src != dst:
                os.rename(src, dst)
                renamed.append((filename, final_name))

        self.log_output.clear()
        if renamed:
            self.log_output.append("Renamed files:\n")
            for old, new in renamed:
                self.log_output.append(f"{old} → {new}")
        else:
            self.log_output.append("No files were renamed.")
