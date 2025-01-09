from flask import Flask, jsonify, render_template
import serial
import threading

app = Flask(__name__)

# Serial port configuration
SERIAL_PORT = 'usbmodem2077345742482' 
BAUD_RATE = 9600

# Shared variable to store the latest data from STM32
stm32_data = {"value": "No data yet"}

def read_serial():
    global stm32_data
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    stm32_data["value"] = line 
    except Exception as e:
        print(f"Error reading serial: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(stm32_data)

if __name__ == '__main__':
    threading.Thread(target=read_serial, daemon=True).start()
    # Run the Flask app
    app.run(debug=True)
