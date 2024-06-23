<div align="center">
  <img src="https://flockahh.b-cdn.net/logo.svg" alt="Logo" width="256" />
</div>

# Overview

Atom Ducky is a **HID** device controlled through a web browser.
It's designed to function as a **wirelessly operated Rubber Ducky, personal authenticator, or casual keyboard.**
Its primary aim is to help ethical hackers gain knowledge about Rubber Ducky devices while integrating their use into everyday life.

# Features

- **Web Interface**
    - **HID**
      - **Inject Payload**
      - **Modify Payload**
      - **Live Keyboard**
      - **Single Payload**
      - **Rubber Mode**
      - **Templates Manager**
    - **BLE** (not related to HID functions)
      - **Sour Apple attack**
      - **Samsung Flood attack**
    - **Ducky**
      - Ducky image 🦆
- **WiFi**
    - **Access Point mode**
    - **Network mode**
    - **Interface**
- **Config**
    - **Switch between AP/Network modes**
    - **Assign custom IP for the Access Point**
    - **Change SSID and Password easily**
    - **Switch between RUBBER/NORMAL modes**

# Setup

> [!IMPORTANT]
> This project may not be suitable for the very beginners, as it requires some knowledge of the operating system command line interface.

Let's fully cover the setup process, **including available microcontrollers**. From first commands in the terminal, to the web interface of Atom Ducky.

First, we will need a Microcontroller device supporting HID, WiFi, and preferably BLE. Perfect choice would be an **AtomS3U**, link to official website: <a href="https://shop.m5stack.com/products/atoms3u">M5Stack AtomS3U</a>.

## Supported Microcontrollers

<sub>For full version of AtomDucky</sub>

**HID, WiFi and BLE:**

<details>
<summary>Click to see full list</summary>
  
<br />

  - Adafruit Feather ESP32 V2
  - Adafruit Feather ESP32-S3 No PSRAM
  - Adafruit QT Py ESP32-S3 no psram
  - Ai Thinker ESP32-CAM
  - Arduino Nano ESP32
  - Cytron EDU PICO W
  - Cytron Maker Feather AIoT S3
  - DFRobot FireBeetle 2 ESP32-S3
  - ES3ink
  - ESP32-S3-Box-2.5
  - ESP32-S3-Box-Lite
  - ESP32-S3-DevKitC-1-N32R8
  - ESP32-S3-DevKitC-1-N8
  - ESP32-S3-DevKitC-1-N8R2
  - ESP32-S3-DevKitC-1-N8R8
  - ESP32-S3-DevKitC-1-N8R8-with-HACKTABLET
  - ESP32-S3-DevKitM-1-N8
  - ESP32-S3-EYE
  - ESP32-S3-USB-OTG-N8
  - FeatherS3
  - FeatherS3 Neo
  - LILYGO T-DISPLAY S3 v1.2
  - LILYGO TEMBED ESP32S3
  - LOLIN S3 16MB Flash 8MB PSRAM
  - LOLIN S3 PRO 16MB Flash 8MB PSRAM
  - M5Stack AtomS3
  - M5Stack AtomS3 Lite
  - M5Stack AtomS3U
  - MakerFabs-ESP32-S3-Parallel-TFT-With-Touch-7inch
  - NanoS3
  - Oxocard Artwork
  - Oxocard Connect
  - Oxocard Galaxy
  - Oxocard Science
  - Pimoroni Badger 2040 W
  - Pimoroni Pico DV Base W
  - Pimoroni Plasma 2040W
  - ProS3
  - Raspberry Pi Pico W
  - Seeed Studio XIAO ESP32C3
  - Spotpear ESP32C3 LCD 1.44
  - Sunton-ESP32-8048S070
  - ThingPulse Pendrive S3
  - TinyS3
  - VCC-GND YD-ESP32-S3 (N16R8)
  - VCC-GND YD-ESP32-S3 (N8R8)
  - Waveshare ESP32-S3-GEEK
  - Waveshare ESP32-S3-Pico
  - Waveshare ESP32-S3-Zero
  - Waveshare ESP32S3 LCD 1.28
  - sunton_esp32_2432S032C
  - 
</details>

<sub>For no_ble version of AtomDucky</sub>

