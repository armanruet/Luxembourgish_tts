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

# Create a sidebar for HF API token (required)
with st.sidebar:
    st.subheader("API Authentication")
    st.warning("⚠️ This model requires authentication to use")

    st.markdown("""
    ### How to get a Hugging Face token:
    1. Create a free account at [huggingface.co](https://huggingface.co/join)
    2. Go to your [settings page](https://huggingface.co/settings/tokens)
    3. Create a new token (read access is sufficient)
    4. Copy and paste the token here
    """)

    hf_token = st.text_input(
        "Hugging Face API Token (required)", type="password")

    st.divider()
    st.markdown("### About")
    st.markdown(
        "This app uses a VITS model fine-tuned for Luxembourgish language.")
    st.markdown(
        f"Model: [mbarnig/lb-de-fr-en-pt-coqui-vits-tts](https://huggingface.co/{HF_MODEL_ID})")

# Function to generate speech using the Hugging Face Inference API


def generate_speech(text, speaker, language, api_token):
    if not api_token:
        raise ValueError(
            "A Hugging Face API token is required to use this model.")

    API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
    headers = {"Authorization": f"Bearer {api_token}"}

    # For custom TTS models, we need to provide the text, speaker, and language
    payload = {
        "inputs": text,
        "parameters": {
            "speaker": speaker,
            "language": language
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 401:
        raise ValueError(
            "Invalid Hugging Face API token. Please check your token and try again.")
    elif response.status_code == 404:
        raise ValueError(
            f"Model '{HF_MODEL_ID}' not found. It may have been renamed or removed.")
    elif response.status_code != 200:
        raise Exception(
            f"API request failed with status code {response.status_code}: {response.text}")

    return response.content


# Warning if no token is provided
if not hf_token:
    st.warning(
        "⚠️ Please enter your Hugging Face API token in the sidebar to use this app.")

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
    submit_button = st.form_submit_button(
        "Convert to Speech", type="primary", disabled=not hf_token)

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
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        st.info(
            "Please check your Hugging Face API token and ensure you have access to this model.")

# Examples section
if hf_token:
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

# Footer
st.divider()
st.caption(
    "Powered by VITS model fine-tuned for Luxembourgish language. Model by mbarnig.")
