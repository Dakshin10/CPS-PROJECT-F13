# Teachers and Students Management System

This is a Python-based GUI application that provides management tools for teachers and students. The program allows users to schedule tests, manage tasks, and view test schedules using an intuitive graphical interface.

## Features

### Teacher's Portal
- **Schedule Tests:** Teachers can assign tests to specific dates and periods using a calendar interface.
- **Dynamic Data Loading:** Loads teacher and subject information from CSV files.
- **Conflict Handling:** Prevents scheduling conflicts with pre-existing test dates.
- **Period Selection:** Displays available periods based on the timetable and selected day.

### Student's Portal
- **Task Management:** Students can add, view, and delete tasks.
- **Calendar Integration:** Displays reminders for tasks due on specific dates.
- **Test Schedule Updates:** Automatically loads test schedules from CSV files into the task list.

## File Structure
The application relies on the following files:
- `faculty_course_info.csv`: Contains information about teachers and the subjects they teach.
- `class_timetable.csv`: Stores the timetable for various classes and periods.
- `test_schedule.csv`: Tracks scheduled tests.
- `tasks.csv`: Stores tasks added by students.

{faculty_course_info.csv -- Columns: Faculty, Course Code, Course Name
class_timetable.csv ------ Columns: Day, Course Name, Slot, Time Range, Room
test_schedule.csv -------- Columns: Teacher, Subject, Date, Period
tasks.csv ---------------- Columns: Title, Due Date (YYYY-MM-DD), Priority, Status

Make sure the CSV files are formatted correctly to avoid runtime errors.
All csv files need to be saved for the code to work properly}


## Installation

### Prerequisites
- Python 3.8 or above
- Required libraries:
  - `tkinter`
  - `tkcalendar`
  - `pandas`

Install the necessary libraries using pip:
```bash
pip install tkcalendar pandas
