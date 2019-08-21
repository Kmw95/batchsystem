"""
Solution for COMP07027 Coursework 2018
written by:  B00307869 and B00312913
"""

#These modules are imported in order for the program to manage files and display an interface for user input
import easygui #use of easygui boxes for user input and selection:  http://easygui.sourceforge.net/
import json
from datetime import *
import os

#Classes Batch used for user input to save the batch number, component type, size, number of components and date
class Batch:
    def __init__(self, batchno):
        self.type = ""
        self.size = ""
        self.batchno = batchno
        self.noofcomponents = 0
        self.date = ""

#this function prints the details from class Batch
    def printbatch(self): #function prints the details of a newly created batch based on user input
        print(self.batchno)
        print(self.noofcomponents)
        print(self.type)
        print(self.size)
        print(self.date)

#Class Component used for the individual component number
class Component:
    def __init__(self, num):
        self.number = num

#function prints component number
    def printcomponent(self):
        print(self.number)

#creates a new batch for user input
def newbatch():
    manufacturedate = datetime.today() #the date the batch is manufctured which is todays date
    with open("batchindex.json", "r") as f: #reads in the "batchindex" json file to append newly created batch numbers
        indata = json.load(f)
        f.close()
    mylist = indata["UsedBatches"]
    if len(mylist) == 0: #if there is no batch number, create one, otherwise, start with the first batch number
        batchindex = 1
    else:
        batchindex = len(mylist) + 1
    print("List of numbers extracted from dictionary :", mylist) #prints existing batch numbers
    batchno = int((manufacturedate.strftime("%d%m%y")+ "{0:04}".format(batchindex))) #formats the batch number of DDMMYY0001 (formatting of manufacturedate: https://docs.python.org/2/library/datetime.html)
    mylist.append(batchno) #appends the batch number to a list
    outdata = {"UsedBatches" : mylist}
    with open("batchindex.json", "w") as f: #writes in the batch list into the json file
        json.dump(outdata, f)
    f.close()
    newbatch = Batch(batchno)

    #allows a user to select how many components they want
    newbatch.noofcomponents = (easygui.integerbox(msg="How many components in this batch?(1-9999)", default=1, lowerbound=1, upperbound=9999))

    #allows user to select the component type they want which prints the choice they select
    newbatch.type = easygui.choicebox(msg="Select Component Type", choices=["Winglet Strut", "Door Handle", "Rudder Pin"])
    if newbatch.type == "Winglet Strut":
        print("Winglet Strut")
    elif newbatch.type == "Door Handle":
        print("Door Handle")
    elif newbatch.type == "Rudder Pin":
        print("Rudder Pin")

    #Allows a user to select a component size out of the two options
    newbatch.size = easygui.buttonbox(msg="Select Component Size", choices=["A320 Series", "A380 Series"])
    if newbatch.size == "A320 Series":
        print("A320 Series")
    elif newbatch.size == "A380 Series":
        print("A380 Series")

    newcomplist = [] #a list for the new components
    componentstatus = [] #list of the component status
    for n in range(1,newbatch.noofcomponents+1): #creates selected number of components based on how many components the user wants
        batchnostr, strn = batchno, "{0:04}".format(n)
        number = "{0}-{1}".format(batchno, strn) #formats the new component numbers as a string.  Source used to format as a strong: https://stackoverflow.com/questions/15593775/python-joining-string-expressions-with-a-hyphen
        newcomp = Component(number)
        newcomp.printcomponent() #prints the new copmonent numbers
        newcomplist.append(number) #appends the new component numbers to the new component list
        componentstatus.append(number + ": Unfininshed Work") #prints the component number with their unfinished status

    #result asking the user to verify the right input, while formatting these variables into a string
    result=("This batch contains %d %s %s is this correct? Y/N") % (newbatch.noofcomponents, newbatch.type, newbatch.size)
    yn = easygui.ynbox(result) #input the result varliable message into an easygui yes/no box
    if yn is False: #if the user selects no, it returns them to the main menu
        main()
    else:
        hhmm = str(manufacturedate)
        ddmmyy = str(datetime.now().strftime("%H:%M"))
        dt=("Batch and Component records created at %s on %s") % (ddmmyy, hhmm) #prints the date and time of when the users new batch was created
        easygui.msgbox(dt) #input the date time message into an easygui message box to be displayed to the user

    #asks the user if they want to see their batch details
    showdetails = "Show batch details? Y/N"
    yn = easygui.ynbox(msg=showdetails)
    if yn is False: #if the user selects no, it returns them to the main menu
        main()
    else: #if the user selects yes, this prints out their batch details
        batchno = "Batch Number: %s" % newbatch.batchno
        type = "\nComponent Type: %s" % newbatch.type #\n makes the message take a new line after each batch attribute to be displayed to the user properly
        size = "\nComponent Size: %s" % newbatch.size #%s inserts the new batch attribute into the string without any awkward or additional formatting to the variable
        noofcomponents = "\nNumber of Components: %s" % newbatch.noofcomponents
        serialnos = "\nSerial Numbers: %s" % newcomplist
        componentstatus = "\nComponent Status: %s" % componentstatus
        easygui.msgbox(msg=batchno + type + size + noofcomponents + serialnos + componentstatus) #prints the batch details into a user friendly easygui message box
    main() #returns the user to the main menu after completion of batch details


#main menu when the user starts the program
def main():
    done = ""
    while done != "QUIT":
        done = easygui.buttonbox(title="Welcome to PPEC Inventory System", msg="Choose an Option", choices=["CREATE","QUIT"]) #easygui menu to either create a new batch or quit the program
        if done == "CREATE":
            newbatch() #if the user selects "create", it begins to create a new batch
        else:
            easygui.msgbox(msg="Goodbye") #if the user selects "Quit" or the exit button, this will quit the program
            quit(0)


#this checks if a file exists, and creates it if it can't be found
if __name__ == "__main__":
    id_list = []
    outdata = {"UsedBatches": id_list}
    if not os.path.exists("batchindex.json"):
        with open("batchindex.json", "w") as f:
            json.dump(outdata, f)
        f.close()
    main()
