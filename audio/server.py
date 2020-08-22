import uuid
import io

from fastapi import FastAPI
from pydantic import BaseModel
import speech_recognition as sr

app = FastAPI()


def recognize(buffer: io.BytesIO, language='ru-RU') -> str:
    '''
    throws: speech_recognition.UnknownValueError, speech_recognition.RequestError
    '''
    r = sr.Recognizer()
    with sr.AudioFile(buffer) as source:
        audio = r.record(source)  # read the entire audio file

    return r.recognize_google(audio, language='ru-RU')


class Item(BaseModel):
    audio: str


@app.post("/recognize")
def read_root(item: Item):
    data = eval(item.audio)

    bytes_io = io.BytesIO(data)

    text = recognize(bytes_io)
    return {'result': text}
