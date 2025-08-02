from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('attendance.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

@app.route('/')
def index():
    students = ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown']
    return render_template('index.html', students=students)

@app.route('/submit', methods=['POST'])
def submit():
    today = date.today().isoformat()
    conn = sqlite3.connect('attendance.db')

    students = request.form.getlist('student_name')
    statuses = request.form.getlist('status')

    for name, status in zip(students, statuses):
        conn.execute('INSERT INTO attendance (student_name, status, date) VALUES (?, ?, ?)', (name, status, today))

    conn.commit()
    conn.close()
    return redirect('/report')

@app.route('/report')
def report():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.execute('SELECT student_name, status, date FROM attendance ORDER BY date DESC')
    records = cursor.fetchall()
    conn.close()
    return render_template('report.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
