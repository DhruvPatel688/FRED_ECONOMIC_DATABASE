'''
FRED ECONOMIC DATA API
This program takes in user input for a particular economic dataset from the federal
reserve economic database and outputs the appropriate data table and graph based 
on a specific time frame.This program uses an official API(you must obtain your own) 
and GUI to work with the data.
'''



import requests # Need this for API usuage
import pandas as pd # For data table
import numpy as np # For arthmetic 
import matplotlib.pyplot as plt # To plot a graph
from tkinter import * #GUI
from tkinter import messagebox #GUI
from api_key import api_key # Private API KEY is neccessary for this to work

#This function takes in user input and outputs the series id for use with API
def input_analysis(response):
	if response == "GDP":
		return "GDP"
	elif response == "CPI":
		return "CPIAUCSL"
	elif response == "Unemployment Rate":
		return "UNRATE"
	elif response == "Federal Funds Rate":
		return "DFF"
	else:
		raise ValueError("Incorrect Formatting")

#This function takes in user input and outputs the correctly formatted start date
def start_date(dates):
	if dates == "50":
		return "1973-01-01"
	elif dates == "20":
		return "2003-01-01"
	elif dates == "10":
		return "2013-01-01"
	else:
		raise ValueError("Incorrect Formatting")

#This is the main function of the program. It takes in all the properly formatted parameters and uses them to obatin the data from FRED.
def data(api_key, series_id, start_date, end_date):
	base_url = "https://api.stlouisfed.org/fred/" #Website

	obs_endpoint = 'series/observations' #End point destination

	#Make the parameters easier to use
	obs_param = {
	    'series_id': series_id,
	    'api_key': api_key,
	    'file_type': 'json',
	    'observation_start_date': start_date,
	    'observation_end_date': end_date
	}

	#Request the FRED API
	response = requests.get(base_url + obs_endpoint, params=obs_param)

	#Format the data
	if response.status_code == 200:
		res_data = response.json() #Dictionary of data
		obs_data = pd.DataFrame(res_data['observations']) #Create a pandas table
		pd.set_option('display.min_rows', 100)
		obs_data['date'] = pd.to_datetime(obs_data['date']) # Separate out the data values
		obs_data.set_index('date', inplace=True) #x axis is automatically date
		# Replace "." with NaN
		obs_data['value'] = obs_data['value'].replace('.', np.nan) 
		# Convert to float
		obs_data['value'] = obs_data['value'].astype(float)#obtain value from data
		obs_data = obs_data[(obs_data.index >= start_date) & (obs_data.index <= end_date)] #Set the range
		obs_data = obs_data.drop(columns=['realtime_start', 'realtime_end'])  # Drop the specified columns
		return obs_data  # Display the DataFrame
		
	else:
		print('Failed to retrieve data. Status code:', response.status_code)

#This function takes the data obtained from FRED and graphs it.
def plot_data(obs_data, response):
	obs_data.plot( y = "value", kind = 'line') # Plot the data, no need for x since set_index
	plt.xlabel('Year')
	plt.ylabel(f'{response} Value')
	plt.title(f"{response} over Time")

	plt.grid(True)
	plt.show() # Output the graph

#This function takes the data obtained from FRED and puts it into a readable file.
def display_data(obs_data):

	if obs_data is not None:
		root = Tk() # Create a GUI window
		root.title("Data Table")
		#Makes the data table more viewable
		table.pack(expand = True, fill = BOTH)
		table.insert(END, obs_data)
		scrollbar.config(command=table.yview)
		num_rows = len(obs_data)
		table.config(height = num_rows)# Format the table for the correct length
		root.mainloop()#Output the table 



# This part of the program is where the user can enter what Economic Data they want to observe.
response = 1
while response != "X":
	#Obtain input
	print("Which type of data do you want to analyze for?")
	response = input("Type GDP, CPI, Unemployment Rate, or Federal Funds Rate (Enter X to exit): ") # user input entered here
	if response == "X":
		break
	try: # Makes sure that the expression formatted correctly 
		series_id = input_analysis(response)
	except ValueError as e:
		print(f"There seems to be a formatting error in your expression")
		break

	dates = input("Do you want to look at data from 10 years ago, 20 years ago, or 50 years ago. Type the number: ")
	try: # Makes sure that the expression formatted correctly 
		start_dates = start_date(dates)
		end_date = "2023-06-30"
	except ValueError as e:
		print(f"There seems to be a formatting error in your expression, try again!")
		break
	obs_data = data(api_key, series_id, start_dates, end_date) #call the first function

	root = Tk()# Create a GUI window to view 
	root.title("FRED Data Viewer")
	root.geometry("400x300")

	#Display the buttons for the GUI and make sure they provide proper output:

	display_button = Button(root, text="Display Table", command = lambda: display_data(obs_data), width = 20, height = 5) 
	display_button.pack()

	plot_button = Button(root, text="Plot Data", command = lambda: plot_data(obs_data, response), width = 20, height = 5) 
	plot_button.pack()

	
	root.mainloop()





