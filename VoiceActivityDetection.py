import sys
import time
import wave
import webrtcvad
import contextlib
import collections
import numpy as np # required to avoid crashing in assigning the callback input which is a numpy object
import sounddevice as sd

class VADDetector():
    def __init__(self, onSpeechStart, onSpeechEnd):
        self.channels = [1]
        self.mapping  = [c - 1 for c in self.channels]
        self.device_info = sd.query_devices(None, 'input')
        self.sample_rate = 16000 # int(self.device_info['default_samplerate'])
        self.interval_size = 10 # audio interval size in ms
        self.sensitivity = .5 #Seconds
        self.block_size = self.sample_rate * self.interval_size / 1000
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(2)
        self.frameHistory = [False]
        self.block_since_last_spoke = 0
        self.onSpeechStart = onSpeechStart
        self.onSpeechEnd = onSpeechEnd
        self.voiced_frames = collections.deque(maxlen=1000)

    def write_wave(self, path, audio, sample_rate):
        with contextlib.closing(wave.open(path, 'w')) as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframesraw(audio)
        
    def voice_activity_detection(self, audio_data):
        return self.vad.is_speech(audio_data, self.sample_rate)

    def audio_callback(self, indata, frames, time, status):        

        if status:
            print(F"underlying audio stack warning:{status}", file=sys.stderr)

        assert frames == self.block_size
        audio_data = indata
        audio_data = map(lambda x: (x+1)/2, audio_data) 
        audio_data = np.fromiter(audio_data, np.float16)
        audio_data = audio_data.tobytes()

        detection = self.voice_activity_detection(audio_data)

        # Write the bytes to the byte array when speech detected

        if(self.frameHistory[-1] == True and detection == True):
            self.onSpeechStart()
            self.voiced_frames.append(audio_data)
            self.block_since_last_spoke = 0
        else:
            if(self.block_since_last_spoke == self.sensitivity * 10 * self.interval_size):
                path = 'chunk-%002d.wav' % (len(self.frameHistory),)
                samp = b''.join(self.voiced_frames)
                self.write_wave(path, samp, self.sample_rate)
                self.onSpeechEnd(path)
                self.voiced_frames = []
            else:
                # if last block was not speech don't add
                if len(self.voiced_frames) > 0:
                    self.voiced_frames.append(audio_data)
            
            self.block_since_last_spoke += 1

        self.frameHistory.append(detection)


    def startListening(self):
        with sd.InputStream(
            device=None,  # the default input device
            channels=1,
            samplerate=self.sample_rate,
            blocksize=int(self.block_size),
            callback=self.audio_callback):

            # avoid shutting down for endless processing of input stream audio
            while True:
                time.sleep(0.1)  # intermittently wake up


if __name__ == "__main__":
    def onSpeechStart():
        print("Speech started")

    def onSpeechEnd(path):
        print("Speech ended")
        print(f"Saved to {path}")
    
    vad = VADDetector(onSpeechStart, onSpeechEnd)
    vad.startListening()