from yaspin import yaspin
from termcolor import colored
print()
print()
print(colored("""
                 _            
                | |           
   ___ __ _ _ __| |_ ___ _ __ 
  / __/ _` | '__| __/ _ \ '__|
 | (_| (_| | |  | ||  __/ |   
  \___\__,_|_|   \__\___|_|   
                              
                              
""", 'magenta'))
print(f"Configure your agent at:")
print(colored("https://controller.carterlabs.ai", "blue"))
print()
print()

        
with yaspin(text="Waking agent...") as spinner:
    import os
    import time
    import requests
    import urllib.parse
    import base64
    import threading
    import scipy.io.wavfile as wav
    from queue import Queue
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    from pygame import mixer
    from VoiceActivityDetection import VADDetector

    mixer.init()
class CarterClient():
    def __init__(self, key, user_id, startListening=False):
       
        print()
        print(f"User ID: {user_id}")

        self.key = key
        self.user_id = user_id
        self.listening = startListening
        self.vad = VADDetector(self.onSpeechStart, self.onSpeechEnd)
        self.vad_data = Queue()
    
        if startListening:
            self.startListening()

            t = threading.Thread(target=self.transcription_loop)
            t.start()        

    def startListening(self):
        print(colored("Listening 👂", 'green'))
        t = threading.Thread(target=self.vad.startListening)
        t.start()

    def toggleListening(self):
        if not self.listening:
            print()
            print(colored("Listening 👂", 'green'))

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
                if self.listening:
                    self.toggleListening()
                
                    wav.write('temp.wav', 16000, data)
                    with open('temp.wav', 'rb') as f:
                        wav_bytes = f.read()   
                        encoded = base64.b64encode(wav_bytes).decode('utf-8')
                        self.sendToCarterRaw(encoded)      
              

    def playAudio(self, text):

        url_safe_text = urllib.parse.quote(text)
        r = requests.get(f'https://api.carterlabs.ai/speak/female/{url_safe_text}/abc123')
        url = r.json()['file_url']

        # download from url
        r = requests.get(url, stream=True)
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
        with yaspin(text="Awaiting Agent...", color="magenta") as spinner:
        
            r = requests.post('https://api.carterlabs.ai/chat', json={
                'key': self.key,
                'audio': text,
                'playerId': self.user_id,
            })
            agent_response = r.json()
            output = agent_response['output']
            
            print()
            print(colored(agent_response['input'], 'grey'))
            print(colored(output['text'], 'magenta'))
            
            self.playAudio(output['text'])

if __name__ == "__main__":

    print("One moment...")

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-k", "--key", help="API KEY")

    if parser.parse_args().key is None:
        print(colored("No API key provided. Please provide an API key with the -k flag.", 'red'))
        exit()
    jc = CarterClient(
        startListening=True, 
        key=parser.parse_args().key,
        user_id='1234')
