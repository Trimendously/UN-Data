# GUI Tool
import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import simpledialog

# Makes tables and allows reading of csv files
import pandas as pd
import pandastable as pt

import numpy as np
# Will fetch the html files
import requests

# Pulls data from html files
from bs4 import BeautifulSoup
import urllib.request



# File contains all stat calculations
from statCalc import*

#Executes statistical analysis upon the data
class Stats_Page:
    def __init__(self,df):
        self.window = Tk()
        self.window.title("Statistical Methods")
        self.window.attributes('-fullscreen',False) #Makes the page take up the ful screen

        #Allows user toggle full screen if desired
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        self.df = df
        self.buttons()
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)
    def buttons(self):
        stat_switch = {
        'Mean': df_mean,
        'Mode': df_mode,
        'Median': df_median,
        'Inner Quartile Range': IQR,
        'Variance': df_variance,
        'Standard Deviation': df_std,
        'Pearson Product Moment Correlation': pear, #These are different with decimal restriction
        'Spearman Rank-Order Correlation': spear,
        'Kendall\'s Tau-b Correlation Coefficient': kendall,
        }
        graph_switch = {
        'Histogram': df_hist,
        'Box Plot': box, #Restrict by year if multiple years given give muktiple boxplots
        'Scatter Plot':scatter,
        'Vertical Box Plots':vert,
        'Horizon Box Plots':hor
        }
        operations = ["Mean","Median","Mode","Inner Quartile Range","Variance",
        "Standard Deviation",'Pearson Product Moment Correlation',
        'Spearman Rank-Order Correlation','Kendall\'s Tau-b Correlation Coefficient']
        graph_operations = ["Histogram", "Box Plot",'Scatter Plot','Vertical Box Plots','Horizon Box Plots']

        for i, op in enumerate(operations):
            calc = stat_switch.get(op)(self.df)
            e =Entry(self.window, width=150, fg='black',font=('Arial',20,'bold'),background = theme(i))
            e.grid(row=i, column= 0)

            formatted = np.round(calc,decimals = 3)

            e.insert(END, op +":  " +str(formatted))
        for j, graph in enumerate(graph_operations,start=1):
            b = Button(self.window,text = graph,background=theme(i+j),font = ('Arial',15,'bold'))
            b.grid(row = i+j, column = 0)
            b.config(command = lambda e=i+j, b = b: graph_switch.get(b['text'])(self.df))

        b = Button(self.window,text = 'Display Data',background = theme(i+j+1),font = ('Arial',15,'bold'))
        b.grid(row = i+j+1, column = 0)
        b.config(command = lambda: self.displayData())

        b = Button(self.window,text = 'Save as Excel File',background = theme(i+j+2),font = ('Arial',15,'bold'))
        b.grid(row = i+j+2, column = 0)
        b.config(command = lambda: self.saveDataframe())

    #Display table full of data
    def displayData(self):
        new = Tk()
        new.title("Data")
        frame = Frame(new)
        frame.pack(fill='both', expand=True)

        table = pt.Table(frame,dataframe=self.df)
        table.show()

    #saves dataframe as excel file
    def saveDataframe(self):
        file_name = simpledialog.askstring("Input", " What do you want the file name to be?",
        parent=save_window)

        file_name = file_name + '.xlsx'
        writers = pd.ExcelWriter(file_name)
        self.df.to_excel(writers)
        writers.save()

