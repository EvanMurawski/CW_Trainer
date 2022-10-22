import random

RATIO_2_3 = 0.5
RATIO_2_2 = 0.65
RATIO_2_1 = 0.75
RATIO_1_3 = 0.9
RATIO_1_2 = 0.95
RATIO_1_1 = 1

capital_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generateCallsign():
        
    callsign = ""
    rand = random.uniform(0,1)

    if(rand < RATIO_2_3):
        prefix = 2
        suffix = 3
    elif(rand < RATIO_2_2):
        prefix = 2
        suffix = 2
    elif(rand < RATIO_2_1):
        prefix = 2
        suffix = 1
    elif(rand < RATIO_1_3):
        prefix = 1
        suffix = 3
    elif(rand < RATIO_1_2):
        prefix = 1
        suffix = 2
    else:
        prefix = 1
        suffix = 1

    for j in range(prefix):
        callsign += random.choice(capital_letters)

    callsign += str(random.randint(0,9))

    for j in range(suffix):
        callsign += random.choice(capital_letters)
        
    return callsign
