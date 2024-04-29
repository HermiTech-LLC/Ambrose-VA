import os
import asyncio
import logging
from configparser import ConfigParser
import requests
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load configuration settings
config = ConfigParser()
config.read('config.ini')
API_KEY = config.get('wolfram', 'API_KEY')
API_URL = "http://api.wolframalpha.com/v2/query"
SUPPORTED_LANGUAGES = {'en': 'English', 'es': 'Spanish', 'de': 'German', 'fr': 'French'}
DEFAULT_LANGUAGE = 'en'
WAKE_WORDS = ['hey Ambrose', 'Ambrose']
EXIT_PHRASE = 'thank you Ambrose'

def query_wolfram_alpha(input_query, lang=DEFAULT_LANGUAGE):
    """Query Wolfram Alpha API and return the result."""
    params = {
        'input': input_query,
        'appid': API_KEY,
        'output': 'JSON',
        'format': 'plaintext',
        'language': lang
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get('queryresult', {}).get('success', False):
            pods = response_data['queryresult']['pods']
            answer = pods[0]['subpods'][0]['plaintext']
            return answer or "Information found, but no readable result available."
        return "Query not understood or no data available."
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return "Failed to fetch response from API."

def asynchronous_speak(text, lang=DEFAULT_LANGUAGE):
    """Convert text to speech and play it asynchronously."""
    def _play_sound(audio_file):
        song = AudioSegment.from_file(audio_file)
        play(song)
        os.remove(audio_file)

    try:
        tts = gTTS(text=text, lang=lang)
        file_path = 'response.mp3'
        tts.save(file_path)
        Thread(target=_play_sound, args=(file_path,)).start()
    except Exception as e:
        logging.error(f"Failed to speak or play sound: {e}")

def listen_for_wake_word(recognizer, source, lang=DEFAULT_LANGUAGE):
    """Listen continuously for a wake word before activating command listening."""
    logging.info("Listening for wake word...")
    audio = recognizer.listen(source)
    try:
        recognized_text = recognizer.recognize_google(audio, language=lang).lower()
        for wake_word in WAKE_WORDS:
            if wake_word in recognized_text:
                logging.info(f"Wake word '{wake_word}' detected.")
                return True
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        logging.error("Speech recognition service unavailable.")
    return False

def listen(recognizer, source, lang=DEFAULT_LANGUAGE):
    """Listen for voice input after wake word and return the recognized text."""
    logging.info("Listening for command...")
    audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        return "Speech not recognized."
    except sr.RequestError:
        return "Speech recognition service unavailable."

async def main_loop():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            if listen_for_wake_word(recognizer, source):
                query = listen(recognizer, source)
                if EXIT_PHRASE in query.lower():
                    asynchronous_speak("Goodbye!", DEFAULT_LANGUAGE)
                    logging.info("Goodbye!")
                    break

                if query:
                    logging.info(f"Received: {query}")
                    result = query_wolfram_alpha(query)
                    logging.info(f"Answer: {result}")
                    asynchronous_speak(result)

def main():
    asyncio.run(main_loop())

if __name__ == "__main__":
    main()
