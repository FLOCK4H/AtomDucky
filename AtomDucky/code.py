import wifi
import socketpool
import ipaddress
import sys
import gc
import time
import os

from atoms.networking import WebHost
from atoms.config_man import ConfigMan
from atoms.hid import AtomDucky, load_payload_from_file
from atoms.buttons import pixel
from atoms.colors import color

pixel.fill(color("yellow"))

class AP:
    def __init__(self, ssid="Atom Ducky", passw="", ap='TRUE', ip="10.0.0.15", mode="NORMAL"):
        self.ssid = ssid
        self.password = passw
        self.ip = ip
        self.ap = ap
        self.mode = mode
        self.config = ConfigMan()
        self.run()
        
    def parse_config(self, config_data):
        for line in config_data.splitlines():
            key, value = line.split('=')
            if key == 'IP':
                self.ip = value
            elif key == 'SSID':
                self.ssid = value
            elif key == 'PASSW':
                self.password = value
            elif key == 'MODE':
                self.mode = value
            elif key == 'AP':
                self.ap = value
    
    def run(self):
        try:
            contents = os.listdir('/atoms')
            cfg_exists = '_config' in contents
            if cfg_exists:
                print("Config exists! Reading the _config..")
                _config = self.config.read_config()
                self.parse_config(_config)
                print(f"""IP: {self.ip}
SSID: {self.ssid}
PASSW: {len(self.password) * '*'}
MODE: {self.mode}
AP: {self.ap}
""")
        except OSError:
            print("You probably need to enable read/write permissions, copy Atom Ducky's boot.py to your drive and press RESET!")
        time.sleep(0.2)
        self.rubber_mode_exec()

        if self.ap == 'FALSE':
            self.connect_to_ap()
        else:
            self.config_ips()
            self.start_host_ap()

        if not cfg_exists:
            self.config = ConfigMan(ip=self.ip, ssid=self.ssid, passw=self.password, mode=self.mode, ap=self.ap)
            self.config.write_config()

        self.config.edit_config(ip=self.ip)
        print(f"Changed the _config IP to: {self.ip}")

        webserver = WebHost(ip=self.ip, port=80)
    
    def rubber_mode_exec(self):
        if self.mode == "RUBBER":
            pixel.fill(color("red"))
            print("Detected RUBBER mode! Injecting first...")
            ducky = AtomDucky()
            payload = load_payload_from_file()
            if payload is not None:
                ducky.payloads_write(payload)
            gc.collect()
            pixel.fill(color("green"))
            time.sleep(0.5)
    
    def connect_to_ap(self):
        try:
            wifi.radio.hostname = "Atom-Ducky"
            print("Connecting to {}...".format(self.ssid))
            wifi.radio.connect(self.ssid, self.password)
            while not wifi.radio.connected:
                time.sleep(0.5)
            self.ip = wifi.radio.ipv4_address
            print("Connected! IP Address of the Atom Ducky: {}".format(self.ip))
        except ConnectionError as e:
            print("Connection failed! Failswitching to AP mode... Error reason:", str(e))
            self.ip = "10.0.0.15"
            self.config_ips()
            self.start_host_ap()

    def start_host_ap(self):
        wifi.radio.start_ap(ssid=self.ssid, password=self.password)
        print("Access Point started with SSID:", self.ssid)
        
    def config_ips(self):
        if not self.ip:
            self.ip = "10.0.0.15"
        ip = ipaddress.IPv4Address(self.ip)
        netmask = ipaddress.IPv4Address("255.255.255.0")
        gateway = ipaddress.IPv4Address(self.ip)
        wifi.radio.set_ipv4_address_ap(ipv4=ip, netmask=netmask, gateway=gateway)
        
def shutdown():
    ip = ipaddress.IPv4Address('192.168.1.42')
    netmask = ipaddress.IPv4Address("255.255.255.255")
    gateway = ipaddress.IPv4Address('192.168.1.42')
    wifi.radio.set_ipv4_address_ap(ipv4=ip, netmask=netmask, gateway=gateway)
    wifi.radio.stop_ap()
    wifi.radio.enabled = False

def main():
    try:
        ap = AP()
        time.sleep(2)
    
    except KeyboardInterrupt:
        print("Catched KeyboardInterrupt")
        shutdown()
            
if __name__ == "__main__":      
    main()