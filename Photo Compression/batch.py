from pathlib import Path
import os
from compress import compressImage
from PIL import Image
import time

def findPath(dir: list, name: str):
    for i in range(len(dir)):
        if name in str(dir[i]):
            return i
    else:
        return None

def getOrgFileName(filePath: Path) -> str:
    return str(filePath).split("\\")[-1]

def main():
    start = time.time()
    curDirPath = os.getcwd()
    curDirCont = Path(curDirPath)
    curDirCont = [x for x in curDirCont.iterdir()]
    imagesDirInd = findPath(curDirCont, "images")
    imagesDirPath = curDirCont[imagesDirInd]
    images = [x for x in imagesDirPath.iterdir()]

    newImgPath = Path(str(curDirPath) + "\\New Images")
    f = open("log.txt", "w")
    try:
        Path.mkdir(newImgPath)
    except FileExistsError:
        pass
    except Exception as error:
        print(f"error: {error}")
    for imgPath in images:
        orgImage = Image.open(imgPath)
        compRateWidth = 8
        compRateHeight = 8
        newImg = compressImage(orgImage, compRateWidth, compRateHeight)
        newPath = Path(str(newImgPath) + "\\" + getOrgFileName(imgPath))
        newImg.save(newPath)
        logtxt = f"""original path:{imgPath}
new image path:{newPath}
original image size: {orgImage.width} x {orgImage.height}
new image size: {newImg.width} x {newImg.height}
compression rate: 
    width: {compRateWidth}
    height: {compRateHeight}

"""
        f.write(logtxt)
    end = time.time()
    completionTime = end - start
    f.write(f"time to complete {len(images)} photos: {round(completionTime, 3)} seconds")
    f.close()

def UI():
    splashText = """Photo compression script written by QCGrub
"""
    print(splashText)
    print('to begin, please provide the path for your folder of images, or type "default" to use a folder called "images" to the side of this script')
    imagesPath = input()
    try:
        imagesPath = Path(imagesPath)
        images = [x for x in imagesPath.iterdir()]
        splitPath = str(imagesPath).split("\\")
        pathstr = ""
        for i in range(len(splitPath) -1):
            pathstr += splitPath[i] + "\\"
        curDirPath = pathstr[:-1]
        print(curDirPath)
    except Exception as e:
        print(e)
        curDirPath = os.getcwd()
        curDirCont = Path(curDirPath)
        curDirCont = [x for x in curDirCont.iterdir()]
        imagesDirInd = findPath(curDirCont, "images")
        imagesDirPath = curDirCont[imagesDirInd]
        images = [x for x in imagesDirPath.iterdir()]
    getCompRatio = False
    while getCompRatio == False:
        x = input("input horizontal compression rate(ex: 2): ")
        y = input("input vertical compression rate(ex: 4): ")
        try:
            x, y = int(x), int(y)
            break
        except:
            print("invalid input")
    getCompRatio = True
    compRateWidth, compRateHeight = x, y
    newImgPath = Path(str(curDirPath) + "\\New Images")
    print(newImgPath)
    try:
        Path.mkdir(newImgPath)
    except FileExistsError:
        pass
    except Exception as error:
        print(f"error: {error}")

    logPath = Path(str(newImgPath) + "\\log.txt")
    try:
        f = open(str(logPath), "w")
    except FileNotFoundError:
        f = open(str(logPath), "x")
    
    start = time.time()
    for imgPath in images:
        orgImage = Image.open(imgPath)
        newImg = compressImage(orgImage, compRateWidth, compRateHeight)
        newPath = Path(str(newImgPath) + "\\" + getOrgFileName(imgPath))
        newImg.save(newPath)
        logtxt = f"""original path:{imgPath}
new image path: {newPath}
original image size: {orgImage.width} x {orgImage.height}
new image size: {newImg.width} x {newImg.height}
compression rate: 
    width: {compRateWidth}
    height: {compRateHeight}

"""

        f.write(logtxt)
    end = time.time()
    completionTime = end - start
    f.write(f"time to complete {len(images)} photos: {round(completionTime, 3)} seconds")
    f.close()

UI()
