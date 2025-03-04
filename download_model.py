from huggingface_hub import hf_hub_download
import os

# Define the repository ID
REPO_ID = "mbarnig/lb-de-fr-en-pt-coqui-vits-tts"

# Define the files to download
files = [
    "best_model.pth",
    "config.json",
    "speakers.pth",
    "language_ids.json",
    "model_se.pth",
    "config_se.json"
]

# Download each file
for file in files:
    print(f"Downloading {file}...")
    hf_hub_download(
        repo_id=REPO_ID,
        filename=file,
        local_dir="."
    )
    
print("All files downloaded successfully!")
