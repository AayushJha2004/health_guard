import RPi.GPIO as GPIO
from flask import Flask, render_template
import time

# Initialize the Flask app
app = Flask(__name__)

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering
GPIO.setup(17, GPIO.OUT)  # GPIO 17 for the buzzer

# Function to trigger buzzer
def trigger_buzzer():
    GPIO.output(17, GPIO.HIGH)  # Turn on the buzzer
    time.sleep(2)  # Buzzer stays on for 0.5 seconds
    GPIO.output(17, GPIO.LOW)
   time.sleep(1)# Turn off the buzzer
 GPIO.output(17, GPIO.HIGH)  # Turn on the buzzer
    time.sleep(2)  # Buzzer stays on for 0.5 seconds
    GPIO.output(17, GPIO.LOW)
# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')  # Web page with a button

# Route to handle the web button press event
@app.route('/button', methods=['POST'])
def button_pressed():
    trigger_buzzer()  # Trigger the buzzer
    return "Buzzer triggered!"  # Respond back to the browser

# Run the app
if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)  # Run the web server
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO when Ctrl+C is pressed
