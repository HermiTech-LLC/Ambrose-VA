# Ambrose-VI

## Introduction
This project is a voice-activated personal assistant that interacts with the Wolfram Alpha API to provide information based on user queries. It listens for wake words, processes voice commands, and converts text to speech for user interaction.

## Features
- **Wake Word Detection:** Listens for specific wake words ("hey wolfram", "wolfram") to activate the assistant.
- **Voice Input:** Processes voice input from the user after the wake word is detected.
- **Wolfram Alpha Integration:** Queries the Wolfram Alpha API for information based on user queries.
- **Text-to-Speech:** Converts API responses to speech for user interaction.
- **Language Support:** Supports multiple languages (English, Spanish, German, French).

## Installation
1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/HermiTech-LLC/Ambrose-VI.git
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Obtain a Wolfram Alpha API key and update the `config.ini` file with your API key.

## Usage
1. Run the assistant using the command line interface:
    ```bash
    python cli.py --lang <language_code>
    ```
    Replace `<language_code>` with the desired language code (e.g., "en" for English, "es" for Spanish).

2. Say one of the wake words ("hey wolfram", "wolfram") to activate the assistant.

3. Speak your query after the wake word.

4. The assistant will process your query and provide the answer.

5. To exit the program, say the exit phrase ("exit program").

## Configuration
- `config.ini`: Configuration file for API keys and settings.

## Directory Structure
- `assistant.py`: Main script for the voice assistant application.
- `cli.py`: Command-line interface script for running the assistant.
- `setup.py`: Setuptools configuration for installing the package.
- `setup.sh`: Bash script for setting up the virtual environment and installing dependencies.
- `requirements.txt`: List of Python dependencies.
- `README.md`: Readme file with project information and usage instructions.

## Dependencies
- `requests`: HTTP library for API requests.
- `speech_recognition`: Speech recognition library.
- `gtts`: Google Text-to-Speech library.
- `pygame`: Library for audio playback.

## License
This project is licensed under the [MIT License](LICENSE).
