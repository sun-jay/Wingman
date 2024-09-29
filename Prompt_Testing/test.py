from gpt import gpt
import re
import time
from pydantic import BaseModel


transcript = """
P1: What are you up to?
P2: Not much, just relaxing.
P1: Sounds nice, but I have a huge rash on my back.
P2: "Uh, okay."
P1: Hey this totally reminds me of the time I went to cal hacks and I totally clapped everyone there. My project was so good that I 
P2: Okay, talk to you later.
P1: Bye!
"""

class BackAndForth(BaseModel):
    person1: str
    person2: str
    analysis: str | None

    def __str__(self):
        return f"P1: {self.person1}\nP2: {self.person2}\nAnalysis: {self.analysis}\n"


transcript = [
    BackAndForth(person1="What are you up to?", person2="Not much, just relaxing.", analysis=None),
    BackAndForth(person1="Sounds nice, but I have a huge rash on my back.", person2="Uh, okay.", analysis="GOOFY"),
]

# transcript = re.split(r'[.!?]', transcript)
print(len(transcript))


for i in range(len(transcript)):
    # time.sleep(0.5)
    input()
    # old_texts.append(transcript[i])
    new_texts.append(transcript[i])

    # time.sleep(0.5)  
    
    # texts.append(transcript[i])
    
    new_line = '\n'
    prompt = f'''You are a helpful assistant that will analyze the following conversation between two people, P1 and P2.


Converation History:
{new_line.join({str(turn) for turn in old_texts})}

The following is the turn of conversation that you should analyze


'''



    print(prompt)
    # response = gpt(prompt)


    if response != "NONE":

        old_texts += new_texts
        new_texts = []

    print(response)


# /opt/homebrew/bin/python3.11 test.py