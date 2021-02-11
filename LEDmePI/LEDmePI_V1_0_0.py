#!/bin/env python3

# LEDmePI
# Tool to use a Raspberry Pi 3 as a LEDmePlay programmer
#
# www.mithotronic.de
#
# Version: 1.0.0
# Author: Michael Rosskopf (2021)
#
# Many thanks to Thomas Laubach
# 
# Release Notes:
# V1.0.0: First release (07.02.2021)


# Import required Python packages
import tkinter as tk # GUI package
import os
from os import walk

# Global variables
programPath = "/home/pi/sketchbook/" # Path to the program directory which contains the programs to be uploaded to the LEDmePlay (can be adopted to your needs)
program = 1                          # Number of first program which is selected
adminModeCounter = 0                 # Helper (admin mode is started if adminModeCounter == 6)


### Startup: Create a list of all available programs

# Create list of subfolder names
programList = os.listdir(programPath)
programList.remove('libraries')

# Iterate over subfolders and check whether expected files are available (.ino file for the Arduino IDE program and .png for the title picture)
deleteList = []
for i in programList:
    if not (os.path.isfile(programPath + i + "/" + i + ".ino") and os.path.isfile(programPath + i + "/" + i + ".png")):
        deleteList.append(i) # Add those folders which not contain the expected files

# Iterate over delete list and remove all contained programs from the program list
for i in deleteList:
    programList.remove(i)

# Sort program list alphabetically
programList = sorted(programList)

# Check number of remaining entries in the programs list
numberOfPrograms=len(programList)

# Output of all programs in the console
print("List of detected programs:")
for i in programList:
    print(i)


### Main window

# Define window
window = tk.Tk()
window.attributes('-type', 'splash') # Removes title bar
window.geometry('480x320')
window.configure(bg="black")

# Define frames
frameProgram = tk.Frame(master = window, relief = tk.RAISED, borderwidth = 0) # Frame with the title screenshot of the selected program
frameControls = tk.Frame(master = window, relief = tk.RAISED, borderwidth = 0) # Frame with the buttons
frameLEDmePI = tk.LabelFrame(master = window, relief = tk.RAISED, borderwidth = 0) # Frame with the LEDmePI label (which is actually a hidden button)
frameMithotronic = tk.LabelFrame(master = window, relief = tk.RAISED, borderwidth = 0) # Frame with the Mithotronic label (which is actually a hidden button)

# Show 1st title screenshot
titlescreen = tk.PhotoImage(file = programPath + programList[0] + "/" + programList[0] + ".png")
labelProgram = tk.Label(master=frameProgram, image=titlescreen)
labelProgram.pack()

# Show title screenshot of the selected program 
def showProgramTitleScreenshot():
    global programList, program
    titlescreen = tk.PhotoImage(file = programPath + programList[program - 1] + "/" + programList[program - 1] + ".png")
    labelProgram.configure(image=titlescreen)
    labelProgram.image=titlescreen

# Go to the last program       
def lastClicked():
    global adminModeCounter, program
    adminModeCounter = 0
    program = program - 1
    if program < 1:
        program = numberOfPrograms
    showProgramTitleScreenshot()

# Go to the next program
def nextClicked():
    global adminModeCounter, program
    adminModeCounter = 0
    program = program + 1
    if program > numberOfPrograms:
        program = 1
    showProgramTitleScreenshot()

# Builds and uploads the currently selected program. If program build is already there, it is directly uploaded (triggered by pop-up; see below).
def upload():
    global programList, program
    os.system("cd " + programPath + programList[program - 1] + " && make upload")
        
# Upload has been confirmed (triggered by pop-up; see below)
def pressUploadOK(messageBox):
    messageBox.destroy()
    
    # Enable buttons in main window
    buttonLast['state'] = tk.NORMAL
    buttonNext['state'] = tk.NORMAL
    buttonUpload['state'] = tk.NORMAL

    # Perform the upload
    upload()

# Upload has been canceled (triggered by pop-up; see below)
def pressUploadCancel(messageBox):
    messageBox.destroy()
    
    # Enable buttons in main window
    buttonLast['state'] = tk.NORMAL
    buttonNext['state'] = tk.NORMAL
    buttonUpload['state'] = tk.NORMAL

