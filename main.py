from pimoroni import RGBLED
from plasma import plasma2040
import plasma
import machine
import time

# Constants for LED setup and fading
NUM_LEDS = 50
FADE_IN_STEPS = 50
FADE_OUT_STEPS = 1000
FADE_DELAY = 0.01
FADE_OUT_DELAY = 0.01
LED_ON_DURATION = 10

# Initialize the WS2812 LED strip
led_strip = plasma.WS2812(NUM_LEDS, pio=0, sm=0, dat=plasma2040.DAT)
led_strip.start()

# Initialize the PIR sensor and RGB LED
pir_pin = machine.Pin(21, machine.Pin.IN)
led = RGBLED(plasma2040.LED_R, plasma2040.LED_G, plasma2040.LED_B)

# Set RGB LED to green (system ready)
led.set_rgb(0, 255, 0)

# Track the state of motion and time
motion_detected = False
last_motion_time = 0
current_g, current_r, current_b = 0, 0, 0

# Function to fade in the main LEDs
def fade_in_leds(start_g, start_r, start_b, target_g, target_r, target_b):
    global current_g, current_r, current_b
    for step in range(FADE_IN_STEPS + 1):
        factor = step / FADE_IN_STEPS
        g = int(start_g + (target_g - start_g) * factor)
        r = int(start_r + (target_r - start_r) * factor)
        b = int(start_b + (target_b - start_b) * factor)
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, g, r, b)
        time.sleep(FADE_DELAY)
    current_g, current_r, current_b = target_g, target_r, target_b

# Function to fade out the main LEDs
def fade_out_leds():
    global current_g, current_r, current_b
    for step in range(FADE_OUT_STEPS, -1, -1):
        if pir_pin.value() == 1:
            print("Motion detected during fade-out.")
            fade_in_leds(current_g, current_r, current_b, 0, 100, 100)
            return
        factor = step / FADE_OUT_STEPS
        g = int(0 * factor)
        r = int(100 * factor)
        b = int(100 * factor)
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, g, r, b)
        current_g, current_r, current_b = g, r, b
        time.sleep(FADE_OUT_DELAY)

# Function to handle the countdown blinking
def blink_red_countdown(duration):
    for _ in range(duration):
        led.set_rgb(255, 0, 0)  # Set LED to red
        time.sleep(0.5)
        led.set_rgb(0, 0, 0)    # Turn off LED
        time.sleep(0.5)

# Main loop to handle motion detection
while True:
    current_motion_state = pir_pin.value() == 1

    if current_motion_state and not motion_detected:
        print("Motion detected!")
        led.set_rgb(255, 0, 0)  # Set RGB LED to red
        fade_in_leds(current_g, current_r, current_b, 0, 100, 100)
        motion_detected = True
        last_motion_time = time.time()

    elif current_motion_state:
        last_motion_time = time.time()

    elif not current_motion_state and motion_detected:
        if time.time() - last_motion_time >= LED_ON_DURATION:
            print("No recent motion. Starting countdown.")
            blink_red_countdown(10)  # Blink red every second
            led.set_rgb(0, 0, 0)     # Turn off RGB LED
            fade_out_leds()
            motion_detected = False
            led.set_rgb(0, 255, 0)   # Set RGB LED back to green

    time.sleep(0.1)

