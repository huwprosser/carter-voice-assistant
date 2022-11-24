import os
import time
import requests
import threading
from queue import Queue
from pygame import mixer
from modules.Whisper import transcribe
from modules.VoiceActivityDetection import VADDetector

mixer.init()
class CarterClient():
    def __init__(self,  key, user_id, startListening=False, voice=False):
        self.key = key
        self.voice = voice
        self.user_id = user_id
        self.listening = startListening
        self.vad = VADDetector(self.onSpeechStart, self.onSpeechEnd)
        self.vad_data = Queue()
       
        if startListening:
            self.startListening()

            t = threading.Thread(target=self.transcription_loop)
            t.start()

    def startListening(self):
        print("Listening...")
        t = threading.Thread(target=self.vad.startListening)
        t.start()

    def toggleListening(self):
        while not self.vad_data.empty():
            self.vad_data.get()
        print("Not Listening..." if self.listening else "Listening...")
        self.listening = not self.listening

    def onSpeechStart(self):
        pass

    def onSpeechEnd(self, data):
        if data.any():
            self.vad_data.put(data)

    def transcription_loop(self):
        while True:
            if not self.vad_data.empty():
                print("Transcribing...")
                data = self.vad_data.get()
                if self.listening:
                    self.toggleListening()
                    text = transcribe(data)
                    self.sendToCarter(text)                   

    def playAudio(self, url):
        
        # download from url
        print("Downloading audio...", flush=True)
        r = requests.get(url, stream=True)
        with open('temp.mp3', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    
                
        mixer.music.load('temp.mp3')

        mixer.music.play()
        
        # wait four duration of audio plus one second
        duration = mixer.Sound('temp.mp3').get_length()
        time.sleep(duration + 1)
        mixer.music.unload()
        os.remove('temp.mp3')
        self.toggleListening()


    def sendToCarter(self, text):      

        print(text,flush=True)
        # send request
        r = requests.post('http://localhost:5000/v0/chat', json={
            'api_key': self.key,
            'query': text,
            'uuid': self.user_id,
        })

        agent_response = r.json()
        output = agent_response['output']
        print(output['text'])

        if self.voice and 'voice' in output:
            self.playAudio(output['voice'])
        

if __name__ == "__main__":

    print("Carter Voice Client Starting...")

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-k", "--key", help="API KEY")
    parser.add_argument("-v", "--voice", help="Activate voice", default=False)

    jc = CarterClient(
        startListening=True, 
        key=parser.parse_args().key,
        voice=parser.parse_args().voice, 
        user_id='1234')
