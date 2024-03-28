
from fpdf import FPDF
import matplotlib.pyplot as plt
import dataframe_image as dfi
import seaborn as sns
import time
import datetime
import pandas as pd
import base64
import requests
import glob
import os
from dotenv import load_dotenv
class PDF(FPDF):
    WIDTH = 210
    HEIGHT = 297
    CHATGPT_API_KEY  = ""

    def setup(self):
        self.df = pd.read_csv('./final_sensor.csv')
        load_dotenv()

# Access environment variables
        PDF.CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
        
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
    def encode_image_to_base64(self,image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    def analysis(self,image_path,question):
        

        encoded_image =self.encode_image_to_base64(image_path)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PDF.CHATGPT_API_KEY}"
            }

        question_about_plots = question

        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {"type": "text", "text": question_about_plots}
            ] + [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}} 
            ]
            }
        ],
        "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        return response.json()['choices'][0]['message']['content']
    def analyse_list_images(self):

        image_paths = glob.glob('./resources/air_quality_plots/*.png')
        encoded_images = [self.encode_image_to_base64(path) for path in image_paths]
          # Replace this with your actual API key

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PDF.CHATGPT_API_KEY}"
        }

        question_about_plots = "What trends are observed across these plots? What are some suggestions of action for the management to take to improve the overall indoor air quality?"

        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {"type": "text", "text": question_about_plots}
            ] + [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}} for img in encoded_images
            ]
            }
        ],
        "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return response.json()['choices'][0]['message']['content']


    
    def classify_air_quality(self,co2, temperature, humidity):
        thresholds = {
            'CO2': 800,  
            'temperature': 27,  
            'humidity': 65  
        }
        
        co2_status = 1 if co2 > thresholds['CO2'] else 0
        temperature_status = 1 if temperature > thresholds['temperature'] else 0
        humidity_status = 1 if humidity > thresholds['humidity'] else 0
        
        air_quality_status = f"{co2_status}{temperature_status}{humidity_status}"
        
        quality_mapping = {
            "000": "Good 🙂",
            "001": "moderate low",
            "010": "moderate low",
            "100": "moderate low",
            "011": "moderate high",
            "101": "moderate high",
            "110": "moderate high",
            "111": "Bad"
        }
        return quality_mapping.get(air_quality_status, "Unknown Status")
    def classify_air_quality_row(self,row):
        return self.classify_air_quality(row['carbon dioxide'], row['temperature'], row['humidity'])
        
       

    def ambient_air_setup(self):
        self.df['Air Quality Rating'] = self.df.apply(self.classify_air_quality_row, axis=1)
    def plot_pie_chart(self):
        count =1
        plt.figure(figsize=(3,3))
        unique_devices = self.df['Device Name'].unique()
        device_dfs = [self.df[self.df['Device Name'] == device] for device in unique_devices]
        for device_df in device_dfs:
            device_df = device_df.reset_index().drop_duplicates(subset='DateTime')
            device_df = device_df.set_index('DateTime')
            device_name = device_df['Device Name'].iloc[0]
            
            plt.figure(figsize=(3, 3))
            device_df['Air Quality Rating'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
            plt.title(f'Air Quality Rating Distribution for {device_name}')
            plt.gcf().set_size_inches(3, 3)
            plt.legend([])  # Clear the legend
            plt.ylabel('')  # Clear the ylabel
            plt.savefig(f'resources/piecharts/{count}.png', dpi=75, bbox_inches='tight', pad_inches=0)
            plt.close()  # Close the figure to prevent accumulation
            count += 1
    def plot_time_chart(self):
        count =1
       
        self.df['Hour'] = self.df.index.floor('H') 

        unique_devices = self.df['Device Name'].unique()

        device_dfs = [self.df[self.df['Device Name'] == device] for device in unique_devices]
        for device_df in device_dfs:
            device_df = device_df.reset_index().drop_duplicates(subset='DateTime')
            device_df = device_df.set_index('DateTime')
            device_name = device_df['Device Name'].iloc[0]
            device_df.groupby('Hour')['Air Quality Rating'].value_counts().unstack().plot(kind='bar', stacked=False, figsize=(20, 10))
            
            plt.title(f'Air Quality Rating vs Hour for {device_name}')
            plt.ylabel('Count')
            plt.tight_layout()
            
          
            plt.savefig(f'resources/air_quality_plots/{count}.png', dpi=75, bbox_inches='tight', pad_inches=0)
            plt.close()  # Close the figure to prevent accumulation
            count += 1

           
        


        



       

        

    

     
       


        


    
    # Add line break
        





    