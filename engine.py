#Imports necessary modules
import pyglet
from pyglet.window import mouse
import random
import time

#The "Card" class 
class Card:

    #Initializes the card object
    def __init__(self,backLoad,frontLoad,listOfPairs,batch):

        #Picks random XY coordinates for the card
        random.shuffle(listOfPairs)
        xNy = listOfPairs[len(listOfPairs) - 1]
        listOfPairs.pop()

        #Sets X and Y variables which will become the card's X and Y coordinates later
        x = xNy[0]
        y = xNy[1]

        #Sets the:
        #   Batch of the card
        #   Status of the card (e.g. permanently flipped because it was matched)
        #   Loaded back face
        #   Loaded front face
        #   Loaded display face
        #   X and Y coordinates
        #   Displayed sprite and scale
        self.batch = batch
        self.status = 'unmatched'
        self.backLoad = backLoad
        self.frontLoad = frontLoad
        self.displayFaceStatus = 'front'
        self.x = x
        self.y = y
        self.displayFace = pyglet.sprite.Sprite(self.frontLoad, x=self.x, y=self.y, subpixel = True, batch = self.batch)
        self.displayFace.scale = 0.5
        
    #"Flips" a card
    def flip(self):
        if self.status == 'matched':
            pass
        
        else:
            if self.displayFaceStatus == 'back':
                self.displayFaceStatus = 'front'
                self.displayFace = pyglet.sprite.Sprite(self.frontLoad, x=self.x, y=self.y, subpixel = True, batch = self.batch)
                self.displayFace.scale = 0.5
                return
            
            if self.displayFaceStatus == 'front':
                self.displayFaceStatus = 'back'
                self.displayFace = pyglet.sprite.Sprite(self.backLoad, x=self.x, y=self.y, subpixel = True, batch = self.batch)
                self.displayFace.scale = 0.5
                return

#Reads a text file, returns a list of filenames of pictures to be used
def cardReader(cardFile):

    cardsFilename = str(cardFile)
    cardsInput = open(cardsFilename,'r')
    cardsAll=[name for name in cardsInput.read().split('\n')]
    cardsInput.close()

    return(cardsAll)

#Updates a high score text file
def highScoreUpdater(scoreFile,finishTime,dateTime):
    scoreFilename = str(scoreFile)
    scoreInput = open(scoreFilename,'r')
    scoreAll=[score for score in scoreInput.read().split('\n')]
    scoreInput.close()


    scoreToAdd = finishTime+'                   '+dateTime
    scoreAll.append(scoreToAdd)
    scoreAll.sort()
    scoreAllString = '\n'.join(scoreAll)

    scoreInput = open(scoreFilename,'w')
    
    scoreInput.write(scoreAllString)
    scoreInput.close()

#Checks if the two flipped cards are a match, and adjusts accordingly
def flipChecker(flippedCards):
    if flippedCards[0].frontLoad == flippedCards[1].frontLoad:
        flippedCards[0].status = 'matched'
        flippedCards[1].status = 'matched'
        flippedCards = []
        return
    
    else:
        time.sleep(0.5)
        flippedCards[0].flip()
        flippedCards[1].flip()
        flippedCards = []
        return

#Checks if the game is "finished" or not
def gameChecker(cardList):
    for i in range(len(cardList)):
        if cardList[i].status == 'unmatched':
            return('unfinished')

    return('finished') 

#Gets time elapsed in seconds (a floating point number)
def timeElapsed(startTime):
    return(time.time()-startTime)

#Converts seconds to "Minutes:Seconds.Miliseconds"
def secondsConverter(seconds):
    mins = int(seconds // 60)
    seconds -=  mins * 60
    
    secs = int(seconds // 1)
    seconds -= secs
    
    mils = int(round(seconds*1000,3))

    if mins < 10:
        mins = '0'+str(mins)

    if secs < 10:
        secs = '0'+str(secs)
    
    if mils < 100:
        mils = '0'+str(mils)

    return(str(mins)+':'+str(secs)+'.'+str(mils))