class Category_Page:
    def __init__(self,csv,index):
        self.window = Tk()
        self.window.title("UN Data (Categories)")
        self.window.attributes('-fullscreen',False) #Makes the page take up the ful screen
        #Allows user toggle full screen if desired
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        #Sets the default resolution of the main page
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(str(width)+ "x" + str(height)) #Sets resolution
        self.buttons(csv,index)
        self.window.mainloop()
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def buttons(self,csv,index):
        df = pd.read_csv(csv[index], skiprows = 1,engine='python',encoding='unicode_escape')
        categories = df['Series'].unique()
        # Populates list to store selected categories
        global selected_category
        selected_category = ['0']*len(categories)

        # Centers column
        self.window.grid_columnconfigure((0), weight=1)

        # Sets the font size
        B_Style = ttk.Style(self.window)
        B_Style.configure("b.TCheckbutton",font=('',30))
        prompt_b = Label(self.window,text = "Please select the data categories that you desire:",font = 30)
        prompt_b.grid(row = 0, column = 0)

        # Creates button for every unique category
        for i,cat in enumerate(categories):
            selected_category[i] = ttk.Checkbutton(self.window,text=cat,style = "b.TCheckbutton")
            selected_category[i].grid(row=i+1, column=0)

        b = Button(self.window,text = "Continue", font = 30)
        b.grid(row = i+2, column = 0)
        b.config(command = lambda: self.restrict(df))

    def restrict(self,df):
        new = Tk()
        new.title("Restricting Data")
        new.geometry('600x450') #Sets resolution
        new_df = []

        # Restrict dataframe to previously chosen category
        for i in range(len(selected_category)):
            if selected_category[i].instate(['selected']):
                temp= df['Series'] == selected_category[i]['text']
                new_df.append(df[temp])
        self.df = pd.concat(new_df)

        # Centers the buttons
        new.grid_columnconfigure((0), weight=1)

        country_b = Button(new,text = 'Country', font = 50)
        country_b.grid(row=0, column=0)
        country_b.config(command = lambda : self.restrictCountry(self.df))

        year_b = Button(new,text = 'Year', font = 50)
        year_b.grid(row=1, column=0)
        year_b.config(command = lambda : self.restrictYear(self.df))

        b = Button(new,text = 'Continue',font = 50)
        b.config(command = lambda: Stats_Page(self.df))
        b.grid(row=2, column=0)

    # Restricts the dataframe to only selected years
    def restrictYear(self,df):
        yearPage = Tk()
        yearPage.title("Year Selector")

        # List to store all selected years
        global selected_year
        selected_year = []

        years = df['Year'].unique()

        columns = 0
        rows = 0
        for i, y in enumerate(years):
            var = IntVar()
            selected_year.append(ttk.Checkbutton(yearPage,text = y, variable = var))
            selected_year[i].grid(row=rows, column = columns)
            rows+=1
            if rows == 35: #Restricts rows to fit in window
                rows = 0
                columns += 1

        # Allows users to click continue to confirm choices
        b = Button(yearPage,text = "Confirm")
        b.grid(column = columns+1)
        b.config(command = lambda : self.yearHelper(df,years,yearPage))

    def yearHelper(self,df,years,yearPage):
        new_df = []
        for i,select in enumerate(selected_year):
            if selected_year[i].instate(['selected']):
                new = df['Year'] == years[i]
                new_df.append(df[new])

        self.df = pd.concat(new_df)
        yearPage.destroy()

    # Restricts the dataframe to only selected countries
    def restrictCountry(self,df):
        countryPage = Tk()
        countryPage.title("Country Selector")
        count = 0
        columnn= 0
        global selected_country

        # Poor implementation
        for dat in df.columns:
            if count == 1:
                column = dat
                break
            count +=1
        countries = df[column].unique()

        selected_country = []

        columns = 0
        rows = 0
        # Creates buttons for each country within file
        for i,c in enumerate(countries):
            var = IntVar()
            selected_country.append(ttk.Checkbutton(countryPage,text = c, variable = var))
            selected_country[i].grid(row=rows, column = columns)
            rows+=1
            if rows == 35: #Restricts rows to fit in window
                rows = 0
                columns += 1

        # Allows users to click continue to confirm choices
        b = Button(countryPage,text = "Confirm")
        b.grid(column = columns+1)
        b.config(command = lambda: self.countryHelper(df,countryPage,countries,column))

    # Helper function to restrict dataframe by country
    def countryHelper(self,df,countryPage,countries,column):
        new_df = []
        for i, country in enumerate(selected_country):
            if selected_country[i].instate(['selected']):
                new = df[column] == countries[i]
                new_df.append(df[new])

        self.df = pd.concat(new_df)
        countryPage.destroy()

class Main_Page:
    def __init__(self,csv):
        self.window = Tk()
        self.window.title("UN Data")
        self.window.attributes('-fullscreen',False) #Makes the page take up the full screen

        #Allows user toggle full screen if desired
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        #Sets the default resolution of the main page
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(str(width)+ "x" + str(height)) #Sets resolution


        #Sets up the buttons
        self.buttons(csv)
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def buttons(self,csv):
        self.selected = []
        for i in range(len(csv)):
            # Creates a color theme
            color = theme(i)
            # Selecting tables to operate on
            b = Button(self.window,text="Select Table",background=color)
            b.grid(row=i, column=0)
            b.config(command = lambda e=i, b = b: self.statPage(e, b))
            # Table displaying button
            b = Button(self.window,text="Display Dataframe",background=color)
            b.grid(row=i, column=1)
            b.config(command = lambda e=i, b = b: self.tablePage(e, b))

            # Displays CSV file names
            self.e = Entry(self.window, width=150, fg='black',font=('Arial',16,'bold'),background = color)
            self.e.grid(row=i, column= 2)
            self.e.insert(END, csv[i]) #Currently reads through all csv files on webpage can be editied to parse lesss

    # Converts csv file into dataframe and displays as panda table
    def tablePage(self, text, btn):
        new = Tk()
        new.title("Data")
        frame = Frame(new)
        frame.pack(fill='both', expand=True)

        df = pd.read_csv(csv[text],engine='python',encoding='unicode_escape')

        table = pt.Table(frame,dataframe=df)
        table.show()

    def statPage(self,index,btn):
        stats = Category_Page(csv,index)

#A function to parse through the url given for all csv file data
def parser():
    url = "http://data.un.org/default.aspx"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    soup = BeautifulSoup((response.read()), "lxml") #Used to read through the webpage
    columns = soup.findAll("div", {"class": "CountryLinks"}) # We only want the first column so 0 index
    categories = columns[0].findAll("li", {"class": "NoBullets"})
    csv = []

    #Iterativelly reads through the webpage and stores each csv file in a new index in the list
    for x in range(len(categories)):
        files = categories[x].findAll('a') #Find every categories 'a' tag

        #Concatenating strings to get the proper url
        temp = "https://data.un.org/"+str(files[1].get('href'))

        csv.append(temp.replace(" ", "%20"))
    return csv

# Sets color theme
def theme(index):
    if index % 2 == 0:
        return 'LightSteelBlue1'
    else:
        return 'white'

csv = parser()
app = Main_Page(csv)
