#import pyttsx3 and request library
import pyttsx3,requests
from matplotlib import pyplot as plt
engine = pyttsx3.init()

class Air_quality:
          def __init__(self,engine):
                    #voice setup 
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice',voices[1].id)
                    engine.setProperty('rate',147)
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
              #       with open('D:\Projects\AQI\data.json','w') as data_file:
              #                data_file.write(str(self.responce.text))
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
                    try:
                            # Ozone
                     self.o3 = self.json_data['data']['iaqi']['o3']['v']
                     self.audio_run(f'The o3 levels are {self.o3}')
                     print(f'The o3 levels are {self.o3}')
                    except:
                          self.audio_run(f'Real time o3 levels are not avilable for this city')
               except TypeError or ValueError as err1:
                      self.audio_run(f'Somthing went wrong')
                      print(err1)
                      self.request_data()

          def audio_run(self,command=None):
               engine.say(command)
               engine.runAndWait()
     

class Processing_data(Air_quality):
     def __init__(self):
          super().__init__(engine)
          self.audio_run(' Description of the Response')
          
          #callinng the description function 
          self.description()

     def description(self):
          if self.aqi >= 0 and self.aqi <= 50:
                 self.audio_run('Air quality is satisfactory and poses litle or no risk')
          elif self.aqi >= 51 and self.aqi <= 100:
                 self.audio_run('Sensitive individual should avoid outdoor activity as they may experience respiratory symptoms')
          elif self.aqi >= 101 and self.aqi <= 150:
                 self.audio_run('General public and sensitive individuals in particular are at risk to experience irritation and respiratory problems')
          elif self.aqi >= 151 and self.aqi <= 200:
                 self.audio_run('Increased likelihood of adverse effects and aggravation to the heart and lungs among general public.')
          elif self.aqi >= 201 and self.aqi <= 300:
                 self.audio_run('General public will be noticebly affected sensitive groups should restrict outdoor activities.')
          else:
                 self.audio_run('General public at high risk of experiencing strong irritations and adverse health effects Should avoid outdoor activities.')
          
          # calling the graph function 
          self.graph()

     def graph(self):
            try:
              # Graph for air quality monitoring pm25
              self.audio_run('Presenting graph for forecast analysis of Air Quality index data')
              aqi_data = self.json_data["data"]["forecast"]["daily"]["pm25"]
              # Extract the days and average AQI values
              days = [item["day"] for item in aqi_data]
              avg_aqi_values = [item["avg"] for item in aqi_data]
              # Plot the data
              plt.plot(days, avg_aqi_values)
              plt.xlabel('Day')
              plt.ylabel('Average AQI')
              plt.title('Average AQI over Time')
              # Rotate x-axis labels
              plt.xticks(rotation=45)
              plt.show()   
            except:
                  pass
            
            try:
              # Graph for ozone monitoring o3
              self.audio_run('Presenting graph for forecast analysis of Ozonel data')
              o3_data = self.json_data["data"]["forecast"]["daily"]["o3"]
              # Extract the days and average AQI values
              days = [item["day"] for item in o3_data]
              avg_o3_values = [item["avg"] for item in o3_data]
              # Plot the data
              plt.plot(days, avg_o3_values)
              plt.xlabel('Day')
              plt.ylabel('Average O3 level')
              plt.title('Average O3 levels over Time')
              # Rotate x-axis labels
              plt.xticks(rotation=45)
              plt.show()   
            except:
                  pass
                  


              
if __name__ == '__main__':
       while True:                 
              P1 = Processing_data()

              #asking user for exit
              choice = input(f'Enter 1 for exit else press any key to continue : ')
              if choice == '1':
                     break
              else:
                     pass
