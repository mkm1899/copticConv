import sys
import os
import shiftAccent


#if len(sys.argv) < 3:
#    print("need to add file name as argument. For example:")
#    print("python convCoptToUni.py [file_name].pdf [output_file_name]")
#    sys.exit()


randomTempFolderName = "temp2935185167"
arguments = []

def options():
    options = 0
    for i in range(0, len(sys.argv)):
        if sys.argv[i][0] == '-' and sys.argv[i][1] == '-':
            if sys.argv[i][2:].lower() == 'help':
                options = options | 1
            elif sys.argv[i][2:].lower() == 'noshift':
                options = options | 2
            elif sys.argv[i][2:].lower() == 'seperatefiles':
                options = options | 4
        elif sys.argv[i][0] == '-':
            if sys.argv[i][1].lower() == 'h':
                options = options | 1
            elif sys.argv[i][1].lower() == 'n':
                options = options | 2
            elif sys.argv[i][1].lower() == 's':
                options = options | 4
        else:
            arguments.append(sys.argv[i]) #arguments does not include options
    return options 

def asksHelp(optionsRequested):
    return ((optionsRequested & 1) == 1)

def asksNoShift(optionsRequested):
    return ((optionsRequested & 2) == 2)

def asksSeperateFiles(optionsRequested):
    return ((optionsRequested & 4) == 4)

#converts image to textFile
def convertImagesToText(optionsRequested, isPdf):
    folder = ".\\" + randomTempFolderName + "\\"
    
    if asksSeperateFiles(optionsRequested) and isPdf:
        files = os.listdir(".\\" + randomTempFolderName)
        i = 0
        for x in files:
            if ".png" in x:
                os.system("tesseract " + folder + x + " " + arguments[2] + "-" + str(i) + " -l cop")
                if not asksNoShift(optionsRequested):
                    shiftAccent.shiftAccent(arguments[2] + "-" + str(i) + ".txt")
                i+=1

    #from pdf but wants the output it one file            
    elif isPdf:
        #print("HERE")
        files = os.listdir(".\\" + randomTempFolderName)
        i = 0
        for x in files:
            if ".png" in x:
                if i == 0: 
                    os.system("tesseract " + folder + x + " stdout -l cop > " + arguments[2] + ".txt") #this makes sure to empty the file before write
                    #print("HERE 68")
                else: os.system("tesseract " + folder + x + " stdout -l cop >> " + arguments[2] + ".txt")
                i+=1
        if not asksNoShift(optionsRequested):
            shiftAccent.shiftAccent(arguments[2] + ".txt")
    
    else:
        os.system("tesseract " + '"' + arguments[1] + '"' + " stdout -l cop > " + arguments[2] + ".txt ")
        if not asksNoShift(optionsRequested):
            shiftAccent.shiftAccent(arguments[2] + ".txt")

    #print("something else")



optionsRequested = options()

if  asksHelp(optionsRequested):
    print("standard use:")
    print("\t python convCoptToUni.py [file_name].pdf [output_file_name] -[options]")
    print("\t python convCoptToUni.py [picture_name] [output_file_name] -[options]")
    print("options include:")
    print("\t -h or --help for help: python convCoptToUni.py -h")
    print("\t -n or --noShift to remove the accent shifting I made to counter the flaw in the tesseract model.")
    print("\t\t Use -n if all the accents are shifted to the left of where it is supposed to be")
    print("\t -s or --seperateFiles to seperate each page of a pdf into its own seperate text file")
    print("\t python convCoptToUni.py [file_name].pdf[page_lower-page_higher] [output_file_name] -[options]")
    print("\t python convCoptToUni.py [file_name].pdf[page_num] [output_file_name] -[options]")
    print("\t\t NOTE PAGE NUMBERS START AT 0")
    sys.exit()

if len(arguments) < 3:
    print("need to add file name as argument. For example:")
    print("python convCoptToUni.py [file_name].pdf [output_file_name]")
    print("For more help use -h or --help option")
    sys.exit()

#since I removed all options in sys.argv[] in arguments[] that means arguments[1] has the file that needs to be converted assuming user put it in the right order
if ".pdf" in arguments[1]:
    #creates temporary folder with randomTempFolderName above
    os.mkdir(".\\" + randomTempFolderName)
    #converts pdf to a set of images
    os.system("magick -density 300 " + sys.argv[1] + " .\\" + randomTempFolderName+ "\\" + "x.png")
    
    #removes page bounds
    for i in range(len(arguments[1])-1, 0, -1):
        if arguments[1][i] == '[':
            arguments[1] = arguments[1][0:i]
            break
        elif arguments[1][i] == '.':
            break
    
    #converts set of images into
    convertImagesToText(optionsRequested, True)
    os.system("rmdir /s/q .\\" + randomTempFolderName)
else:
    convertImagesToText(optionsRequested, False)
