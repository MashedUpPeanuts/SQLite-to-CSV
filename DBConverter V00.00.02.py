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

    fNameSupport = "Supports.csv"
    fNameRestraint = "Anchors.csv"

    #Defining full output file paths
    path_fSupport = os.path.join(savePath, fNameSupport)
    path_fRestraint = os.path.join(savePath, fNameRestraint)

    subConvertDB(path_fSupport, dbFile, "Support")
    subConvertDB(path_fRestraint, dbFile, "Restraint")

#Opens a dialogue to select a .DB file from Windows explorer
def openFile():
    global filePath  # Setting filePath as global variable for use elsewhere
    filePath = filedialog.askopenfilename(title="Open an AutoPIPE results output file (.DB Format)",
                                          filetypes=(("SQLite3 Database File", "*.db"), ("all files", "*.*")))
    my_text.configure(state="normal")
    my_text.delete(1.0, END)  # Clearing existing input

    if filePath.endswith(".DB") or filePath.endswith(".db"):
        my_text.insert(END, filePath)   #Adding new input to text box

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

#If the selected DB file and directory are suitable, runs the conversion function and exits window
def exitWindow():
    if outputPath and (filePath.endswith(".DB") or filePath.endswith(".db")):
        con = sqlite3.connect(filePath)
        cur = con.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Support'")
        supportTable = cur.fetchone()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Support'")
        restraintTable = cur.fetchone()

        if supportTable and restraintTable:
            ConvertDB(filePath, outputPath)
            errorOutput.configure(text="The AutoPIPE Results Database has been successfully converted into CSV files!",
                                  fg='Dark Green')
            cancelButton.configure(text="Exit")
        else:
            errorOutput.configure(text="Selected database is not an AutoPIPE Results Database. Please select a valid AutoPIPE Results Database Output file.",
                                  fg='Red')
    else:
        #Outputs error if either the selected file or directory are unsuitable
        errorOutput.configure(text = "Please ensure a suitable file and directory have been selected.", fg='Red')

#Immediately exits thr program
def cancelProcess():
    window.destroy()


#Setting global variables to false in case of immediate exit of file selection
filePath = FALSE
outputPath = FALSE

window = Tk()   #Opening window for file selection

#Basic window geometry
window.geometry("1200x300")
window.resizable(False, False)
window.title("AutoPIPE Results Database Conversion Tool")

#Labels and buttons for the input file selection
winLabelIn = Label(window, text="Press the button below to select an AutoPIPE results file (*.DB)")
my_text = Text(window, width=135, height=1)
my_text.configure(state="disabled")
buttonIn = Button(text="Open File (.DB)",command=openFile)

#Labels and buttons for the output directory selection
winLabelOut = Label(window, text="Press the button below to select a directory to save the *.csv outputs to")
my_output = Text(window, width=135, height=1)
my_output.configure(state="disabled")
buttonOut = Button(text="Select Directory", command=saveLocation)

#Button for confirming selections
confirmButton = Button(text="Confirm Selections", command=exitWindow)

#Button for immediately exiting the program
cancelButton = Button(text="Cancel", command=cancelProcess, width=10)

#Error (and success) text output
errorOutputString = ''
colourCode = 'black'
errorOutput=Label(window, text=errorOutputString, fg=colourCode)

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

window.mainloop()
