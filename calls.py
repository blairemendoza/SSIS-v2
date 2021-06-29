import sqlite3

# SQL Database

def databaseSetup():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Students"(
            ID_Number VARCHAR(9) NOT NULL,
            Name VARCHAR(100) NOT NULL,
            Age INTEGER NOT NULL,
            Gender VARCHAR(10),
            Year_Level INTEGER NOT NULL,
            Course_Code VARCHAR(5) NOT NULL,
            PRIMARY KEY(ID_Number)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Courses"(
            Course_Code VARCHAR(5) NOT NULL,
            Course_Name VARCHAR(100) NOT NULL,
            FOREIGN KEY(Course_Code) REFERENCES Students(Course_Code)
        );
    """)
    conn.close()
    return 0