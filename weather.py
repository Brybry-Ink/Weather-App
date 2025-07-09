import pandas as pd  # table manipulation
import plotly.express as px  # data visualization
from datetime import datetime
import pyowm
import streamlit as st
from matplotlib import dates
from matplotlib import pyplot as plt
import numpy as np


# streamlit run weather.py
# sometimes for windows: python -m streamlit run weather.py


# Use streamlit secrets to fetch the secret ApiKey.
api_key = st.secrets["api_key"]


sign = u"\N{DEGREE SIGN}"
owm = pyowm.OWM(api_key)
mgr = owm.weather_manager()


st.markdown("<h1 style='text-align: center;'>Weather Forecast</h1>", unsafe_allow_html=True)
# st.write("## Made by Bryan")
st.write("##")


st.write("#### Enter the city name, choose a Temperature unit and a graph")


location = st.text_input("Enter a city name:", "Miami")
units = st.selectbox("Select Temperature Unit: ", ('fahrenheit', 'celsius'))
graph = st.selectbox("Select Temperature Graph Type:", ('Line Graph', 'Bar Graph'))


if units == 'fahrenheit':
   degree = 'F'
else:
   degree = 'C'




def get_temperature():
       # Get the max and min temperatures for the next 5 days using API calling
   forecaster = mgr.forecast_at_place(location, '3h')
   forecast = forecaster.forecast


   days = []
   dates = []
   temp_min = []
   temp_max = []
   for weather in forecast:
       day = datetime.utcfromtimestamp(weather.reference_time())
       date = day.date()
       if date not in dates:
           dates.append(date)
           temp_min.append(None)
           temp_max.append(None)
           days.append(date)
       temp = weather.temperature(unit=units)['temp']
       if not temp_min[-1] or temp < temp_min[-1]:
           temp_min[-1] = temp
       if not temp_max[-1] or temp > temp_max[-1]:
           temp_max[-1] = temp
   return (days, temp_min, temp_max)




def init_plot():
       # Initialize the plot and label x and y-axis
   plt.style.use('ggplot')
   plt.figure('PyOWM Weather')
   plt.xlabel('Day')
   plt.ylabel(f'Temperature({sign}{degree})')
   plt.title("Weekly Forecast")


def plot_temperature():
       # Plot the bar graph of final min and max temperature of the week
   days, temp_min, temp_max = get_temperature()
   days = dates.date2num(days)
   bar_x = plt.bar(days - 0.25, temp_min, width=0.5, color='#42bff4', label='Min')
   bar_y = plt.bar(days + 0.25, temp_max, width=0.5, color='#ff5349', label='Max')
   plt.legend(fontsize='x-small')
   return (bar_x, bar_y)




def label_xaxis():
       # Label the date in the format 'mm/dd' on the x label
   days, temp_min, temp_max = get_temperature()
   days = dates.date2num(days)
   plt.xticks(days)
   axes = plt.gca()
   xaxis_format = dates.DateFormatter('%m/%d')
   axes.xaxis.set_major_formatter(xaxis_format)




def show_max_temp_on_barchart():
       # Show max and min temp on the bar plot
   bar_x, bar_y = plot_temperature()
   axes = plt.gca()
   y_axis_max = axes.get_ylim()[1]
   label_offset = y_axis_max * 0.1
   for bar_chart in [bar_x, bar_y]:
       for index, bar in enumerate(bar_chart):
           bar_height = bar.get_height()
           xpos = bar.get_x() + bar.get_width() / 2.0
           ypos = bar_height - label_offset
           label_text = f"{int(bar_height)}{sign}"
           plt.text(xpos, ypos, label_text, ha='center', va='bottom', color='white')




def plot_line_graph_temp():
       # Plot the line graph of final min and max temperature of the week
   st.write("_____________________________________")
   st.markdown("<h1 style='text-align: center;'>5 Day Min and Max Temperature</h1>", unsafe_allow_html=True)
   init_plot()
   days, temp_min, temp_max = get_temperature()
   days = dates.date2num(days)
   plt.xticks(days)
   axes = plt.gca()
   xaxis_format = dates.DateFormatter('%m/%d')
   axes.xaxis.set_major_formatter(xaxis_format)
   plt.plot(days, temp_min, label='Min', color='#42bff4', marker='o')
   plt.plot(days, temp_max, label='Max', color='#ff5349', marker='o')
   plt.legend(fontsize='x-small')
   st.set_option('deprecation.showPyplotGlobalUse', False)
   st.pyplot(plt.show())




