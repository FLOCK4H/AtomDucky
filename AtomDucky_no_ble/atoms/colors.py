text_to_rgb = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "brown": (165, 42, 42),
    "pink": (255, 192, 203),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "lime": (0, 255, 0),
    "aqua": (0, 255, 255),
    "fuchsia": (255, 0, 255),
    "silver": (192, 192, 192),
    "gold": (255, 215, 0),
    "indigo": (75, 0, 130),
    "violet": (238, 130, 238),
    "plum": (221, 160, 221),
    "rose": (255, 0, 127),
    "lavender": (230, 230, 250),
    "tan": (210, 180, 140),
    "coral": (255, 127, 80),
    "turquoise": (64, 224, 208),
    "wheat": (245, 222, 179),
    "khaki": (240, 230, 140),
    "beige": (245, 245, 220),
    "peach": (255, 218, 185),
    "mint": (189, 252, 201),
    "azure": (240, 255, 255)
}

def color(color):
    for text, rgb in text_to_rgb.items():
        if color == text:
            return rgb