#Importing libraries for SQLite3 conversion
import os
import sqlite3
import csv

from tkinter import *
from tkinter import filedialog

def subConvertDB(fullpath, dbFPath, tableName):
    con = sqlite3.connect(dbFPath)
    cur = con.cursor()

    cols = cur.execute("PRAGMA table_info('%s')" % tableName).fetchall()

    f = open(fullpath, 'w', newline='', encoding='utf-8')
    writer = csv.writer(f, dialect=csv.excel, quoting=csv.QUOTE_ALL)
    field_name_row = []

    for col in cols:
        col_name = col[1]
        field_name_row.append(col_name)
    writer.writerow(field_name_row)  # write field labels in the first row

    # Selecting the data from the support tab
    cur.execute("SELECT * FROM " + tableName + ";")
    rows = cur.fetchall()

    for row in rows:
        writer.writerow(row)  # write data row
    f.closed

#Manages setting output file locations and running subConvertDB for each of the required output tables
def ConvertDB(dbFile, savePath):

    readStates()

    con = sqlite3.connect(filePath)
    cur = con.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    table_names = [table[0] for table in tables]

    count = 0

    for table in tables:
        tableName = table_names[count]
        path_f = os.path.join(savePath, tableName + ".csv")

        if tickStates[count] == 1:
            subConvertDB(path_f, dbFile, tableName)
        count += 1

#Opens a dialogue to select a .DB file from Windows explorer
def openFile():
    global filePath  # Setting filePath as global variable for use elsewhere
    filePath = filedialog.askopenfilename(title="Open an SQLite3 Database file (*.DB Format)",
                                          filetypes=(("SQLite3 Database File", "*.db"), ("all files", "*.*")))
    my_text.configure(state="normal")
    my_text.delete(1.0, END)  # Clearing existing input

    if filePath.endswith(".DB") or filePath.endswith(".db"):
        my_text.insert(END, filePath)   #Adding new input to text box

        con = sqlite3.connect(filePath)
        cur = con.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        global table_names
        table_names=[table[0] for table in tables]

        global checkbox_vars
        checkbox_vars = []
        rowPos = 1

        for widget in fTable.winfo_children():
            widget.destroy()

        for table in tables:
            var = IntVar()
            checkbox_vars.append(var)
            Checkbutton(fTable, text=table, variable = var).grid(row=rowPos, column=1, sticky="W")
            rowPos += 1
        updateScrollRegion()

    my_text.configure(state="disabled")

#Opens a dialogue to select a directory from Windows explorer
def saveLocation():
    global outputPath  # Setting outputPath as global variable for use elsewhere
    outputPath = filedialog.askdirectory(mustexist=TRUE)    #Opening dialogue to select file directory

    my_output.configure(state="normal")
    my_output.delete(1.0, END)  # Clearing existing input

    if outputPath:
        my_output.insert(END, outputPath)   #Adding new input to text box

    my_output.configure(state="disabled")

#If the selected DB file and directory are suitable, runs the conversion function
def ConversionWindow():
    errorOutput.configure(text="")

    if outputPath and (filePath.endswith(".DB") or filePath.endswith(".db")):
        ConvertDB(filePath, outputPath)
        errorOutput.configure(text="The database has been successfully converted into CSV files!",
                                fg='Dark Green')
        cancelButton.configure(text="Exit")
    else:
        #Outputs error if either the selected file or directory are unsuitable
        errorOutput.configure(text = "Please ensure a suitable file and directory have been selected.", fg='Red')

#Immediately exits thr program
def cancelProcess():
    mainWindow.destroy()

def readStates():
    global tickStates
    tickStates = []
    tickStates = [var.get() for var in checkbox_vars]


#Setting global variables to false in case of immediate exit of file selection
filePath = FALSE
outputPath = FALSE
checkbox_vars = []

mainWindow = Tk()   #Opening window for file selection

#Basic window geometry
mainWindow.geometry('%dx%d+%d+%d' % (1200, 300, 400, 400))
mainWindow.resizable(False, False)
mainWindow.title("SQLite3 Database (*.DB) Conversion Tool")

#Labels and buttons for the input file selection
winLabelIn = Label(mainWindow, text="Press the button below to select an SQLite3 database file (*.DB)")
my_text = Text(mainWindow, width=135, height=1)
my_text.configure(state="disabled")
buttonIn = Button(text="Open File (.DB)",command=openFile)

#Labels and buttons for the output directory selection
winLabelOut = Label(mainWindow, text="Press the button below to select a directory to save the *.csv outputs to")
my_output = Text(mainWindow, width=135, height=1)
my_output.configure(state="disabled")
buttonOut = Button(text="Select Directory", command=saveLocation)

#Button for confirming selections
confirmButton = Button(text="Confirm Selections", command=ConversionWindow)

#Button for immediately exiting the program
cancelButton = Button(text="Cancel", command=cancelProcess, width=10)

#Error (and success) text output
errorOutputString = ''
colourCode = 'black'
errorOutput=Label(mainWindow, text=errorOutputString, fg=colourCode)

#Packing display window
winLabelIn.pack(pady=(5, 0))
my_text.pack(pady=(5, 0))
buttonIn.pack(pady=(5, 0))
winLabelOut.pack(pady=(20, 0))
my_output.pack(pady=(5, 0))
buttonOut.pack(pady=(5,0))
confirmButton.pack(pady=(15, 0))
cancelButton.pack(pady=(5, 0))
errorOutput.pack(pady=(10,0))


#Database table selection window
tickWindow = Toplevel(mainWindow)
tickWindow.title("Select tables to export")
tickWindow.geometry('%dx%d+%d+%d' % (300, 300, 1600, 400))
tickWindow.resizable(False, False)

cTableContainer = Canvas(tickWindow)
fTable = Frame(cTableContainer)
sbVerticalScrollBar = Scrollbar(tickWindow)

def updateScrollRegion():
    cTableContainer.update_idletasks()
    cTableContainer.config(scrollregion=fTable.bbox())

def createScrollableContainer():
    cTableContainer.config(yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
    sbVerticalScrollBar.config(orient=VERTICAL, command=cTableContainer.yview)

    sbVerticalScrollBar.pack(fill=Y, side=RIGHT, expand=FALSE)
    cTableContainer.pack(fill=BOTH, side=LEFT, expand=TRUE)
    cTableContainer.create_window(0, 0, window=fTable, anchor=NW)

createScrollableContainer()

tickWindow.mainloop()
mainWindow.mainloop()