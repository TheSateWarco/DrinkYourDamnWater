# tracking.py
from lib import *
# program tracking


def get_active_window_title():
    window=win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def extract_website_from_title(title):
    #try to extract the website name from the browser title format
    match=re.search(r'(.+) - (Google Chrome|Mozilla Firefox|Microsoft Edge|DuckDuckGo|Safari)', title) # Regular expression to match the title format
    print(match)
    # If the title matches the expected format, extract the website name
    # and return it without the browser name
    if match:
        return match.group(1)
    return None