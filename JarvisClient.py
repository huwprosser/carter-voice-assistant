import time
import librosa
import keyboard  # using module keyboard
import threading
import os
from SpeechToText import STT
from VoiceActivityDetection import VADDetector
from pydub import AudioSegment, effects  
from SocketClient import SocketClient

class JarvisClient():
    def __init__(self, startListening=False):
        self.listening = False
        self.vad = VADDetector(self.onSpeechStart, self.onSpeechEnd)
        self.stt = STT(self.done)
        self.socket_client = SocketClient()

        if startListening:
            t = threading.Thread(target=self.vad.startListening)
            t.start()

    def startListening(self):
        t = threading.Thread(target=self.vad.startListening)
        t.start()

    def toggleListening(self):
        self.listening = not self.listening
        print("Listening:", self.listening)

    def done(self):
        # on stt load
        print("done")

    def onSpeechStart(self):
        pass

    def onSpeechEnd(self,path):
        if self.listening:
            audio = AudioSegment.from_wav(path)
            audio = audio + 3
            audio = effects.normalize(audio)  
            audio.export(path, "wav")
            input_audio, _ = librosa.load(path, sr=16000)
            transcription = self.stt.convert(input_audio)
            print(transcription) 
            self.socket_client.send(transcription)

            self.toggleListening()
        
        os.remove(path)

         
jc = JarvisClient(startListening=True)

# pressing enter toggles the listening in a loop
while True:
    if keyboard.is_pressed('enter'):
        jc.toggleListening()
        time.sleep(1)
    time.sleep(0.1)


