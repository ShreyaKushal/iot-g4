
from fpdf import FPDF
import matplotlib.pyplot as plt
import dataframe_image as dfi
import seaborn as sns
import time
import datetime
import pandas as pd
class PDF(FPDF):
    WIDTH = 210
    HEIGHT = 297

    def setup(self):
        self.df = pd.read_csv('./final_sensor.csv')
        self.df['Time'] = pd.to_datetime(self.df['Time'])

        # Convert the datetime to a more human-readable format
        dateTime = self.df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        self.df['Date'] = dateTime.str.split(' ').str[0]
        self.df['Time'] = dateTime.str.split(' ').str[1]

        self.df['DateTime'] = pd.to_datetime(self.df['Time'])

        self.df.set_index('DateTime',inplace=True)

        self.df.drop(columns=['Time','Date'],inplace=True)
        


    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
    def create_letterhead(self):
        self.image("./resources/letter_head.png", 0, 0, 210)
    def create_title(self,type):
        day_dict = {'one':1,
                    'two' :2,
                    'three' :3}
        
        self.ln(12)
        self.set_font('Helvetica', 'b', 15)  
        self.ln(40)
        self.write(5, "Trend and Problem Analysis")
        self.ln(10)
    # Add date of report
        self.set_font('Helvetica', '', 14)
        self.set_text_color(r=128,g=128,b=128)
        start =   (datetime.datetime.now() - datetime.timedelta(days=day_dict[type])).strftime("%d/%m/%Y")
        today = time.strftime("%d/%m/%Y")
        self.write(4, f'{start} - {today}')
    def write_to_pdf(self,words):
        self.set_text_color(r=0,g=0,b=0)
        self.set_font('Helvetica', '', 10)
        self.write(5, words)
    
    def write_heading_pdf(self,words):
        self.set_text_color(r=0,g=0,b=0)
        self.set_font('Helvetica','b',12)
        self.write(5,words)

    def temperature_trend_analysis(self):
        sns.set_style("whitegrid")

    # Plotting
        fig,axs = plt.subplots(1, 1, figsize=(20, 10))

        red_thresholds = {
        'carbon dioxide': 800,  # ppm
        'temperature': 27,      # Celsius
        'humidity': 65          # Percentage
        }

        # Temperature
        sns.lineplot(data=self.df, x='DateTime', y='temperature', hue='Device Name', ax=axs, ci=None)
        red_threshold_value = red_thresholds['temperature']
        axs.axhline(red_threshold_value, linestyle='-', color='red', label=f'Red Threshold: {red_threshold_value}')
        axs.annotate(f'Red Threshold: {red_threshold_value}', xy=(1, red_threshold_value), xytext=(8, 10),
                    xycoords=('axes fraction', 'data'), textcoords='offset points',
                    verticalalignment='bottom', horizontalalignment='right', color='red')
        axs.set_title('Temperature VS Time')
        axs.set_ylabel('Temperature (°C)')
        plt.savefig('resources/temperature.png', dpi=75, bbox_inches='tight', pad_inches=0)
    def co2_trend_analysis(self):
        

# Plotting
        red_thresholds = {
    'carbon dioxide': 800,  # ppm
    'temperature': 27,      # Celsius
    'humidity': 65          # Percentage
}

# Set the style of seaborn for better visualization
        sns.set_style("whitegrid")

        # Plotting
        fig, axs = plt.subplots(1, 1, figsize=(20, 10))

        # Carbon Dioxide
        sns.lineplot(data=self.df, x='DateTime', y='carbon dioxide', hue='Device Name', ax=axs, ci=None)
        red_threshold_value = red_thresholds['carbon dioxide']
        axs.axhline(red_threshold_value, linestyle='-', color='red', label=f'Red Threshold: {red_threshold_value}')
        axs.annotate(f'Red Threshold: {red_threshold_value}', xy=(1, red_threshold_value), xytext=(8, 10),
                                xycoords=('axes fraction', 'data'), textcoords='offset points',
                                verticalalignment='bottom', horizontalalignment='right', color='red')
        axs.set_title('CO2 VS Time')
        axs.set_ylabel('Carbon Dioxide (ppm)')
        plt.savefig('resources/CO2.png', dpi=75, bbox_inches='tight', pad_inches=0)


    
    def humidity_trend_analysis(self):
        
        red_thresholds = {
            'carbon dioxide': 800,  # ppm
            'temperature': 27,      # Celsius
            'humidity': 65          # Percentage
        }

        # Set the style of seaborn for better visualization
        sns.set_style("whitegrid")

        # Plotting
        fig, axs = plt.subplots(1, 1, figsize=(20, 10))

        # Humidity
        sns.lineplot(data=self.df, x='DateTime', y='humidity', hue='Device Name', ax=axs, ci=None)
        red_threshold_value = red_thresholds['humidity']
        axs.axhline(red_threshold_value, linestyle='-', color='red', label=f'Red Threshold: {red_threshold_value}')
        axs.annotate(f'Red Threshold: {red_threshold_value}', xy=(1, red_threshold_value), xytext=(8, 10),
                                xycoords=('axes fraction', 'data'), textcoords='offset points',
                                verticalalignment='bottom', horizontalalignment='right', color='red')
        axs.set_title('Humidity VS Time')
        axs.set_ylabel('Humidity (%)')
        plt.savefig('resources/Humidity.png', dpi=75, bbox_inches='tight', pad_inches=0)


       

        

    

     
       


        


    
    # Add line break
        





    