def weather_forcast():
       # Show the current weather forecast
   st.write("_____________________________________")
   st.markdown("<h1 style='text-align: center;'>Current Weather</h1>", unsafe_allow_html=True)


   obs = mgr.weather_at_place(location)
   weather = obs.weather
   icon = weather.weather_icon_url(size='4x')


   temp = weather.temperature(unit=units)['temp']
   temp_felt = weather.temperature(unit=units)['feels_like']
   st.image(icon, caption="")
   st.write(f"#### {(weather.detailed_status).title()}")
   st.write("")
   st.markdown(f"## Temperature: **{round(temp)}{sign}{degree}**")
   st.write(f"### Feels Like: {round(temp_felt)}{sign}{degree}")


   cloud = weather.clouds
   st.write(f"### Clouds Coverage: {cloud}%")


   wind = weather.wind()['speed']
   if degree == "F":
       seen2 = "f/s"
       wind = round(wind * 3.28084, 2)  # math converting to feet
   else:
       seen2 = "m/s"
   st.write(f"### Wind Speed: {wind} " + seen2)


   humidity = weather.humidity
   st.write(f"### Humidity: {humidity}%")


   visibility = weather.visibility(unit='kilometers')
   if degree == "F":
       seen = "miles"
       visibility = round(visibility * 0.621371, 2)    # math converting to miles
   else:
       seen = "kilometers"
   st.write(f"### Visibility: {visibility} " + seen)


def get_humidity():
       # Get the humidity data of 5 days using API call
   days = []
   dates = []
   humidity_max = []
   forecaster = mgr.forecast_at_place(location, '3h')
   forecast = forecaster.forecast


   for weather in forecast:
       day = datetime.utcfromtimestamp(weather.reference_time())
       date = day.date()
       if date not in dates:
           dates.append(date)
           humidity_max.append(None)
           days.append(date)


       humidity = weather.humidity
       if not humidity_max[-1] or humidity > humidity_max[-1]:
           humidity_max[-1] = humidity


   return (days, humidity_max)




def plot_humidity():
       # Plot the 5 days humidity graph
   days, humidity = get_humidity()
   st.write("_____________________________________")
   st.markdown("<h1 style='text-align: center;'>Humidity Index of 5 days</h1>", unsafe_allow_html=True)
   plt.style.use('ggplot')
   plt.figure('PyOWM Weather')
   plt.xlabel('Day')
   plt.ylabel('Humidity (%)')
   plt.title('Humidity Forecast')


   days = dates.date2num(days)
   plt.xticks(days)
   axes = plt.gca()
   xaxis_format = dates.DateFormatter('%m/%d')
   axes.xaxis.set_major_formatter(xaxis_format)


   bar = plt.bar(days, humidity, color='#42bff4')
   return bar




def show_max_humidity_on_bar():
       # Display the maximum humidity on the top of the graph
   bar_max = plot_humidity()
   axes = plt.gca()
   y_max = axes.get_ylim()[1]
   label_offset = y_max * 0.1
   for bar_chart in [bar_max]:
       for index, bar in enumerate(bar_chart):
           height = bar.get_height()
           xpos = bar.get_x() + bar.get_width() / 2.0
           ypos = height - label_offset
           label_text = f"{str(height)}%"
           plt.text(xpos, ypos, label_text, ha='center', va='bottom', color='white')




def plot_humidity_graph():
   show_max_humidity_on_bar()
   st.pyplot(plt.show())




def plot_bar_graph_temp():
   st.write("_____________________________________")
   st.title("5 Day Min and Max Temperature")
   init_plot()
   plot_temperature()
   label_xaxis()
   show_max_temp_on_barchart()




if __name__ == '__main__':
       # When button is clicked this will show all weather information
   if st.button('Submit'):
       if location == '':
           st.warning('Provide a city name!!')
       else:
           try:
               weather_forcast()
               if graph == 'Bar Graph':
                   plot_bar_graph_temp()
                   st.pyplot(plt.show())
               elif graph == 'Line Graph':
                   plot_line_graph_temp()


               plot_humidity_graph()
           except:
               st.error("City not found or API issue. Please try again.")
