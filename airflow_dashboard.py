from flask import Flask, render_template_string, redirect, url_for
import os
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime

app = Flask(__name__)

# Define paths
BASE_DIR = Path(__file__).resolve().parent
AIRFLOW_DAGS_DIR = BASE_DIR / 'airflow' / 'dags'
LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

# Template for the dashboard
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Airflow Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #3573A3;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3573A3;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: #3573A3;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 10px;
        }
        .btn:hover {
            background-color: #285A84;
        }
        .success {
            color: green;
        }
        .failure {
            color: red;
        }
        .running {
            color: orange;
        }
        pre {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Simple Airflow Dashboard</h1>
        
        <h2>Available DAGs</h2>
        <table>
            <tr>
                <th>DAG ID</th>
                <th>Last Run</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
            {% for dag in dags %}
            <tr>
                <td>{{ dag.id }}</td>
                <td>{{ dag.last_run_at }}</td>
                <td class="{{ dag.status.lower() }}">{{ dag.status }}</td>
                <td>
                    <a href="{{ url_for('run_dag', dag_id=dag.id) }}" class="btn">Run</a>
                    <a href="{{ url_for('view_dag_details', dag_id=dag.id) }}" class="btn">View Details</a>
                </td>
            </tr>
            {% endfor %}
        </table>
        
        {% if dag_details %}
        <h2>DAG Details: {{ dag_details.id }}</h2>
        <h3>Log Output:</h3>
        <pre>{{ dag_details.log }}</pre>
        {% endif %}
    </div>
</body>
</html>
'''

# Store DAG execution information
DAG_EXECUTIONS = {}

def get_dag_files():
    """Get all Python files in the DAGs directory"""
    dag_files = []
    for file in AIRFLOW_DAGS_DIR.glob('*.py'):
        if file.name != '__init__.py':
            dag_files.append(file)
    return dag_files

def get_dag_info():
    """Get information about available DAGs"""
    dags = []
    for dag_file in get_dag_files():
        dag_id = dag_file.stem
        execution_info = DAG_EXECUTIONS.get(dag_id, {})
        last_run_at = execution_info.get('last_run_at', 'Never')
        status = execution_info.get('status', 'Not Run')
        
        dags.append({
            'id': dag_id,
            'file': str(dag_file),
            'last_run_at': last_run_at,
            'status': status
        })
    return dags

def run_dag_process(dag_id):
    """Run the DAG using the standalone ETL script and capture output"""
    log_file = LOGS_DIR / f"{dag_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Run the standalone ETL script as a subprocess
    cmd = [sys.executable, 'run_etl_pipeline.py']
    try:
        with open(log_file, 'w') as f:
            process = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, text=True)
        
        # Read the log file
        with open(log_file, 'r') as f:
            log = f.read()
        
        # Update DAG execution information
        DAG_EXECUTIONS[dag_id] = {
            'last_run_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Success' if process.returncode == 0 else 'Failed',
            'log': log,
            'log_file': str(log_file)
        }
        
        return DAG_EXECUTIONS[dag_id]
    except Exception as e:
        error_message = f"Error running DAG: {str(e)}"
        DAG_EXECUTIONS[dag_id] = {
            'last_run_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Failed',
            'log': error_message,
            'log_file': None
        }
        return DAG_EXECUTIONS[dag_id]

@app.route('/')
def dashboard():
    """Main dashboard view"""
    dags = get_dag_info()
    return render_template_string(HTML_TEMPLATE, dags=dags, dag_details=None)

@app.route('/dag/<dag_id>')
def view_dag_details(dag_id):
    """View DAG details"""
    dags = get_dag_info()
    dag_details = DAG_EXECUTIONS.get(dag_id, {'id': dag_id, 'log': 'No execution record found'})
    dag_details['id'] = dag_id
    return render_template_string(HTML_TEMPLATE, dags=dags, dag_details=dag_details)

@app.route('/run/<dag_id>')
def run_dag(dag_id):
    """Run a DAG"""
    run_dag_process(dag_id)
    return redirect(url_for('view_dag_details', dag_id=dag_id))

if __name__ == '__main__':
    app.run(debug=True, port=8080) 