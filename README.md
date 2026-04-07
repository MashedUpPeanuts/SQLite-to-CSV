# SQLite to CSV Conversion Tool
This project provides a GUI based application to select tables from an SQLite3 Database and export them .CSV files.

<p float="left">
  <img src="/Assets/MainMenu.png?" width="79.1%" />
  <img src="/Assets/ChecklistMenu.png?" width="19.8%" />
</p>

This project's original purpose was to provide a tool for converting Bentley AutoPIPE Results Database files into .csv files for easier processing for Engineering analysis. However, the tool has now been generalized to allow it to work for conversion of any SQLite3 database tables.

# How It Works
This project was coded in Python, using standard libraries.

# Installation and Use
The [latest release](https://github.com/MashedUpPeanuts/SQLite-to-CSV/releases) contains a pre-compiled executable, which can be downloaded and used immediately.

Alternatively, the source code package can be downloaded from the latest release and compiled using:

`py -m PyInstaller -F --icon='Icon.png' --add-data "Icon.png;." --onefile --noconsole 'DBConverter.py'`