**Boards supporting WiFi and HID:**

<details>
<summary>Click to see full list</summary>
  
  - ATMegaZero ESP32-S2
  - Adafruit Camera
  - Adafruit Feather ESP32-S2 Reverse TFT
  - Adafruit Feather ESP32-S2 TFT
  - Adafruit Feather ESP32-S3 Reverse TFT
  - Adafruit Feather ESP32-S3 TFT
  - Adafruit Feather ESP32S2
  - Adafruit Feather ESP32S3 4MB Flash 2MB PSRAM
  - Adafruit Feather ESP32S3 No PSRAM
  - Adafruit FunHouse
  - Adafruit MagTag
  - Adafruit MatrixPortal S3
  - Adafruit Metro ESP32S2
  - Adafruit Metro ESP32S3
  - Adafruit QT Py ESP32-S3 4MB Flash 2MB PSRAM
  - Adafruit QT Py ESP32-S3 no psram
  - Adafruit QT Py ESP32S2
  - Adafruit-Qualia-S3-RGB666
  - Ai Thinker ESP32-CAM
  - Arduino Nano ESP32
  - Artisense Reference Design RD00
  - AutosportLabs-ESP32-CAN-X2
  - BLING!
  - BPI-Bit-S2
  - BPI-Leaf-S3
  - BPI-PicoW-S3
  - BastWiFi
  - Bee-Data-Logger
  - Bee-Motion-S3
  - Bee-S3
  - BlizzardS3
  - ColumbiaDSL-Sensor-Board-V1
  - CrumpS2
  - Cytron EDU PICO W
  - Cytron Maker Feather AIoT S3
  - DFRobot FireBeetle 2 ESP32-S3
  - Deneyap Mini
  - Deneyap Mini v2
  - ES3ink
  - ESP 12k NodeMCU
  - ESP32-S2-DevKitC-1-N4
  - ESP32-S2-DevKitC-1-N4R2
  - ESP32-S2-DevKitC-1-N8R2
  - ESP32-S3-Box-2.5
  - ESP32-S3-Box-Lite
  - ESP32-S3-DevKitC-1-N32R8
  - ESP32-S3-DevKitC-1-N8
  - ESP32-S3-DevKitC-1-N8R2
  - ESP32-S3-DevKitC-1-N8R8
  - ESP32-S3-DevKitC-1-N8R8-with-HACKTABLET
  - ESP32-S3-DevKitM-1-N8
  - ESP32-S3-EYE
  - ESP32-S3-USB-OTG-N8
  - Espressif-ESP32-S3-LCD-EV-Board
  - FeatherS2
  - FeatherS2 Neo
  - FeatherS3
  - FeatherS3 Neo
  - Flipper Zero Wi-Fi Dev
  - Franzininho WIFI w/Wroom
  - Franzininho WIFI w/Wrover
  - Freenove ESP32-WROVER-DEV-CAM
  - Gravitech Cucumber M
  - Gravitech Cucumber MS
  - Gravitech Cucumber R
  - Gravitech Cucumber RS
  - HMI-DevKit-1.1
  - Hardkernel Odroid Go
  - Heltec ESP32-S3-WIFI-LoRa-V3
  - HexKyS2
  - IoTs2
  - Kaluga 1
  - LILYGO T-DECK
  - LILYGO T-DISPLAY S3 v1.2
  - LILYGO TEMBED ESP32S3
  - LILYGO TTGO T8 ESP32-S2
  - LILYGO TTGO T8 ESP32-S2 w/Display
  - LOLIN S3 16MB Flash 8MB PSRAM
  - LOLIN S3 MINI 4MB Flash 2MB PSRAM
  - LOLIN S3 PRO 16MB Flash 8MB PSRAM
  - Lilygo T-watch 2020 V3
  - M5Stack AtomS3
  - M5Stack AtomS3 Lite
  - M5Stack AtomS3U
  - M5Stack Cardputer
  - M5Stack CoreS3
  - M5Stack Dial
  - MakerFabs-ESP32-S3-Parallel-TFT-With-Touch-7inch
  - MicroDev microS2
  - MixGo CE
  - NanoS3
  - Neuron
  - Oak Dev Tech PixelWing ESP32S2
  - Oxocard Artwork
  - Oxocard Connect
  - Oxocard Galaxy
  - Oxocard Science
  - Pajenicko PicoPad
  - Pimoroni Badger 2040 W
  - Pimoroni Inky Frame 5.7
  - Pimoroni Inky Frame 7.3
  - Pimoroni Pico DV Base W
  - Pimoroni Plasma 2040W
  - ProS3
  - Raspberry Pi Pico W
  - S2Mini
  - S2Pico
  - Saola 1 w/Wroom
  - Saola 1 w/Wrover
  - Seeed Studio XIAO ESP32C3
  - Spotpear ESP32C3 LCD 1.44
  - Sunton-ESP32-8048S070
  - TTGO T8 ESP32-S2-WROOM
  - Targett Module Clip w/Wroom
  - Targett Module Clip w/Wrover
  - ThingPulse Pendrive S3
  - TinyS2
  - TinyS3
  - TinyWATCH S3
  - VCC-GND YD-ESP32-S3 (N16R8)
  - VCC-GND YD-ESP32-S3 (N8R8)
  - Waveshare ESP32-S2-Pico
  - Waveshare ESP32-S2-Pico-LCD
  - Waveshare ESP32-S3-GEEK
  - Waveshare ESP32-S3-Pico
  - Waveshare ESP32-S3-Zero
  - Waveshare ESP32S3 LCD 1.28
  - nanoESP32-S2 w/Wrover
  - nanoESP32-S2 w/Wroom
  - senseBox MCU-S2 ESP32S2
  - sunton_esp32_2432S032C

