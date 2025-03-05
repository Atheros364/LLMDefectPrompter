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

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Paste your defect description in the top text box
3. Select a prompt template file (optional)
4. Select a project context file (optional)
5. Choose your project's root folder
6. Select relevant files from the file tree
7. Click "Generate & Copy Prompt" to create and copy the structured prompt

## File Structure

- `main.py`: Application entry point
- `ui.py`: Main UI implementation
- `settings.json`: Persistent settings storage
- `requirements.txt`: Python dependencies
- `templates/`: Directory for prompt templates 