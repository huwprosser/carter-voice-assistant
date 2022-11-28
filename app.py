from yaspin import yaspin
from termcolor import colored
print()
print()
print(colored("Welcome to Carter", 'magenta'))
print(f"Configure your agent at:")
print(colored("https://dashboard.carterapi.com", "blue"))
print()
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
    from modules.Whisper import transcribe
    from modules.VoiceActivityDetection import VADDetector

    mixer.init()
class CarterClient():
    def __init__(self, key, user_id, startListening=False, voice=False, local=False):
       
        print()
        print(f"User ID: {user_id}")
        print(f"Voice Output Enabled: {voice}")
        print(f"Local Voice Recognition Enabled: {local}")

        self.key = key
        self.voice = voice
        self.user_id = user_id
        self.listening = startListening
        self.vad = VADDetector(self.onSpeechStart, self.onSpeechEnd)
        self.vad_data = Queue()
        self.local = local
    
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
                if self.local == False:
                    wav.write('temp.wav', 16000, data)
                    with open('temp.wav', 'rb') as f:
                        wav_bytes = f.read()   
                        encoded = base64.b64encode(wav_bytes).decode('utf-8')
                        self.sendToCarterRaw(encoded)  
                else:
                    text = transcribe(data)
                    self.sendToCarter(text)            

    def playAudio(self, url):
        
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


    def sendToCarterRaw(self, text):      
        # display spinner                
        with yaspin(text="Awaiting Agent...", color="magenta") as spinner:
        
            r = requests.post('https://api.carterapi.com/v0/audio-chat-raw', json={
                'api_key': self.key,
                'audio': text,
                'uuid': self.user_id,
            })
            agent_response = r.json()
            output = agent_response['output']

            print(colored(agent_response['input'], 'grey'))
            print(colored(output['text'], 'magenta'))

            if self.voice and 'voice' in output:
                self.playAudio(output['voice'])

    def sendToCarter(self, text):      

        print(text,flush=True)
        # send request
        r = requests.post('https://api.carterapi.com/v0/chat', json={
            'api_key': self.key,
            'query': text,
            'uuid': self.user_id,
        })

        agent_response = r.json()
        output = agent_response['output']
        
        print(colored(f"🤖: {agent_response['input']}", 'gray'))
        print(colored(output['text'], 'violet'))

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
