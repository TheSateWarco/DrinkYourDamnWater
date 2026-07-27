# main.py
import win32gui
import re
# ui pyside
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
# time 
import time
# multi processing
from multiprocessing import Process
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

class MainWindow(QMainWindow):
    def buttonClicked(self):
        # Initial active window title
        active_window = get_active_window_title()
        print("Activity tracking started...\n")

        try:# Start an infinite loop to track the active window
            while True:
                current_window = get_active_window_title()

                if current_window != active_window:

                    activity_name = extract_website_from_title(active_window) or active_window

                    print("window: " + current_window)
                    print("act: " + activity_name)
                    active_window = current_window
                    # popup
                    popUp = QMessageBox(self)
                    popUp.setWindowTitle("I have a question!")
                    popUp.setText("This is a simple dialog")
                    popUp.setIcon(QMessageBox.Information)
                    popUp.setStandardButtons(QMessageBox.Close)
                    button = popUp.exec()

                time.sleep(2)

        except KeyboardInterrupt:
            print("\n Tracking stopped.")
            # button response
    def __init__(self):
        super().__init__()
        # title
        self.setWindowTitle("Drink Your Damn Water!")
        # width, height
        self.resize(500,350)

        # checkable buttom
        button = QPushButton("press")
        button.setCheckable(True)
        button.clicked.connect(self.buttonClicked)
        self.setCentralWidget(button)


        

        


'''
def countdown(self, secs):
    s = secs
    while s:
        time.sleep(1)
        s -= 1

    print("Fire in the hole!!")
    # popup
    popUp = QMessageBox(self)
    popUp.setWindowTitle("I have a question!")
    popUp.setText("This is a simple dialog")
    popUp.setIcon(QMessageBox.Information)
    popUp.setStandardButtons(QMessageBox.Close)
    button = popUp.exec()
    if button == QMessageBox.Close:
        print("Drank Water!")   
        countdown(self,secs)     
'''

        


if __name__=='__main__':
    # QApplication instance
    app = QApplication()
    # create
    window = MainWindow()
    # show
    window.show()
    
    # time variable
    seconds = 3
    # keep window up indefinately
    app.exec()
    '''startTimer = Process(target=countdown(window,seconds))
    startTimer.start()
    startWindow = Process(target=app.exec())
    startWindow.start()'''