#for whatever reason the tesseract model consistently puts the ̀  on top of the character to the right of where it is supposed to be   

def assignCharinStr(string, index, char):
    string = string[:index] + char + string[index+1:]
    return string

def shiftAccent(fileName):
    f = open(fileName, "r", encoding="utf8")

    text = f.read()

    f.close()

    for i in range(len(text)):
        if text[i] == '̀' and text[i-1] != ' ':
            text = assignCharinStr(text, i, text[i-1])
            text = assignCharinStr(text, i-1, '̀')
            
    output = open("output.txt", "w", encoding="utf8")

    output.write(text)

    output.close()