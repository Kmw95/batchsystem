"""
Solution for COMP07027 Coursework 2018
written by:  B00307869 and B00312913
"""

#These modules are imported in order for the program to manage files and display an interface for user input
import easygui #use of easygui boxes for user input and selection:  http://easygui.sourceforge.net/
import json
from datetime import *
import os
import pickle
from pprint import *

#Classes Batch used for user input to save the batch number, component type, size, number of components and date
class Batch:
    def __init__(self, batchno):
        self.type = ""
        self.size = ""
        self.batchno = batchno
        self.noofcomponents = 0
        self.date = ""
        self.newcomplist = []
        self.componentstatus = []

#this function prints the details from class Batch
    def printbatch(self): #function prints the details of a newly created batch based on user input
        print(self.batchno)
        print(self.noofcomponents)
        print(self.type)
        print(self.size)
        print(self.date)
        print(self.newcomplist)

#Class Component used for the individual component number
class Component:
    def __init__(self, num):
        self.batchno = num

#function prints component number
    def printcomponent(self):
        print(self.batchno)

#creates new batch as pickle file
def makefile(batch):
    print(type(batch))
    filename = str(batch.batchno) + ".pck"
    f = open(filename, "wb")
    pickle.dump(batch, f)
    f.close()

#reads back file contents contained in a pickle file
def readfile(batchno):
    filename = str(batchno) + ".pck"
    if os.path.exists(filename):
        f1 = open(filename, "rb")
        file_contents = pickle.load(f1)
        print(type(file_contents))
        return file_contents
    else:
        return 0

#creates a new batch for user input
def newbatch():
    manufacturedate = datetime.today()#the date the batch is manufctured which is todays date
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
    newbatch.date = manufacturedate.strftime("%d/%m/%y")
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

    makefile(newbatch) #creates the pickle file of the new batch
    thisbatch = readfile(newbatch.batchno) #reads the file named after its batch number
    if thisbatch == 0:
        easygui.msgbox(msg="ERROR - The file is either missing or corrupt")
    else:
        pprint(thisbatch)

    #creates the new component numbers and appends them to a list
    for n in range(1,newbatch.noofcomponents+1): #creates selected number of components based on how many components the user wants
        batchnostr, strn = batchno, "{0:04}".format(n)
        number = "{0}-{1}".format(batchno, strn) #formats the new component numbers as a string.  Source used to format as a strong: https://stackoverflow.com/questions/15593775/python-joining-string-expressions-with-a-hyphen
        newcomp = Component(number)
        newcomp.printcomponent()#prints the new copmonent numbers
        newbatch.newcomplist.append(number) #appends the new component numbers to the new component list
        newbatch.componentstatus.append(number + ": Unfininshed Work") #prints the component number with their unfinished status
        makefile(newcomp)

    #result asking the user to verify the right input, while formatting these variables into a string
    result=("This batch contains %d %s %s is this correct? Y/N") % (newbatch.noofcomponents, newbatch.type, newbatch.size)
    yn = easygui.ynbox(result) #input the result varliable message into an easygui yes/no box
    if yn is False: #if the user selects no, it returns them to the main menu
        main()
    else:
        hhmm = str(manufacturedate)
        ddmmyy = str(datetime.now().strftime("%H:%M"))
        dt=("Batch and Component records created at %s on %s") % (ddmmyy, hhmm)
        easygui.msgbox(dt)

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
        serialnos = "\nSerial Numbers: %s" % newbatch.newcomplist
        componentstatus = "\nComponent Status: %s" % newbatch.componentstatus
        easygui.msgbox(msg=batchno + type + size + noofcomponents + serialnos + componentstatus) #prints the batch details into a user friendly easygui message box
    main() #returns the user to the main menu after completion of batch details

