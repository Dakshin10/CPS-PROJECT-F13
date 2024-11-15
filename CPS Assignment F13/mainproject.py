cluck=True
def proffesion():
    global cluck
    while cluck==True:
        prof=input("Enter 't' if teacher and 's' if student (to exit-'e'): ")
        if prof=='t':
         program1()
        elif prof=='s':
         program2()
        elif prof=='e':
         cluck=False
        else:
         print("Enter only 't' or 's'(or 'e')")

def program1():
    import tkinter as tk
    from tkinter import ttk, messagebox
    from tkcalendar import Calendar
    import pandas as pd
    from datetime import datetime

    # File paths
    FACULTY_FILE = 'faculty_course_info.csv'
    TIMETABLE_FILE = 'class_timetable.csv'
    TEST_SCHEDULE_FILE = 'test_schedule.csv'

    # Load data function
    def load_data(file):
        """Load data from CSV file into a list of dictionaries."""
        data = []
        
        with open(file, 'r') as file:
            lines = file.readlines()  # Read all lines in the file
            headers = lines[0].strip().split(',')  # Get the first line (headers)
            
            # Loop through the rest of the lines and create dictionaries
            for line in lines[1:]:
                values = line.strip().split(',')  # Split each line by commas
                
                # Check if the number of values matches the number of headers
                if len(values) == len(headers):
                    row = {}  
                    for i in range(len(headers)):
                        row[headers[i]] = values[i]  
                    data.append(row) 
        
        return data

    # Loads data in the form of Dictionary
    teacher_info = load_data(FACULTY_FILE)
    timetable = load_data(TIMETABLE_FILE)
    test_schedule = load_data(TEST_SCHEDULE_FILE)

    #creating gui
    root = tk.Tk()
    root.title("Teachers Management System")
    root.geometry("1000x600")
    title_label = tk.Label(root, text="Teachers Test Assignment Portal", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Variables for selections
    teacher_name_var = tk.StringVar()
    subject_var = tk.StringVar()
    period_var = tk.StringVar()

    #Using combobox for Teacher Selection
    tk.Label(root, text="Select Teacher:", font=("Arial", 12)).pack(pady=5)
    teacher_names = []
    for teacher in teacher_info:
        if teacher['Faculty'] and teacher['Faculty'] not in teacher_names:
            teacher_names.append(teacher['Faculty'])

    teacher_combo = ttk.Combobox(root, textvariable=teacher_name_var, values=teacher_names, state="readonly", font=("Arial", 12))
    teacher_combo.set("Select Teacher")
    teacher_combo.pack(pady=5)

    # Subject Selection
    tk.Label(root, text="Select Subject:", font=("Arial", 12)).pack(pady=5)
    subject_combo = ttk.Combobox(root, textvariable=subject_var, state="readonly", font=("Arial", 12))
    subject_combo.set("Select Subject")
    subject_combo.pack(pady=5)

    # Date Selection
    tk.Label(root, text="Select Date:", font=("Arial", 12)).pack(pady=5)
    cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=5)

    # Update subjects based on selected teacher
    def update_subjects(event):
        teacher_name = teacher_name_var.get()
        subjects = []
        for info in teacher_info:
            if info['Faculty'] == teacher_name:
                subject_name = info['Course Name']
                if subject_name not in subjects:
                    subjects.append(subject_name)

        subject_combo['values'] = subjects
        subject_var.set("Select Subject")

    def load_available_periods(): #Load available periods if no test is scheduled on the selected date
        teacher_name = teacher_name_var.get()
        selected_subject = subject_var.get()
        selected_date = cal.get_date()
        select_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        today_date = datetime.now().date()
        # Check if the selected date is before or today
        if select_date <= today_date:
            messagebox.showinfo("Invalid Date", "Please choose dates from tomorrow.")   
            return
        # Check if a test is already scheduled on this date
        for test in test_schedule:
            if test['Date'] == selected_date:
                messagebox.showinfo("Date Conflict", "A test is already scheduled on this date. Please choose another date.")
                return
        selected_day = pd.Timestamp(selected_date).day_name()# Get the selected day of the week
        teacher_courses = []
        for info in teacher_info:
            if info['Faculty'] == teacher_name:
                teacher_courses.append(info['Course Code'])
        subject_periods = []
        for row in timetable:
            if row['Day'] == selected_day and row['Course Name'] == selected_subject :
                period_info = f"{row['Slot']} ({row['Time Range']}) - {row['Room']}"
                subject_periods.append(period_info)
        # If available periods exist, shows periods as radio buttons
        if subject_periods:    
            for widget in period_frame.winfo_children():# Clear previous radio buttons if any
                widget.destroy()

            tk.Label(period_frame, text="Select Period:", font=("Arial", 12)).pack(pady=5)

            # Create a radio button for each available period
            for idx, period in enumerate(subject_periods):
                tk.Radiobutton(period_frame, text=period, variable=period_var, value=period, font=("Arial", 10)).pack(anchor="w")
        else:
            messagebox.showinfo("No Periods", f"No scheduled periods for {selected_subject} on {selected_day}.")
            period_var.set("")  # Clear the period selection
            # Hide radio buttons if no periods are available
            for widget in period_frame.winfo_children():
                widget.destroy()
            tk.Label(period_frame, text=f"No Period(s) Available on {selected_day}", font=("Arial", 12), fg="red").pack(pady=5)

    period_frame = tk.Frame(root)
    period_frame.pack(pady=5)

    tk.Button(root, text="Load Available Periods", command=load_available_periods, font=("Arial", 10, "bold")).pack(pady=10)

    def confirm_test_schedule():
        teacher_name = teacher_name_var.get()
        subject = subject_var.get()
        date = cal.get_date()
        period = period_var.get()

        if teacher_name and subject and date and period and period != "Select Period":
            with open(TEST_SCHEDULE_FILE, 'a') as file:
                file.write(f"{teacher_name},{subject},{date},{period}\n")
            messagebox.showinfo("Success", f"Test for {subject} scheduled on {date} during {period}.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    teacher_combo.bind("<<ComboboxSelected>>", update_subjects) 
    tk.Button(root, text="Confirm Schedule", command=confirm_test_schedule, font=("Arial", 10, "bold")).pack(pady=20)

    #Close the program
    def exit_program():
        root.destroy()
    exit_button = tk.Button(root, text="Exit", command=exit_program, width=15, height=2)
    exit_button.pack(pady=20)

    root.mainloop()

    
def program2():
    import csv
    import tkinter
    from tkinter import messagebox
    from tkcalendar import Calendar
    from datetime import datetime

    # List to store task objects
    tasks=[]

    class Task:
        def __init__(self, ttl, dueDate, prio, stat="Pending"):
            self.ttl=ttl
            try:
                self.dueDate=datetime.strptime(dueDate, '%Y-%m-%d')
            except ValueError:
                self.dueDate=None
            self.prio=prio
            self.stat=stat

    # Load tasks from CSV file
    def loadTasks():
        try:
            with open("tasks.csv", "r") as file:
                reader=csv.reader(file)
                for row in reader:
                    ttl, dueDate, prio, stat=row
                    tsk=Task(ttl, dueDate, prio, stat)
                    tasks.append(tsk)
        except FileNotFoundError:
            messagebox.showerror("File Error", "The CSV file 'tasks.csv' was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def saveTasks():
        with open("tasks.csv", "w", newline="") as file:
            writer=csv.writer(file)
            for tsk in tasks:
                writer.writerow([tsk.ttl, tsk.dueDate.strftime('%Y-%m-%d'), tsk.prio, tsk.stat])

    #Pyhton GUI
    root=tkinter.Tk()
    root.title("Study and Assignment Tracker")
    root.geometry("800x800")

    label=tkinter.Label(root, text="TASK MANAGER\n", font=("Georgia", 24))
    label.grid(row=0, column=0, columnspan=4, pady=(10, 5), sticky="n")

    # Widgets for task details
    titleLabel=tkinter.Label(root, text="Title: ")
    titleLabel.grid(row=1, column=0, pady=(10, 5), padx=10, sticky="e")

    titleEntry=tkinter.Entry(root, width=40)
    titleEntry.grid(row=1, column=1, pady=(10, 5), padx=10, sticky="w")

    dueDateLabel=tkinter.Label(root, text="Due/Log Date (YYYY-MM-DD): ")
    dueDateLabel.grid(row=1, column=2, pady=(10, 5), padx=10, sticky="e")

    dueDateEntry=tkinter.Entry(root, width=40)
    dueDateEntry.grid(row=1, column=3, pady=(10, 5), padx=10, sticky="w")

    prioLabel=tkinter.Label(root, text="Priority: ")
    prioLabel.grid(row=2, column=0, pady=(5, 5), padx=10, sticky="e")

    prioEntry=tkinter.Entry(root, width=40)
    prioEntry.grid(row=2, column=1, pady=(5, 5), padx=10, sticky="w")

    statLabel=tkinter.Label(root, text="Status: ")
    statLabel.grid(row=2, column=2, pady=(5, 5), padx=10, sticky="e")

    statEntry=tkinter.Entry(root, width=40)
    statEntry.grid(row=2, column=3, pady=(5, 5), padx=10, sticky="w")

    taskListbox=tkinter.Listbox(root, width=50, height=15)
    taskListbox.grid(row=3, column=0, columnspan=8, pady=(10, 5), padx=10)
    taskListbox.config(width=100, height=10)

    #Adding custom tasks
    def addTask():
        ttl=titleEntry.get()
        dueDate=dueDateEntry.get()
        prio=prioEntry.get()
        stat=statEntry.get() if statEntry.get() else "Pending"
        if ttl and dueDate and prio:
            tsk=Task(ttl, dueDate, prio, stat)
            tasks.append(tsk)
            saveTasks()
            taskInfo=f"{ttl} | Due: {dueDate} | Priority: {prio} | Status: {stat}"
            taskListbox.insert("end", taskInfo)
            titleEntry.delete(0, "end")
            dueDateEntry.delete(0, "end")
            prioEntry.delete(0, "end")
            statEntry.delete(0, "end")
        else:
            messagebox.showwarning("Input Error", "Please fill in all blanks.")
        updateCalendar()

    addTaskButton=tkinter.Button(root, text="Add Task", command=addTask)
    addTaskButton.grid(row=4, column=1, pady=(5, 10), padx=5, sticky="e")

    #Delete finished tasks
    def removeTask():
        sIndex=taskListbox.curselection()
        if sIndex:
            indx=sIndex[0]
            taskListbox.delete(indx)
            tasks.pop(indx)
            saveTasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to remove.")
        updateCalendar()

    removeTaskButton=tkinter.Button(root, text="Remove Task", command=removeTask)
    removeTaskButton.grid(row=4, column=2, pady=(5, 10), padx=5, sticky="w")

    calendar=Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
    calendar.grid(row=5, column=0, columnspan=4, pady=(10, 5), padx=10)

    def remOnCal():
        selectDate=datetime.strptime(calendar.get_date(), "%Y-%m-%d").date()
        remainders=[]
        for tsk in tasks:
            if tsk.dueDate and tsk.dueDate.date() == selectDate:
                remainder=f"{tsk.ttl} | Priority: {tsk.prio} | Status: {tsk.stat}"
                remainders.append(remainder)
        remTxt="\n".join(remainders) if remainders else "No tasks due"
        messagebox.showinfo("Reminders", f"Reminders for {selectDate}:\n{remTxt}")

    checkTaskButton=tkinter.Button(root, text="Check Tasks for Selected Dates", command=remOnCal)
    checkTaskButton.grid(row=6, column=1, pady=(5, 10), padx=5, sticky="e")

    def updateCalendar():
        calendar.calevent_remove("all")
        for tsk in tasks:
            if tsk.dueDate:
                calendar.calevent_create(tsk.dueDate, tsk.ttl, "taskDue")

    #loads data from the test schedule csv file
    def loadCSVData():
        try:
            with open("test_schedule.csv", newline='') as csvfile:
                reader=csv.DictReader(csvfile)
                for row in reader:
                    teacher=row.get('Teacher')
                    subject=row.get('Subject')
                    dueDate=row.get('Date')
                    period=row.get('Period')
                    
                    if subject and dueDate:
                        # Format display to include teacher and period info
                        tsk=Task(subject, dueDate, 'Normal')
                        tasks.append(tsk)
                        taskInfo=f"{subject} | Teacher: {teacher} | Due: {dueDate} | Period: {period}"
                        taskListbox.insert("end", taskInfo)
                updateCalendar()
                messagebox.showinfo("Load Complete", "CSV data loaded successfully.")
        except FileNotFoundError:
            messagebox.showerror("File Error", "The CSV file 'test_schedule.csv' was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    loadCSVButton=tkinter.Button(root, text="Update Schedule", command=loadCSVData)
    loadCSVButton.grid(row=6, column=2, pady=(5, 10), padx=5, sticky="w")

    root.mainloop()

    


proffesion()