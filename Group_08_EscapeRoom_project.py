from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Global variable declarations
background_color=0.0
gate_color=0.0

thiefX = -685
thiefY = -435
thiefRadius = 13
thiefSpeed = 10
W_Width, W_Height = 1500, 1000

gunX = 18
gunY = -5
gunAchieve = False
keyAchieve = False
keyX = 590
keyY = -430

gamePaused = False
gameOver = False
win = False

# firing part
firedBallCenX = thiefX
firedBallCenY = thiefY + thiefRadius
firedBallRadius = 6
firedBallSpeed = 10
fired = False
firedDirection = "r"
policeKillCount = 0
original_restart = False
hearts = 3
missed_firing=0

# teleportation part 
teleport = [
    {"x": -500, "y": -300, "positionX": 400, "positionY": 150, "color": (0.1, 0.2, 0.8)},
    {"x": 400, "y": 150, "positionX": -500, "positionY": -300, "color": (0.1, 0.2, 0.8)},
    {"x": -150, "y": 200, "positionX": 600, "positionY": -200, "color": (0.3, 0.6, 0.7)},
    {"x": 600, "y": -200, "positionX": -150, "positionY": 200, "color": (0.3, 0.6, 0.7)}
]
last_pad = None


policeArr = [
    {
        "x1": -600,
        "y1": -380,
        "r": 11,
        "viewRange": 50,
        "theta": 90,
        "baseTheta": 0,
        "thetaRotation": 0,
        "movementType": "t",
        "speed": 3,
        "boundaries": {"top": -320, "bottom": -380, "right": -510, "left": -600},
        "direction": "clockwise",
        "killed": False,
    },
    {
        "x1": 20,
        "y1": -370,
        "r": 11,
        "viewRange": 60,
        "theta": 0,
        "baseTheta": 270,
        "thetaRotation": 0,
        "movementType": "r",
        "speed": 5,
        "boundaries": {"top": -340, "bottom": -370, "right": 80, "left": 20},
        "direction": "antiClockwise",
        "killed": False,
    },
    {
        "x1": -350,
        "y1": -320,
        "r": 11,
        "viewRange": 70,
        "theta": 0,
        "baseTheta": 270,
        "thetaRotation": 0,
        "movementType": "r",
        "speed": 2,
        "boundaries": {"top": -140, "bottom": -320, "right": -180, "left": -350},
        "direction": "antiClockwise",
        "killed": False,
    },
    {
        "x1": -380,
        "y1": 170,
        "r": 11,
        "viewRange": 70,
        "theta": 90,
        "baseTheta": 0,
        "thetaRotation": 0,
        "movementType": "t",
        "speed": 3,
        "boundaries": {"top": 220, "bottom": 170, "right": -210, "left": -380},
        "direction": "clockwise",
        "killed": False,
    },
    {
        "x1": -60,
        "y1": 220,
        "r": 11,
        "viewRange": 70,
        "theta": 90,
        "baseTheta": 0,
        "thetaRotation": 0,
        "movementType": "t",
        "speed": 5,
        "boundaries": {"top": 350, "bottom": 220, "right": 100, "left": -60},
        "direction": "clockwise",
        "killed": False,
    },
    {
        "x1": 275,
        "y1": 200,
        "r": 11,
        "viewRange": 70,
        "theta": 0,
        "baseTheta": 270,
        "thetaRotation": 0,
        "movementType": "r",
        "speed": 5,
        "boundaries": {"top": 370, "bottom": 200, "right": 410, "left": 275},
        "direction": "antiClockwise",
        "killed": False,
    },
    {
        "x1": 630,
        "y1": -100,
        "r": 11,
        "viewRange": 50,
        "theta": 90,
        "baseTheta": 0,
        "thetaRotation": 0,
        "movementType": "t",
        "speed": 9,
        "boundaries": {"top": 70, "bottom": -100, "right": 630, "left": 550},
        "direction": "antiClockwise",
        "killed": False,
    },
    {
        "x1": 630,
        "y1": -280,
        "r": 11,
        "viewRange": 50,
        "theta": 0,
        "baseTheta": 270,
        "thetaRotation": 0,
        "movementType": "r",
        "speed": 9,
        "boundaries": {"top": -200, "bottom": -280, "right": 630, "left": 410},
        "direction": "antiClockwise",
        "killed": False,
    },
    {
        "x1": -60,
        "y1": -10,
        "r": 11,
        "viewRange": 70,
        "theta": 0,
        "baseTheta": 270,
        "thetaRotation": 0,
        "movementType": "r",
        "speed": 9,
        "boundaries": {"top": 120, "bottom": -10, "right": 200, "left": -60},
        "direction": "antiClockwise",
        "killed": False,
    },
    {
        "x1": 580,
        "y1": 320,
        "r": 11,
        "viewRange": 50,
        "theta": 0,
        "baseTheta": 270,
        "thetaRotation": 0,
        "movementType": "r",
        "speed": 9,
        "boundaries": {"top": 380, "bottom": 320, "right": 630, "left": 580},
        "direction": "antiClockwise",
        "killed": False,
    },
]


