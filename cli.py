import argparse
import logging
from assistant import LearningAssistant

def main():
    parser = argparse.ArgumentParser(description="Voice-activated Personal Assistant")
    parser.add_argument('--lang', type=str, default=LearningAssistant.DEFAULT_LANGUAGE, help="Specify the language for the assistant")
    args = parser.parse_args()

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO)
    
    # Create an instance of the assistant
    assistant = LearningAssistant()

    # Start the assistant main loop with the specified language
    assistant.main_loop(args.lang)  # Assuming main_loop is designed to accept language as a parameter

if __name__ == "__main__":
    main()