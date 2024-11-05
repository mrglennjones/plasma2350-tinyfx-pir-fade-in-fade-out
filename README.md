This micropython script for the pimoroni plasma 2350/2040, detects motion with the pimoroni tinyfx PIR sensor connected to the Qwic port then fades in a connected led string, it also waits for a few seconds of no motion detection, then gently fades out the led strip.

one small additional feature is that it will interrupt fade-out when motion is detected and captures the current brightness level, allowing LEDs to fade in from the interrupted level back to full brightness. 

Requirements:-
- Plasma 2350: https://shop.pimoroni.com/products/plasma-2350?variant=42092628246611
- PIR Stick for Tiny FX: https://shop.pimoroni.com/products/pir-stick?variant=53489719017851
- Any WS2812/Neopixel compatible LED strip

The Tinyfx pir sensor comes with a 3 pin connector to connect it to the TinyFX system but i spliced together with a 4pin Qwiic connector using just the positive, negative and yellow wire, leaving the blue one unused)


![20241105_141219](https://github.com/user-attachments/assets/cf1e8c2e-e318-4350-b77a-15130c428cfe)
