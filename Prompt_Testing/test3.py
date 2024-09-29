from gpt import gpt
import re
import time

transcripts = [
    """P1: Hey, how's it going?
P2: Pretty good, just finished a workout.
P1: Oh nice, I tried working out yesterday, and i totally benched 350.
P2: Haha, happens to the best of us.
P1: Yeah, well, I felt kind of sick after. Anyway, what's up with you?
P2: Not much, just chilling now.
P1: Oh! Did I ever tell you about that time I got lost in the mall for, like, 3 hours?
P2: Uh, no, you didn’t.
P1: Yeah, it was crazy! I walked in circles, then I found the food court and got a pretzel. Then I found my way out. Then I drove home. Then I went to bed.
P2: That’s... okay?
P1: Anyway, good talk! Catch you later!""",
    
    """P1: Hey, long time no see!
P2: Yeah, it’s been a while. How have you been?
P1: Oh, you know, busy with work and stuff. Also, I spilled coffee on my laptop last week.
P2: Ouch, that sounds rough.
P1: Yeah, it was everywhere, like even in the keyboard. But it still works... mostly.
P2: Well, that’s good at least.
P1: Oh! Did I tell you I started learning the banjo? I mean, I’m pretty bad at it, but...
P2: Banjo? That’s cool, I guess?
P1: Yeah, but my neighbor kind of hates me now.
P2: I can see why... Anyway, I’ve got to go. Talk soon!""",
    
    """P1: Yo! What's up?
P2: Hey! Not much, just finishing up some work.
P1: Oh, work... speaking of which, I had this dream last night where my boss turned into a giant taco.
P2: Uh... okay, interesting dream.
P1: Yeah, super weird, right? Anyway, what are you working on?
P2: Just some reports for tomorrow.
P1: Oh, fun. You know, I once tried to do all my reports the night before, and I stayed up until 4 a.m. 
P2: That sounds... stressful.
P1: Yeah, it was, but I powered through with six cups of coffee!
P2: Wow, impressive... I guess?
P1: Anyway, I’m probably rambling. I’ll let you get back to it."""
]



def parse_transcript(transcript):
    transcript = transcript.replace("...", ".")
    # transcript = re.split(r'[.!?]', transcript)
    transcript = transcript.split("P1")
    transcript = ["P1"+t for t in transcript if len(t) > 1]
    print(len(transcript))
    # exit()
    texts = []

    for i in range(len(transcript)):
        time.sleep(0.3)  
        
        texts.append(transcript[i])

        
        prompt = '''
        Read this conversation turn and return a single word that will tell us if P1 is making one of the following conversaional mistakes
        1. Two or three sentences said by P1 before the other person talks (rambling): return "TALKING"
        2. Saying something goofy or embarassing: return "GOOFY:
        3. No conversational mistakes: return "NONE"

        '''

        prompt += transcript[i]

        response = gpt(prompt, model="gpt-4o-mini")

        # if response != "NONE":
        #     texts = []
        print(transcript[i])
        print(response)

        if response == "NONE":
            return ""
        else:
            return response

for transcript in transcripts[0:]:
    parse_transcript(transcript)
    break