prisonsArr = [
    {"shape": "E1", "x1": -640, "y1": 100, "x2": -490, "y2": -20, "width": 25},
    {"shape": "E2", "x1": 220, "y1": -210, "x2": 330, "y2": -410, "width": 50},
    {"shape": "E3", "x1": -350, "y1": 400, "x2": -150, "y2": 280, "width": 25},
    {"shape": "L4", "x1": 50, "y1": 420, "x2": 200, "y2": 250, "width": 25},
    {"shape": "L1", "x1": 500, "y1": 350, "x2": 610, "y2": 200, "width": 40},
    {"shape": "L2", "x1": -650, "y1": 450, "x2": -520, "y2": 270, "width": 50},
    {"shape": "L2", "x1": -320, "y1": 100, "x2": -160, "y2": -50, "width": 50},
    {"shape": "L3", "x1": -280, "y1": -360, "x2": -80, "y2": -450, "width": 30},
    {"shape": "L3", "x1": 10, "y1": -80, "x2": 130, "y2": -250, "width": 30},
    {"shape": "L3", "x1": 510, "y1": -320, "x2": 630, "y2": -450, "width": 30},
    {"shape": "L4", "x1": -600, "y1": -205, "x2": -420, "y2": -415, "width": 25},
    {"shape": "I", "x1": 290, "y1": 40, "x2": 490, "y2": -20},
]


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0

    if dx == 0:
        if dy > 0:
            zone = 1
        else:
            zone = 6
    elif dy == 0:
        if dx > 0:
            zone = 7
        else:
            zone = 3
    else:
        if abs(dx) >= abs(dy):
            if dx > 0 and dy > 0:
                zone = 0
            if dx < 0 and dy > 0:
                zone = 3
            if dx < 0 and dy < 0:
                zone = 4
            if dx > 0 and dy < 0:
                zone = 7
        else:
            if dx > 0 and dy > 0:
                zone = 1
            if dx < 0 and dy > 0:
                zone = 2
            if dx < 0 and dy < 0:
                zone = 5
            if dx > 0 and dy < 0:
                zone = 6

    return zone


def convertToZone0(givenZone, X, Y):
    x = 0
    y = 0

    if givenZone == 0:
        x = X
        y = Y

    if givenZone == 1:
        x = Y
        y = X

    if givenZone == 2:
        x = Y
        y = -X

    if givenZone == 3:
        x = -X
        y = Y

    if givenZone == 4:
        x = -X
        y = -Y

    if givenZone == 5:
        x = -Y
        y = -X

    if givenZone == 6:
        x = -Y
        y = X

    if givenZone == 7:
        x = X
        y = -Y

    return x, y


def convertZone0ToActualZone(toZone, X, Y):
    x = 0
    y = 0

    if toZone == 0:
        x = X
        y = Y

    if toZone == 1:
        x = Y
        y = X

    if toZone == 2:
        x = -Y
        y = X

    if toZone == 3:
        x = -X
        y = Y

    if toZone == 4:
        x = -X
        y = -Y

    if toZone == 5:
        x = -Y
        y = -X

    if toZone == 6:
        x = Y
        y = -X

    if toZone == 7:
        x = X
        y = -Y

    return x, y


def midPointLine(x1, y1, x2, y2, curZone, pointSize):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1
    x = x1

    while x <= x2:
        actualX, actualY = convertZone0ToActualZone(curZone, x, y)
        drawPoints(actualX, actualY, pointSize)

        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

        x += 1


def drawLine(x1, y1, x2, y2, pointSize=3):
    curZone = findZone(x1, y1, x2, y2)
    zone0X1, zone0Y1 = convertToZone0(curZone, x1, y1)
    zone0X2, zone0Y2 = convertToZone0(curZone, x2, y2)
    midPointLine(zone0X1, zone0Y1, zone0X2, zone0Y2, curZone, pointSize)


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b


def drawPoints(x, y, pointSize=2):
    glPointSize(pointSize)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def drawCirclePoints(x, y, centerX, centerY, pointSize):
    drawPoints(x + centerX, y + centerY, pointSize)
    drawPoints(y + centerX, x + centerY, pointSize)
    drawPoints(-y + centerX, x + centerY, pointSize)
    drawPoints(-x + centerX, y + centerY, pointSize)
    drawPoints(-x + centerX, -y + centerY, pointSize)
    drawPoints(-y + centerX, -x + centerY, pointSize)
    drawPoints(y + centerX, -x + centerY, pointSize)
    drawPoints(x + centerX, -y + centerY, pointSize)


def midPointCircle(r, centerX, centerY, pointSize=2):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        drawCirclePoints(x, y, centerX, centerY, pointSize)

        incE = 2 * x + 3
        incSE = 2 * (x - y) + 3

        if d >= 0:
            d += incSE
            y -= 1
        else:
            d += incE

        x += 1


def hasCollided(
    box1x, box1y, box1Width, box1Height, box2x, box2y, box2Width, box2Height
):

    # for a box
    # box1x --> min
    # box1x + box1Width --> max
    # box1y --> min
    # box1y + box1Height --> max

    return (
        box1x < box2x + box2Width
        and box1x + box1Width > box2x
        and box1y < box2y + box2Height
        and box1y + box1Height > box2y
    )


def drawthief():
    glColor(1, 0.5, 0.5)
    midPointCircle(thiefRadius, thiefX, thiefY,5)


def drawkey():
    global keyX, keyY
    glColor(0.4, 0.7, 0.5)
    midPointCircle(4, keyX, keyY, 1)
    midPointCircle(7, keyX, keyY, 1)
    drawLine(590, -400, 590, -430, 1)
    drawLine(590, -410, 598, -410, 1)
    drawLine(590, -405, 600, -405, 1)


def drawFireBall():
    midPointCircle(firedBallRadius, firedBallCenX, firedBallCenY)


