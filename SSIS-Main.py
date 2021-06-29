from os import name
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import BOLD, Font

import sqlite3
import calls

# Setting up tables
calls.databaseSetup()

TITLE = ("Arial", 40, BOLD)
SUBTITLE = ("Arial", 32, BOLD)

# Configuring root window
root = Tk()
root.title('Student Information System')
# root window geomtry
root.geometry("1300x700")
root.minsize(950,550)
root.resizable(True, True)


# Global variable data from database
#data = []
idTracker = ''

# Title for main window
titleApp = tk.Label(root, text='Student Information System', font=TITLE)
titleApp.place(anchor=W, relx=0.05, rely=0.1)

# TREEVIEW OF ALL STUDENTS
# treeview frame contain self and scrollbar
treeViewContainer = tk.LabelFrame(root, text='')
treeViewContainer.place(anchor=N, relx=0.5, rely=0.2, relwidth=0.9, relheight=0.75)
treeViewFrame = tk.Frame(treeViewContainer)
treeViewFrame.place(anchor=N, relx=0.5, rely=0.05, relwidth=0.94, relheight=0.75)

# treeview scrollbar
treeviewScrollbar = tk.Scrollbar(treeViewFrame)
treeviewScrollbar.pack(fill='y', side='right')

# treeview
treeView = ttk.Treeview(treeViewFrame, yscrollcommand=treeviewScrollbar.set)
treeView['columns'] = (
    "ID_Number", "Name", "Age", "Gender", "Year_Level", "Course_Code")
treeView.column("#0", width=0, stretch="NO")
treeView.column("ID_Number", anchor="center", width=30)
treeView.column("Name", anchor="w", width=250)
treeView.column("Age", anchor="center", width=10)
treeView.column("Gender", anchor="center", width=20)
treeView.column("Year_Level", anchor="center", width=10)
treeView.column("Course_Code", anchor="w", width=175)

treeView.heading("ID_Number", text="ID Number", anchor="center")
treeView.heading("Name", text="Name", anchor="w")
treeView.heading("Age", text="Age", anchor="center")
treeView.heading("Gender", text="Gender", anchor="center")
treeView.heading("Year_Level", text="Year", anchor="center")
treeView.heading("Course_Code", text="Course Code", anchor="w")

treeView.place(anchor=W, relx=0, rely=0.5, relwidth=0.985, relheight=1)

# MAIN FUNCTIONS
#def onFocus():

