import os
import aiohttp
import threading
import json
import websockets
import asyncio

URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"
API_KEY = "70df636016519322537185557f1f8735884cb40b"

DEEPGRAM_URL = f"wss://api.deepgram.com/v1/listen?punctuate=true&model=nova-2&language=en-US&diarize=true&interim_results=false&smart_format=true"

async def transcribe():
    async with websockets.connect(DEEPGRAM_URL, extra_headers={"Authorization": f"Token {API_KEY}"}) as ws:
        
        print(f"Connected to Deepgram. Request ID: {ws.response_headers.get('dg-request-id')}")

        async def receiver():
            async for message in ws:
                response = json.loads(message)
                words = response.get("channel", {}).get("alternatives", [{}])[0].get("words", [])
                speaker_transcripts = {}
                
                # Group words by speaker
                for word_info in words:
                    speaker = word_info.get("speaker", 0)
                    word = word_info.get("punctuated_word", "")
                    if speaker not in speaker_transcripts:
                        speaker_transcripts[speaker] = []
                    speaker_transcripts[speaker].append(word)

                # Print sentences grouped by speaker
                for speaker, transcript in speaker_transcripts.items():
                    sentence = " ".join(transcript)
                    print(f"Speaker {speaker}: {sentence}")

        
        async def sender():
            async with aiohttp.ClientSession() as session:
                async with session.get(URL) as audio_stream:
                    async for data in audio_stream.content.iter_any():
                        await ws.send(data)
        
        await asyncio.gather(sender(), receiver())

def main():
    try:
        asyncio.run(transcribe())
    except Exception as e:
        print(f"Could not open socket: {e}")
        return

if __name__ == "__main__":
    main()
