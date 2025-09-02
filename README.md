# Biological Honey Pot

A cybersecurity decoy system that mimics biological research infrastructure to attract and monitor potential attackers targeting scientific institutions.

## Features

- **Fake Biological Database**: Simulates sequence databases with realistic endpoints
- **Lab Equipment Simulation**: Mimics control interfaces for laboratory equipment
- **Research Data Endpoints**: Provides fake experimental data and research information
- **Authentication Simulation**: Implements fake login systems to capture credentials
- **Comprehensive Logging**: Records all interactions for security analysis
- **Web Interface**: Realistic biological research institute website

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the honey pot:
```bash
python app.py
```

3. Access the honey pot at `http://localhost:8080`

## Docker Deployment

```bash
docker build -t bio-honeypot .
docker run -p 8080:8080 bio-honeypot
```

## API Endpoints

### Biological Sequences
- `GET /api/sequences/<id>` - Retrieve fake DNA/RNA sequences
- `POST /api/sequences` - Upload sequences (fake)

### Lab Equipment
- `GET /api/equipment/<id>/status` - Equipment status
- `POST /api/equipment/<id>/control` - Control equipment

### Research Data
- `GET /api/experiments` - List experiments
- `GET /api/experiments/<id>/data` - Experiment data

### Authentication
- `POST /api/auth/login` - Fake login endpoint

### Monitoring
- `GET /api/honeypot/interactions` - View logged interactions
- `GET /api/honeypot/stats` - Honey pot statistics

## Security Monitoring

All interactions are logged to:
- Console output
- `honeypot.log` file
- In-memory storage for API access

Monitor the honey pot by watching:
- Failed authentication attempts
- Unusual API access patterns
- Administrative interface access
- Equipment control attempts

## Configuration

Set environment variables:
- `PORT`: Server port (default: 8080)

## Warning

This is a honey pot system designed for cybersecurity research and monitoring. Do not use in production environments or expose sensitive data.