def addStudentWindow():
    newWindow = Toplevel(root)
    newWindow.title("Add New Student")
    newWindow.geometry("550x450")
    newWindow.resizable(False, False)
    newWindow.grab_set()

    addStudentFrame = tk.LabelFrame(newWindow, text="New Student Details")
    addStudentFrame.place(anchor=N, relx=0.5, rely=0.05, relwidth=0.9, relheight=0.83)

    # window grid configuration
    addStudentFrame.rowconfigure(0, weight=1)
    addStudentFrame.rowconfigure(1, weight=1)
    addStudentFrame.rowconfigure(2, weight=1)
    addStudentFrame.rowconfigure(3, weight=1)
    addStudentFrame.rowconfigure(4, weight=1)
    addStudentFrame.rowconfigure(5, weight=1)
    addStudentFrame.columnconfigure(0, weight=1)
    addStudentFrame.columnconfigure(1, weight=2)

    # Labels and Entries
    idNumberLabel = ttk.Label(addStudentFrame, text='ID Number')
    nameLabel = ttk.Label(addStudentFrame, text='Name')
    ageLabel = ttk.Label(addStudentFrame, text='Age')
    genderLabel = ttk.Label(addStudentFrame, text='Gender')
    yearLabel = ttk.Label(addStudentFrame, text='Year')
    courseCodeLabel = ttk.Label(addStudentFrame, text='Course Code')

    idNumberEntry = ttk.Entry(addStudentFrame)
    nameEntry = ttk.Entry(addStudentFrame)
    ageEntry = ttk.Entry(addStudentFrame)
    genderEntry = ttk.Entry(addStudentFrame)
    yearEntry = ttk.Entry(addStudentFrame)
    courseCodeEntry = ttk.Entry(addStudentFrame)

    idNumberLabel.grid(row=0, column=0, sticky=W, padx=(30,0), pady=(20,3))
    nameLabel.grid(row=1, column=0, sticky=W, padx=(30,0), pady=3)
    ageLabel.grid(row=2, column=0, sticky=W, padx=(30,0), pady=3)
    genderLabel.grid(row=3, column=0, sticky=W, padx=(30,0), pady=3)
    yearLabel.grid(row=4, column=0, sticky=W, padx=(30,0), pady=3)
    courseCodeLabel.grid(row=5, column=0, sticky=W, padx=(30,0), pady=(3,20))

    idNumberEntry.grid(row=0, column=1, ipady=3, padx=(0,30), pady=(20,3), sticky=EW)
    nameEntry.grid(row=1, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    ageEntry.grid(row=2, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    genderEntry.grid(row=3, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    yearEntry.grid(row=4, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    courseCodeEntry.grid(row=5, column=1, ipady=3, padx=(0,30), pady=(3,20), sticky=EW)

    # primary validation for duplicate ID Number
    def validate():
        idEnt = idNumberEntry.get()
        nameEnt = nameEntry.get()
        ageEnt = ageEntry.get()
        genEnt = genderEntry.get()
        yrEnt = yearEntry.get()
        crsEnt = courseCodeEntry.get()
        idEntVal = idNumberEntry.get()

        # showing error if entries are not complete
        if idEnt == '' or nameEnt == '' or ageEnt == '' or genEnt =='' or yrEnt == '' or crsEnt == '':
            messagebox.showerror(title='Error', message='Make sure to fill every information before adding new student.')
            return

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("SELECT ID_Number FROM Students WHERE ID_Number='{}'".format(idEntVal))
        output = cur.fetchone()
        conn.close()
        
        # checks fetchone output if None or existing
        if output == None:
            addStudent()
            return
        else:
            messagebox.showerror(title='Error', message='ID Number already exists.')

    # Add student after validation
    def addStudent():
        idEnt = idNumberEntry.get()
        nameEnt = nameEntry.get()
        ageEnt = ageEntry.get()
        genEnt = genderEntry.get()
        yrEnt = yearEntry.get()
        crsEnt = courseCodeEntry.get()
        
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Students(ID_Number, Name, Age, Gender, Year_Level, Course_Code) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(idEnt, nameEnt, ageEnt, genEnt, yrEnt, crsEnt))
        conn.commit()
        conn.close()
        newWindow.destroy()
        populateTreeView()

    def cancel():
        idEnt = idNumberEntry.get()
        nameEnt = nameEntry.get()
        ageEnt = ageEntry.get()
        genEnt = genderEntry.get()
        yrEnt = yearEntry.get()
        crsEnt = courseCodeEntry.get()

        if idEnt == '' and nameEnt == '' and ageEnt == '' and genEnt == '' and yrEnt == '' and crsEnt == '':
            newWindow.destroy()
        else:
            decision = messagebox.askyesno(title='Cancel Add Student', message='Are you sure you would like to cancel?')
            if decision == FALSE:
                return
            else:
                newWindow.destroy()

    # ADD and CANCEL Button
    addStudentConfirm = ttk.Button(newWindow, text='Add Student',
                                   command=validate)
    cancelButton = ttk.Button(newWindow, text='Cancel',
                              command=cancel)
    addStudentConfirm.place(anchor=E, relx=0.95, rely=0.93, y=3, relwidth=0.25, relheight=0.06)
    cancelButton.place(anchor=E, relx=0.67, rely=0.93, y=3, relwidth=0.25, relheight=0.06)

def updateStudentWindow():
    updateWindow = Toplevel(root)
    updateWindow.title("Update Student")
    updateWindow.geometry("550x450")
    updateWindow.resizable(False, False)
    updateWindow.grab_set()

    addStudentFrame = tk.LabelFrame(updateWindow, text="Student Details")
    addStudentFrame.place(anchor=N, relx=0.5, rely=0.05, relwidth=0.9, relheight=0.83)

    # window grid configuration
    addStudentFrame.rowconfigure(0, weight=1)
    addStudentFrame.rowconfigure(1, weight=1)
    addStudentFrame.rowconfigure(2, weight=1)
    addStudentFrame.rowconfigure(3, weight=1)
    addStudentFrame.rowconfigure(4, weight=1)
    addStudentFrame.rowconfigure(5, weight=1)
    addStudentFrame.columnconfigure(0, weight=1)
    addStudentFrame.columnconfigure(1, weight=2)

    # Labels and Entries
    idNumberLabel = ttk.Label(addStudentFrame, text='ID Number')
    nameLabel = ttk.Label(addStudentFrame, text='Name')
    ageLabel = ttk.Label(addStudentFrame, text='Age')
    genderLabel = ttk.Label(addStudentFrame, text='Gender')
    yearLabel = ttk.Label(addStudentFrame, text='Year')
    courseCodeLabel = ttk.Label(addStudentFrame, text='Course Code')

    idNumberEntry = ttk.Entry(addStudentFrame)
    nameEntry = ttk.Entry(addStudentFrame)
    ageEntry = ttk.Entry(addStudentFrame)
    genderEntry = ttk.Entry(addStudentFrame)
    yearEntry = ttk.Entry(addStudentFrame)
    courseCodeEntry = ttk.Entry(addStudentFrame)

    idNumberLabel.grid(row=0, column=0, sticky=W, padx=(30,0), pady=(20,3))
    nameLabel.grid(row=1, column=0, sticky=W, padx=(30,0), pady=3)
    ageLabel.grid(row=2, column=0, sticky=W, padx=(30,0), pady=3)
    genderLabel.grid(row=3, column=0, sticky=W, padx=(30,0), pady=3)
    yearLabel.grid(row=4, column=0, sticky=W, padx=(30,0), pady=3)
    courseCodeLabel.grid(row=5, column=0, sticky=W, padx=(30,0), pady=(3,20))

    idNumberEntry.grid(row=0, column=1, ipady=3, padx=(0,30), pady=(20,3), sticky=EW)
    nameEntry.grid(row=1, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    ageEntry.grid(row=2, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    genderEntry.grid(row=3, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    yearEntry.grid(row=4, column=1, ipady=3, padx=(0,30), pady=3, sticky=EW)
    courseCodeEntry.grid(row=5, column=1, ipady=3, padx=(0,30), pady=(3,20), sticky=EW)

    # Filling Entries in Update window from database using ID_Number
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students WHERE ID_Number='{}'".format(idTracker))
    fetch = cur.fetchone()
    # inserting data from fetch to entries
    idNumberEntry.insert(0, fetch[0])
    idNumberEntry.configure(state=DISABLED)
    nameEntry.insert(0, fetch[1])
    ageEntry.insert(0, fetch[2])
    genderEntry.insert(0, fetch[3])
    yearEntry.insert(0, fetch[4])
    courseCodeEntry.insert(0, fetch[5])

    def updateStudent():
        # retrieving values from entries
        nameEnt = nameEntry.get()
        ageEnt = ageEntry.get()
        gendEnt = genderEntry.get()
        yrEnt = yearEntry.get()
        crsEnt = courseCodeEntry.get()

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("UPDATE Students SET Name='{}', Age='{}', Gender='{}', Year_Level='{}', Course_Code='{}' WHERE ID_Number='{}'".format(nameEnt, ageEnt, gendEnt, yrEnt, crsEnt, idTracker))
        conn.commit()
        conn.close()

        updateStudentButton.configure(state=DISABLED)
        removeStudentButton.configure(state=DISABLED)
        updateWindow.destroy()
        populateTreeView()

    # cancel action confirmation
    def cancel():
        decision = messagebox.askyesno(title='Cancel Action', message='Are you sure you would like to cancel updating this student?')
        if decision == FALSE:
            return
        else:
            updateWindow.destroy()


    updateStudentConfirm = ttk.Button(updateWindow, text='Update Student', command=updateStudent)
    cancelButton = ttk.Button(updateWindow, text='Cancel', command=cancel)
    updateStudentConfirm.place(anchor=E, relx=0.95, rely=0.93, y=3, relwidth=0.25, relheight=0.06)
    cancelButton.place(anchor=E, relx=0.67, rely=0.93, y=3, relwidth=0.25, relheight=0.06)\

def removeStudent():
    decision = messagebox.askyesno(title='Remove Student', message='Are you sure you would like to remove this student? This action cannot be undone.')
    if decision == FALSE:
        return
    else:
        global idTracker
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM Students WHERE ID_Number='{}'".format(idTracker))
        conn.commit()
        conn.close()

        idTracker = ''

        messagebox.showinfo(title='Student Removed', message='Student has been successfully removed.')
        updateStudentButton.configure(state=DISABLED)
        removeStudentButton.configure(state=DISABLED)
        populateTreeView()

def populateTreeView():
    treeView.delete(*treeView.get_children())
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students ORDER BY ID_Number")
    fetch = cur.fetchall()
    for data in fetch:
        treeView.insert("", tk.END, values=data)
    conn.close()
    return

def select(x):
    updateStudentButton.configure(state=NORMAL)
    removeStudentButton.configure(state=NORMAL)
    highlight = treeView.focus()
    values = treeView.item(highlight, 'values')
    global idTracker
    idTracker = values[0]
    print(idTracker)

#val

# fill treeview on run
populateTreeView()
treeView.bind('<<TreeviewSelect>>', select)
#treeView.bind('<<TreeviewSelect>>', treeViewSelect)

# Action buttons
addStudentButton = ttk.Button(treeViewContainer, text='Add New Student',
                              command=addStudentWindow)
updateStudentButton = ttk.Button(treeViewContainer, text='Update Student',
                                 command=updateStudentWindow)
removeStudentButton = ttk.Button(treeViewContainer, text='Remove Student',
                                 command=removeStudent)

addStudentButton.place(anchor=W, relx=0.03, rely=0.9, relwidth=0.15, relheight=0.1)
updateStudentButton.place(anchor=W, relx=0.2, rely=0.9, relwidth=0.15, relheight=0.1)
removeStudentButton.place(anchor=W, relx=0.37, rely=0.9, relwidth=0.15, relheight=0.1)

updateStudentButton.configure(state=DISABLED)
removeStudentButton.configure(state=DISABLED)

# Filter treeview
filterFrame = tk.LabelFrame(treeViewContainer, background='#DFDFDF')
filterLabel = tk.Label(filterFrame, text='Filter:', background='#DFDFDF')
filterEntry = tk.Entry(filterFrame)
filterFrame.place(anchor=E, relx=0.97, rely=0.9, relwidth=0.3, relheight=0.1)
# configuring grid layout in filterFrame
filterFrame.rowconfigure(0, weight=1)
filterFrame.columnconfigure(0, weight=1)
filterFrame.columnconfigure(1, weight=5)
filterLabel.grid(row=0, column=0, sticky=NSEW)
filterEntry.grid(row=0, column=1, ipady=2, padx=(0,20), sticky=EW)

# Add Course to DB
addCourse = ttk.Button(root, text='Add New Course')
addCourse.place(anchor=E, relx=0.95, rely=0.16, relwidth=0.13, relheight=0.05)

treeViewContainer.place(anchor=N, relx=0.5, rely=0.2, relwidth=0.9, relheight=0.75)


root.mainloop()