import math
import os
import time
from obj import OBJ

global sz
global pixels, emptyScreenPixels
global xOffset, yOffset



def importObj(file: str) -> list:
    #obj is a list of lists, with the first list containing the points, and the second list containing the lines
    obj = [[], []]
    with open(file, "r") as f:
        text = f.readlines()
    cleanText = []
    ind = 0
    for val in text:
        if val == "\n":
            ind = 1    
        val = val.split()
        for i in range(len(val)):
            if ind == 0:
                val[i] = float(val[i].strip("(,)"))
            else:
                val[i] = int(val[i].strip("(,)"))
        val = tuple(val)
        obj[ind].append(val)
    obj[1].pop(0)
    return obj



def rotateXZ(points: list, angle: float) -> list:
    rotatedPoints = []
    c = math.cos(angle)
    s = math.sin(angle)
    for p in points:
        x = p[0] * c - p[2] * s
        y = p[1]
        z = p[0] * s + p[2] * c
        rotatedPoints.append((x, y, z))
    return rotatedPoints

def makePixelBuffer(windowW, windowH):
    pixels = []
    emptyScreenPixels = []
    for i in range(windowH):
        pixels.append([])
        emptyScreenPixels.append([])
        for l in range(windowW):
            pixels[i].append(emptyPixel)
            emptyScreenPixels[i].append(emptyPixel)
    return pixels, emptyScreenPixels


def draw():
    pixelBuffer = ""
    for y in range(len(pixels)):
        for x in range(len(pixels[y])):
            pixelBuffer += pixels[y][x]
        pixelBuffer += "\n"
    os.system("cls")
    print(pixelBuffer)

def plotLineLow(x0, y0, x1, y1) -> list:
    points = []
    #
    #using bresenham line algorithm
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = (2 * dy) - dx
    y = y0

    for x in range(x0, x1):
        points.append((x/sz, y/sz))
        #pixels[int(y + yOffset)][int(x + xOffset)] = dot
        #f.write(f"x: {x} y: {y}\n")
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2*dy
    return points

def plotLineHigh(x0, y0, x1, y1):
    points = []
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = (2 * dx) - dy
    x = x0
    for y in range(y0, y1):
        points.append((x/sz, y/sz))
        #pixels[int(y+yOffset)][int(x+xOffset)] = dot
        #f.write(f"x: {x} y: {y}\n")
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2*dx
    return points

def drawLine(p1, p2, drawFace=False):
    x0, y0 = int(p1[0] * sz), int(p1[1] * sz)
    x1, y1 = int(p2[0] * sz), int(p2[1] * sz)
    #input(((x0, y0), (x1, y1)))
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            points = plotLineLow(x1, y1, x0, y0)
        else:
            points = plotLineLow(x0, y0, x1, y1)
    else:
        if y0 > y1:
            points = plotLineHigh(x1, y1, x0, y0)
        else:
            points = plotLineHigh(x0, y0, x1, y1)
    if drawFace == False:
        for point in points:
            pixels[int((point[1]*sz)+yOffset)][int((point[0]*sz)+xOffset)] = dot
    else:
        return points

def drawTriangle(points):
    p1, p2, p3 = points[0], points[1], points[2]
    points = drawLine(p1, p2, drawFace=True)
    input(points)
    for point in points:
        x = point[0]
        y = point[1]
        drawLine(p3, (x, y))


def project(points: list) -> list:
    translatedPoints = []
    for p in points:
        x = p[0] / (p[2])
        y = p[1] / (p[2])
        z = p[2]
        translatedPoints.append((x, y, z))
    return translatedPoints

def translateZ(points: list, dz) -> list:
    translatedPoints = []
    for p in points:
        translatedPoints.append((p[0], p[1], p[2] + dz))
    return translatedPoints



windowW = 256
windowH = 256
xOffset = int(windowW / 2 - 1)
yOffset = int(windowH / 2 -1)
sz = int((windowW + windowH) / 8)
emptyPixel = "  "
dot = "##"
pixels, emptyScreenPixels = makePixelBuffer(windowW, windowH)
obj = OBJ("square.obj")
angle = 0
dz = 4
FPS = 60
while True:
    cos = math.cos(angle)
    sin = math.sin(angle)
    points = obj.points
    
    points = rotateXZ(points, angle)
    points = translateZ(points, dz)
    points = project(points)
    for i in range(len(obj.lines)):
        drawLine(points[obj.lines[i][0]], points[obj.lines[i][1]])
    for face in obj.faces:
        drawTriangle((obj.points[face[0]], obj.points[face[1]], obj.points[face[2]]))
    """
    translatedPoints = translate(cube[0], dz)
    rotatedPoints = rotateXZ(translatedPoints, angle)
    
    for i in range(len(cube[1])):
        drawLine(rotatedPoints[cube[1][i][0]], rotatedPoints[cube[1][i][1]])
    """
    
    draw()
    for i in range(len(pixels)):
        pixels[i] = [emptyScreenPixels[i][x] for x in range(len(emptyScreenPixels[i]))]

    
    angle += 2 / FPS

    time.sleep(1 / FPS)