def drawgun():
    glColor(0.7, 0.4, 0.1)
    drawLine(20, 20, 60, 20, 1)
    drawLine(20, 12, 60, 12, 1)
    drawLine(20, 20, 20, 12, 1)
    drawLine(60, 20, 60, 12, 1)
    drawLine(20, 12, 18, -5, 1)
    drawLine(28, 12, 26, -5, 1)
    drawLine(18, -5, 26, -5, 1)
    drawLine(18, -5, 26, -5, 1)
    #
    drawLine(26, 12, 52, 12, 1)
    drawLine(26, 8, 52, 8, 1)
    drawLine(52, 12, 52, 8, 1)
    drawLine(26, 12, 26, 8, 1)
    #
    drawLine(38, 1, 38, 8, 1.5)
    drawLine(40, 1, 40, 8, 1.5)
    drawLine(40, 1, 38, 1, 1.5)


def drawPrisonCells():
    for i in range(len(prisonsArr)):

        if prisonsArr[i]["shape"] != "I":
            shape, x1, y1, x2, y2, width = prisonsArr[i].values()
        else:
            shape, x1, y1, x2, y2 = prisonsArr[i].values()

        if shape == "E1":
            drawPrisonCellE1(x1, y1, x2, y2, width)

        if shape == "E2":
            drawPrisonCellE2(x1, y1, x2, y2, width)

        if shape == "E3":
            drawPrisonCellE3(x1, y1, x2, y2, width)

        if shape == "L1":
            drawPrisonCellL1(x1, y1, x2, y2, width)

        if shape == "L2":
            drawPrisonCellL2(x1, y1, x2, y2, width)

        if shape == "L3":
            drawPrisonCellL3(x1, y1, x2, y2, width)

        if shape == "L4":
            drawPrisonCellL4(x1, y1, x2, y2, width)

        if shape == "I":
            drawPrisonCellI(x1, y1, x2, y2)
# Drawing the teleport pads
def draw_Teleport_Pads():
    for pad in teleport:
        glColor(*pad["color"])
        midPointCircle(20, pad["x"], pad["y"], 4)

def checkCellCollision(cell):
    shape = cell["shape"]

    if shape != "I":
        shape, x1, y1, x2, y2, width = cell.values()
    else:
        shape, x1, y1, x2, y2 = cell.values()

    thiefBoxX = thiefX - thiefRadius
    thiefBoxY = thiefY - thiefRadius
    thiefWidth = thiefHeight = thiefRadius * 2

    if shape == "I":
        cond = hasCollided(
            x1, y2, x2 - x1, y1 - y2, thiefBoxX, thiefBoxY, thiefWidth, thiefHeight
        )

        return cond

    if shape == "E1":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        cond2 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond3 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        return cond1 or cond2 or cond3

    if shape == "E2":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        cond2 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond3 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        return cond1 or cond2 or cond3

    if shape == "E3":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond3 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        return cond1 or cond2 or cond3

    if shape == "L1":
        cond1 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        return cond1 or cond2

    if shape == "L2":
        cond1 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        return cond1 or cond2

    if shape == "L3":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        return cond1 or cond2

    if shape == "L4":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )
        cond2 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            thiefBoxX,
            thiefBoxY,
            thiefWidth,
            thiefHeight,
        )

        return cond1 or cond2

# Check teleportation 
def checking_teleportation():
    global thiefX, thiefY, last_pad
    
    for pad in teleport:
        dist = math.sqrt((thiefX - pad["x"])**2 + (thiefY - pad["y"])**2)
        if dist <= thiefRadius + 15:            
            if last_pad ==  (pad["x"], pad["y"]): 
               return
            prev_thiefX, prev_thiefY = pad["x"], pad["y"]
            print(f"Thief vanished from ({prev_thiefX}, {prev_thiefY}).")
            thiefX, thiefY = pad["positionX"], pad["positionY"]
            last_pad = (pad["positionX"], pad["positionY"])
            print(f"Teleporting to ({thiefX}, {thiefY})...")

            break

def checkGateCollision():
    global thiefX, thiefY, thiefRadius, win

    flag = hasCollided(
        thiefX - thiefRadius,
        thiefY - thiefRadius,
        thiefRadius + thiefRadius,
        thiefRadius + thiefRadius,
        690,
        -30,
        0,
        60,
    )
    if flag:
        print("Mission Passed! Respect++")
        win = True
        return


def checkCollisionWithPrisonCell():
    global hearts
    for i in range(len(prisonsArr)):
        if checkCellCollision(prisonsArr[i]):
            
            return True
    return False


def checkKeyCollision():
    global thiefX, thiefY, thiefRadius, keyX, keyY, keyAchieve
    flag = hasCollided(
        thiefX - thiefRadius,
        thiefY - thiefRadius,
        thiefRadius + thiefRadius,
        thiefRadius + thiefRadius,
        keyX + 7,
        keyY - 7,
        17,
        37,
    )
    if flag:
        print("You acquired the key!")
        keyAchieve = True


def checkGunCollision():
    global thiefX, thiefY, thiefRadius, gunX, gunY, gunAchieve
    flag = hasCollided(
        thiefX - thiefRadius,
        thiefY - thiefRadius,
        thiefRadius + thiefRadius,
        thiefRadius + thiefRadius,
        gunX,
        gunY,
        42,
        25,
    )
    if flag:
        gunAchieve = True
        print("You acquired the gun!")


