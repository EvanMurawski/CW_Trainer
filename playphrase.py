import winsound
import time
DAH_PATH = r'.\Dah_D5_15WPM.wav'
DIT_PATH = r'.\Dit_D5_15WPM.wav'



def playPhrase(phrase, dit_time, dah_time, letterDict):

    
    letterDictInv = {v: k for k, v in letterDict.items()}


    for letter in phrase:

        if letter == " ":
            time.sleep(dit_time * 7)
            continue
        
        characters = letterDictInv.get(letter)

        for character in characters:

            if character == "i":
                winsound.PlaySound(DIT_PATH, winsound.SND_ASYNC)
                time.sleep(dit_time + dit_time)
            elif character == "a":
                winsound.PlaySound(DAH_PATH, winsound.SND_ASYNC)
                time.sleep(dit_time + dah_time)
            else:
                time.sleep(dit_time + dah_time)

        time.sleep(dit_time*2)

    time.sleep(dit_time * 4)

        


