import os
import tempfile
import streamlit as st
import requests
import io
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

# Define the Hugging Face model ID
HF_MODEL_ID = "mbarnig/lb-de-fr-en-pt-coqui-vits-tts"

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

# Create a sidebar for HF API token (optional)
with st.sidebar:
    st.subheader("Configuration")
    hf_token = st.text_input("Hugging Face API Token (optional)", type="password",
                             help="Enter your Hugging Face API token to increase rate limits")
    st.write(
        "If you don't have a token, the app will still work with limited requests.")
    st.divider()
    st.markdown("### About")
    st.markdown(
        "This app uses a VITS model fine-tuned for Luxembourgish language.")
    st.markdown(
        f"Model: [mbarnig/lb-de-fr-en-pt-coqui-vits-tts](https://huggingface.co/{HF_MODEL_ID})")

# Function to generate speech using the Hugging Face Inference API


def generate_speech(text, speaker, language, api_token=None):
    API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
    headers = {}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    # For custom TTS models, we need to provide the text, speaker, and language
    payload = {
        "inputs": text,
        "parameters": {
            "speaker": speaker,
            "language": language
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(
            f"API request failed with status code {response.status_code}: {response.text}")

    return response.content


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
            audio_bytes = generate_speech(
                text_input, speaker, language_code, hf_token)

            # Save to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
                temp_filename = fp.name
                fp.write(audio_bytes)

            # Display audio
            st.audio(temp_filename)

            # Provide download button
            st.download_button(
                label="Download audio",
                data=audio_bytes,
                file_name=f"tts_output_{speaker}_{language}.wav",
                mime="audio/wav"
            )

            st.success(
                f"Speech generated successfully with {speaker}'s voice in {language}.")
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        st.info(
            "If you're seeing rate limit errors, try adding your Hugging Face API token in the sidebar.")

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
                    audio_bytes = generate_speech(
                        example_text, example_speaker, language_code, hf_token)

                    # Save to a temporary file
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
                        temp_filename = fp.name
                        fp.write(audio_bytes)

                    st.audio(temp_filename)
            except Exception as e:
                st.error(f"Error generating speech: {str(e)}")
                st.info(
                    "If you're seeing rate limit errors, try adding your Hugging Face API token in the sidebar.")

# Footer
st.divider()
st.caption(
    "Powered by VITS model fine-tuned for Luxembourgish language. Model by mbarnig.")
