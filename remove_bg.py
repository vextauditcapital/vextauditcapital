import subprocess
import sys
import os

def install(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import rembg
except ImportError:
    install("rembg")
    import rembg

from PIL import Image
import io

input_path = "VEXT-AUDIT-CAPITAL-LOGO.jpg"
output_path = "VEXT-AUDIT-CAPITAL-LOGO-TRANSPARENT.png"

print(f"Removing background from {input_path}...")
with open(input_path, 'rb') as i:
    input_data = i.read()
    output_data = rembg.remove(input_data)

with open(output_path, 'wb') as o:
    o.write(output_data)

print(f"Saved transparent logo to {output_path}")
