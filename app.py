import os
import time
import requests
import base64
import threading
import scipy.io.wavfile as wav
from io import BytesIO
from queue import Queue
from pygame import mixer
from yaspin import yaspin
from termcolor import colored
from pydub import AudioSegment
from VoiceActivityDetection import VADDetector

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
mixer.init()

print(colored("""
                             dP                     
                             88                     
.d8888b. .d8888b. 88d888b. d8888P .d8888b. 88d888b. 
88'  `"" 88'  `88 88'  `88   88   88ooood8 88'  `88 
88.  ... 88.  .88 88         88   88.  ... 88       
`88888P' `88888P8 dP         dP   `88888P' dP                                         
""", 'magenta'))

print(colored("https://carterlabs.ai", "light_grey"))
print()


class CarterClient():
    def __init__(self, key, user_id, startListening=True):
        self.key = key
        self.user_id = user_id
        self.listening = False
        self.vad = VADDetector(self.onSpeechStart, self.onSpeechEnd, sensitivity=.5)
        self.vad_data = Queue()
    
        if startListening:
               
            self.getOpener()  
            self.startListening()
            t = threading.Thread(target=self.transcription_loop)
            t.start()  


    def startListening(self):
        t = threading.Thread(target=self.vad.startListening)
        t.start()

    def toggleListening(self):
        if not self.listening:
            print()
            print(colored(f"{self.name} is listening...", 'green'))

        while not self.vad_data.empty():
            self.vad_data.get()
            
        self.listening = not self.listening

    def onSpeechStart(self):
        pass

    def onSpeechEnd(self, data):
        if data.any():
            self.vad_data.put(data)

    def transcription_loop(self):
        while True:
            if not self.vad_data.empty():
                data = self.vad_data.get()
                if self.listening and len(data) > 14000:
                   
                    self.toggleListening()
                
                    wav.write('temp.wav', 16000, data)
                    with open('temp.wav', 'rb') as f:
                        wav_bytes = f.read()   
                        encoded = base64.b64encode(wav_bytes).decode('utf-8')
                        self.sendToCarterRaw(encoded)      

    def speak(self, text):
        r = requests.post('https://api.carterlabs.ai/speak', json={
            'key': self.key,
            'text': text,
            'playerId': self.user_id,
            'voice_id': 'female'
        })
        agent_response = r.json()
        output = agent_response['file_url']

        # play audio
        self.playAudio(output)

    def playAudio(self, audioURL):

        # retrive the audio file
        r = requests.get(audioURL)
                    
        # play audio
        audio_data = AudioSegment.from_file(BytesIO(r.content)).export(format='wav')

        audio = mixer.Sound(audio_data)
        audio.play()

        # wait for audio to finish
        duration = audio.get_length()
        time.sleep(duration + 1)

        # unload and delete audio
        # mixer.music.unload()

        # re-activate microphone
        self.toggleListening()

        return duration

    def sendToCarterRaw(self, text):      
        # display spinner                
        wait_text = "One moment, thinking..." if self.name is None else f"{self.name} is typing..."
        with yaspin(text=wait_text, color="magenta") as spinner:
        
            r = requests.post('https://api.carterlabs.ai/chat', json={
                'key': self.key,
                'audio': text,
                'playerId': self.user_id
            })
            agent_response = r.json()
            output = agent_response['output']
            
        # print what the user said
        print(colored(agent_response['input'], 'dark_grey'))

        # print what the agent said
        print(colored(output['text'], 'magenta'))
            
        self.speak(output['text'])
        
    def getOpener(self):          
        with yaspin(text="Waking agent...", color="magenta") as spinner:
        
            r = requests.post('https://api.carterlabs.ai/opener', json={
                'key': self.key,
                'playerId': self.user_id,
                '
            })
            agent_response = r.json()
            output = agent_response['output']

            self.name = agent_response['agent']['name']
            
        print(colored(output['text'], 'magenta'))
            
        self.playAudio(output['audio'])

       


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-k", "--key", help="API KEY")
    parser.add_argument("-u", "--user", help="USER_ID")

    if parser.parse_args().key is None:
        print(colored("No API key provided. Please provide an API key with the -k flag.", 'red'))
        exit()
    jc = CarterClient(
        startListening=True, 
        key=parser.parse_args().key,
        user_id=parser.parse_args().user)
