import os
import asyncio
import logging
import requests
import time
import functools
from configparser import ConfigParser
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
from google.cloud import dialogflow
import openai
from dotenv import load_dotenv
from nlp_engine import NlpEngine
from database_manager import DatabaseManager
import wx

# Initialize and load configuration
logging.basicConfig(level=logging.INFO)
config = ConfigParser()
config.read('config.ini')
API_KEY = config.get('wolfram', 'API_KEY')
API_URL = "http://api.wolframalpha.com/v2/query"
DIALOGFLOW_PROJECT_ID = config.get('Dialogflow', 'project_id')
DIALOGFLOW_SESSION_ID = config.get('Dialogflow', 'session_id')
DIALOGFLOW_LANGUAGE_CODE = config.get('Dialogflow', 'language_code', fallback='en')
SUPPORTED_LANGUAGES = {'en': 'English', 'es': 'Spanish', 'de': 'German', 'fr': 'French'}
DEFAULT_LANGUAGE = 'en'
WAKE_WORDS = ['hey Ambrose', 'Ambrose']
EXIT_PHRASE = 'thank you Ambrose'

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def safe_api_call(func):
    """Decorator to handle exceptions for any API call."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None
    return wrapper

class LearningAssistant:
    def __init__(self):
        self.db_manager = DatabaseManager('assistant_memory.db')
        self.nlp_engine = NlpEngine('en_core_web_trf')
        self.recognizer = sr.Recognizer()

    @safe_api_call
    def query_wolfram_alpha(self, input_query, lang=DEFAULT_LANGUAGE):
        """Query Wolfram Alpha API and return the result."""
        params = {
            'input': input_query,
            'appid': API_KEY,
            'output': 'JSON',
            'format': 'plaintext',
            'language': lang
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get('queryresult', {}).get('success', False):
            pods = response_data['queryresult']['pods']
            answer = pods[0]['subpods'][0]['plaintext']
            return answer or "Information found, but no readable result available."
        return "Query not understood or no data available."

    def detect_intent_dialogflow(self, query, session_id, language_code):
        """Send query to Dialogflow and get the response."""
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
        text_input = dialogflow.TextInput(text=query, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        return response.query_result.fulfillment_text

    def asynchronous_speak(self, text, lang=DEFAULT_LANGUAGE):
        """Convert text to speech and play it asynchronously."""
        def _play_sound(audio_file):
            song = AudioSegment.from_file(audio_file)
            play(song)
            os.remove(audio_file)

        tts = gTTS(text=text, lang=lang)
        file_path = 'response.mp3'
        tts.save(file_path)
        Thread(target=_play_sound, args=(file_path,)).start()

    def listen_for_wake_word(self, source, lang=DEFAULT_LANGUAGE):
        """Listen continuously for a wake word before activating command listening."""
        logging.info("Listening for wake word...")
        audio = self.recognizer.listen(source)
        recognized_text = self.recognizer.recognize_google(audio, language=lang).lower()
        for wake_word in WAKE_WORDS:
            if wake_word in recognized_text:
                logging.info(f"Wake word '{wake_word}' detected.")
                return True
        return False

    def listen(self, source, lang=DEFAULT_LANGUAGE):
        """Listen for voice input after wake word and return the recognized text."""
        logging.info("Listening for command...")
        audio = self.recognizer.listen(source)
        return self.recognizer.recognize_google(audio, language=lang)

    async def main_loop(self, frame):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                if self.listen_for_wake_word(source):
                    query = self.listen(source)
                    if EXIT_PHRASE in query.lower():
                        self.asynchronous_speak("Goodbye!", DEFAULT_LANGUAGE)
                        logging.info("Goodbye!")
                        break

                    if query:
                        logging.info(f"Received: {query}")
                        result = self.query_wolfram_alpha(query)
                        if 'no readable result' in result:
                            result = self.detect_intent_dialogflow(query, DIALOGFLOW_SESSION_ID, DIALOGFLOW_LANGUAGE_CODE)
                        logging.info(f"Answer: {result}")
                        self.asynchronous_speak(result)

class ChatFrame(wx.Frame):
    def __init__(self, parent, title):
        super(ChatFrame, self).__init__(parent, title=title, size=(700, 500))
        self.assistant = LearningAssistant()
        self.panel = wx.Panel(self)
        self.setup_ui()

    def setup_ui(self):
        self.output = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.listen_button = wx.Button(self.panel, label="Listen")
        self.listen_button.Bind(wx.EVT_BUTTON, self.on_listen_pressed)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.output, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.listen_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        self.panel.SetSizer(sizer)
        self.Show()

    async def on_listen_pressed(self, event):
        await self.assistant.main_loop(self)

def main():
    app = wx.App(False)
    frame = ChatFrame(None, "LearningAssistant")
    asyncio.run(app.MainLoop())

if __name__ == "__main__":
    main()