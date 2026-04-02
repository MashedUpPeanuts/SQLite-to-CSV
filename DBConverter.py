#####################
# VERSION 1.02.01 #
#####################

###################
# LIBRARY IMPORTS #
###################

import os
import sqlite3
import csv
from tkinter import *
from tkinter import filedialog

########################
# VARIABLE DEFINITIONS #
########################

extensionsAllowable = [".DB", ".db", ".db3", ".sqlite", ".sqlite3"] #List of common SQLite3 file extensions
filePath = FALSE
outputPath = FALSE
checkboxVars = []

########################
# FUNCTION DEFINITIONS #
########################

#WRITES SELECTED DATABASE TABLE TO A CSV FILE
def subConvertDB(fullpath, dbFPath, tableName):

    con = sqlite3.connect(dbFPath)
    cur = con.cursor()

    cols = cur.execute("PRAGMA table_info('%s')" % tableName).fetchall()

    fileOpen = open(fullpath, 'w', newline='', encoding='utf-8')
    writer = csv.writer(fileOpen, dialect=csv.excel, quoting=csv.QUOTE_ALL)
    fieldNameRow = []

    #DETERMINING FIELD TITLES
    for col in cols:
        col_name = col[1]
        fieldNameRow.append(col_name)
    writer.writerow(fieldNameRow)

    #FETCHING DATA FROM DB TABLE
    cur.execute("SELECT * FROM " + tableName + ";")
    rows = cur.fetchall()

    #WRITING TO CSV
    for row in rows:
        writer.writerow(row)  # write data row
    fileOpen.closed

#CHECKS WHICH TABLES ARE SELECTED AND LOOPS TO RUN CSV WRITE FUNCTION
def ConvertDB(dbFile, savePath):

    #CHECKS STATE OF TABLE CHECKLIST CHECKBOXES
    readStates()

    #QUERIES SQLITE3 DATABASE
    con = sqlite3.connect(filePath)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    tableNames = [table[0] for table in tables]

    #LOOPS subConvertDB FOR EACH SELECTED TABLE
    count = 0
    for table in tables:
        tableName = tableNames[count]
        path_f = os.path.join(savePath, tableName + ".csv")
        if tickStates[count] == True:
            subConvertDB(path_f, dbFile, tableName)
        count += 1

#OPENS FILE EXPLORER DIALOGUE TO SELECT AN SQLITE3 DATABASE
def openFile():

    #OPENING FILE DIALOG
    global filePath
    filePath = filedialog.askopenfilename(title="Open an SQLite3 Database file",
                                          filetypes=(("SQLite3 Database File", tuple(extensionsAllowable)), ("all files", "*.*")))
    #CLEARING EXISTING FILE SELECTION
    mainTextInput.configure(state="normal")
    mainTextInput.delete(1.0, END)

    #IF EXTENSION VALID QUERY TABLE AND CREATE CHECKLIST OF DATABASE TABLES. IF INVALID CLEAR CHECKLIST.
    if filePath.endswith(tuple(extensionsAllowable)):

        mainTextInput.insert(END, filePath)

        con = sqlite3.connect(filePath)
        cur = con.cursor()

        #QUERYING DATABASE
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        global tableNames
        tableNames=[table[0] for table in tables]

        #CLEARING EXISTING CHECKBOXES AND VARIABLES
        global checkboxVars
        checkboxVars = []
        rowPos = 2
        for widget in checkFrame.winfo_children():
            if isinstance(widget, Checkbutton):
                widget.destroy()

        #GENERATING CHECKLIST AND VARIABLES
        for table in tables:
            var = BooleanVar()
            checkboxVars.append(var)
            Checkbutton(checkFrame, text=table, variable = var).grid(row=rowPos, column=1, sticky="W")
            rowPos += 1
        updateScrollRegion()
        checkButtonSelect.configure(state="normal")
    else:
       checkboxVars=[]
       for widget in checkFrame.winfo_children():
           if isinstance(widget, Checkbutton):
               widget.destroy()
       checkButtonSelect.configure(text="Select All", state="disabled")

    mainTextInput.configure(state="disabled")

#OUTPUT DIRECTORY SELECTION DIALOG.
def saveLocation():

    global outputPath
    outputPath = filedialog.askdirectory(mustexist=TRUE)

    #CLEARING ANY EXISTING DIRECTORY SELECTION
    mainTextOutput.configure(state="normal")
    mainTextOutput.delete(1.0, END)

    #PRINTING SELECTED DIRECTORY IN TEXT BOX
    if outputPath:
        mainTextOutput.insert(END, outputPath)

    mainTextOutput.configure(state="disabled")

#DETERMINES IF THE SELECTED FILE IS SUITABLE, RUNS CONVERSION, OUTPUTS COMPLETION OR ERROR MESSAGE
def conversionWindow():
    mainLabelError.configure(text="")

    if outputPath and (filePath.endswith(tuple(extensionsAllowable))):
        ConvertDB(filePath, outputPath)
        mainLabelError.configure(text="The selected SQLite3 database table(s) have been successfully converted into CSV file(s)!",
                                fg='Dark Green')
        mainButtonCancel.configure(text="Exit")
    else:
        mainLabelError.configure(text = "Please ensure a suitable file and directory have been selected.", fg='Red')

