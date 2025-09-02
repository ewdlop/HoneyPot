#!/usr/bin/env python3
"""
Tests for the biological honey pot
"""

import unittest
import json
import sys
import os

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestBiologicalHoneyPot(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test the home page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Advanced Biological Research Institute', response.data)

    def test_sequence_endpoint(self):
        """Test sequence retrieval endpoint"""
        response = self.app.get('/api/sequences/test123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertIn('sequence', data)
        self.assertIn('organism', data)
        self.assertEqual(data['id'], 'test123')

    def test_sequence_upload(self):
        """Test sequence upload endpoint"""
        test_data = {
            'sequence': 'ATCGATCG',
            'organism': 'Test organism'
        }
        response = self.app.post('/api/sequences', 
                                json=test_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('id', data)

    def test_equipment_status(self):
        """Test equipment status endpoint"""
        response = self.app.get('/api/equipment/PCR001/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('equipment_id', data)
        self.assertIn('status', data)
        self.assertIn('temperature', data)

    def test_equipment_control(self):
        """Test equipment control endpoint"""
        test_command = {'action': 'start', 'temperature': 95}
        response = self.app.post('/api/equipment/PCR001/control',
                                json=test_command,
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'executed')

    def test_experiments_list(self):
        """Test experiments listing"""
        response = self.app.get('/api/experiments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_experiment_data(self):
        """Test experiment data endpoint"""
        response = self.app.get('/api/experiments/EXP001/data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('experiment_id', data)
        self.assertIn('data_points', data)

    def test_fake_login(self):
        """Test fake authentication"""
        credentials = {'username': 'testuser', 'password': 'testpass'}
        response = self.app.post('/api/auth/login',
                                json=credentials,
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('token', data)

    def test_admin_panel(self):
        """Test admin panel access"""
        response = self.app.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'BioLab Management System', response.data)

    def test_admin_users(self):
        """Test admin users endpoint"""
        response = self.app.get('/admin/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_honeypot_stats(self):
        """Test honey pot statistics"""
        response = self.app.get('/api/honeypot/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_interactions', data)
        self.assertIn('unique_ips', data)

    def test_honeypot_interactions(self):
        """Test interactions logging"""
        # Make a few requests to generate interactions
        self.app.get('/')
        self.app.get('/api/sequences/test')
        
        response = self.app.get('/api/honeypot/interactions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()