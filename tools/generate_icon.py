from PIL import Image

source = "assets/branding/rme_icon_1024.png"
destination = "assets/branding/rme.ico"

img = Image.open(source)

sizes = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]

img.save(destination, format="ICO", sizes=sizes)

print(f"Icon generated: {destination}")