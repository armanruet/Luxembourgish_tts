import os
import tempfile
import streamlit as st
from TTS.utils.synthesizer import Synthesizer
from huggingface_hub import hf_hub_download
import base64

# Set page configuration
st.set_page_config(
    page_title="Luxembourgish Text-to-Speech",
    page_icon="🎙️",
    layout="wide"
)

# App title and description
st.title("Luxembourgish Text-to-Speech Converter")
st.markdown(
    "Enter text in Luxembourgish (or other supported languages) to convert to speech.")

# Define the repository ID
REPO_ID = "mbarnig/lb-de-fr-en-pt-coqui-vits-tts"

# Define function to ensure model files are downloaded


@st.cache_resource
def load_synthesizer():
    st.info("Initializing TTS model... This may take a minute on first run.")

    # Create a models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Define the files to download
    files = [
        "best_model.pth",
        "config.json",
        "speakers.pth",
        "language_ids.json",
        "model_se.pth",
        "config_se.json"
    ]

    # Download each file if it doesn't exist
    for file in files:
        file_path = os.path.join("models", file)
        if not os.path.exists(file_path):
            with st.status(f"Downloading {file}..."):
                hf_hub_download(
                    repo_id=REPO_ID,
                    filename=file,
                    local_dir="models"
                )

    # Initialize the synthesizer
    synthesizer = Synthesizer(
        os.path.join("models", "best_model.pth"),
        os.path.join("models", "config.json"),
        use_cuda=False  # Set to True if you have a GPU
    )

    return synthesizer


# Available speakers and languages
SPEAKERS = ["Bernard", "Bunny", "Ed", "Guy",
            "Judith", "Kerstin", "Linda", "Thorsten"]
LANGUAGES = {
    "Luxembourgish": "x-lb",
    "German": "x-de",
    "French": "fr-fr",
    "English": "en",
    "Portuguese": "pt-br"
}

# Load the synthesizer
synthesizer = load_synthesizer()

# Create the input form
with st.form("tts_form"):
    # Text input
    text_input = st.text_area(
        "Text to Convert",
        placeholder="Enter text here... e.g., Moien, wéi geet et dir?",
        height=150
    )

    # Two-column layout for options
    col1, col2 = st.columns(2)

    with col1:
        speaker = st.selectbox("Speaker Voice", SPEAKERS,
                               index=SPEAKERS.index("Judith"))

    with col2:
        language = st.selectbox("Language", list(LANGUAGES.keys()), index=0)

    # Submit button
    submit_button = st.form_submit_button("Convert to Speech", type="primary")

# Handle form submission
if submit_button and text_input:
    try:
        with st.spinner("Generating speech..."):
            # Get the language code from the language name
            language_code = LANGUAGES[language]

            # Generate speech
            wav = synthesizer.tts(
                text_input,
                speaker_name=speaker,
                language_name=language_code
            )

            # Create a temporary file to save the audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
                temp_filename = fp.name
                synthesizer.save_wav(wav, temp_filename)

            # Display audio
            st.audio(temp_filename)

            # Provide download button
            with open(temp_filename, "rb") as file:
                btn = st.download_button(
                    label="Download audio",
                    data=file,
                    file_name=f"tts_output_{speaker}_{language}.wav",
                    mime="audio/wav"
                )

            st.success(
                f"Speech generated successfully with {speaker}'s voice in {language}.")
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")

# Examples section
st.divider()
st.subheader("Examples")

examples = [
    ("Moien, wéi geet et dir?", "Judith", "Luxembourgish"),
    ("Guten Tag, wie geht es Ihnen?", "Thorsten", "German"),
    ("Bonjour, comment ça va?", "Kerstin", "French"),
    ("Hello, how are you today?", "Guy", "English"),
    ("Olá, como vai você?", "Linda", "Portuguese")
]

for i, (example_text, example_speaker, example_language) in enumerate(examples):
    with st.expander(f"Example {i+1}: {example_language}"):
        st.write(f"**Text:** {example_text}")
        st.write(f"**Speaker:** {example_speaker}")
        st.write(f"**Language:** {example_language}")

        if st.button(f"Try this example", key=f"example_{i}"):
            try:
                with st.spinner("Generating speech from example..."):
                    language_code = LANGUAGES[example_language]
                    wav = synthesizer.tts(
                        example_text,
                        speaker_name=example_speaker,
                        language_name=language_code
                    )

                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
                        temp_filename = fp.name
                        synthesizer.save_wav(wav, temp_filename)

                    st.audio(temp_filename)
            except Exception as e:
                st.error(f"Error generating speech: {str(e)}")

# Footer
st.divider()
st.caption(
    "Powered by VITS model fine-tuned for Luxembourgish language. Model by mbarnig.")