def drawPolice(police):

    glColor(0.1450980392156863, 0.38823529411764707, 0.9215686274509803)

    polR = police["r"]
    theta = police["theta"]
    baseTheta = police["baseTheta"]
    polViewPointRange = police["viewRange"]
    polX1 = police["x1"]
    polY1 = police["y1"]
    polX2 = polX1 + (polR * 2) * math.cos(math.radians(baseTheta))
    polY2 = polY1 + (polR * 2) * math.sin(math.radians(baseTheta))

    polLeftX1 = polX1 + polViewPointRange * math.cos(math.radians(theta))
    polLeftY1 = polY1 + polViewPointRange * math.sin(math.radians(theta))
    polRightX2 = polX2 + polViewPointRange * math.cos(math.radians(theta))
    polRightY2 = polY2 + polViewPointRange * math.sin(math.radians(theta))

    # police circle
    cenX1 = (polX1 + polX2) / 2
    cenY1 = (polY1 + polY2) / 2
    midPointCircle(polR, cenX1, cenY1, 3)

    glColor(0.24705882352941178, 0.24705882352941178, 0.27450980392156865)
    midPointCircle(polViewPointRange, cenX1, cenY1, 0.5)

    # police view triangle

    glColor(1, 0, 0)
    drawLine(cenX1, cenY1, polLeftX1, polLeftY1, 1)
    drawLine(cenX1, cenY1, polRightX2, polRightY2, 1)
    drawLine(polLeftX1, polLeftY1, polRightX2, polRightY2, 1)


def checkPolCollision(police):
    polR = police["r"]
    baseTheta = police["baseTheta"]
    polViewPointRange = police["viewRange"]
    polX1 = police["x1"]
    polY1 = police["y1"]
    polX2 = polX1 + (polR * 2) * math.cos(math.radians(baseTheta))
    polY2 = polY1 + (polR * 2) * math.sin(math.radians(baseTheta))

    # police circle centre
    cenX1 = (polX1 + polX2) / 2
    cenY1 = (polY1 + polY2) / 2

    distance = math.sqrt((thiefX - cenX1) ** 2 + (thiefY - cenY1) ** 2)
    if distance < thiefRadius + polViewPointRange:
        return True

    return False


def checkCollisionWithPatrol():
    global gameOver, hearts

    for i in range(len(policeArr)):
        if not policeArr[i]["killed"]:
            if checkPolCollision(policeArr[i]):
                hearts -= 1  # Lose a heart
                if hearts <= 0:
                    gameOver = True
                    print("Game is Over!")
                else:
                    print(f"You were caught! Hearts left: {hearts}")
                    restartgame()  # Restart with remaining hearts



