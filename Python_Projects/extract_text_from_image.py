"""
specify: 
language
psm: page segmentation mode
oem: OCR engine mode

can save into a file
can definitely go throuhg multiple images
"""
import pytesseract
import PIL.Image
import cv2

# here is where we specify : numbers can be inputs
#can be "-l kor"#
myconfig = r"--psm 6 --oem 3"
text = pytesseract.image_to_string(PIL.Image.open("Screenshot 2023-04-05 020717.png"), config=myconfig)
print(text)