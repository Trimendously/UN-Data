# GUI Tool
from tkinter import*
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

class Stats_Page:
    def __init__(self,csv,index):
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
        self.buttons(csv,index)
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)
    def buttons(self,csv,index):
        print('wip')

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

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def buttons(self,csv,index):
        df = pd.read_csv(csv[index], skiprows = 1)
        categories = df['Series'].unique()
        selected_category = []
        i = 0
        # Creates button for every unique category
        for cat in categories:
            selected_category.append(IntVar())
            b = Checkbutton(self.window,text=cat,variable = selected_category[i],onvalue=1,offvalue=0, command =self.test(selected_category[i]))
            b.grid(row=i, column=0)
            i += 1

        b = Button(self.window,text = "Continue")
        b.grid(row = i+1, column = 2, sticky = 'nsew')
        b.config(command = lambda e=i+1, b = b: self.restrict(csv, e, selected_category))

    def restrict(self,csv,index,selected):
        new = Tk()
        new.title("Restricting Data")
        new.geometry('200x150') #Sets resolution

        country_b = Button(new,text = 'Country')
        country_b.grid(row=0, column=0)
        country_b.config(command = lambda e = 0, b = country_b: self.restrictCountry(csv, e,country_b['text']))

        year_b = Button(new,text = 'Year')
        year_b.grid(row=1, column=0)
        year_b.config(command = lambda e = 1, b = year_b: self.restrictYear(e, year_b['text']))

    # Restricts the dataframe to only selected countries
    def restrictCountry(self,csv,index, selected):
        countryPage = Tk()
        countryPage.title("County Selector")
        df_country = pd.read_csv(csv[index])
        count = 0
        columnn= 0
        selected_country = []

        # Kinda dumb method but can't figure out other way
        for dat in df_country.columns:
            if count == 1:
                column = dat
                break
            count +=1
        countries = df_country[column].unique()


        i = 0
        j = 0
        # Creates buttons for each country iwthin file
        for c in countries:
            var = IntVar()
            b = Checkbutton(countryPage,text = c, variable = var)
            selected_country.append(var)
            b.grid(row=i, column = j)
            i+=1
            if i == 35:
                i = 0
                j += 1

        # Allows users to click continue to confirm choices
        b = Button(countryPage,text = "Continue")
        b.grid(column = j+1, sticky = 'se')
        b.config(command = lambda e=i+1, b = b: self.countryHelper(csv,index,selected_country,countries,column))

    # Helper function to restrict country "wip"
    def countryHelper(self,csv,index,selected_country,countries,column):
        new_df = []
        df = pd.read_csv(csv[index])
        g = [i for i, e in enumerate(selected_country) if e == 1]


        # Rewrite to use .index()
        for i in len(selected_country):
            if selected_country[i] == 1:
                new = df[column] == countries[i]
                new_df.append(df[new])

        new_df.concat()


class Main_Page:
    def __init__(self,csv):
        self.window = Tk()
        self.window.title("UN Data")
        self.window.attributes('-fullscreen',False) #Makes the page take up the ful screen

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
        b = Button(self.window,text = "Continue",background = 'SteelBlue1')
        b.grid(row = i+1, column = 2, sticky = 'nsew')
        b.config(command = lambda e=i+1, b = b: self.statPage(e, b, self.selected))

    # Converts csv file into dataframe and displays as panda table
    def tablePage(self, text, btn):
        new = Tk()
        new.title("Data")
        frame = Frame(new)
        frame.pack(fill='both', expand=True)


        df = (pd.read_csv(csv[int(text)]))

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

opened = [] #A list to keep track of opened csv files to reduce runtime "wip"
