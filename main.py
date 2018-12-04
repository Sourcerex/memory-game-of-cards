#Imports necessary modules and functions
import pyglet
from pyglet.window import mouse
from pyglet.clock import unschedule
from engine import cardReader
from engine import highScoreUpdater
from engine import Card
from engine import flipChecker
from engine import gameChecker
from engine import timeElapsed
from engine import secondsConverter
import random
import time
import datetime

#Gets the filenames of the card faces file, as well as the high score list
allCardsFile = 'CardImages.txt'
allScoresFile = 'HighScores.txt'

#Gets the filenames of the card's back and front faces
allCardImages = cardReader(allCardsFile)

#Loads the back face for all cards
cardBackName = allCardImages[0]
cardBackLoad = pyglet.image.load(cardBackName)

#Loads the 6 possible front faces for all cards
cardFrontNames = allCardImages[1:7]
clubLoad = pyglet.image.load(cardFrontNames[0])
cupLoad = pyglet.image.load(cardFrontNames[1])
diamondLoad = pyglet.image.load(cardFrontNames[2])
heartLoad = pyglet.image.load(cardFrontNames[3])
shieldLoad = pyglet.image.load(cardFrontNames[4])
spadeLoad = pyglet.image.load(cardFrontNames[5])

#Makes a batch and list for printing and manipulating the cards, defines 12 XY coordinates for the cards 
cardBatch = pyglet.graphics.Batch()
cards = []
xyCoordinates = [
    [0,0],
    [159,0],
    [318,0],
    [477,0],
    [0,210],
    [159,210],
    [318,210],
    [477,210],
    [0,420],
    [159,420],
    [318,420],
    [477,420]
]

#Creates 12 cards, 2 for each front face
C01 = Card(cardBackLoad,clubLoad,xyCoordinates,cardBatch)
cards.append(C01)
C02 = Card(cardBackLoad,clubLoad,xyCoordinates,cardBatch)
cards.append(C02)
C03 = Card(cardBackLoad,cupLoad,xyCoordinates,cardBatch)
cards.append(C03)
C04 = Card(cardBackLoad,cupLoad,xyCoordinates,cardBatch)
cards.append(C04)
C05 = Card(cardBackLoad,diamondLoad,xyCoordinates,cardBatch)
cards.append(C05)
C06 = Card(cardBackLoad,diamondLoad,xyCoordinates,cardBatch)
cards.append(C06)
C07 = Card(cardBackLoad,heartLoad,xyCoordinates,cardBatch)
cards.append(C07)
C08 = Card(cardBackLoad,heartLoad,xyCoordinates,cardBatch)
cards.append(C08)
C09 = Card(cardBackLoad,shieldLoad,xyCoordinates,cardBatch)
cards.append(C09)
C10 = Card(cardBackLoad,shieldLoad,xyCoordinates,cardBatch)
cards.append(C10)
C11 = Card(cardBackLoad,spadeLoad,xyCoordinates,cardBatch)
cards.append(C11)
C12 = Card(cardBackLoad,spadeLoad,xyCoordinates,cardBatch)
cards.append(C12)

#A list of cards marked as "flipped up", to be updated as the game goes
flippedCards = []

#Initializes the windows to be used in the game
window1 = pyglet.window.Window(width = 596, height = 670)

#Creates the text which displays the timer, sets a placeholder start and finish time
timer = pyglet.text.Label('',
                        font_name='Times New Roman',
                        font_size=32,
                        x=window1.width//2, y=window1.height,
                        anchor_x='center', anchor_y='top')
startTime = 'XX:XX.XXX'
finishTime = 'XX:XX.XXX'

#Flips all cards so that they become face down
# Schedules functions which: regularly update the timer, check if the game is finished, and check the flipped cards
def allFlip(dt):
    global startTime

    time.sleep(3)

    for j in range(len(cards)):
        cards[j].flip()
    
    startTime = time.time()

    unschedule(allFlip)
    pyglet.clock.schedule_interval(timerUpdate, 1/60)
    pyglet.clock.schedule_interval(gameUpdate, 1/60)
    pyglet.clock.schedule_interval(flipCheck,1/2)

#Updates the timer
def timerUpdate(dt):
    timer.text = secondsConverter(timeElapsed(startTime))

#Checks if the game is finished, ends the game if it is, gets the finish time and date, and writes it to the scores file 
def gameUpdate(dt):
    if gameChecker(cards) == 'finished':
        finishTime = secondsConverter(timeElapsed(startTime))
        now = datetime.datetime.now()
        finishDate = str(datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond))
        highScoreUpdater(allScoresFile,finishTime,finishDate)
        unschedule(timerUpdate)
        unschedule(gameUpdate)
        unschedule(flipCheck)
        window1.close()

#Checks if the two flipped cards are a match, and adjusts accordingly
def flipCheck(dt):
    global flippedCards

    if len(flippedCards) == 2:
        flipChecker(flippedCards)
        flippedCards = []
    else:
        pass

#"Flips" the clicked card
@window1.event 
def on_mouse_press(x,y,button,modifiers):
    if button == mouse.LEFT and len(flippedCards) != 2:
        for i in range(len(cards)):
            if x >= cards[i].x and x <= cards[i].x + 119 and y >= cards[i].y and y <= cards[i].y + 180:
                cards[i].flip()

                if cards[i].displayFaceStatus == 'front':
                    flippedCards.append(cards[i])
                
                else:
                    flippedCards.remove(cards[i])

@window1.event
def on_draw():
    window1.clear()
    cardBatch.draw()
    timer.draw()

pyglet.clock.schedule_interval(allFlip,1/2)
pyglet.app.run()