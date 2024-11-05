#

import plasma
from plasma import plasma2040
import machine
import time

# Set up the number of LEDs and fade effect parameters
NUM_LEDS = 50
FADE_IN_STEPS = 50        # Number of steps for fade-in
FADE_OUT_STEPS = 1000     # Number of steps for fade-out
FADE_DELAY = 0.01         # Delay between each fade-in step in seconds
FADE_OUT_DELAY = 0.01     # Delay between each fade-out step in seconds
LED_ON_DURATION = 3       # Duration in seconds to keep LEDs on after no motion

# Initialize the WS2812 / NeoPixel LED strip
led_strip = plasma.WS2812(NUM_LEDS, pio=0, sm=0, dat=plasma2040.DAT)
led_strip.start()

# Initialize the PIR sensor on GPIO 21 as a digital input
pir_pin = machine.Pin(21, machine.Pin.IN)

# Track the last state of motion and last time motion was detected
motion_detected = False  # Initially, no motion is detected
last_motion_time = 0     # Last time motion was detected
current_g, current_r, current_b = 0, 0, 0  # Track the current brightness

# Function to fade in the LED strip to purple (GRB order) from a given start brightness
def fade_in_leds(start_g, start_r, start_b, target_g, target_r, target_b):
    global current_g, current_r, current_b
    for step in range(FADE_IN_STEPS + 1):  # Go from start to target brightness
        # Calculate the brightness level based on the current step
        factor = step / FADE_IN_STEPS
        g = int(start_g + (target_g - start_g) * factor)
        r = int(start_r + (target_r - start_r) * factor)
        b = int(start_b + (target_b - start_b) * factor)

        # Set each LED to the calculated brightness level
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, g, r, b)

        # Update current brightness level
        current_g, current_r, current_b = g, r, b
        time.sleep(FADE_DELAY)  # Delay for smooth fade-in transition

# Function to fade out the LED strip from purple with immediate exit if motion is detected
def fade_out_leds():
    global current_g, current_r, current_b
    for step in range(FADE_OUT_STEPS, -1, -1):  # Go from current brightness to 0
        # If motion is detected, immediately exit fade-out and capture current brightness
        if pir_pin.value() == 1:
            print("Motion detected during fade-out. Capturing current brightness and exiting fade-out.")
            return  # Exit fade-out without completing, main loop will handle fade-in

        # Calculate the brightness level based on the current step (GRB for purple)
        factor = step / FADE_OUT_STEPS
        g = int(0 * factor)    # Green value for purple (0)
        r = int(100 * factor)  # Red value for purple (100)
        b = int(100 * factor)  # Blue value for purple (100)

        # Set each LED to the calculated brightness level
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, g, r, b)

        # Update current brightness level
        current_g, current_r, current_b = g, r, b
        time.sleep(FADE_OUT_DELAY)  # Delay for smooth fade-out transition

# Main loop to check motion and control LEDs with fade effect and time delay
while True:
    # Read the current state of the PIR sensor
    current_motion_state = pir_pin.value() == 1  # True if motion detected, else False

    # Check for a state change
    if current_motion_state and not motion_detected:
        # Motion has started
        print("Motion detected! Fading in LEDs from current brightness.")
        fade_in_leds(current_g, current_r, current_b, 0, 100, 100)  # Fade in to full purple (GRB order)
        motion_detected = True  # Update the state to indicate motion is ongoing
        last_motion_time = time.time()  # Update last motion time
    elif current_motion_state:
        # Update the last motion time if motion is still detected
        last_motion_time = time.time()
    elif not current_motion_state and motion_detected:
        # If no motion is detected and motion was previously ongoing, check the delay
        if time.time() - last_motion_time > LED_ON_DURATION:
            # Turn off LEDs after the delay
            print("No recent motion. Fading out LEDs.")
            fade_out_leds()  # Start fade-out, will capture brightness if interrupted
            motion_detected = False  # Update the state to indicate no motion

    time.sleep(0.1)  # Short delay to avoid rapid polling


