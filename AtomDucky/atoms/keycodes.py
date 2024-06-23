# keycodes.py
from adafruit_hid.keycode import Keycode

class KeyCodes:
    def __init__(self):
        self.keys = self.load_keys()
        
    def load_keys(self):
        keys_dict = {}
        
        letters = 'abcdefghijklmnopqrstuvwxyz'
        for letter in letters:
            keycode_attr = getattr(Keycode, letter.upper(), None)
            if keycode_attr is not None:
                keys_dict[letter] = keycode_attr
                
        numbers = {
            "1": Keycode.ONE,
            "2": Keycode.TWO,
            "3": Keycode.THREE,
            "4": Keycode.FOUR,
            "5": Keycode.FIVE,
            "6": Keycode.SIX,
            "7": Keycode.SEVEN,
            "8": Keycode.EIGHT,
            "9": Keycode.NINE,
            "0": Keycode.ZERO
        }
        keys_dict.update(numbers)
        
        spacers = {
            " ": Keycode.SPACE,
            "	": Keycode.SPACE,
            "\n": Keycode.RETURN,
        }
        keys_dict.update(spacers)
                
        chars = {
            "-": Keycode.MINUS,
            "=": Keycode.EQUALS,
            "[": Keycode.LEFT_BRACKET,
            "]": Keycode.RIGHT_BRACKET,
            "\\": Keycode.BACKSLASH,
            ";": Keycode.SEMICOLON,
            "'": Keycode.QUOTE,
            "`": Keycode.GRAVE_ACCENT,
            ",": Keycode.COMMA,
            ".": Keycode.PERIOD,
            "/": Keycode.FORWARD_SLASH,
        }
        keys_dict.update(chars)

        self.shift_char = {
            "!": Keycode.ONE,
            "@": Keycode.TWO,
            "#": Keycode.THREE,
            "$": Keycode.FOUR,
            "%": Keycode.FIVE,
            "^": Keycode.SIX,
            "&": Keycode.SEVEN,
            "*": Keycode.EIGHT,
            "(": Keycode.NINE,
            ")": Keycode.ZERO,
            "_": Keycode.MINUS,
            "+": Keycode.EQUALS,
            "{": Keycode.LEFT_BRACKET,
            "}": Keycode.RIGHT_BRACKET,
            "|": Keycode.BACKSLASH,
            ":": Keycode.SEMICOLON,
            "\"": Keycode.QUOTE,
            "~": Keycode.GRAVE_ACCENT,
            "<": Keycode.COMMA,
            ">": Keycode.PERIOD,
            "?": Keycode.FORWARD_SLASH,
        }
        
        uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in uppercase_letters:
            keycode_attr = getattr(Keycode, letter, None)
            if keycode_attr is not None:
                self.shift_char[letter] = keycode_attr
        
        self.system_chars = {
            "<ESC>": Keycode.ESCAPE,
            "<BSC>": Keycode.BACKSPACE,
            "<TAB>": Keycode.TAB,
            "<SCR>": Keycode.PRINT_SCREEN,
            "<SLK>": Keycode.SCROLL_LOCK,
            "<PAS>": Keycode.PAUSE,
            "<INS>": Keycode.INSERT,
            "<HOE>": Keycode.HOME,
            "<PGU>": Keycode.PAGE_UP,
            "<PGD>": Keycode.PAGE_DOWN,
            "<ARR>": Keycode.RIGHT_ARROW,
            "<ARL>": Keycode.LEFT_ARROW,
            "<ARD>": Keycode.DOWN_ARROW,
            "<ARU>": Keycode.UP_ARROW,
            "<NLK>": Keycode.KEYPAD_NUMLOCK,
            "<APP>": Keycode.APPLICATION,
            "<PWR>": Keycode.POWER, # macOS only
            "<GUI>": Keycode.GUI, # MAC or WINDOWS key / Search key for android/ ios
            "<CMD>": Keycode.GUI, 
            "<WIN>": Keycode.GUI,  
            "<CTL>": Keycode.LEFT_CONTROL,
            "<SPC>": Keycode.SPACEBAR,
            "<RET>": Keycode.RETURN
            }
        
        self.toggles = {
            "<CTRL>": Keycode.LEFT_CONTROL,
            "<LALT>": Keycode.LEFT_ALT,
            "<CTRR>": Keycode.RIGHT_CONTROL,
            "<RALT>": Keycode.RIGHT_ALT,
            "<GCMD>": Keycode.COMMAND, # or GUI or WINDOWS
            "<LSHT>": Keycode.LEFT_SHIFT,
            "<RSHT>": Keycode.RIGHT_SHIFT,
            "<CAPS>": Keycode.CAPS_LOCK
            }
        
        return keys_dict