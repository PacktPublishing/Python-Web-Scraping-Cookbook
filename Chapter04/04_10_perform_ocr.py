import pytesseract as pt
from PIL import Image

img = Image.open("textinimage.png")
text = pt.image_to_string(img)
print(text)