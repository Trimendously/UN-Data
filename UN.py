# GUI Tool
import tkinter
from tkinter import*
from tkinter import ttk
# Makes tables and allows reading of csv files
import pandas as pd
from pandastable import Table

# Will fetch the html files
import requests

# Pulls data from html files
from bs4 import BeautifulSoup
import urllib.request

# Tool for images
from PIL import ImageTk, Image

# File contains all stat calculations
from statCalc import*

#Executes statistical analysis upon the data
class Stats_Page:
    def __init__(self,df):
        self.window = Tk()
        self.window.title("Statstical Methods")
        self.window.attributes('-fullscreen',False) #Makes the page take up the ful screen

        #Allows user toggle full screen if desired
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        #Sets the default resolution of the main page
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(str(width)+ "x" + str(height)) #Sets resolution
        self.buttons(df)
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)
    def buttons(self,df):
        stat_switch = {
        'Mean': df_mean,
        'Mode': df_mode,
        'Median': df_median,
        'Inner Quartile Range': IQR,
        'Variance': df_variance,
        'Standard Deviation': df_std,
        'Pearson Product Moment Correlation': pear,
        'Spearman Rank-Order Correlation': spear,
        'Kendall\'s Tau-b Correlation Coefficient': kendall,
        }
        graph_switch = {
        'Histogram': df_hist,
        'Box Plot': box,
        'Scatter Plot':scatter,
        'Vertical Box Plots':vert,
        'Horizon Box Plots':hor
        }

        operations = ["Mean","Median","Mode","Inner Quartile Range","Variance",
        "Standard Deviation",'Pearson Product Moment Correlation',
        'Spearman Rank-Order Correlation','Kendall\'s Tau-b Correlation Coefficient'
        ]
        graph_operations = ["Histogram", "Box Plot",'Scatter Plot','Vertical Box Plots','Horizon Box Plots']

        for i, op in enumerate(operations):
            calc = stat_switch.get(op)(df)
            e =Entry(self.window, width=150, fg='black',font=('Arial',16,'bold'))
            e.grid(row=i, column= 0,sticky='nsew')
            e.insert(END, op +":  " +str(calc))
        for j, graph in enumerate(graph_operations):
            b = Button(self.window,text = graph)
            b.grid(row = i+j, column = 0, sticky = 'nsew')
            b.config(command = lambda e=i+j, b = b: graph_switch.get(b['text'])(df))
        b = Button(self.window,text = 'Display Data')
        b.grid(row = i+j+1, column = 0, sticky = 'nsew')
        b.config(command = lambda: self.displayData(df))

    #Display table full of data
    def displayData(self,df):
        new = Tk()
        new.title("Data")
        frame = Frame(new)
        frame.pack(fill='both', expand=True)

        pt = Table(frame,dataframe=df)
        pt.show()
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
        global selected_category
        selected_category = ['0']*len(categories)
        i = 0
        # Creates button for every unique category
        for cat in categories:
            selected_category[i] = ttk.Checkbutton(self.window,text=cat)
            selected_category[i].grid(row=i, column=0)
            i += 1

        b = Button(self.window,text = "Continue")
        b.grid(row = i+1, column = 2, sticky = 'nsew')
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


        country_b = Button(new,text = 'Country')
        country_b.grid(row=0, column=0)
        country_b.config(command = lambda : self.restrictCountry(self.df))
        year_b = Button(new,text = 'Year')
        year_b.grid(row=1, column=0)
        year_b.config(command = lambda : self.restrictYear(self.df))
        b = Button(new,text = 'Continue')
        #b.config(command = Stats_Page(self.df))
        b.config(command = lambda: Stats_Page(self.df))
        b.grid(row=2, column=0)

    # Restricts the dataframe to only selected years
    def restrictYear(self,df):
        self.yearPage = Tk()
        self.yearPage.title("Year Selector")
        columnn= 0
        global selected_year
        selected_year = []

        years = df['Year'].unique()
        j = 0
        h = 0
        for i, y in enumerate(years):
            var = IntVar()
            selected_year.append(ttk.Checkbutton(self.yearPage,text = y, variable = var))
            selected_year[i].grid(row=h, column = j)
            h+=1
            if h == 35: #Restricts rows to fit in window
                h = 0
                j += 1

        # Allows users to click continue to confirm choices
        b = Button(self.yearPage,text = "Confirm")
        b.grid(column = j+1, sticky = 'se')
        b.config(command = lambda : self.yearHelper(df,years))

    def yearHelper(self,df,years):
        new_df = []
        for i in range(len(selected_year)):
            if selected_year[i].instate(['selected']):
                new = df['Year'] == years[i]
                new_df.append(df[new])

        self.df = pd.concat(new_df)
        self.yearPage.destroy

    # Restricts the dataframe to only selected countries
    def restrictCountry(self,df):
        countryPage = Tk()
        countryPage.title("Country Selector")
        count = 0
        columnn= 0
        global selected_country


        # Kinda dumb method but can't figure out other way
        for dat in df.columns:
            if count == 1:
                column = dat
                break
            count +=1
        countries = df[column].unique()

        selected_country = []
        i = 0
        j = 0
        h =0
        # Creates buttons for each country iwthin file
        for c in countries:
            var = IntVar()
            selected_country.append(ttk.Checkbutton(countryPage,text = c, variable = var))
            selected_country[i].grid(row=h, column = j)
            i+=1
            h+=1
            if h == 35: #Restricts rows to fit in window
                h = 0
                j += 1

        # Allows users to click continue to confirm choices
        b = Button(countryPage,text = "Continue")
        b.grid(column = j+1, sticky = 'se')
        b.config(command = lambda: self.countryHelper(df,countryPage,countries,column))

    # Helper function to restrict dataframe by country
    def countryHelper(self,df,countryPage,countries,column):
        new_df = []
        for i in range(len(selected_country)):
            if selected_country[i].instate(['selected']):
                new = df[column] == countries[i]
                new_df.append(df[new])

        self.df = pd.concat(new_df)
        countryPage.destroy

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

        # Adds the UN symbol
        symbol = PhotoImage(file = "UN_symbol.png")
        self.window.iconphoto(False, symbol)
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
            if i % 2 == 0:
                color = 'LightSteelBlue1'
            else:
                color = 'white'
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

        pt = Table(frame,dataframe=df)
        pt.show()

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


csv = parser()
app = Main_Page(csv)
