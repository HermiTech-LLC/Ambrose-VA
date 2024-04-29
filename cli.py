import argparse
import logging
from assistant import main as assistant_main, DEFAULT_LANGUAGE

def main():
    parser = argparse.ArgumentParser(description="Voice-activated Personal Assistant")
    parser.add_argument('--lang', type=str, default=DEFAULT_LANGUAGE, help="Specify the language for the assistant")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    
    assistant_main(args.lang)

if __name__ == "__main__":
    main()