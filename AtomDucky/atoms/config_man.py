class ConfigMan:
    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip', '10.0.0.15')
        self.ssid = kwargs.get('ssid', 'Atom Ducky')
        self.passw = kwargs.get('passw', '')
        self.mode = kwargs.get('mode', 'NORMAL')
        self.ap = kwargs.get('ap', 'TRUE')

    def write_config(self):
        try:
            with open('atoms/_config', 'w') as f:
                f.write(f"""IP={self.ip}
SSID={self.ssid}
PASSW={self.passw}
MODE={self.mode}
AP={self.ap}
""")
                print("Successfully saved the config!")
        except Exception as e:
            print("Error when writing to _config!", str(e))

    def read_config(self):
        try:
            with open('atoms/_config', 'r') as f:
                data = f.read()
                return data
        except Exception as e:
            print("Error when reading _config!", str(e))

    def edit_config(self, **kwargs):
        current_config = self.read_config()

        config_dict = {}
        for line in current_config.splitlines():
            if '=' in line: 
                key, value = line.split('=', 1)
                config_dict[key.strip()] = value.strip()

        for key, value in kwargs.items():
            if key.upper() in config_dict:
                config_dict[key.upper()] = value

        self.ip = config_dict.get('IP', self.ip)
        self.ssid = config_dict.get('SSID', self.ssid)
        self.passw = config_dict.get('PASSW', self.passw)
        self.mode = config_dict.get('MODE', self.mode)
        self.ap = config_dict.get('AP', self.ap)
        self.write_config()
        print("Successfully modified the config!")
