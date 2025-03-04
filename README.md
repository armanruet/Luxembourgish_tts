# Luxembourgish Text-to-Speech (TTS)

A web interface for Luxembourgish text-to-speech synthesis using a VITS model.

## Features

- Support for multiple languages: Luxembourgish, German, French, English, and Portuguese
- Multiple speaker voices
- Simple web interface built with Streamlit
- Automatic model loading from Hugging Face Hub

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

1. Clone this repository:
```bash
git clone https://github.com/armanruet/Luxembourgish_tts.git
cd Luxembourgish_tts
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the web interface:

```bash
streamlit run app.py
```

The web interface will be available at http://localhost:8501

## Deployment

### Deploying to Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Select your repository
5. Choose the main branch and enter the path to your app file: `app.py`
6. Click "Deploy"

The app will automatically download all required model files from Hugging Face Hub on first launch. No need to upload large model files!

### Other Deployment Options

- [Hugging Face Spaces](https://huggingface.co/spaces) (also supports automatic model loading)
- Any cloud provider with Python support (AWS, GCP, Azure, etc.)

## Model Information

This project uses a VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech) model fine-tuned for Luxembourgish language. The model is hosted on Hugging Face Hub at [mbarnig/lb-de-fr-en-pt-coqui-vits-tts](https://huggingface.co/mbarnig/lb-de-fr-en-pt-coqui-vits-tts).

## License

[Specify the license here] 