from yaspin import yaspin
from termcolor import colored
print()
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

        
with yaspin(text="Waking agent...") as spinner:
    import os
    import time
    import requests
    import base64
    import threading
    import scipy.io.wavfile as wav
    from queue import Queue
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    from pygame import mixer
    from VoiceActivityDetection import VADDetector

    mixer.init()
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
        print()
        print(colored("Listening...", 'green'))
        print()
        t = threading.Thread(target=self.vad.startListening)
        t.start()

    def toggleListening(self):
        if not self.listening:
            print()
            print(colored("Listening...", 'green'))

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
              

    def playAudio(self, audioURL):

        r = requests.get(audioURL, stream=True)
        with open('temp.mp3', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    
        # play audio
        mixer.music.load('temp.mp3')
        mixer.music.play()

        # wait for audio to finish
        duration = mixer.Sound('temp.mp3').get_length()
        time.sleep(duration + 1)

        # unload and delete audio
        mixer.music.unload()
        os.remove('temp.mp3')

        # re-activate microphone
        self.toggleListening()

        return duration


    def sendToCarterRaw(self, text):      
        # display spinner                
        with yaspin(text="One moment, thinking...", color="magenta") as spinner:
        
            r = requests.post('https://api.carterlabs.ai/chat', json={
                'key': self.key,
                'audio': text,
                'playerId': self.user_id,
            })
            print(r)
            agent_response = r.json()
            print(agent_response)
            output = agent_response['output']
            
            print()
        print(colored(agent_response['input'], 'dark_grey'))
        print(colored(output['text'], 'magenta'))
            
        self.playAudio(output['audio'])
        
    def getOpener(self):      
        # display spinner           
        # self.toggleListening()     
        with yaspin(text="Loading", color="magenta") as spinner:
        
            r = requests.post('https://api.carterlabs.ai/opener', json={
                'key': self.key,
                'playerId': self.user_id,
            })
            agent_response = r.json()
            print(agent_response)
            output = agent_response['output']
            
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
