from PIL import Image

def averagePixels(pixels: list) -> tuple:
    R, G, B = 0, 0, 0
    for val in pixels:
        R += val[0]
        G += val[1]
        B += val[2]
    ln = len(pixels)
    return (R // ln, G // ln, B // ln)

def compressImage(img: Image, compRateWidth: int, compRateHeight: int) -> Image:
    imgpx = img.load()
    newImgWidth = img.width // compRateWidth
    newImgHeight = img.height // compRateHeight
    newImg = Image.new("RGB", (newImgWidth, newImgHeight))
    newImgW = 0
    newImgH = 0
    #f.write(str((newImgWidth, newImgHeight)))
    for x in range(0, img.width - compRateWidth+1, compRateWidth):
        for y in range(0, img.height - compRateHeight+1, compRateHeight):
            #f.write(str((x, y, newImgW, newImgH)) + "\n")
            compPixels = []
            for i in range(compRateWidth):
                for l in range(compRateHeight):
                    compPixels.append(imgpx[x+i, y+l])
            newPixel = averagePixels(compPixels)
            newImg.putpixel((newImgW, newImgH), newPixel)
            newImgH += 1
        newImgW += 1
        newImgH = 0
    return newImg
"""
img = Image.open("red.jpg")
imgcopy = img.copy()
#pixelclass = [width index, height index]
f = open("debug.txt", "w")
newImg = compressImage(imgcopy, 9, 9)
print(img.width * img.height)
print(newImg.width * newImg.height)
newImg.show()
        



exit()
with open("img.txt", "w") as f:
    for x in range(img.width):
        for y in range(img.height):
            f.write(str(imgpx[x, y]) + "\n")
        f.write("endline\n")
"""