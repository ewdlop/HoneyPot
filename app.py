#!/usr/bin/env python3
"""
Biological Honey Pot - A cybersecurity decoy system that mimics biological research infrastructure
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import random
import string

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('honeypot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Store all interactions for analysis
interactions = []

def log_interaction(endpoint, method, source_ip, headers, data=None):
    """Log all interactions with the honey pot"""
    interaction = {
        'timestamp': datetime.now().isoformat(),
        'endpoint': endpoint,
        'method': method,
        'source_ip': source_ip,
        'headers': dict(headers),
        'data': data,
        'user_agent': headers.get('User-Agent', 'Unknown')
    }
    interactions.append(interaction)
    logger.warning(f"HONEYPOT INTERACTION: {source_ip} -> {method} {endpoint}")
    return interaction

@app.before_request
def before_request():
    """Log all requests before processing"""
    log_interaction(
        request.endpoint or request.path,
        request.method,
        request.remote_addr,
        request.headers,
        request.get_json(silent=True) if request.is_json else request.form.to_dict()
    )

# Fake biological sequence database endpoints
@app.route('/api/sequences/<sequence_id>')
def get_sequence(sequence_id):
    """Fake biological sequence retrieval"""
    fake_sequence = ''.join(random.choices('ATCG', k=random.randint(100, 1000)))
    return jsonify({
        'id': sequence_id,
        'sequence': fake_sequence,
        'organism': random.choice(['E. coli', 'S. cerevisiae', 'H. sapiens', 'M. musculus']),
        'length': len(fake_sequence),
        'type': 'DNA'
    })

@app.route('/api/sequences', methods=['POST'])
def upload_sequence():
    """Fake sequence upload endpoint"""
    data = request.get_json()
    return jsonify({
        'status': 'success',
        'id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        'message': 'Sequence uploaded successfully'
    })

# Fake lab equipment interfaces
@app.route('/api/equipment/<equipment_id>/status')
def equipment_status(equipment_id):
    """Fake lab equipment status"""
    return jsonify({
        'equipment_id': equipment_id,
        'status': random.choice(['online', 'offline', 'maintenance', 'busy']),
        'temperature': round(random.uniform(20.0, 37.0), 1),
        'last_used': datetime.now().isoformat()
    })

@app.route('/api/equipment/<equipment_id>/control', methods=['POST'])
def control_equipment(equipment_id):
    """Fake equipment control"""
    command = request.get_json()
    return jsonify({
        'equipment_id': equipment_id,
        'command': command,
        'status': 'executed',
        'result': 'Command processed successfully'
    })

# Fake research data endpoints
@app.route('/api/experiments')
def list_experiments():
    """List fake experiments"""
    experiments = []
    for i in range(random.randint(5, 15)):
        experiments.append({
            'id': f'EXP_{i:03d}',
            'title': f'Study of {random.choice(["protein", "gene", "enzyme"])} expression',
            'researcher': f'Dr. {random.choice(["Smith", "Johnson", "Brown", "Wilson"])}',
            'status': random.choice(['active', 'completed', 'pending']),
            'created': datetime.now().isoformat()
        })
    return jsonify(experiments)

@app.route('/api/experiments/<exp_id>/data')
def get_experiment_data(exp_id):
    """Fake experiment data"""
    return jsonify({
        'experiment_id': exp_id,
        'data_points': [random.uniform(0, 100) for _ in range(50)],
        'metadata': {
            'samples': random.randint(10, 100),
            'duration_hours': random.randint(1, 72)
        }
    })

# Authentication simulation
@app.route('/api/auth/login', methods=['POST'])
def fake_login():
    """Fake authentication endpoint"""
    credentials = request.get_json()
    # Always return success to encourage further interaction
    return jsonify({
        'status': 'success',
        'token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
        'user': credentials.get('username', 'guest'),
        'permissions': ['read', 'write', 'admin']
    })

# Admin interface (highly attractive to attackers)
@app.route('/admin')
def admin_panel():
    """Fake admin panel"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BioLab Management System - Admin</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { background: #f0f0f0; padding: 20px; margin-bottom: 20px; }
            .section { margin: 20px 0; }
            .equipment { border: 1px solid #ccc; padding: 10px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🧬 BioLab Management System</h1>
            <p>Advanced Biological Research Platform v2.1.3</p>
        </div>
        
        <div class="section">
            <h2>Laboratory Equipment Status</h2>
            <div class="equipment">
                <strong>PCR Machine #1:</strong> Online | Temperature: 25.3°C
            </div>
            <div class="equipment">
                <strong>DNA Sequencer #2:</strong> Busy | Processing Sample BIO-2023-4419
            </div>
            <div class="equipment">
                <strong>Centrifuge #3:</strong> Maintenance Required
            </div>
        </div>
        
        <div class="section">
            <h2>Recent Experiments</h2>
            <ul>
                <li>Gene Expression Study - Dr. Anderson (Active)</li>
                <li>Protein Folding Analysis - Dr. Chen (Completed)</li>
                <li>CRISPR Efficiency Test - Dr. Rodriguez (Pending)</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>System Administration</h2>
            <p><a href="/admin/users">User Management</a></p>
            <p><a href="/admin/backup">Database Backup</a></p>
            <p><a href="/admin/logs">System Logs</a></p>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/admin/users')
def admin_users():
    """Fake user management"""
    return jsonify([
        {'id': 1, 'username': 'admin', 'role': 'administrator', 'last_login': '2023-10-15'},
        {'id': 2, 'username': 'researcher1', 'role': 'researcher', 'last_login': '2023-10-14'},
        {'id': 3, 'username': 'labtech', 'role': 'technician', 'last_login': '2023-10-13'}
    ])

# Monitoring and logging endpoints
@app.route('/api/honeypot/interactions')
def get_interactions():
    """Get all logged interactions (for monitoring)"""
    return jsonify(interactions[-50:])  # Return last 50 interactions

@app.route('/api/honeypot/stats')
def get_stats():
    """Get honey pot statistics"""
    return jsonify({
        'total_interactions': len(interactions),
        'unique_ips': len(set(i['source_ip'] for i in interactions)),
        'most_accessed_endpoints': {},
        'recent_activity': len([i for i in interactions if (datetime.now() - datetime.fromisoformat(i['timestamp'])).seconds < 3600])
    })

@app.route('/')
def home():
    """Main landing page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Advanced Biological Research Institute</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            .header { text-align: center; border-bottom: 2px solid #0066cc; padding-bottom: 20px; margin-bottom: 30px; }
            .nav { margin: 20px 0; }
            .nav a { margin-right: 20px; color: #0066cc; text-decoration: none; }
            .section { margin: 30px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧬 Advanced Biological Research Institute</h1>
                <p>Leading genomics and proteomics research facility</p>
            </div>
            
            <div class="nav">
                <a href="/api/sequences">Sequence Database</a>
                <a href="/api/experiments">Experiments</a>
                <a href="/api/equipment">Equipment</a>
                <a href="/admin">Admin Panel</a>
            </div>
            
            <div class="section">
                <h2>Welcome to ABRI</h2>
                <p>Our institute specializes in cutting-edge biological research including:</p>
                <ul>
                    <li>Genomic sequencing and analysis</li>
                    <li>Protein structure determination</li>
                    <li>CRISPR gene editing research</li>
                    <li>Synthetic biology applications</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>Research Facilities</h2>
                <p>State-of-the-art equipment including PCR machines, DNA sequencers, 
                mass spectrometers, and automated liquid handling systems.</p>
            </div>
            
            <div class="section">
                <h2>Database Access</h2>
                <p>Researchers can access our biological sequence databases and 
                experimental data through our API endpoints.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)