# firing collision with prison cells
def checkFireCellCollision(cell):
    shape = cell["shape"]

    if shape != "I":
        shape, x1, y1, x2, y2, width = cell.values()
    else:
        shape, x1, y1, x2, y2 = cell.values()

    fireBoxX = firedBallCenX - firedBallRadius
    fireBoxY = firedBallCenY - firedBallRadius
    fireWidth = fireHeight = firedBallRadius * 2

    if shape == "I":
        cond = hasCollided(
            x1, y2, x2 - x1, y1 - y2, fireBoxX, fireBoxY, fireWidth, fireHeight
        )
        return cond

    if shape == "E1":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        cond2 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond3 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        return cond1 or cond2 or cond3

    if shape == "E2":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        cond2 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond3 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        return cond1 or cond2 or cond3

    if shape == "E3":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond3 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        return cond1 or cond2 or cond3

    if shape == "L1":
        cond1 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        return cond1 or cond2

    if shape == "L2":
        cond1 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        return cond1 or cond2

    if shape == "L3":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond2 = hasCollided(
            x1,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        return cond1 or cond2

    if shape == "L4":
        cond1 = hasCollided(
            x1,
            y1 - width,
            x2 - x1,
            width,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )
        cond2 = hasCollided(
            x2 - width,
            y2,
            width,
            y1 - y2,
            fireBoxX,
            fireBoxY,
            fireWidth,
            fireHeight,
        )

        return cond1 or cond2


def checkFirePrisonCellsCollision():
    for i in range(len(prisonsArr)):
        if checkFireCellCollision(prisonsArr[i]):
            return True
    return False


def checkFirePoliceCollision(police):
    polR = police["r"]
    baseTheta = police["baseTheta"]
    polX1 = police["x1"]
    polY1 = police["y1"]
    polX2 = polX1 + (polR * 2) * math.cos(math.radians(baseTheta))
    polY2 = polY1 + (polR * 2) * math.sin(math.radians(baseTheta))

    # police circle centre
    cenX1 = (polX1 + polX2) / 2
    cenY1 = (polY1 + polY2) / 2

    distance = math.sqrt((firedBallCenX - cenX1) ** 2 + (firedBallCenY - cenY1) ** 2)
    if distance < firedBallRadius + polR:
        return True

    return False


def checkFirePatrolCollision():
    global policeArr, policeKillCount
    for i in range(len(policeArr)):
        if not policeArr[i]["killed"]:
            if checkFirePoliceCollision(policeArr[i]):
                policeArr[i]["killed"] = True
                policeKillCount += 1
                print(f"You Killed a Police! Police Kill Count: {policeKillCount}")
                return True
    return False


def backbtn():
    glColor(0.21, 0.74, 0.97)
    drawLine(600, 475, 610, 465, 1.7)
    drawLine(600, 475, 610, 485, 1.7)
    drawLine(620, 475, 600, 475, 1.7)


def playbtn():
    glColor(0.98, 0.82, 0.3)
    drawLine(635, 485, 650, 475, 1.7)
    drawLine(635, 465, 650, 475, 1.7)
    drawLine(635, 485, 635, 465, 1.7)


def pausebtn():
    glColor(0.98, 0.82, 0.3)
    drawLine(647, 485, 647, 465, 1.7)
    drawLine(638, 485, 638, 465, 1.7)


def exitbtn():
    glColor(1, 0, 0)
    drawLine(670, 485, 690, 465, 1.7)
    drawLine(690, 485, 670, 465, 1.7)


def pausegame():
    global gamePaused
    gamePaused = True


def resumegame():
    global gamePaused
    gamePaused = False


def exitgame():
    global thiefX, thiefY
    print(f"Goodbye")
    thiefX = -685
    thiefY = -435
    glutLeaveMainLoop()


def restartgame():
    global gameOver, thiefX, thiefY, keyAchieve, gunAchieve, policeArr, policeKillCount, win, fired, original_restart

    gameOver = False
    win = False
    policeKillCount = 0
    print("Restarting with remaining hearts...")
    thiefX = -685
    thiefY = -435
    keyAchieve = False
    gunAchieve = False
    fired = False
    if original_restart == True:
        drawAllHearts()
    original_restart = False

    policeArr = [
        {
            "x1": -600,
            "y1": -380,
            "r": 11,
            "viewRange": 50,
            "theta": 90,
            "baseTheta": 0,
            "thetaRotation": 0,
            "movementType": "t",
            "speed": 3,
            "boundaries": {"top": -320, "bottom": -380, "right": -510, "left": -600},
            "direction": "clockwise",
            "killed": False,
        },
        {
            "x1": 20,
            "y1": -370,
            "r": 11,
            "viewRange": 60,
            "theta": 0,
            "baseTheta": 270,
            "thetaRotation": 0,
            "movementType": "r",
            "speed": 5,
            "boundaries": {"top": -340, "bottom": -370, "right": 80, "left": 20},
            "direction": "antiClockwise",
            "killed": False,
        },
        {
            "x1": -350,
            "y1": -320,
            "r": 11,
            "viewRange": 70,
            "theta": 0,
            "baseTheta": 270,
            "thetaRotation": 0,
            "movementType": "r",
            "speed": 2,
            "boundaries": {"top": -140, "bottom": -320, "right": -180, "left": -350},
            "direction": "antiClockwise",
            "killed": False,
        },
        {
            "x1": -380,
            "y1": 170,
            "r": 11,
            "viewRange": 70,
            "theta": 90,
            "baseTheta": 0,
            "thetaRotation": 0,
            "movementType": "t",
            "speed": 3,
            "boundaries": {"top": 220, "bottom": 170, "right": -210, "left": -380},
            "direction": "clockwise",
            "killed": False,
        },
        {
            "x1": -60,
            "y1": 220,
            "r": 11,
            "viewRange": 70,
            "theta": 90,
            "baseTheta": 0,
            "thetaRotation": 0,
            "movementType": "t",
            "speed": 5,
            "boundaries": {"top": 350, "bottom": 220, "right": 100, "left": -60},
            "direction": "clockwise",
            "killed": False,
        },
        {
            "x1": 275,
            "y1": 200,
            "r": 11,
            "viewRange": 70,
            "theta": 0,
            "baseTheta": 270,
            "thetaRotation": 0,
            "movementType": "r",
            "speed": 5,
            "boundaries": {"top": 370, "bottom": 200, "right": 410, "left": 275},
            "direction": "antiClockwise",
            "killed": False,
        },
        {
            "x1": 630,
            "y1": -100,
            "r": 11,
            "viewRange": 50,
            "theta": 90,
            "baseTheta": 0,
            "thetaRotation": 0,
            "movementType": "t",
            "speed": 6,
            "boundaries": {"top": 70, "bottom": -100, "right": 630, "left": 550},
            "direction": "antiClockwise",
            "killed": False,
        },
        {
            "x1": 630,
            "y1": -280,
            "r": 11,
            "viewRange": 50,
            "theta": 0,
            "baseTheta": 270,
            "thetaRotation": 0,
            "movementType": "r",
            "speed": 6,
            "boundaries": {"top": -200, "bottom": -280, "right": 630, "left": 410},
            "direction": "antiClockwise",
            "killed": False,
        },
        {
            "x1": -60,
            "y1": -10,
            "r": 11,
            "viewRange": 70,
            "theta": 0,
            "baseTheta": 270,
            "thetaRotation": 0,
            "movementType": "r",
            "speed": 5,
            "boundaries": {"top": 120, "bottom": -10, "right": 200, "left": -60},
            "direction": "antiClockwise",
            "killed": False,
        },
        {
            "x1": 580,
            "y1": 320,
            "r": 11,
            "viewRange": 50,
            "theta": 0,
            "baseTheta": 270,
            "thetaRotation": 0,
            "movementType": "r",
            "speed": 3,
            "boundaries": {"top": 380, "bottom": 320, "right": 630, "left": 580},
            "direction": "antiClockwise",
            "killed": False,
        },
    ]


def drawPrisonCellE1(x1, y1, x2, y2, width):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)

    # outer lines
    drawLine(x1, y1, x2, y1)
    drawLine(x1, y1, x1, y2)
    drawLine(x1, y2, x2, y2)
    # inner lines
    drawLine(x1 + width, y1 - width, x2, y1 - width)
    drawLine(x1 + width, y1 - width, x1 + width, y2 + width)
    drawLine(x1 + width, y2 + width, x2, y2 + width)
    # lids
    drawLine(x2, y1, x2, y1 - width)
    drawLine(x2, y2, x2, y2 + width)