#allows user to search for specific batch to view their details
def viewbatchdetails():
    with open("batchindex.json", "r") as f: #reads json data
        indata = json.load(f)
        f.close()
    mylist = indata["UsedBatches"]
    n = 0
    batchno = easygui.integerbox(msg="Enter batch number:", upperbound=9999999999) #user can input batch number to search for specific batch
    while n < len(mylist):
        filename = str(batchno) + ".pck"
        if os.path.exists(filename):
            batchno = mylist[n]
            f1 = open(filename, "rb")
            file_contents = pickle.load(f1)
            f1.close()
            btchno = "Batch Number: %s" % file_contents.batchno #returns the following attributes of the batch
            date = "\nManufacturedate: %s" % file_contents.date
            typ = "\nComponent Type: %s" % file_contents.type
            sze = "\nComponent Size: %s" % file_contents.size
            quanty = "\nNumber of Components %s" % file_contents.noofcomponents
            serialno = "\nSerial Numbers: %s" % file_contents.newcomplist
            status = "\nComponent Status: %s" % file_contents.componentstatus
            details = easygui.msgbox(btchno + date + typ + sze + quanty + serialno + status) #displays attributes in easygui message box
            break
        else:
            easygui.msgbox(msg="Batch not found") #if there is no batch, returns error message
            break

#allows user to search for specific component
def viewcomponents():
    with open("batchindex.json", "r") as f: #reads json data
        indata = json.load(f)
        f.close()
    mylist = indata["UsedBatches"]
    n = 0
    newcomp = easygui.integerbox(msg="Enter component serial number", upperbound=99999999999999) #user inputs component number
    while n < len(mylist):
        filename = str(newcomp) + ".pck"
        if os.path.exists(filename):
            newcomp = mylist[n]
            f1 = open(filename, "rb") #reads back the pickle file
            file_contents = pickle.load(f1)
            f1.close()
            msg = "Component Details for %s" % newcomp #returns following file contents from pickle file
            typ = "\nType: %s" % file_contents.type
            siz = "\nSize: %s" % file_contents.size
            date = "\nDate: %s" % file_contents.date
            stat = "\nCurrent Status: %s" % file_contents.componentstatus
            part = "\nPart of Batch: %s" % file_contents.batchno
            details = easygui.msgbox(msg + typ + siz + date + stat + part)
            break
        else:
            easygui.msgbox(msg="Component not found") #error message if component can't be found
            break

#lists all existing batches saved
def listallbatches():
    with open("batchindex.json", "r") as f: #reads json data
        indata = json.load(f)
        f.close()
    mylist = indata["UsedBatches"]
    n = 0
    displaystring = ("\tBatch#\t \tType\t \tSize\t \tQuantity Made\t") #displays the headers for each batch attribute in a tabular format
    while n < len(mylist):
        n = n+1
        batchno = mylist[n-1]
        filename = str(batchno) + ".pck"
        if os.path.exists(filename):
            f1 = open(filename, "rb") #reads back pickle files
            file_contents = pickle.load(f1)
            f1.close()
            batch = file_contents.batchno
            typ = file_contents.type
            sze = file_contents.size
            qunty = file_contents.noofcomponents
            details = ("\t{0}\t \t{1}\t \t{2}\t \t{3}\t").format(batch, typ, sze, qunty) #returns following batch attributes in a tabular format
            displaystring = (displaystring + "\n" + (details))#connects the headers for each batch attribute and the details of the batch information
    batchlist = easygui.msgbox(msg=displaystring)
    main()

#main menu when the user starts the program
def main():
    done = ""
    while done != "QUIT":
        done = easygui.buttonbox(title="Welcome to PPEC Inventory System", msg="Choose an Option", choices=["CREATE","QUIT","View details of Batch", "View details of Component","List all Batches",])
        if done == "CREATE": #if the user selects one of the easygui buttons, it calls the function to begin user input and selection
            newbatch()
        elif done == "View details of Batch":
            viewbatchdetails()
        elif done == "View details of Component":
            viewcomponents()
        elif done == "List all Batches":
            listallbatches()
        elif done == "QUIT":
            easygui.msgbox(msg="Goodbye")
            exit(0)
        else:
            exit(0)

#this checks if a file exists, and creates it if it can't be found
if __name__ == "__main__":
    id_list = []
    outdata = {"UsedBatches": id_list}
    if not os.path.exists("batchindex.json"):
        with open("batchindex.json", "w") as f:
            json.dump(outdata, f)
        f.close()
    main()