</details>

> [!TIP]
> Choosing a board supporting BLE will let you have two bonus features, but they are not relevant to the keyboard at all.

## Installing CircuitPython

Not not every board has CircuitPython installed by default (very few to be clear), and installation process may vary between devices, the general advice is to plug your microcontroller into the computer and visit <a href="https://circuitpython.org/downloads">CircuitPython Official Website</a>
and search for your board.

**Boards without .UF2 bootloader**:

<details>
<summary>Click to expand</summary>
  
### Dependencies

- Python
- esptool

In case of the ATOM S3U based on ESP32S3 (<a href="https://circuitpython.org/board/m5stack_atoms3u/">CircuitPython M5stack AtomS3U</a>), scroll down until you see:

![image](https://github.com/FLOCK4H/AtomDucky/assets/161654571/482e15f0-5554-43ae-95fb-b34fe332ce88)

Click on **Download Bootloader ZIP** on the website, create a folder anywhere, and unpack the downloaded **.zip** file there.
Save the path of the folder to your clipboard, or just remember it.

For flashing the **bootloader**, we will need an **esptool.py**, we can also try using our webbrowser <a href="https://adafruit.github.io/Adafruit_WebSerial_ESPTool/">ESP Web Flasher</a>.

**Install esptool.py**, use terminal and make sure you have <a href="https://www.python.org/downloads/">Python</a> installed.

```
  $ pip install esptool
```

**Flash the device with bootloader**.

Before flashing, the board has to enter into the bootloader mode, this is different between all boards, usually holding the button itself works, but in case of Atom S3U we must hold the main button and the reset button until the green light.

<sub>The flash offset '-z' may vary, please check which flash offset your board has, common offsets to try are '0, 0x0, 0x1000'</sub>

```
  # Find the port

  # Windows:
  $ mode
  # Look for devices that have 9600-460800 Baud
      Status for device COM13:
      ------------------------
          Baud:            9600
          Parity:          None
          Data Bits:       8
          Stop Bits:       1.5
          Timeout:         OFF
          XON/XOFF:        OFF
          CTS handshaking: OFF
          DSR handshaking: OFF
          DSR sensitivity: OFF
          DTR circuit:     OFF
          RTS circuit:     OFF

  # Linux:
  dmesg | grep tty
```

Next, use the esptool to flash:

```
  # (--port /dev/ttyPORT for linux)

  $ esptool --port COM13 erase_flash
  $ esptool --port COM13 --baud 460800 write_flash -z 0 /path/to/your/downloaded/bootloader/combined.bin
```

Great, now click RESET button once, or just unplug and plug the board.

There should be a new drive detected by your computer, usually with the BOOT name or 'BOARD_NAMEBOOT'.

</details>

<br />

**With bootloader installed**:

Visit the <a href="https://circuitpython.org/downloads">CircuitPython Official Website</a> and search for your board, the CircuitPython version that interests us is:

![image](https://github.com/FLOCK4H/AtomDucky/assets/161654571/d592cd25-76b1-401b-a2a0-74855161a2fe)

Download the .uf2 file and just copy or move it to the BOOT drive of the microcontroller.

This same drive should now be named **CIRCUITPY**, that means we have **successfully installed CircuitPython**.

## Recipe for Atom Ducky

1. Clone this repository to your local drive:

```
  $ git clone https://github.com/FLOCK4H/AtomDucky
```

2. Move all files from AtomDucky folder, or AtomDucky_no_ble folder for boards without BLE module, excluding README.md, to the **CIRCUITPY** drive.

3. Press RESET button once, or plug the device again.

**Voila, the AtomDucky is ready to use, and it should already create an Access Point**

## Web Setup

1. The LED on the board should signal whether the device is starting (yellow light) or has initialized successfully (cyan light).

2. We need to join the Access Point hosted by our device, ESSID of the network is Atom Ducky, and it should have no encryption.

![IMG_2984](https://github.com/FLOCK4H/AtomDucky/assets/161654571/113850db-657e-4f4f-9356-bcf43580ee4c)

3. Open the web browser and navigate to http://10.0.0.15

![IMG_2987](https://github.com/FLOCK4H/AtomDucky/assets/161654571/065ae33c-7281-40df-ba77-af0ae3195d34)

4. Click on a white hamburger dropdown menu and select `Setup`

![IMG_2988](https://github.com/FLOCK4H/AtomDucky/assets/161654571/4e671ab6-9422-487e-9a07-388178ad47da)

5. Configuration:

- Access Point IP address, we do not need to change it at all, so just press `Next` whenever you're ready.
- SSID is either your local **Network SSID** or **Atom Ducky Access Point SSID**, if you want to pair with existing network, you need to provide its SSID.
- Password, can be left empty, can be set, or in case of pairing with existing network - we must provide correct password.
- Device Mode, there are two, first is `NORMAL`, second is `RUBBER`. The difference is that `RUBBER` mode will inject the payload from `atoms/payload.txt` before the initialization of the web interface.
- AP Mode, leave `TRUE` for the Atom Ducky access point, or necessarily change to `FALSE` if you are connecting it to your network.

**Click `Save` button, this will save the config to `atoms/_config` file and restart the board**.

Connecting Atom Ducky to your network will result in different IP address assigned to the device (and this address may change irregularly), without this address, it's not possible to open the web interface. One may find the new IP address on network's config website in e.g. `Attached Devices` subpage.

<sub>The hostname is ATOM-DUCKY</sub>

![image](https://github.com/FLOCK4H/AtomDucky/assets/161654571/148595d0-ba67-4a85-83e4-6a886d151db3)

# Usage

After plugging the Atom Ducky into a device supporting HID (computer, smartphone etc.), we want to open the web interface (open web browser and go to the IP address of Atom Ducky).

**Web interface buttons:**

- Inject Payload - :)
- Modify Payload - Modify and save the payload
- Live Keyboard - Open keyboard layout, press keys to send them
- Single Payload - Compose and send a single payload (not affecting payload.txt)
- Templates Manager - Add, modify and run payloads
- Rubber Mode - Toggle Rubber Mode (Rubber Mode does inject the payload before the web interface is initialized)

In the hamburger dropdown menu, there is a `Settings` page where we can modify `_config` file easily.

![image](https://github.com/FLOCK4H/AtomDucky/assets/161654571/b9589b66-3d51-4141-96bd-01c4276c9d32)

The **BLE** section is fully additional, and it contains functions that when launched can crash/ freeze iOS devices, or disrupt others in using their iOS/Samsung phones.

- Sour Apple - [SourApple](https://github.com/RapierXbox/ESP32-Sour-Apple)
- Samsung BLE Spam - [ble-spam-samsung-circuitpy](https://github.com/FLOCK4H/ble-spam-samsung-circuitpy)