def drawPrisonCellE2(x1, y1, x2, y2, width):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)

    # outer lines
    drawLine(x1, y1, x2, y1)
    drawLine(x2, y1, x2, y2)
    drawLine(x1, y2, x2, y2)
    # inner lines
    drawLine(x1, y1 - width, x2 - width, y1 - width)
    drawLine(x2 - width, y1 - width, x2 - width, y2 + width)
    drawLine(x2 - width, y2 + width, x1, y2 + width)
    # lids
    drawLine(x1, y1, x1, y1 - width)
    drawLine(x1, y2, x1, y2 + width)


def drawPrisonCellE3(x1, y1, x2, y2, width):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)

    # outer lines
    drawLine(x2, y2, x2, y1)
    drawLine(x1, y1, x2, y1)
    drawLine(x1, y1, x1, y2)
    # inner lines
    drawLine(x2 - width, y1 - width, x2 - width, y2)
    drawLine(x1 + width, y1 - width, x2 - width, y1 - width)
    drawLine(x1 + width, y1 - width, x1 + width, y2)
    # lids
    drawLine(x1, y2, x1 + width, y2)
    drawLine(x2, y2, x2 - width, y2)


def drawPrisonCellL1(x1, y1, x2, y2, width):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)
    # outer lines
    drawLine(x1, y1, x1, y2)
    drawLine(x1, y2, x2, y2)
    # inner lines
    drawLine(x1 + width, y1, x1 + width, y2 + width)
    drawLine(x1 + width, y2 + width, x2, y2 + width)

    # lids
    drawLine(x1, y1, x1 + width, y1)
    drawLine(x2, y2, x2, y2 + width)


def drawPrisonCellL2(x1, y1, x2, y2, width):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)
    # outer lines
    drawLine(x2, y1, x2, y2)
    drawLine(x1, y2, x2, y2)
    # inner lines
    drawLine(x2 - width, y1, x2 - width, y2 + width)
    drawLine(x1, y2 + width, x2 - width, y2 + width)

    # lids
    drawLine(x2 - width, y1, x2, y1)
    drawLine(x1, y2, x1, y2 + width)


def drawPrisonCellL3(x1, y1, x2, y2, width):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)
    # outer lines
    drawLine(x1, y1, x2, y1)
    drawLine(x1, y1, x1, y2)
    # inner lines
    drawLine(x1 + width, y1 - width, x2, y1 - width)
    drawLine(x1 + width, y1 - width, x1 + width, y2)
    # lids
    drawLine(x2, y1, x2, y1 - width)
    drawLine(x1, y2, x1 + width, y2)


def drawPrisonCellL4(x1, y1, x2, y2, width):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)
    # outer lines
    drawLine(x1, y1, x2, y1)
    drawLine(x2, y1, x2, y2)
    # inner lines
    drawLine(x1, y1 - width, x2 - width, y1 - width)
    drawLine(x2 - width, y1 - width, x2 - width, y2)

    # lids
    drawLine(x1, y1, x1, y1 - width)
    drawLine(x2 - width, y2, x2, y2)


def drawPrisonCellI(x1, y1, x2, y2):
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)
    # upper
    drawLine(x1, y1, x2, y1)
    # left
    drawLine(x1, y1, x1, y2)
    # right
    drawLine(x2, y1, x2, y2)
    # down
    drawLine(x1, y2, x2, y2)


def mouseListener(button, state, x, y):
    global gamePaused, original_restart, hearts

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            c_x, c_y = convert_coordinate(x, y)

            if (670 <= c_x <= 690) and (465 <= c_y <= 485):
                exitgame()

            if (600 <= c_x <= 620) and (465 <= c_y <= 485):
                original_restart = True
                hearts = 3
                restartgame()

            if (638 <= c_x <= 647) and (465 <= c_y <= 485) and not gamePaused:
                pausegame()
            elif (635 <= c_x <= 650) and (465 <= c_y <= 485) and gamePaused:
                resumegame()


def specialKeyListener(key, x, y):
    global thiefX, thiefY, thiefSpeed, gamePaused, gameOver

    if key == GLUT_KEY_LEFT and not gameOver and not gamePaused and not win:
        if thiefX >= -700 + thiefRadius + 5:
            thiefX -= thiefSpeed
            if checkCollisionWithPrisonCell():
                thiefX += thiefSpeed

    if key == GLUT_KEY_RIGHT and not gameOver and not gamePaused and not win:
        if thiefX <= 700 - thiefRadius - 5:
            thiefX += thiefSpeed
            if checkCollisionWithPrisonCell():
                thiefX -= thiefSpeed

    if key == GLUT_KEY_UP and not gameOver and not gamePaused and not win:
        if thiefY <= 450 - thiefRadius - 5:
            thiefY += thiefSpeed
            if checkCollisionWithPrisonCell():
                thiefY -= thiefSpeed

    if key == GLUT_KEY_DOWN and not gameOver and not gamePaused and not win:
        if thiefY >= -450 + thiefRadius + 5:
            thiefY -= thiefSpeed
            if checkCollisionWithPrisonCell():
                thiefY += thiefSpeed

    glutPostRedisplay()


