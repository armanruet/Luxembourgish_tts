# Luxembourgish Text-to-Speech (TTS)

A web interface for Luxembourgish text-to-speech synthesis using a VITS model.

## Features

- Support for multiple languages: Luxembourgish, German, French, English, and Portuguese
- Multiple speaker voices
- Simple web interface built with Gradio

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

3. Download the model files:
```bash
python download_model.py
```

## Usage

Run the web interface:

```bash
python check.py
```

The web interface will be available at http://127.0.0.1:7860

## Deployment

This app can be deployed on:

- [Hugging Face Spaces](https://huggingface.co/spaces) (recommended)
- [Streamlit](https://streamlit.io/)
- Any server with Python support

## Model Information

This project uses a VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech) model fine-tuned for Luxembourgish language.

## License

[Specify the license here] 