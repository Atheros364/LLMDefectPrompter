# LLM Defect Prompt Generator

A cross-platform desktop application that helps software developers generate structured prompts for diagnosing software defects with Large Language Models (LLMs).

## Features

- Input box for defect descriptions
- Template file selection for prompt structure
- Context file selection for project details
- Project root folder selection
- File tree for selecting relevant code files
- Automatic prompt generation and clipboard copying
- Persistent settings across sessions

## Development Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .\.venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Building the Executable

### Prerequisites
Install PyInstaller:
```bash
pip install pyinstaller
```

### Building

1. For all platforms, use:
   ```bash
   pyinstaller app.spec
   ```

The executable will be created in the `dist` folder:
- Windows: `dist/LLMDefectPrompter.exe`
- macOS: `dist/LLMDefectPrompter.app`
- Linux: `dist/LLMDefectPrompter`

### Platform-Specific Notes

#### Windows
- Double-click `LLMDefectPrompter.exe` to run
- Or run from command line: `.\dist\LLMDefectPrompter.exe`

#### macOS
- Double-click `LLMDefectPrompter.app` to run
- Or run from terminal: `open dist/LLMDefectPrompter.app`
- If you get a security warning, go to System Preferences > Security & Privacy to allow the app

#### Linux
- Make the file executable: `chmod +x dist/LLMDefectPrompter`
- Run: `./dist/LLMDefectPrompter`

## Usage

1. Launch the application using the appropriate method for your platform
2. Paste your defect description in the top text box
3. Select a prompt template file (optional)
4. Select a project context file (optional)
5. Choose your project's root folder
6. Select relevant files from the file tree
7. Click "Generate Prompt" to create and copy the structured prompt

## Project Structure

- `main.py`: Application entry point
- `ui.py`: Main UI implementation
- `settings.json`: Persistent settings storage
- `requirements.txt`: Python dependencies
- `templates/`: Directory for prompt templates
- `assets/`: Application icons and resources
- `app.spec`: PyInstaller specification file

## Requirements

- Python 3.7 or higher
- PyQt6
- pyperclip
- Operating System: Windows 10+, macOS 10.13+, or Linux with X11/Wayland 
