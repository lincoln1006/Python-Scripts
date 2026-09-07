from PIL import Image
from compress import compressImage

def transformBandW(img: Image) -> Image:
    imgPixels = img.load()
    for i in range(img.height):
        for l in range(img.width):
            colors = imgPixels[l, i]
            colorsAvg = (colors[0] + colors[1] + colors[2]) // 3
            img.putpixel((l, i), (colorsAvg, colorsAvg, colorsAvg))
    return img

def imgToAscii(img: Image) -> list:
    asciiScale = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
    txtPixels = []
    imgPixels = img.load()
    for i in range(img.height):
        txtPixels.append([])
        for l in range(img.width):
            colorAvg = (imgPixels[l, i][0] + imgPixels[l, i][1] + imgPixels[l, i][2]) // 3
            pixel = int(round((((255 - colorAvg) / 255) * len(asciiScale)) - 1, 0))
            txtPixels[i].append(asciiScale[pixel])
    return txtPixels

def saveAsciiImage(imgPixels: list):
    with open("asciiImage.txt", "w") as f:
        for i in range(len(imgPixels)):
            tempStr = str()
            for val in imgPixels[i]:
                tempStr += val
                tempStr += "  "
            print(tempStr)
            tempStr += "\n"
            f.write(tempStr)
            

img = Image.open("ar152.jpg")
if type(img.load()[0, 0]) != type(tuple()):
    newimg = Image.new("RGB", (img.width, img.height))
    imgPixels = img.load()
    for i in range(img.height):
        for l in range(img.width):
            newimg.putpixel((l, i), (imgPixels[l, i], imgPixels[l, i], imgPixels[l, i]))
    img = newimg
print(img.width, img.height)
img = compressImage(img, 4, 4)
img = transformBandW(img)
txtPixels = imgToAscii(img)
saveAsciiImage(txtPixels)
img.show()