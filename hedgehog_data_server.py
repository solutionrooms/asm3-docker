#!/usr/bin/env python3
"""
Simple Hedgehog Care Data Collection Server

This is a minimal web server that can collect hedgehog care data without needing
to rebuild ASM3 or modify the main system. It runs alongside ASM3 and provides
an immediate solution for hedgehog care tracking.

Usage:
    python3 hedgehog_data_server.py

Then access: http://localhost:8080/hedgehog_care_standalone.html?hedgehog=Spike
"""

import http.server
import socketserver
import json
import os
import datetime
import urllib.parse
from pathlib import Path

PORT = 8080
DATA_DIR = "hedgehog_care_data"

class HedgehogCareHandler(http.server.SimpleHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        # Create data directory if it doesn't exist
        Path(DATA_DIR).mkdir(exist_ok=True)
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """Handle form submissions"""
        if self.path == '/submit_care':
            self.handle_care_submission()
        else:
            self.send_error(404, "Not Found")
    
    def do_GET(self):
        """Handle file serving and API endpoints"""
        if self.path == '/api/care_records':
            self.send_care_records()
        elif self.path.startswith('/api/hedgehog/'):
            hedgehog_name = self.path.split('/')[-1]
            self.send_hedgehog_records(hedgehog_name)
        else:
            # Serve static files
            super().do_GET()
    
    def handle_care_submission(self):
        """Process hedgehog care form submission"""
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            # Add server timestamp
            data['server_timestamp'] = datetime.datetime.now().isoformat()
            data['submission_id'] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save to file
            filename = f"{DATA_DIR}/care_{data['hedgehog']}_{data['submission_id']}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'message': f'Care record for {data["hedgehog"]} saved successfully',
                'submission_id': data['submission_id'],
                'filename': filename
            }
            
            self.wfile.write(json.dumps(response).encode())
            
            print(f"✅ Saved care record for {data['hedgehog']} to {filename}")
            
        except Exception as e:
            print(f"❌ Error handling submission: {e}")
            self.send_error(500, f"Server Error: {e}")
    
    def send_care_records(self):
        """Send all care records as JSON"""
        try:
            records = []
            
            for filename in os.listdir(DATA_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(DATA_DIR, filename)
                    with open(filepath, 'r') as f:
                        record = json.load(f)
                        records.append(record)
            
            # Sort by timestamp
            records.sort(key=lambda x: x.get('server_timestamp', ''), reverse=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(records, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Error retrieving records: {e}")
    
    def send_hedgehog_records(self, hedgehog_name):
        """Send records for a specific hedgehog"""
        try:
            records = []
            
            for filename in os.listdir(DATA_DIR):
                if filename.endswith('.json') and hedgehog_name.lower() in filename.lower():
                    filepath = os.path.join(DATA_DIR, filename)
                    with open(filepath, 'r') as f:
                        record = json.load(f)
                        records.append(record)
            
            # Sort by timestamp
            records.sort(key=lambda x: x.get('server_timestamp', ''), reverse=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(records, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Error retrieving hedgehog records: {e}")
    
    def log_message(self, format, *args):
        """Custom logging"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def main():
    """Start the hedgehog care data server"""
    
    print("🦔 Starting Hedgehog Care Data Server...")
    print(f"📁 Data will be saved to: {os.path.abspath(DATA_DIR)}")
    print(f"🌐 Server starting on http://localhost:{PORT}")
    print()
    print("📋 Form URL: http://localhost:8080/hedgehog_care_standalone.html?hedgehog=HEDGEHOG_NAME")
    print("📊 View all data: http://localhost:8080/api/care_records")
    print("🦔 View hedgehog data: http://localhost:8080/api/hedgehog/HEDGEHOG_NAME")
    print()
    print("💡 Examples:")
    print("   http://localhost:8080/hedgehog_care_standalone.html?hedgehog=Spike")
    print("   http://localhost:8080/hedgehog_care_standalone.html?hedgehog=Luna")
    print("   http://localhost:8080/api/hedgehog/Spike")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Change to the directory containing the HTML file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        with socketserver.TCPServer(("", PORT), HedgehogCareHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()