def keyboardListener(key, x, y):
    global fired, firedBallCenX, firedBallCenY, thiefX, thiefY, firedDirection
    global background_color,gate_color

    if gunAchieve:
        if key == b"w" and not gamePaused and not gameOver and not win:
            fired = True
            firedDirection = "t"
            firedBallCenX = thiefX
            firedBallCenY = thiefY + thiefRadius

        if key == b"a" and not gamePaused and not gameOver and not win:
            fired = True
            firedDirection = "l"
            firedBallCenX = thiefX - thiefRadius
            firedBallCenY = thiefY

        if key == b"s" and not gamePaused and not gameOver and not win:
            fired = True
            firedDirection = "b"
            firedBallCenX = thiefX
            firedBallCenY = thiefY - thiefRadius

        if key == b"d" and not gamePaused and not gameOver and not win:
            fired = True
            firedDirection = "r"
            firedBallCenX = thiefX + thiefRadius
            firedBallCenY = thiefY


    if key== b"m":
        background_color+=0.1
        gate_color+=0.1
        # glClearColor(background_color,background_color,background_color,0)
        print("Day Mode")

    if key==b"n":
        background_color-=0.1
        gate_color-=0.1
        # glClearColor(background_color,background_color,background_color,0) 
        print("Night Mode")   

    glutPostRedisplay()


def winningMsg():
    glColor(1, 0.7, 0)
    drawLine(0, 480, 10, 455, 1)  # w
    drawLine(10, 455, 20, 480, 1)
    drawLine(30, 455, 20, 480, 1)
    drawLine(30, 455, 40, 480, 1)  # w
    drawLine(50, 455, 50, 480, 1)  # i
    drawLine(60, 455, 60, 480, 1)  # n
    drawLine(80, 455, 60, 480, 1)
    drawLine(80, 455, 80, 480, 1)


def gameoverMsg():
    glColor(1, 0.7, 0)
    drawLine(-50, 480, -40, 480, 1.5)  # g
    drawLine(-50, 480, -50, 455, 1.5)
    drawLine(-50, 455, -40, 455, 1.5)
    drawLine(-40, 465, -40, 455, 1.5)
    drawLine(-40, 465, -45, 465, 1.5)  # g

    drawLine(-30, 455, -30, 480, 1.5)  # a
    drawLine(-20, 455, -20, 480, 1.5)
    drawLine(-30, 480, -20, 480, 1.5)
    drawLine(-30, 470, -20, 470, 1.5)  # a

    drawLine(-10, 455, -5, 480, 1.5)  # m
    drawLine(0, 455, -5, 480, 1.5)
    drawLine(10, 480, 0, 455, 1.5)
    drawLine(10, 480, 12, 455, 1.5)  # m

    drawLine(20, 480, 20, 455, 1.5)  # e
    drawLine(20, 480, 25, 480, 1.5)  # e
    drawLine(20, 455, 25, 455, 1.5)  # e
    drawLine(20, 465, 23, 465, 1.5)  # e

    drawLine(50, 455, 50, 480, 1.5)  # 0
    drawLine(60, 455, 60, 480, 1.5)
    drawLine(50, 455, 60, 455, 1.5)
    drawLine(50, 480, 60, 480, 1.5)  # o

    drawLine(70, 480, 75, 455, 1.5)  # v
    drawLine(80, 480, 75, 455, 1.5)  # v

    drawLine(90, 480, 90, 455, 1.5)  # e
    drawLine(90, 480, 95, 480, 1.5)  # e
    drawLine(90, 455, 95, 455, 1.5)  # e
    drawLine(90, 465, 93, 465, 1.5)  # e

    drawLine(100, 480, 100, 455, 1.5)  # r
    drawLine(100, 480, 110, 480, 1.5)
    drawLine(110, 480, 110, 470, 1.5)
    drawLine(110, 470, 100, 470, 1.5)
    drawLine(100, 470, 110, 455, 1.5)  # r


def drawGate():
    global keyAchieve
    global background_color,gate_color
    
    if keyAchieve:
        
        glColor(gate_color,gate_color,gate_color)
            
    else:
        glColor(1, 0, 0)
    drawLine(700, 30, 700, -30)


def drawBoundaries():
    global background_color
    if background_color>0.6: 
        glColor(0,0,0)
    else:       
        glColor(1, 1, 1)


    drawLine(-700, 450, 700, 450)
    drawLine(-700, -450, 700, -450)
    drawLine(-700, -450, -700, 450)
    drawLine(700, 450, 700, -450)


def drawPatrolSquad():
    for i in range(len(policeArr)):
        if not policeArr[i]["killed"]:
            drawPolice(policeArr[i])


def patrolPolice():
    for i in range(len(policeArr)):
        if not policeArr[i]["killed"]:
            if policeArr[i]["direction"] == "antiClockwise":
                polAntiClockMov(policeArr[i])
            else:
                polClockMov(policeArr[i])


