import instaloader
import openpyxl
import os
import time
from os import path
from datetime import datetime
from openpyxl.styles import Font

###
### ---->>  IMPORANT: << ----- 
### YOU NEED TO HAVE A FILE CALLED loginInfo.txt where the first line is your username and the second line is your password
###

# AYO YOU NEED TO CHANGE THIS
printDirectoryEscaped =  "C:\\Users\\James\\Documents\\coding\\python projects\\Instagram\\Book1.xlsx"
printDirectoryNotEscaped = "C:/Users/James/Documents/coding/python projects/Instagram/Book1.xlsx"

###
### This sends a job to your default printer. Some calculations are done to resize the name depending on how long it is.
###
def print_user(username):

    theFile = openpyxl.load_workbook('Book1.xlsx')
    print(theFile.sheetnames)
    currentSheet = theFile['Sheet1']
    
    now = datetime.now()
    currentSheet['A2'].value = username

    fontSize = (22) - ((len(username) - 11) * 1.2)

    fontStyle = Font(size = str(fontSize))
    currentSheet['A2'].font = fontStyle

    currentSheet['A3'].value = str(now.strftime("%H:%M:%S"))
    print(currentSheet['A2'].value , "-> ", currentSheet['A3'].value)

    theFile.save(printDirectoryEscaped)

    time.sleep(1)

    os.startfile(printDirectoryNotEscaped, "print")

def main():
    L = instaloader.Instaloader()

    username = ""
    password = ""

    # You don't have to be logged into this user to get their followeres
    userToGetFollowersFor = "hoppuman_"

    with open('loginInfo.txt' , 'r') as reader:
        loginInfo = reader.readlines()
        username = loginInfo[0].strip()
        password = loginInfo[1].strip()

    L.login(username, password)

    profile = instaloader.Profile.from_username(L.context , userToGetFollowersFor)

    # This is the "In Memory" list (as opposed to the cached list in the text file) 
    myset = set()

    file_created = True
    # Creates a profile of hte current followers, so you don't have to recreate the list every time. You can also load in a new profile to do some testing
    if(path.exists(str(userToGetFollowersFor) + ".txt")):
        file_created = True
        file1 = open(str(userToGetFollowersFor) + ".txt" , "r+")
    else:
        file_created = False
        file1 = open(str(userToGetFollowersFor) + ".txt" , "a+")

    if(file_created):
        Lines = file1.readlines()
        for line in Lines:
             myset.add(line.strip())
             #print(line.strip())
    else:
        print("Loading initial set of followers into file")
        followers = profile.get_followers()
        for follower in followers:
            username = follower.username
            myset.add(username)
            file1.write(username + "\n")

    #loop through followers to see if there is a new one
    count = 0
    userCount = 0
    while(True):
        print("loop: " , count)
        potentialNew = profile.get_followers()
        for followee in potentialNew:
            username = followee.username
            userCount = userCount + 1
            if(userCount % 1000 == 0):
                print(userCount)
            if username not in myset:
                print("new follower found: " , username)
                myset.add(username)
                print_user(username)
                file1.write("\n" + username)

        # The Instagram API will terminate your account if you query it too much
        # I am not sure how long this should be set ot just yet but if it starts to try to delete your account then add in this value
        #time.sleep(300)
        
        # Close the File
        file1.close()
        break

print_user("testuser")
#main()