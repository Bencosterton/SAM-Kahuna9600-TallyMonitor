#!/usr/bin/env python3
from flask import Flask, render_template
import socket
import threading
import queue
import argparse

app = Flask(__name__)

#Interface set up with two Gallery spaces (PCR1 & PCR2)
current_sources = {
    'PCR1': None, 
    'PCR2': None  
}

tally_queue = queue.Queue()

# Dictionary used to translate 
SOURCE_NAMES = {
    'CCU 1': 'ST1 CAM1',
    'CCU 2': 'ST1 CAm2',
    'CCU 3': 'ST1 CAM3',
    'CCU 4': 'ST1 CAM4'
}

# List of sources to ignore
IGNORED_SOURCES = [
    'PGM',
    'PVW',
    'ME2 PGM',
    'ME3 PGM',
    'STOR 1',
    'STOR 5'
]

def translate_source_name(source):
    """Translate source names using the dictionary"""
    return SOURCE_NAMES.get(source, source)

def process_tally_message(chunk):
    """Process a 24-byte tally message"""
    try:
        control_byte = chunk[8]
        source_name = chunk[10:24].decode('ascii').strip('\x00').strip()
        
        if source_name in IGNORED_SOURCES:
            return
            
        translated_name = translate_source_name(source_name)
        
        # This is where we look at the ontrol byte from each source, and compare it to the relevent switcher (gallery) - See README.MD
        if control_byte == 0xA0:
            current_sources['PCR1'] = translated_name
        elif control_byte == 0x90:
            current_sources['PCR2'] = translated_name
            
    except Exception as e:
        print(f"Error processing tally message: {e}")

def tally_monitor(host, port):
    """Background thread to monitor tally data"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        chunk_size = 24
        
        while True:
            data = sock.recv(1024)
            if not data:
                break
                
            # Tally info can come in a chunks of 24-bit. 24/48/94.... Each sources seems to occupy 24 bits, so we will seperate each message out into 24-but chunks, therefore one chunk per source.
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                if len(chunk) == chunk_size:
                    process_tally_message(chunk)
                    
    except Exception as e:
        print(f"Tally monitor error: {e}")
    finally:
        sock.close()

@app.route('/')
def index():
    """Main page showing current sources"""
    return render_template('index.html', sources=current_sources)

@app.route('/api/sources')
def get_sources():
    """API endpoint for getting current sources"""
    return current_sources

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kahuna Tally Monitor')
    parser.add_argument('-i', type=str, required=True, help='Kahuna IP address')
    parser.add_argument('-p', type=int, required=True, help='Kahuna port number')
    args = parser.parse_args()

    tally_thread = threading.Thread(
        target=tally_monitor,
        args=(args.i, args.p),
        daemon=True
    )
    tally_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
