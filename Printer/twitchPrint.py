import openpyxl
import os
import time

if __name__ == "__main__":
    subName = '500'
    message = 'mixed'

    theFile = openpyxl.load_workbook('Book1.xlsx')
    print(theFile.sheetnames)
    currentSheet = theFile['Sheet1']

    currentSheet['A1'].value = subName
    currentSheet['A2'].value = message

    print(currentSheet['A1'].value)

    theFile.save("C:\\Users\\James\\Documents\\coding\\python projects\\Printer\\Book1.xlsx")

    time.sleep(1)

    os.startfile("C:/Users/James/Documents/coding/python projects/Printer/Book1.xlsx", "print")

