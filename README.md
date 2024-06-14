<div align="center">
  <img src="https://flockahh.b-cdn.net/logo.svg" alt="Logo" width="256" />
</div>

# Overview

Atom Ducky is a multiplatform HID device controlled through a web browser.
It's designed to function as a wirelessly operated Rubber Ducky, personal authenticator, or casual keyboard.
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
    - **BLE** (not related to HID - BONUS)
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

Let's fully cover the setup process, **including available microcontrollers**. From first commands in the terminal, to setup in the web interface of Atom Ducky.

1. We will need a Microcontroller device supporting HID, WiFi, and preferably BLE. Perfect choice would be an **AtomS3U**, link to official website: <a href="https://shop.m5stack.com/products/atoms3u">M5Stack AtomS3U</a>
