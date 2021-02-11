LEDmePI

www.mithotronic.de

Version: 1.0.0
Author: Michael Rosskopf (2021)
Many thanks to Thomas Laubach

Release Notes:
V1.0.0: First release (07.02.2021)

LEDmePI is a tool to use a Raspberry Pi 3 as a LEDmePlay programmer. It requires Python 3.x and the Arduino Makefile (see https://github.com/sudar/Arduino-Makefile) which can be installed by typing "sudo apt-get install arduino-mk" into the console. The tool has been optimized for the usage with an MHS3528 display since the size of its window fits perfectly to the MHS3528 (see http://www.lcdwiki.com/3.5inch_RPi_Display). However, you can also use it with normal screens.

Programs to be uploaded to the LEDmePlay must be stored in a folder "/home/pi/sketchbook". They must be stored in a subfolder with the same name than the name of the program. It is also required to store a png-image (e.g., a title picture) and a copy of the "Makefile" which is located in the "LEDmePI" folder. As an example, assume you want to add "KeenKenny_LEDmePlay_V1_1_1". In this case you need the following structure:

sketchbook
|-KeenKenny_LEDmePlay_V1_1_1
  |-KeenKenny_LEDmePlay_V1_1_1.ino
  |-KeenKenny_LEDmePlay_V1_1_1.png
  |-Makefile

Programs which fulfill these conditions are automatically detected. Attach a LEDmePlay via USB, open a console, and navigate to the directory in which LEDmePI is stored (we recommend "/home/pi/LEDmePI"): Enter "python3 ./LEDmePI_V1_0_0.py" to start the program. You can also copy the file "ledmepi.desktop" to "/home/pi/Desktop" and double-click the LEDmePI icon. Use the buttons "Last" and "Next" to switch between the programs and press "UPLOAD!" to upload the program to the LEDmePlay. This must be confirmed in a pop-up dialog. If you upload a program for the first time, it must be built before. This is triggered automatically and might take some time.

To end the tool, you have to enter the admin mode. Just click the labels "LEDmePlay", "Mithotronic", "LEDmePlay", "Mithotronic", "LEDmePlay", "Mithotronic" (these are actually hidden buttons), to open the admin mode window. You can end the program ("End kiosk mode") or shut down the Raspberry Pi ("Shutdown"). Furthermore, you can build all programs in advance to save time if you upload something for the first time ("Build everything").
