import os
import tempfile
import gradio as gr
from TTS.utils.synthesizer import Synthesizer

# Path to model files
MODEL_PATH = os.path.expanduser("~/.local/share/tts/custom_models/luxembourgish")
MODEL_FILE = os.path.join(MODEL_PATH, "best_model.pth")
CONFIG_FILE = os.path.join(MODEL_PATH, "config.json")

# Check if model files exist
if not os.path.isfile(MODEL_FILE):
    raise FileNotFoundError(f"Model file not found at {MODEL_FILE}")
if not os.path.isfile(CONFIG_FILE):
    raise FileNotFoundError(f"Config file not found at {CONFIG_FILE}")

# Initialize the synthesizer (only once at startup)
print("Initializing TTS model...")
synthesizer = Synthesizer(
    MODEL_FILE,
    CONFIG_FILE,
    use_cuda=False  # Set to True if you have a GPU
)

# Available speakers and languages
SPEAKERS = ["Bernard", "Bunny", "Ed", "Guy", "Judith", "Kerstin", "Linda", "Thorsten"]
LANGUAGES = {
    "Luxembourgish": "x-lb",
    "German": "x-de",
    "French": "fr-fr",
    "English": "en",
    "Portuguese": "pt-br"
}

def text_to_speech(text, speaker, language):
    """Convert text to speech using the TTS model"""
    if not text:
        return None, "Please enter some text to convert to speech."
    
    try:
        # Get the language code from the language name
        language_code = LANGUAGES[language]
        
        # Generate speech
        print(f"Generating speech for: {text}")
        wav = synthesizer.tts(
            text,
            speaker_name=speaker,
            language_name=language_code
        )
        
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            temp_filename = fp.name
            synthesizer.save_wav(wav, temp_filename)
        
        return temp_filename, f"Speech generated successfully with {speaker}'s voice in {language}."
    except Exception as e:
        print(f"Error generating speech: {str(e)}")
        return None, f"Error generating speech: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Luxembourgish Text-to-Speech") as demo:
    gr.Markdown("# Luxembourgish Text-to-Speech Converter")
    gr.Markdown("Enter text in Luxembourgish (or other supported languages) to convert to speech.")
    
    with gr.Row():
        with gr.Column():
            # Input components
            text_input = gr.Textbox(
                label="Text to Convert", 
                placeholder="Enter text here... e.g., Moien, wéi geet et dir?",
                lines=5
            )
            
            with gr.Row():
                speaker_dropdown = gr.Dropdown(
                    choices=SPEAKERS, 
                    value="Judith", 
                    label="Speaker Voice"
                )
                language_dropdown = gr.Dropdown(
                    choices=list(LANGUAGES.keys()), 
                    value="Luxembourgish", 
                    label="Language"
                )
            
            convert_btn = gr.Button("Convert to Speech", variant="primary")
        
        with gr.Column():
            # Output components
            audio_output = gr.Audio(label="Generated Speech")
            message_output = gr.Textbox(label="Status")
    
    # Set up the click event
    convert_btn.click(
        fn=text_to_speech,
        inputs=[text_input, speaker_dropdown, language_dropdown],
        outputs=[audio_output, message_output]
    )
    
    # Example inputs
    gr.Examples(
        [
            ["Moien, wéi geet et dir?", "Judith", "Luxembourgish"],
            ["Guten Tag, wie geht es Ihnen?", "Thorsten", "German"],
            ["Bonjour, comment ça va?", "Kerstin", "French"],
            ["Hello, how are you today?", "Guy", "English"],
            ["Olá, como vai você?", "Linda", "Portuguese"]
        ],
        inputs=[text_input, speaker_dropdown, language_dropdown]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)  # Set share=False if you don't want a public link
    print("Gradio app launched!")