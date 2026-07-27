# main.py

# helper functions
    # app/website tracking
import tracking as tracking
    # settings
import settings as config
    # program
import app as program
from lib import *


def openJson():
    with open('settings.json', "r") as json_file:
        data = json.load(json_file)
        return data
        
# main window
class MainWindow(QMainWindow):
    
    # initialize window
    def __init__(self):
        super().__init__()
        # title
        self.setWindowTitle("Drink Your Damn Water!")
        # width, height
        self.resize(200,100)

        program.createMainScreen(self)

    # start button
    def startClicked(self):
        # load json file
        data = openJson()
        # change start to stop button
        stopBtn = QPushButton("Stop")
        global state,generalTimerNote,doomScrollNoteTimerNote,websiteNote,appTimerNote
        for x in range (4):
            amount = data["UserSettings"][x]["drinkAmount"]
            drinksize = program.checkSize(amount, data["UserSettings"][x]["size"])
            match x:
                case 0:
                    appTimerNote.message ="Take " + str(data["UserSettings"][x]["drinkAmount"]) + " "+ drinksize+ " " + "of water!"
                case 1:
                    websiteNote.message ="Take " + str(data["UserSettings"][x]["drinkAmount"]) + " "+ drinksize+ " " + "of water!"
                
                case 2:
                    generalTimerNote.message ="Take " + str(data["UserSettings"][x]["drinkAmount"]) + " "+ drinksize+ " " + "of water!"
                case 3:
                    doomScrollNoteTimerNote.message ="Take " + str(data["UserSettings"][x]["drinkAmount"]) + " "+ drinksize+ " " + "of water!"

        doomScrollActive = data["UserSettings"][3]["active"]
        
        stopBtn.clicked.connect((lambda: program.stopProgram(self)))
        
        layout = QVBoxLayout()
        layout.addWidget(stopBtn)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        n = int(data["UserSettings"][2]["time"])
        startProgramThread = thread.Thread(target=program.startProgram, args=[n,data["UserSettings"][1]["list"], data["UserSettings"][0]["list"],data["UserSettings"][2]["active"],doomScrollActive,int(data["UserSettings"][3]["time"])])
        # start notification system (check app py)
        startProgramThread.start()

    # help pop up
    def helpClicked(self):
        help = QMessageBox()
        help.setWindowTitle("Help")
        help.setText("This is a drinking water reminder app\n\n" +
                    "Features:\n"+
                    "1. Uses a general timer to remind you to drink water\n"+
                    "2. Tracks what applications and websites are open and\n"+
                    "will notify when it is opened after a few seconds\n"+
                    "3. Uses webcam facial tracking to see if you are doomscrolling on your phone\n\n"+
                    "Note: These can be changed in settings"
                    )
        help.exec()
    # credits pop up
    def creditsClicked(self):
            credits = QMessageBox()
            credits.setWindowTitle("Credits")
            credits.setText("Programming: TheSateWarco")
            credits.exec()
    # settings pop up
    def settingsClicked(self):
        data = openJson()
        settings = QDialog()
        settings.setWindowTitle("Settings")
            # number of rules
        ruleAmount = len(data["UserSettings"])
        # row/col num (ruleAmount, number of items in a rule)
        rows, cols = ruleAmount, len(data["UserSettings"][ruleAmount -1])
            # make widget arr
        widgetMatrix = [[0 for c in range(cols)] for r in range(rows)]

        # Buttons
            # settings button
        restore = QPushButton("Restore Default")
        restore.clicked.connect(lambda: config.changeConfig("restore", data, self, ruleAmount, widgetMatrix))
            # settings button
        apply = QPushButton("Apply Changes")
        apply.clicked.connect(lambda: config.changeConfig("apply", data, self, ruleAmount, widgetMatrix))
            # settings button
        close = QPushButton("Close")
        close.clicked.connect(settings.accept)

        # main laiout
        layout = QVBoxLayout()
        # button layout
        buttons = QHBoxLayout()
        buttons.addWidget(restore)
        buttons.addWidget(apply)
        buttons.addWidget(close)
        # appContainer
        
            # for length of settings
        for r in range(rows):
                # make rule
            curContainer = config.makeRule(data, widgetMatrix, r)
            layout.addLayout(curContainer)
            layout.addSpacerItem(QSpacerItem(1,40))
        layout.addLayout(buttons)
        settings.setLayout(layout)
        # show all settings
        # check whch button clicked
        settings.exec()
        # save changes button

    


# make sure this is main
if __name__=='__main__':    
    # show window
    state = 0
    n = 10
    
    # QApplication instance
    app = QApplication()
    # create
    window = MainWindow()
    # show
    window.show()
    #program.startProgram(n, state)
    # keep window up indefinately
    app.exec()
    
