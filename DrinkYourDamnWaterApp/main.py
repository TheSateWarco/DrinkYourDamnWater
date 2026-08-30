# main.py

# helper functions
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
    returnToMain = Signal()
    # initialize window
    def __init__(self):
        super().__init__()
        
            #self.setStyleSheet("QMainWindow{background-image: url('./hand-drawn-speech-bubble-cartoon-ah-shout-png-1343987513.png')};")
        # self.setStyleSheet("QMainWindow{background-color: #C5D6F0;}"
        #                     "QPushButton{background-color: #BBCEF0;" 
        #                     "border-style: solid;"
        #                 "border-width: 1px;"
        #                 "border-color: #AEBAD2;}")
        # title
        self.setWindowTitle("Drink Your Damn Water!")
        # width, height
        self.setFixedSize(300,150)
        self.returnToMain.connect(lambda: program.createMainScreen(self))
        program.createMainScreen(self)

    # start button
    def startClicked(self):
        # load json file
        data = openJson()
        # change start to stop button
        stopBtn = QPushButton("Stop")
        global generalTimerNote,doomScrollNoteTimerNote,websiteNote,appTimerNote
        for rule in Rule:
            record = data["UserSettings"][rule.value]
            amount = record["drinkAmount"]
            drinksize = program.checkSize(amount, record["size"])
            NOTIFIERS[rule].message = "Take " + str(amount) + " " + drinksize + " " + "of water!"

        doomScrollActive = data["UserSettings"][Rule.DOOMSCROLL_TIMER.value]["active"]
        
        stopBtn.clicked.connect((lambda: program.stopProgram(self)))
        
        layout = QVBoxLayout()
        layout.addWidget(stopBtn)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        n = int(data["UserSettings"][Rule.TIMER.value]["time"])
        startProgramThread = thread.Thread(target=program.startProgram, args=[n,data["UserSettings"][Rule.WEBSITE.value]["list"], data["UserSettings"][Rule.APPLICATION.value]["list"],data["UserSettings"][Rule.TIMER.value]["active"],doomScrollActive,int(data["UserSettings"][Rule.DOOMSCROLL_TIMER.value]["time"])],daemon=True)
        self.workerThread = startProgramThread
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
                    "3. Experimental: Uses webcam facial tracking to see if\n"+ 
                    "you are doomscrolling on your phone. This is AUTOMATICALLY"+
                    "turned off my default\n\n"+
                    "Note: These can be changed in settings"
                    )
        help.exec()
    # credits pop up
    def creditsClicked(self):
            credits = QMessageBox()
            credits.setWindowTitle("Credits")
            credits.setText("Main Programmer: TheSateWarco")
            credits.exec()
    # settings pop up
    def settingsClicked(self):
        data = openJson()
        settings = QDialog()
        settings.setWindowTitle("Settings")

        allRuleWidgets: dict[Rule, dict[str, QWidget]] = {}

        # Buttons
        restore = QPushButton("Restore Default")
        restore.clicked.connect(lambda: config.changeConfig("restore", data, self, allRuleWidgets))
        apply = QPushButton("Apply Changes")
        apply.clicked.connect(lambda: config.changeConfig("apply", data, self, allRuleWidgets))
        close = QPushButton("Close")
        close.clicked.connect(settings.accept)

        layout = QVBoxLayout()
        buttons = QHBoxLayout()
        buttons.addWidget(restore)
        buttons.addWidget(apply)
        buttons.addWidget(close)

        for rule in Rule:
            curContainer, widgets = config.makeRule(data, rule)
            allRuleWidgets[rule] = widgets
            layout.addLayout(curContainer)
            layout.addSpacerItem(QSpacerItem(1, 40))

        layout.addLayout(buttons)
        settings.setLayout(layout)
        settings.exec()



# make sure this is main
if __name__=='__main__':    
    # show window
    n = 10
    
    # QApplication instance
    app = QApplication()
    app.setWindowIcon(QIcon(LOGO_PATH))
    # create
    window = MainWindow()
    window.setWindowIcon(QIcon(LOGO_PATH))
    # show
    window.show()
    # keep window up indefinately
    app.exec()
    
