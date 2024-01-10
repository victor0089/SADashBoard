from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import pandas as pd

app = Flask(__name__)

# Load data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Helper function to save data back to JSON file
def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Home Page
@app.route('/')
def home():
    return render_template('base.html')

# Admin Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', sales=data['sales'])

# Import Sales Sheet
@app.route('/import', methods=['POST'])
def import_sales():
    if 'file' not in request.files:
        return redirect(url_for('dashboard'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('dashboard'))

    if file:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file)

        # Append the new data to the existing sales data
        data['sales'] = data['sales'].append(df, ignore_index=True)

        # Save the updated data to the JSON file
        save_data()

    return redirect(url_for('dashboard'))

# Export Reports to Excel
@app.route('/export-excel')
def export_excel():
    # Generate a summary report using pandas
    summary_report = data['sales'].groupby(['Product', 'Category']).sum()

    # Save the report to an Excel file
    summary_report.to_excel('summary_report.xlsx')

    return jsonify({'message': 'Export successful'})

if __name__ == '__main__':
    app.run(debug=True)
