import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2CTCTokenizer, AutoFeatureExtractor

class STT():
    def __init__(self, onLoad):
        self.model_name = "facebook/wav2vec2-base-960h"
        self.tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(self.model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name)
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
        if onLoad:
            onLoad()

    def convert(self, audio):
        input_values =  self.feature_extractor(audio, return_tensors="pt", sampling_rate=16000).input_values
        # convert to Double
        input_values = input_values.type(torch.FloatTensor)
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        return self.tokenizer.batch_decode(predicted_ids)[0]