# Opens a pop-up window to confirm upload
def uploadClicked():
    
    # Disable buttons in main window
    buttonLast['state'] = tk.DISABLED
    buttonNext['state'] = tk.DISABLED
    buttonUpload['state'] = tk.DISABLED
    
    messageBox = tk.Tk()
    messageBox.focus_set()
    messageBox.attributes('-type','dock')
    messageBox.geometry('480x140')
    messageBox.configure(bg="black", highlightthickness=1, highlightbackground="white")
    frameQuestion = tk.LabelFrame(master = messageBox, relief = tk.RAISED, borderwidth = 0)
    frameAnswer = tk.LabelFrame(master = messageBox, relief = tk.RAISED, borderwidth = 0)
    labelMessage=tk.Label(frameQuestion, text="Do you want to upload the selected program?", fg="white", bg="black", width=48, height=3)
    labelMessage.pack()
    buttonOK=tk.Button(frameAnswer, text="OK", fg="white", bg="black", width=12, height=3, command=lambda: pressUploadOK(messageBox))
    buttonOK.grid(column=0, row=0)
    buttonCancel=tk.Button(frameAnswer, text="Cancel", fg="white", bg="black", width=12, height=3, command=lambda: pressUploadCancel(messageBox))
    buttonCancel.grid(column=2, row=0)
    frameQuestion.pack(side='top')
    frameAnswer.pack()


### Admin mode (required, e.g., for stopping LEDmePI and for a controlled shut-down)

# End kiosk mode and go back to OS
def pressAdminModeEndKioskMode(adminWindow):
    global window
    adminWindow.destroy()
    window.destroy()

# Shutdown Raspberry Pi
def pressAdminModeShutdown(adminWindow):
    os.system("sudo shutdown -h now")

# Leave admin mode
def pressAdminModeBack(adminWindow):
    adminWindow.destroy()
    
    # Enable buttons in main window
    buttonLast['state'] = tk.NORMAL
    buttonNext['state'] = tk.NORMAL
    buttonUpload['state'] = tk.NORMAL

# Build all programs from the programs list
def pressAdminModeBuildEverything(adminWindow):
    global programList, numberOfPrograms
    for i in programList:
        print("Build " + i + " (" + str(programList.index(i) + 1) + "/" + str(numberOfPrograms) + ")")
        os.system("cd " + programPath + i + " && make")

    adminWindow.destroy()
    
    # Enable buttons in main window
    buttonLast['state'] = tk.NORMAL
    buttonNext['state'] = tk.NORMAL
    buttonUpload['state'] = tk.NORMAL

# Remove all builds
def pressAdminModeRemoveAllBuilds(adminWindow):
    global programList, numberOfPrograms
    for i in programList:
        print("Remove " + i + " (" + str(programList.index(i) + 1) + "/" + str(numberOfPrograms) + ")")
        os.system("sudo rm -rf " + programPath + i + "/build-mega2560")

    adminWindow.destroy()
    
    # Enable buttons in main window
    buttonLast['state'] = tk.NORMAL
    buttonNext['state'] = tk.NORMAL
    buttonUpload['state'] = tk.NORMAL
    
