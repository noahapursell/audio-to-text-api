import whisper

class AudioToText:
    
    def __init__(self):
        self.model = whisper.load_model('base.en')
        
    def convert_audio_to_text(self, audio_file:str):
        return self.model.transcribe(audio_file)['text']
    