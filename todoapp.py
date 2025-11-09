from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Initial To Do list
todo_items = [
    "mop floors",
    "sweep floors",
    "clean mirrors",
    "clean bathroom",
    "vacuum floors",
    "tidy up bedroom",
    "do laundry",
    "pick up clutter"
]

@app.route('/', methods=['GET', 'POST'])
def weekend_chores():
    global todo_items
    if request.method == 'POST':
        if 'clear' in request.form:
            todo_items = []
        elif 'replace' in request.form:
            new_items = request.form.get('new_items', '')
            todo_items = [item.strip() for item in new_items.split(',') if item.strip()]
        return redirect(url_for('weekend_chores'))
    return render_template('chores.html', items=todo_items)

@app.route('/submit', methods=['POST'])
def submit():
    global todo_items
    task = request.form.get('task', '').strip()
    email = request.form.get('email', '').strip()
    priority = request.form.get('priority', '').strip()

    # Email validation using regex
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        flash("Invalid email address.")
        return redirect(url_for('weekend_chores'))

    # Priority validation
    if priority not in ['Low', 'Medium', 'High']:
        flash("Invalid priority level selected.")
        return redirect(url_for('weekend_chores'))

    # Task validation
    if not task:
        flash("Task cannot be empty.")
        return redirect(url_for('weekend_chores'))

    # Append new item
    todo_items.append(f"{task} (Priority: {priority}, Contact: {email})")
    return redirect(url_for('weekend_chores'))

@app.route('/clear', methods=['POST'])
def clear_list():
    global todo_items
    todo_items = []
    return redirect(url_for('weekend_chores'))

if __name__ == '__main__':
    app.run(debug=True)

