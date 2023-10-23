#import pyttsx3 and request library
import pyttsx3,requests,json
engine = pyttsx3.init()

class Audio:
          def __init__(self,engine):
                    #voice setup 
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice',voices[1].id)
                    engine.setProperty('rate',149)
                    engine.setProperty('volume',1.0)
                    self.request_data()
                    self.pm = None
                    
          def request_data(self):
               try:
                    # Asking the user for city name
                    self.audio_run('Enter the name of the City for which you want to check the Air quality index')
                    self.city_name = str(input('Enter the name of the City for which you want to check the air quality index :'))

                     # key for API
                    self.api_key = 'ff62b27efa22d1c0ef04fec53f87729570a57df2'
                    
                    # URL 
                    self.url = f'https://api.waqi.info/feed/{self.city_name}/?token={self.api_key}'

                    
                    self.responce = requests.get(self.url)
                    with open('D:\Projects\AQI\data.json','w') as data_file:
                             data_file.write(str(self.responce.text))
                    self.json_response()
               except ValueError as err:
                      self.audio_run(err)
                      print(err)
                      self.request_data()

          def json_response(self):
               self.json_data = self.responce.json()
               try:
                      
                    # AQI 
                    self.aqi = self.json_data['data']['aqi']
                    self.details = self.json_data['data']['city']['name']
                    self.audio_run(f'The air quality index of {self.city_name} is {self.aqi}')
                    print(f'The AQI is {self.aqi} pm2.5')
                    print(f'{self.details}')

                    try:
                           
                         #  Atmospheric particulate matter (PM) 
                         self.pm = self.json_data['data']['iaqi']['pm10']['v']
                         self.audio_run(f'The  atmospheric particulate matter (PM) of {self.city_name} is {self.pm} pm10')
                         print(f'The AQI is {self.pm} pm10')
                    except:
                           pass
                         # Ozone 
                    self.o3 = self.json_data['data']['iaqi']['o3']['v']
                    self.audio_run(f'The o3 levels are {self.o3}')
                    print(f'The o3 levels are {self.o3}')
               except TypeError or ValueError as err1:
                      self.audio_run(f'Somthing went wrong')
                      print(err1)
                      self.request_data()

          def audio_run(self,command=None):
               engine.say(command)
               engine.runAndWait()
     
A1 = Audio(engine)
