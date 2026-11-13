
import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT,
    marks REAL
)
""")
conn.commit()

st.title("🎓 Student Record Management System")
st.write("Manage student records using CRUD operations.")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add New Student")

    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    course = st.text_input("Course")
    marks = st.number_input("Marks", min_value=0.0, max_value=100.0)

    if st.button("Add Student"):
        if name and course:
            cursor.execute(
                "INSERT INTO students (name, age, course, marks) VALUES (?, ?, ?, ?)",
                (name, age, course, marks)
            )
            conn.commit()
            st.success("Student added successfully!")
        else:
            st.error("Please enter name and course.")

# READ
elif menu == "View Students":
    st.header("All Student Records")

    df = pd.read_sql_query("SELECT * FROM students", conn)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No student records found.")

# UPDATE
elif menu == "Update Student":
    st.header("Update Student Details")

    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    if students:
        student_dict = {
            f"{s[0]} - {s[1]}": s[0] for s in students
        }

        selected = st.selectbox("Select Student", student_dict.keys())
        student_id = student_dict[selected]

        cursor.execute(
            "SELECT name, age, course, marks FROM students WHERE id=?",
            (student_id,)
        )
        student = cursor.fetchone()

        name = st.text_input("Name", value=student[0])
        age = st.number_input("Age", min_value=1, max_value=100, value=student[1])
        course = st.text_input("Course", value=student[2])
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0, value=float(student[3]))

        if st.button("Update Record"):
            cursor.execute("""
                UPDATE students
                SET name=?, age=?, course=?, marks=?
                WHERE id=?
            """, (name, age, course, marks, student_id))

            conn.commit()
            st.success("Student record updated!")
    else:
        st.info("No students available to update.")

# DELETE
elif menu == "Delete Student":
    st.header("Delete Student Record")

    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    if students:
        student_dict = {
            f"{s[0]} - {s[1]}": s[0] for s in students
        }

        selected = st.selectbox("Select Student", student_dict.keys())

        if st.button("Delete Student"):
            student_id = student_dict[selected]

            cursor.execute(
                "DELETE FROM students WHERE id=?",
                (student_id,)
            )
            conn.commit()
            st.success("Student deleted successfully!")
    else:
        st.info("No students available to delete.")

conn.close()
