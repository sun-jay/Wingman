from gpt import gpt
import re
import time
from openai import OpenAI
import io
import base64
from PIL import Image
import os
import dotenv
import numpy as np

dotenv.load_dotenv()

def gpt(prompt, images = [], model = "gpt-4o-mini"):
    # print("GPT CALLED")
    # return ["Yes", "No"]
    """
    Creates a chat completion using the OpenAI API, with a prompt and an array of images.

    Args:
        prompt (str): The text prompt to send to the API.
        images (list): A list of PIL Image objects.

    Returns:
        dict: Response object from the OpenAI API call.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Start constructing the content
    content = [
        {
            "type": "text",
            "text": prompt
        }
    ]

    # For each image, encode it as a data URL and add to the content
    for image in images:
        # Encode the image as a data URL
        data_url = encode_image_as_data_url(image)
        # Add the data URL to the content
        content.append({
            "type": "image_url",
            "image_url": {"url": data_url}
        })

    # Construct the messages
    messages = [
        {
            "role": "user",
            "content": content
        }
    ]

    # Make the API call
    response = client.chat.completions.create(
        model= model,
        messages=messages,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )

    return response.choices[0].message.content

def encode_image_as_data_url(image):
    """
    Encodes a PIL image as a data URL.

    Args:
        image (PIL.Image.Image): The image to encode.

    Returns:
        str: The data URL of the image.
    """
    # Convert the image to bytes
    img_byte_arr = io.BytesIO()
    # Default to 'PNG' if image format is not set
    image_format = image.format if image.format else 'PNG'
    image.save(img_byte_arr, format=image_format)
    img_bytes = img_byte_arr.getvalue()

    # Encode the image bytes to base64
    base64_encoded = base64.b64encode(img_bytes).decode('utf-8')

    # Construct the data URL
    mime_type = f"image/{image_format.lower()}"
    data_url = f"data:{mime_type};base64,{base64_encoded}"

    return data_url


# transcript = """
# Person 1: Hello, how 
# Person 1: are you.
# Person 2: I am fine,
# Person 2: thank you.
# Person 1: That's good to hear.
# Person 2: Yes, it is.
# Person 1: What are you up to?
# Person 2: Not much, just relaxing.
# Person 1: Sounds nice, but I have a huge rash on my back.
# Person 2: "Uh, okay."
# Person 1: Oh also, I forgot to tell you about how I won at Cal Hacks. 
# Person 1: I went there with an awesome team and totally blew everyone away. 
# Person 1: We won first place and 2 thousand dollars.
# Person 1: We celebrated by going to the beach after. Then we went to a party.
# Person 2: Okay, talk to you later.
# Person 1: Bye!
# """
transcript = """
Person 1: Hey, how's it going?
Person 2: I'm good, how about you?
Person 1: I'm doing well, just got back from a crazy week at college.
Person 2: Oh really? What happened?
Person 1: Well, first, I slept through my alarm and missed my morning class. I was so embarrassed.
Person 1: Then, later in the week, I had a massive group project due, and everyone was freaking out.
Person 1: We had to pull an all-nighter to finish it on time.
Person 1: But, somehow, we managed to get an A on it!
Person 1: I couldn’t believe it. It was so crazy. Honestly, I'm still recovering from it. 
Person 2: Yikes, did you manage to finish it?
Person 1: Barely! We pulled an all-nighter, but we actually got an A! I couldn’t believe it.
Person 2: That’s awesome, congrats! So, how did you celebrate?
Person 1: Oh, we went to the campus food truck, had way too many tacos, and then just crashed afterward.
Person 2: Haha, sounds like a typical college night.
Person 1: Pretty much! Anyway, what's new with you?
"""


context = []

def parse(sentence, context_len = 5):
    if not sentence.startswith("Person 1") or sentence.startswith("person 1"):
        return ""
    
    context_string = "\n".join(context[-context_len:])

    directions = '''
        Read this conversation and return a single word that will tell us if P1 is making one of the following conversaional mistakes
        1. Three or four sentences said by P1 before the other person talks : return "TALKING"
        2. Saying something embarassing: return "GOOFY:
        3. No conversational mistakes: return "NONE"

        '''
    
    prompt = directions + context_string + '\n' + sentence

    response = gpt(prompt)

    # print(response)
    print(sentence)

    if response == "NONE":
        return ""
    else:
        return response

lines = transcript.split("\n")

for line in lines:
    time.sleep(0.5)
    print(parse(line))