#IMMEDIATELY EXITS THE PROGRAM
def cancelProcess():
    mainWindow.destroy()

#READS THE STATES OF THE TABLE CHECKLIST BUTTONS WRITES TO GLOBAL VARIABLE
def readStates():
    global tickStates
    tickStates = []
    tickStates = [var.get() for var in checkboxVars]

#SETS ALL TABLE CHECKLIST BUTTONS TO TRUE, TOGGLES SELECT ALL TO UNSELECT ALL
def selectAll():
    if checkboxVars:
        [var.set(True) for var in checkboxVars]
        checkButtonSelect.configure(text="Unselect All", command=unselectAll)

#SETS ALL TABLE CHECKLIST BUTTONS TO FALSE. TOGGLES UNSELECT ALL TO SELECT ALL
def unselectAll():
    if checkboxVars:
        [var.set(False) for var in checkboxVars]
        checkButtonSelect.configure(text="Select All", command = selectAll)

#UPDATES SCROLLABLE REGION IN checkWindow
def updateScrollRegion():
    checkContainer.update_idletasks()
    checkContainer.config(scrollregion=checkFrame.bbox())

#CREATES A SCROLLABLE FRAME FOR checkWindow
def createScrollableContainer():
    checkContainer.config(yscrollcommand=checkScrollbar.set, highlightthickness=0)
    checkScrollbar.config(orient=VERTICAL, command=checkContainer.yview)

    checkScrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
    checkContainer.pack(fill=BOTH, side=LEFT, expand=TRUE)
    checkContainer.create_window(0, 0, window=checkFrame, anchor=NW)


##################
# GUI GEOMETRIES #
##################

#DISPLAY DIMENSIONS
root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.destroy()

#WINDOW GEOMETRIES
mainWidth = 1200
mainHeight = 300
checkWidth = 300
checkHeight = mainHeight

#WINDOW POSITIONING
mainCornerX = (screenWidth - mainWidth - checkWidth) / 2
mainCornerY = (screenHeight - mainHeight) / 2
checkCornerX = mainCornerX + mainWidth
checkCornerY = mainCornerY


#############
# MAIN MENU #
#############

#INITIALIZING AND CONFIGURING
mainWindow = Tk()
mainWindow.geometry('%dx%d+%d+%d' % (mainWidth, mainHeight, mainCornerX, mainCornerY))
mainWindow.resizable(False, False)
mainWindow.title("SQLite3 Database Conversion Tool")

#DATABASE SELECTION WIDGETS
mainLabelInput = Label(mainWindow, text="Press the button below to select an SQLite3 database file")
mainTextInput = Text(mainWindow, width=135, height=1)
mainTextInput.configure(state="disabled")
mainButtonInput = Button(text="Open Database", command=openFile)

#OUTPUT DIRECTORY SELECTION WIDGETS
mainLabelOutput = Label(mainWindow, text="Press the button below to select a directory to save the *.csv outputs to")
mainTextOutput = Text(mainWindow, width=135, height=1)
mainTextOutput.configure(state="disabled")
mainButtonOutput = Button(text="Select Directory", command=saveLocation)

#CONFIRMATION AND CANCEL WIDGETS
mainButtonConfirm = Button(text="Confirm Selections", command=conversionWindow)
mainButtonCancel = Button(text="Cancel", command=cancelProcess, width=10)
mainLabelError=Label(mainWindow, text='', fg='black')

#PACKING MAIN MENU
mainLabelInput.pack(pady=(5, 0))
mainTextInput.pack(pady=(5, 0))
mainButtonInput.pack(pady=(5, 0))

mainLabelOutput.pack(pady=(20, 0))
mainTextOutput.pack(pady=(5, 0))
mainButtonOutput.pack(pady=(5,0))

mainButtonConfirm.pack(pady=(15, 0))
mainButtonCancel.pack(pady=(5, 0))
mainLabelError.pack(pady=(10,0))


########################
# TABLE SELECTION MENU #
########################

#INITIALIZING AND CONFIGURING
checkWindow = Toplevel(mainWindow)
checkWindow.title("Select tables to export")
checkWindow.geometry('%dx%d+%d+%d' % (checkWidth, checkHeight, checkCornerX, checkCornerY))
checkWindow.resizable(False, False)
checkWindow.protocol("WM_DELETE_WINDOW", cancelProcess) #Closes main window when child window is closed

#WINDOW AND SCROLLBAR CONFIGURATION
checkContainer = Canvas(checkWindow)
checkFrame = Frame(checkContainer)
checkScrollbar = Scrollbar(checkWindow)

#SELECT ALL BUTTON
checkButtonSelect = Button(checkFrame, text="Select All", command=selectAll)
checkButtonSelect.configure(width=2, height=1)
checkButtonSelect.grid(row=1, column=1, ipadx=120, padx=10)
checkButtonSelect.configure(state="disabled")


##############
# MAIN LOOPS #
##############

createScrollableContainer()
checkWindow.mainloop()
mainWindow.mainloop()