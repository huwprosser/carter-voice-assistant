import os
import requests
import warnings
import threading
from playsound import playsound
from modules.SpeechToText import STT
from modules.VoiceActivityDetection import VADDetector

# Supress PyAudio warning if you don't have ffmeg installed:
warnings.filterwarnings("ignore")

class CarterClient():
    def __init__(self,  key, user_id, startListening=False, voice=False):
        self.key = key
        self.voice = voice
        self.user_id = user_id
        self.listening = startListening
        self.vad = VADDetector(self.onSpeechStart, self.onSpeechEnd)
        self.stt = STT(self.done)

        if startListening:
            print("Listening...")
            t = threading.Thread(target=self.vad.startListening)
            t.start()

    def startListening(self):
        t = threading.Thread(target=self.vad.startListening)
        t.start()

    def toggleListening(self):
        self.listening = not self.listening

    def done(self):
        print("done")

    def onSpeechStart(self):
        pass

    def onSpeechEnd(self, data):
        if self.listening and data.any():
            self.toggleListening()
            transcription = self.stt.convert(data)
            
            if len(transcription) > 1:
                print("You: ", transcription)
                self.sendToCarter(transcription)
            
            print("\n\nListening...")
            self.toggleListening();

    def playAudio(self, url):
        
        # download from url
        r = requests.get(url, stream=True)
        with open('temp.mp3', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    
        playsound('temp.mp3')           
        # remove temp file
        os.remove('temp.mp3')

    
    def sendToCarter(self, text):
        print("Waiting for agent to respond...")
        r = requests.post('https://api.carterapi.com/v0/chat', json={
            'api_key': self.key,
            'query': text,
            'uuid': self.user_id,
        })

        agent_response = r.json()
        output = agent_response['output']
        print("Agent: " , output['text'])

        if self.voice and 'voice' in output:
            self.playAudio(output['voice'])


if __name__ == "__main__":

    print("Carter Voice Client Starting...")
    print("Loading voice models. This may take a second...")

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-k", "--key", help="API KEY")
    parser.add_argument("-v", "--voice", help="Activate voice", default=False)

    jc = CarterClient(
        startListening=True, 
        key=parser.parse_args().key,
        voice=parser.parse_args().voice, 
        user_id='1234')

    

# TO DO
# remove need for saving wav by converting form bytes into np array
# cleanup everything
# add to server