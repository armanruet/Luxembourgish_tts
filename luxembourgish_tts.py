import argparse
from TTS.utils.synthesizer import Synthesizer
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Generate speech with Luxembourgish TTS model")
    parser.add_argument("--text", type=str, required=True, help="Text to convert to speech")
    parser.add_argument("--language", type=str, default="x-lb", 
                        choices=["x-lb", "x-de", "fr-fr", "en", "pt-br"], 
                        help="Language code (x-lb: Luxembourgish, x-de: German, fr-fr: French, en: English, pt-br: Portuguese)")
    parser.add_argument("--speaker", type=str, default="Judith", 
                        choices=["Bernard", "Bunny", "Ed", "Guy", "Judith", "Kerstin", "Linda", "Thorsten"],
                        help="Speaker voice to use")
    parser.add_argument("--output", type=str, default="output.wav", help="Output file path")
    
    args = parser.parse_args()
    
    # Path to model files
    model_path = os.path.expanduser("~/.local/share/tts/custom_models/luxembourgish")
    model_file = os.path.join(model_path, "best_model.pth")
    config_file = os.path.join(model_path, "config.json")
    
    # Check if files exist
    if not os.path.isfile(model_file):
        print(f"Error: Model file not found at {model_file}")
        sys.exit(1)
    if not os.path.isfile(config_file):
        print(f"Error: Config file not found at {config_file}")
        sys.exit(1)
    
    try:
        # Create synthesizer - simplified initialization
        synthesizer = Synthesizer(
            model_file,
            config_file,
            use_cuda=False  # Set to True if you have a GPU
        )
        
        # Create wav file - passing speaker and language here
        print(f"Generating speech using language '{args.language}' and speaker '{args.speaker}'...")
        wav = synthesizer.tts(
            args.text,
            speaker_name=args.speaker,  # Pass speaker here
            language_name=args.language  # Pass language here
        )
        
        # Save to file
        synthesizer.save_wav(wav, args.output)
        print(f"Speech saved to {args.output}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("If you're seeing errors about missing files or parameters, please ensure you've downloaded")
        print("all the necessary model files, including language_ids.json and speakers.pth")
        sys.exit(1)

if __name__ == "__main__":
    main()
