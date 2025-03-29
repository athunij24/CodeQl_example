from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    db_file = 'gradebook.db'
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Create the students table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, studentId TEXT, name TEXT, grade TEXT)''')
    
    # Check if the table is empty
    c.execute("SELECT COUNT(*) FROM students")
    row_count = c.fetchone()[0]
    
    # If the table is empty, populate it with sample data
    if row_count == 0:
        print("Table is empty. Populating with sample data...")
        students = [
            ("50034", "John", "A"),
            ("40052", "Charlie", "B"),
            ("43312", "Alex", "C"),
            ("56378", "Jake", "A"),
            ("12412", "Grace", "B"),
            ("92232", "Lily", "C"),
        ]
        c.executemany('INSERT INTO students (studentId, name, grade) VALUES (?, ?, ?)', students)
        conn.commit()
        print("Sample data added to the table.")
    else:
        print("Table already contains data. Skipping population.")
    
    conn.close()

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        student_id = request.form['student_id']
        
        # Insecure query: directly concatenates user input
        query = f"SELECT name, grade FROM students WHERE studentId = '{student_id}'"
        
        conn = sqlite3.connect('gradebook.db')
        c = conn.cursor()
        c.execute(query)
        result = c.fetchone()
        conn.close()
        
        if result:
            return f"Student: {result[0]}, Grade: {result[1]}"
        else:
            return "Student not found."
    
    return render_template_string('''
        <h1>Gradebook</h1>
        <form method="POST">
            <label for="student_id">Enter student id:</label>
            <input type="text" id="student_id" name="student_id" required>
            <button type="submit">View Grade</button>
        </form>
    ''')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)