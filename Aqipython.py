#import pyttsx3 and request library
import pyttsx3,requests

engine = pyttsx3.init()

class Audio:
    def __init__(self,engine):
            #voice setup 
            voices = engine.getProperty('voices')
            engine.setProperty('voice',voices[0].id)
            engine.setProperty('rate',145)
            engine.setProperty('volume',1.0)
            
            
            # Asking the user for city name
            self.audio_run('Enter the name of the City for which you want to check the Air quality index')
            self.city_name = input('Enter the name of the City for which you want to check the air quality index :')


            
            # key for API
            self.api_key = 'ff62b27efa22d1c0ef04fec53f87729570a57df2'
            
            # URL 
            self.url = f'https://api.waqi.info/feed/{self.city_name}/?token={self.api_key}'

            self.request_data()

    def request_data(self):
         self.responce = requests.get(self.url)
         self.json_response()

    def json_response(self):
         self.json_data = self.responce.json()

         # AQI 
         self.aqi = self.json_data['data']['aqi']
         self.audio_run(f'The air quality index of {self.city_name} is {self.aqi}')
         print(self.aqi)


    def audio_run(self,command=None):
        engine.say(command)
        engine.runAndWait()

A1 = Audio(engine)
