from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QFileDialog, QLabel
)
from PyQt6.QtCore import Qt, QSettings
import os
import json
import pyperclip


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Defect Prompt Generator")
        self.setMinimumSize(800, 600)

        # Initialize settings
        self.settings = {}
        self.load_settings()

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Defect description section
        layout.addWidget(QLabel("Defect Description:"))
        self.defect_input = QTextEdit()
        layout.addWidget(self.defect_input)

        # File selection buttons
        button_layout = QHBoxLayout()

        self.template_btn = QPushButton("Select Template")
        self.template_btn.clicked.connect(self.select_template)
        button_layout.addWidget(self.template_btn)

        self.context_btn = QPushButton("Select Context")
        self.context_btn.clicked.connect(self.select_context)
        button_layout.addWidget(self.context_btn)

        self.root_btn = QPushButton("Select Root Folder")
        self.root_btn.clicked.connect(self.select_root_folder)
        button_layout.addWidget(self.root_btn)

        layout.addLayout(button_layout)

        # File paths display
        self.template_label = QLabel("Template: Not selected")
        self.context_label = QLabel("Context: Not selected")
        self.root_label = QLabel("Root Folder: Not selected")
        layout.addWidget(self.template_label)
        layout.addWidget(self.context_label)
        layout.addWidget(self.root_label)

        # File tree
        layout.addWidget(QLabel("Select Project Files:"))
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel("Project Files")
        self.file_tree.setSelectionMode(
            QTreeWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.file_tree)

        # Generate button and output
        self.generate_btn = QPushButton("Generate & Copy Prompt")
        self.generate_btn.clicked.connect(self.generate_prompt)
        layout.addWidget(self.generate_btn)

        layout.addWidget(QLabel("Generated Prompt:"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        # Load saved settings
        self.apply_saved_settings()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {
                "prompt_template": "",
                "context_file": "",
                "root_folder": ""
            }

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)

    def apply_saved_settings(self):
        if self.settings.get("prompt_template"):
            self.template_label.setText(
                f"Template: {self.settings['prompt_template']}")
        if self.settings.get("context_file"):
            self.context_label.setText(
                f"Context: {self.settings['context_file']}")
        if self.settings.get("root_folder"):
            self.root_label.setText(
                f"Root Folder: {self.settings['root_folder']}")
            self.populate_file_tree()

    def select_template(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Template File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.settings["prompt_template"] = file_path
            self.template_label.setText(f"Template: {file_path}")
            self.save_settings()

    def select_context(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Context File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.settings["context_file"] = file_path
            self.context_label.setText(f"Context: {file_path}")
            self.save_settings()

    def select_root_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Root Folder"
        )
        if folder_path:
            self.settings["root_folder"] = folder_path
            self.root_label.setText(f"Root Folder: {folder_path}")
            self.save_settings()
            self.populate_file_tree()

    def populate_file_tree(self):
        self.file_tree.clear()
        root_path = self.settings.get("root_folder")
        if not root_path:
            return

        root_item = QTreeWidgetItem(
            self.file_tree, [os.path.basename(root_path)])
        self._populate_tree_recursive(root_path, root_item)
        self.file_tree.expandAll()

    def _populate_tree_recursive(self, path, parent_item):
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                item = QTreeWidgetItem(parent_item, [entry])
                if os.path.isdir(full_path):
                    self._populate_tree_recursive(full_path, item)
        except PermissionError:
            pass

    def get_selected_files(self):
        selected_files = []
        for item in self.file_tree.selectedItems():
            path_parts = []
            current = item
            while current:
                path_parts.insert(0, current.text(0))
                current = current.parent()
            full_path = os.path.join(
                self.settings["root_folder"], *path_parts[1:])
            if os.path.isfile(full_path):
                selected_files.append(full_path)
        return selected_files

    def generate_prompt(self):
        # Read template
        template_content = ""
        if os.path.exists(self.settings.get("prompt_template", "")):
            with open(self.settings["prompt_template"], 'r') as f:
                template_content = f.read()

        # Read context
        context_content = ""
        if os.path.exists(self.settings.get("context_file", "")):
            with open(self.settings["context_file"], 'r') as f:
                context_content = f.read()

        # Get selected files
        selected_files = self.get_selected_files()

        # Build prompt
        prompt = f"{template_content}\n\n"
        prompt += f"**Defect Description:**\n{self.defect_input.toPlainText()}\n\n"
        prompt += f"**Project Context:**\n{context_content}\n\n"

        # Add file structure
        prompt += "**Project File Structure:**\n"
        for file in selected_files:
            prompt += f"{os.path.relpath(file, self.settings['root_folder'])}\n"

        # Add file contents
        prompt += "\n**File Contents:**\n"
        for file in selected_files:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                rel_path = os.path.relpath(file, self.settings['root_folder'])
                prompt += f"\n[File: {rel_path}]\n{content}\n"
            except Exception as e:
                prompt += f"\n[Error reading {file}: {str(e)}]\n"

        self.output_text.setText(prompt)
        pyperclip.copy(prompt)