# Opens a pop-up window for admin tasks (admin window)
def adminMode():
    
    # Disable buttons in main window
    buttonLast['state'] = tk.DISABLED
    buttonNext['state'] = tk.DISABLED
    buttonUpload['state'] = tk.DISABLED

    adminWindow = tk.Tk()
    adminWindow.focus_set()
    adminWindow.attributes('-type','dock')
    adminWindow.geometry('480x260')
    adminWindow.configure(bg="black", highlightthickness=1, highlightbackground="white")
    frameAdminWindow1 = tk.Frame(master = adminWindow, relief = tk.RAISED, borderwidth = 0)
    frameAdminWindow2 = tk.Frame(master = adminWindow, relief = tk.RAISED, borderwidth = 0)
    frameAdminWindow3 = tk.Frame(master = adminWindow, relief = tk.RAISED, borderwidth = 0)
    frameAdminWindow4 = tk.Frame(master = adminWindow, relief = tk.RAISED, borderwidth = 0)
    
    labelAdminWindow1=tk.Label(frameAdminWindow1, text="Control options", fg="white", bg="black", width=48, height=3)
    labelAdminWindow1.pack()
    buttonKiosk=tk.Button(frameAdminWindow2, text="End kiosk mode", fg="white", bg="black", width=12, height=3, command=lambda: pressAdminModeEndKioskMode(adminWindow))
    buttonKiosk.grid(column=0, row=0)
    buttonShutdown=tk.Button(frameAdminWindow2, text="SHUTDOWN\n(Just now)", fg="white", bg="black", width=12, height=3, command=lambda: pressAdminModeShutdown(adminWindow))
    buttonShutdown.grid(column=1, row=0)
    buttonBack=tk.Button(frameAdminWindow2, text="Back", fg="white", bg="black", width=12, height=3, command=lambda: pressAdminModeBack(adminWindow))
    buttonBack.grid(column=2, row=0)
    labelAdminWindow2=tk.Label(frameAdminWindow3, text="Build options", fg="white", bg="black", width=48, height=3)
    labelAdminWindow2.pack()
    buttonBuildEverything=tk.Button(frameAdminWindow4, text="Build everything\n(Might take long)", fg="white", bg="black", width=12, height=3, command=lambda: pressAdminModeBuildEverything(adminWindow))
    buttonBuildEverything.grid(column=0, row=0)
    buttonRemoveBuilds=tk.Button(frameAdminWindow4, text="Remove all builds", fg="white", bg="black", width=12, height=3, command=lambda: pressAdminModeRemoveAllBuilds(adminWindow))
    buttonRemoveBuilds.grid(column=1, row=0)
    
    frameAdminWindow1.pack(side='top')
    frameAdminWindow2.pack()
    frameAdminWindow3.pack()
    frameAdminWindow4.pack()
    

# Start Admin Mode: The user has to click "LEDmePlay", "Mithotronic", "LEDmePlay", "Mithotronic", "LEDmePlay", "Mithotronic".

# Increases adminModeCounter if conditions are fulfilled
def lEDmePlayClicked():
    global adminModeCounter
    if adminModeCounter == 0 or adminModeCounter == 2 or adminModeCounter == 4:
        adminModeCounter = adminModeCounter + 1
    else:
        adminModeCounter = 0

# Increases adminModeCounter if conditions are fulfilled
def byMithotronicClicked():
    global adminModeCounter
    if adminModeCounter == 1 or adminModeCounter == 3 or adminModeCounter == 5:
        adminModeCounter = adminModeCounter + 1
    else:
        adminModeCounter = 0
    if adminModeCounter == 6:
        adminModeCounter = 0
        adminMode() # Enter admin mode


### Main window: Buttons and layout

# Define buttons
buttonLEDmePI = tk.Button(master=frameLEDmePI, text="LEDmePI V1.0.0", relief="flat", highlightthickness=0, fg="white", bg="black", width=12, height=2, command=lEDmePlayClicked) # Hidden button which looks like a label according to parameters
buttonLEDmePI.grid(column=0, row=0)

buttonLast = tk.Button(master=frameControls, text="Last", fg="white", bg="black", width=12, height=3, command=lastClicked)
buttonLast.grid(column=0, row=0)

buttonNext = tk.Button(master=frameControls, text="Next", fg="white", bg="black", width=12, height=3, command=nextClicked)
buttonNext.grid(column=0, row=1)

labelEmpty = tk.Label(master=frameControls, text="", width=12, height=1)
labelEmpty.grid(column=0, row=3)

buttonUpload = tk.Button(master=frameControls, text="UPLOAD!", fg="white", bg="black", width=12, height=4, command=uploadClicked)
buttonUpload.grid(column=0, row=4)

buttonMithotronic = tk.Button(master=frameMithotronic, text="Mithotronic (2021)", relief="flat", highlightthickness=0, fg="white", bg="black", width=12, height=2, command=byMithotronicClicked) # Hidden button which looks like a label according to parameters
buttonMithotronic.grid(column=0, row=0)

# Pack frames in window
frameProgram.pack(side='left')
frameLEDmePI.pack()
frameControls.pack()
frameMithotronic.pack()

window.mainloop()
