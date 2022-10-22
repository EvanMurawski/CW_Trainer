#TODO:
#break down operate function into smaller functions
#generate other phrases besides callsigns
#Create simulated QSO
#cancel with multiple E's
#show a report of the user's accuracy
#Create a GUI


import serial
import time
from colorama import Fore, Back, Style, init
import callsign
import playphrase


# Configuration

SHOW_TX_PHRASE = True
DIT_TIME = 0.08
DAH_TIME = 0.24
ser = serial.Serial(port = "COM4", baudrate = 115200)

# Configuration

DAH = "a"
DIT = "i"

phrases = []

letterDict = {"ia" : "A",
              "aiii" : "B",
              "aiai" : "C",
              "aii" : "D",
              "i" : "E",
              "iiai" : "F",
              "aai" : "G",
              "iiii" : "H",
              "ii" : "I",
              "iaaa" : "J",
              "aia" : "K",
              "iaii" : "L",
              "aa" : "M",
              "ai" : "N",
              "aaa" : "O",
              "iaai" : "P",
              "aaia" : "Q",
              "iai" : "R",
              "iii" : "S",
              "a" : "T",
              "iia" : "U",
              "iiia" : "V",
              "iaa" : "W",
              "aiia" : "X",
              "aiaa" : "Y",
              "aaii" : "Z",
              "iaaaa" : "1",
              "iiaaa" : "2",
              "iiiaa" : "3",
              "iiiia" : "4",
              "iiiii" : "5",
              "aiiii" : "6",
              "aaiii" : "7",
              "aaaii" : "8",
              "aaaai" : "9",
              "aaaaa" : "0",
              "iiaaii" : "?",
              "iaiaia" : ".",
              "aaiiaa" : ",",
              "aiiai" : "/",
              "aiiia" : "="}
              

def operate(testPhrase):
    
    lastChar = DIT
    charString = ""
    receivedFirstWord = False
    receivedFirstChar = False
    firstCall = True
    style = ""
    characterIndex = 0
    transmittedPhrase = ""
    timing = []
    sendingErrors = False
    
    start = time.time()
    while True:
        
        bytesToRead = ser.inWaiting()
        if (bytesToRead > 0):

            data = ser.read(bytesToRead)
            end = time.time()
            
            thisChar = (DIT if data == b'i' else DAH)
            elapsed = end - start
            offTime = elapsed - (DIT_TIME if lastChar == DIT else DAH_TIME)


            #First Dit / Dah of new letter
            if(offTime > 1.5*DIT_TIME):
                
                printChar = letterDict.get(charString)
                if printChar == None:
                    printChar = "~"
                if printChar == "?":
                    print(Back.BLACK + "?", end='')
                    return timing, True
                
                if receivedFirstChar:
                    timing.append(offTime)
                    transmittedPhrase += printChar

                    style, error = checkCharAndSetStyle(testPhrase, transmittedPhrase, style)
                    if error:
                        sendingErrors = True
                    #Check if have reached end of test phrase
                    if(len(transmittedPhrase) == len(testPhrase)):
                        print(style + printChar)
                        return timing, sendingErrors
                    
                    print(style + printChar, end='')

                #Set style for next character
                if not receivedFirstChar:
                    style = Back.BLACK
                elif offTime > 4.5*DIT_TIME:
                    style = Back.YELLOW
                    
                elif offTime < 2.5*DIT_TIME:
                    style = Back.BLUE
                else:
                    style = Back.BLACK

                charString = ""
                receivedFirstChar = True
                
            #First Dit / Dah of new word
            if(offTime > 5.5*DIT_TIME and not firstCall):
                transmittedPhrase += " "

                #Have reached end of test phrase
                if(len(transmittedPhrase) == len(testPhrase)):
                    style = ""
                    print(" ")
                    return timing, sendingErrors
                
                #Set style for space + next character
                if offTime > 8.5*DIT_TIME:
                    style = Back.YELLOW
                elif offTime < 6*DIT_TIME:
                    style = Back.BLUE
                else:
                    style = Back.BLACK

                spaceStyle, error = checkCharAndSetStyle(testPhrase, transmittedPhrase, style)
                if error:
                    sendingErrors = True
                print(spaceStyle + " ", end='')

                receivedFirstWord = True

            firstCall = False
            charString += thisChar
            lastChar = thisChar
            start = end


def checkCharAndSetStyle(phrase, transmittedPhrase, style):

    index = len(transmittedPhrase) - 1
    if (transmittedPhrase[index] != phrase[index]):
        return Back.RED, True
    else:
        return style, False

    
def main():

    init()

    print("started")

    for i in range(10):
        phrases.append(callsign.generateCallsign())

    j = 0
    while j < len(phrases):
        testPhrase = phrases[j]
        if SHOW_TX_PHRASE:
            print(testPhrase)
            
        playphrase.playPhrase(testPhrase, DIT_TIME, DAH_TIME, letterDict)
        timing, sendingErrors = operate(testPhrase)
        
        if not sendingErrors:
            printResult(timing, testPhrase)
            j +=1
        else:
            print(Back.BLACK, "")

def printResult(timing, testPhrase):

    myFormatter = "{:.1f}"
    style = Back.BLACK
    print(style+ "\n")

    i = 0
    for letter in testPhrase:

        if letter != " ":
            print(style+ letter, ": ", end='')
        if i>0 and letter != " ":
            formattedTiming = myFormatter.format(timing[i-1]/DIT_TIME)
            print(style+ formattedTiming, end='')

        if letter != " ":
            i +=1

        print(style+ "")

    print(style+ "")
    return
          

if __name__ == "__main__":
    main()
