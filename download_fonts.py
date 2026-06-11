import os
import requests

FONT_DIR = "agents/utils/fonts"
os.makedirs(FONT_DIR, exist_ok=True)

fonts_to_download = {
    "Cinzel-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    "CormorantGaramond-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond-Regular.ttf",
    "CormorantGaramond-Bold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond-Bold.ttf",
    "Jost-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/jost/Jost%5Bital%2Cwght%5D.ttf"
}

for filename, url in fonts_to_download.items():
    print(f"Downloading {filename}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        extracted_path = os.path.join(FONT_DIR, filename)
        with open(extracted_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully saved {filename}.")
    else:
        print(f"Failed to download {filename}: Status {response.status_code}")

print("Font download complete.")
