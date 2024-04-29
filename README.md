# Ambrose-VA

## Introduction
This project is a voice-activated personal assistant that integrates with the Wolfram Alpha and Dialogflow APIs to provide information and answer queries based on user commands. It features wake word detection, voice command processing, and text-to-speech capabilities for interactive user communication.

___
![ambrose](https://github.com/HermiTech-LLC/Ambrose-VI/blob/main/IMG_9806.jpeg)
## Features
- **Wake Word Detection:** Listens for specific wake words ("hey Ambrose", "Ambrose") to activate the assistant.
- **Voice Input:** Processes voice input from the user after the wake word is detected.
- **API Integration:** Queries the Wolfram Alpha API for structured information and Dialogflow for natural language understanding.
- **Text-to-Speech:** Converts API responses to speech, facilitating interactive communication.
- **Language Support:** Supports multiple languages including English, Spanish, German, and French.
___

## Installation
1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/HermiTech-LLC/Ambrose-VI.git
    ```

2. Navigate to the project directory and run the setup script:
    ```bash
    ./setup.sh
    ```

3. Obtain a Wolfram Alpha API key and a Dialogflow project ID and session ID, then update the `config.ini` file with these details.

## Usage
1. Run the assistant using the command line interface:
    ```bash
    python cli.py --lang <language_code>
    ```
    Replace `<language_code>` with the desired language code (e.g., "en" for English).

2. Say one of the wake words ("hey Ambrose", "Ambrose") to activate the assistant.

3. Speak your query after the wake word.

4. The assistant will process your query through Wolfram Alpha or Dialogflow and provide a response.

5. To exit the program, say the exit phrase ("thank you Ambrose").

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
- `pydub`: Library for audio playback.
- `google-cloud-dialogflow`: Library for accessing Dialogflow services.

## License
This project is licensed under the [MIT License](LICENSE).