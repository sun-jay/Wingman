from gpt import gpt
import re
import time


transcript = """
P1: Hello, how are you.
P2: I am fine, thank you.
P1: That's good to hear.
P2: Yes, it is.
P1: What are you up to?
P2: Not much, just relaxing.
P1: Sounds nice, but I have a huge rash on my back.
P2: "Uh, okay."
P1: Well, I have to go now.
P2: Okay, talk to you later.
P1: Bye!
"""

transcript = re.split(r'[.!?]', transcript)
print(len(transcript))
# exit()
texts = []

for i in range(len(transcript)):
    time.sleep(0.5)  
    
    texts.append(transcript[i])
    
    prompt = '''
    Read this conversation and return a single word that will tell us if P1 is making one of the following conversaional mistakes
    1. Talking too much in one turn of conversation : return "TALKING"
    2. Saying something goofy or embarassing: return "GOOFY:
    3. No conversational mistakes: return "NONE"
    '''

    prompt += "".join(texts)

    response = gpt(prompt)

    if response != "NONE":
        texts = []

    print(response)