def polClockMov(police):
    theta = police["theta"]
    thetaRotation = police["thetaRotation"]
    polX1 = police["x1"]
    polY1 = police["y1"]
    mode = police["movementType"]
    speed = police["speed"]
    top, bottom, right, left = police["boundaries"].values()

    if mode == "t":
        police["y1"] += speed
        if polY1 >= top:
            police["movementType"] = "rotate"

    if mode == "l":
        police["x1"] -= speed
        if polX1 <= left:
            police["movementType"] = "rotate"

    if mode == "b":
        police["y1"] -= speed
        if polY1 <= bottom:
            police["movementType"] = "rotate"

    if mode == "r":
        police["x1"] += speed
        if polX1 >= right:
            police["movementType"] = "rotate"

    if mode == "rotate":
        if thetaRotation >= 90:
            if theta >= 270:
                police["movementType"] = "b"
                police["baseTheta"] = 360
            elif theta >= 180:
                police["movementType"] = "l"
            elif theta >= 90:
                police["movementType"] = "t"

            elif theta >= 0:
                police["movementType"] = "r"
                police["theta"] = 360

            police["thetaRotation"] = 0

        else:
            police["thetaRotation"] += speed
            police["theta"] -= speed
            police["baseTheta"] -= speed


def polAntiClockMov(police):
    theta = police["theta"]
    thetaRotation = police["thetaRotation"]
    polX1 = police["x1"]
    polY1 = police["y1"]
    mode = police["movementType"]
    speed = police["speed"]
    top, bottom, right, left = police["boundaries"].values()

    if mode == "t":
        police["y1"] += speed
        if polY1 >= top:
            police["movementType"] = "rotate"

    if mode == "l":
        police["x1"] -= speed
        if polX1 <= left:
            police["movementType"] = "rotate"

    if mode == "b":
        police["y1"] -= speed
        if polY1 <= bottom:
            police["movementType"] = "rotate"

    if mode == "r":
        police["x1"] += speed
        if polX1 >= right:
            police["movementType"] = "rotate"

    if mode == "rotate":
        if thetaRotation >= 90:
            if theta >= 360:
                police["movementType"] = "r"
                police["theta"] = 0
            elif theta >= 270:
                police["movementType"] = "b"
            elif theta >= 180:
                police["movementType"] = "l"
            elif theta >= 90:
                police["movementType"] = "t"
                police["baseTheta"] = 0

            police["thetaRotation"] = 0

        else:
            police["thetaRotation"] += speed
            police["theta"] += speed
            police["baseTheta"] += speed

def drawHeart(adder):
    glColor(1, 0, 0)  # Red Color for hearts

    # Left semicircle
    for angle in range(0, 180, 10):
        angle_rad = math.radians(angle)
        x = math.cos(angle_rad) * 10 - 685 + adder
        y = math.sin(angle_rad) * 10 + 480
        drawPoints(x, y, 1)

    # Right semicircle
    for angle in range(0, 180, 10):
        angle_rad = math.radians(angle)
        x = math.cos(angle_rad) * 10 - 670 + adder
        y = math.sin(angle_rad) * 10 + 480
        drawPoints(x, y, 1)

    # Bottom triangle
    drawLine(-695 + adder, 480, -680 + adder, 460, 2)
    drawLine(-665 + adder, 480, -680 + adder, 460, 2)


def drawAllHearts():
    for i in range(hearts):
        drawHeart(i * 50)





def handleFiring():
    global firedBallCenX, firedBallCenY, fired, hearts, missed_firing

    if fired:
        if firedDirection == "t":
            firedBallCenY += firedBallSpeed
        elif firedDirection == "b":
            firedBallCenY -= firedBallSpeed
        elif firedDirection == "r":
            firedBallCenX += firedBallSpeed
        elif firedDirection == "l":
            firedBallCenX -= firedBallSpeed

        if (firedBallCenX + firedBallRadius >= 690) or (
            firedBallCenX - firedBallRadius <= -690
        ):
            
            missed_firing+=1
            fired = False

        if (firedBallCenY + firedBallRadius >= 440) or (
            firedBallCenY - firedBallRadius <= -440
        ):
            missed_firing+=1
            fired = False

        if checkFirePrisonCellsCollision(): 
            missed_firing+=1
            fired = False
            
            
        if  checkFirePatrolCollision():
            fired = False
            
def handle_missed_firing():            
    global firedBallCenX, firedBallCenY, fired, hearts, gameOver, missed_firing
    if missed_firing==3:
        hearts-=1
        missed_firing=0
    if hearts == 0:
        gameOver = True
    

def animate():
    if gameOver or win or gamePaused:
        return

    if keyAchieve == False:
        checkKeyCollision()

    if gunAchieve == False:
        checkGunCollision()

    if keyAchieve:
        checkGateCollision()
    
    checking_teleportation()
    checkCollisionWithPatrol()
    patrolPolice()
    handleFiring()
    handle_missed_firing()

    glutPostRedisplay()





def showScreen():
    
    global background_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(background_color,background_color,background_color,1.0)
    
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    
    

    # Draw from here

    exitbtn()
    backbtn()

    if gamePaused:
        playbtn()
    else:
        pausebtn()

    if win:
        winningMsg()

    if gameOver:
        gameoverMsg()  # Show game over message
    else:
        if not win:
            drawPatrolSquad()

        if fired:
            drawFireBall()

        if not keyAchieve:
            drawkey()

        if not gunAchieve:
            drawgun()

    drawBoundaries()
    drawPrisonCells()
    drawAllHearts()  # Show remaining hearts
    drawthief()
    drawGate()
    draw_Teleport_Pads()

    glutSwapBuffers()




def init():
    
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W_Width / 2, W_Width / 2, -W_Height / 2, W_Height / 2, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitWindowSize(W_Width, W_Height)  # window size
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Grand Theft Auto VII")
init()
glutSpecialFunc(specialKeyListener)
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)

glutMainLoop()


