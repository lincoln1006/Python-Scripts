from pathlib import Path
import os
from compress import compressImage
from PIL import Image
import time
from math import sqrt

img = Image.new("RGB", (16, 16))
widthOffset = 0
heightOffset = 0
imgSizeAvg = int((img.width + img.height) // 2)
sizeSqrt = int(sqrt(imgSizeAvg)) * 2
colorMult = 255 // sizeSqrt
bRatio =(sizeSqrt // 4) ** 2
for b in range(bRatio):
    for g in range(sizeSqrt):
        for r in range(sizeSqrt):
            color = (r * colorMult, g * colorMult, int(b * (255 / bRatio)))
            
            img.putpixel((r + widthOffset, g + heightOffset), color)

    if widthOffset >= (imgSizeAvg - sizeSqrt):
        widthOffset = 0
        heightOffset += sizeSqrt
    else:
        widthOffset += sizeSqrt
img.show()