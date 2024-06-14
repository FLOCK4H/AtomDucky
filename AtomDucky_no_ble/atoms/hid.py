# hid.py
import time
import board
from adafruit_hid.keyboard import Keyboard
from usb_hid import devices
from adafruit_hid.keycode import Keycode
import atoms.keycodes as keycodes
from atoms.analyzer import analyze_payload
import gc
from os import listdir
from random import randint, uniform

def load_payload_from_file():
    try:
        with open(f'atoms/payload.txt', 'r') as f:
            processed_payload = ''
            payload = ''
            for line in f:
                processed_line = line.strip().rstrip(';').replace('\\n', '\n').replace('\\t', '\t')
                processed_payload += processed_line
            payload = processed_payload
            gc.collect()
                
        return payload
    except OSError as e:
        print(f"Failed to load payloads: {str(e)}")
        return []

class AtomDucky:
    def __init__(self):
        self.kc = keycodes.KeyCodes()
        self.keyboard = Keyboard(devices)
        self.active_toggles = set()

    def handle_toggle(self, token):
        if token in self.active_toggles:
            self.keyboard.release(self.kc.toggles[token])
            self.active_toggles.remove(token)
        else:
            self.keyboard.press(self.kc.toggles[token])
            self.active_toggles.add(token)

    def execute_payload(self, tokens, skip_release=False):
        for token in tokens:
            if token.startswith('<') and token.endswith('>'):
                if "time" in token[1:-1]:
                    try:
                        sleep_time = float(token[token.find("time") + 4:-1])
                        time.sleep(sleep_time)
                    except ValueError:
                        print(f"Invalid time value in token '{token}'")
                elif token in self.kc.system_chars:
                    self.keyboard.send(self.kc.system_chars[token])
                elif token in self.kc.toggles:
                    self.handle_toggle(token)
            else:
                for char in token:
                    if char in self.kc.shift_char:
                        self.keyboard.press(Keycode.SHIFT)
                        self.keyboard.press(self.kc.shift_char[char])
                        self.keyboard.release_all()
                    elif char in self.kc.keys:
                        self.keyboard.send(self.kc.keys[char])
                    else:
                        print(f"No keycode mapping found for '{char}'")

                    # one day i'll figure out how it got here
                    # for active_toggle in self.active_toggles:
                    #     self.keyboard.press(self.kc.toggles[active_toggle])

        if not skip_release:
            for toggle in list(self.active_toggles):
                self.keyboard.release(self.kc.toggles[toggle])
            self.active_toggles.clear()

    def payloads_write(self, payload, skip_release=False):
        loop_payload = "<LOOP>" in payload
        if loop_payload:
            payload = payload.replace("<LOOP>", "")
        tokens = analyze_payload(payload)
        while True:
            self.execute_payload(tokens, skip_release=skip_release)
            if not skip_release:
                for toggle in list(self.active_toggles):
                    self.keyboard.release(self.kc.toggles[toggle])
                self.active_toggles.clear()
            if not loop_payload:
                break
            #                       !!!
            #  REMOVE THE DELAY ONLY IF YOU SURE WHAT YOU DOING
            #  USING <LOOP> WITHOUT TIMERS IS DANGEROUSLY STUPID 
            #                       !!!
            time.sleep(0.4)