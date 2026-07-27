# settings.py
# ui pyside
from lib import *

# write to the setting json
def changeConfig(instruction, data, settings, ruleAmount,widgetMatrix):
    if instruction == "restore":
        data["UserSettings"] = data["OGSettings"]
    with open('settings.json', "w") as json_file:
        json.dump(data, json_file, indent=2)
    if instruction == "restore":
        for numOfRule in range(ruleAmount):
            print(numOfRule)
            match (numOfRule):
                case 0:
                    # set the value to current calue in python dict
                    widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][0]["drinkAmount"]))
                    # set the value to current calue in python dict
                    widgetMatrix[numOfRule][1].setCurrentIndex(int(data["UserSettings"][0]["size"]))
                    widgetMatrix[numOfRule][2].clear()
                    for i in data["UserSettings"][0]["list"]:
                        print(i)
                        widgetMatrix[numOfRule][2].addItem(i)
                        
                case 1:
                    # set the value to current calue in python dict
                    widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][1]["drinkAmount"]))
                    # set the value to current calue in python dict
                    widgetMatrix[numOfRule][1].setCurrentIndex(int(data["UserSettings"][1]["size"]))
                    widgetMatrix[numOfRule][2].clear()
                    for i in data["UserSettings"][1]["list"]:
                        widgetMatrix[numOfRule][2].addItem(i)
                case 2:
                    widgetMatrix[numOfRule][3].setChecked(data["UserSettings"][2]["active"])
                    widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][2]["time"]))
                    widgetMatrix[numOfRule][1].setValue(int(data["UserSettings"][2]["drinkAmount"]))
                    widgetMatrix[numOfRule][2].setCurrentIndex(int(data["UserSettings"][2]["size"]))

                case 3:
                    widgetMatrix[numOfRule][3].setChecked(data["UserSettings"][3]["active"])
                    widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][3]["time"]))
                    widgetMatrix[numOfRule][1].setValue(int(data["UserSettings"][3]["drinkAmount"]))
                    widgetMatrix[numOfRule][2].setCurrentIndex(int(data["UserSettings"][3]["size"]))
        settings.update()
# change the python dictionary
def changeValue(data, numOfRule, subpartOfRule, newValue):
        data["UserSettings"][numOfRule][subpartOfRule] = newValue
        

def makeRule(data, widgetMatrix, numOfRule):
    # cointainer that will be returned
    container = QVBoxLayout()
    # message includes text, num range, and size of drink
    message = QHBoxLayout()
    # check numOfRule if the number is a website or application
    if numOfRule == 0 or numOfRule == 1:
        # text shown for the rule
        string = "Following websites will require "
        if numOfRule == 0:
            string = "Following applications will require "
        label = QLabel(string)
        # num range of amount of drinks
        widgetMatrix[numOfRule][0] = QSpinBox()
        widgetMatrix[numOfRule][0].setRange(1,10)
        
        # dropdown of type of drink
        widgetMatrix[numOfRule][1] = QComboBox()
        widgetMatrix[numOfRule][1].addItems(["Sip", "Shot", "Cup"])
        
        # - button (delete)
        delete = QPushButton("-")
        
        # message stuff
        message.addWidget(label)
        message.addWidget(widgetMatrix[numOfRule][0])
        message.addWidget(widgetMatrix[numOfRule][1])
        message.addWidget(delete)
        container.addLayout(message)

        # set values as currents
        if numOfRule == 0:
            # set the value to current calue in python dict
            widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][0]["drinkAmount"]))
            # set the value to current calue in python dict
            widgetMatrix[numOfRule][1].setCurrentIndex(int(data["UserSettings"][0]["size"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "drinkAmount")
            # connect the amount change signel to the function
            widgetMatrix[0][0].textChanged.connect(changeVal)
            # set change val func to type
            changeVal = partial(changeValue,data, numOfRule, "size")
            # connect the amount change signel to the function
            widgetMatrix[0][1].currentIndexChanged.connect(changeVal)
        else:
            # set the value to current calue in python dict
            widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][1]["drinkAmount"]))
            # set the value to current calue in python dict
            widgetMatrix[numOfRule][1].setCurrentIndex(int(data["UserSettings"][1]["size"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "drinkAmount")
            # connect the amount change signel to the function
            widgetMatrix[1][0].textChanged.connect(changeVal)
            # set change val func to type
            changeVal = partial(changeValue,data, numOfRule, "size")
            # connect the amount change signel to the function
            widgetMatrix[1][1].currentIndexChanged.connect(changeVal)

        # make list of web/apps
        widgetMatrix[numOfRule][2] = QListWidget()
        widgetMatrix[numOfRule][2].setDisabled(False)
        if numOfRule == 0:
            
            for i in data["UserSettings"][0]["list"]:
                widgetMatrix[numOfRule][2].addItem(i)
        else:
            for i in data["UserSettings"][1]["list"]:
                widgetMatrix[numOfRule][2].addItem(i)
        # connect delete button
        delete.clicked.connect(lambda: deleteItem(data, numOfRule, widgetMatrix[numOfRule][2]))

        # insert box
        insertLine = QHBoxLayout()
        editBox = QLineEdit("New Item")

        # + button
        widgetMatrix[numOfRule][3] = QPushButton("+")
        insertLine.addWidget(editBox)
        insertLine.addWidget(widgetMatrix[numOfRule][3])
        # conned add button
        if numOfRule == 0:
            widgetMatrix[numOfRule][3].clicked.connect(lambda: addNewLine(data, 0, widgetMatrix[numOfRule][2], editBox))
        else:
            widgetMatrix[numOfRule][3].clicked.connect(lambda: addNewLine(data, 1, widgetMatrix[numOfRule][2], editBox))
        
        
        container.addWidget(widgetMatrix[numOfRule][2])
        container.addLayout(insertLine)

    # static rule (2 or 3)
    else:
        # checkbox
        widgetMatrix[numOfRule][3] = QCheckBox()
        # text
        string = "After "
        label1 = QLabel(string)
        # sec range
        widgetMatrix[numOfRule][0] = QSpinBox()
        widgetMatrix[numOfRule][0].setRange(0,600)
        string = " minutes "
        if numOfRule == 3:
            string = " minutes of doomscrolling, take "
        label2 = QLabel(string)
        # num range
        widgetMatrix[numOfRule][1] = QSpinBox()
        widgetMatrix[numOfRule][1].setRange(1,10)
        # dropdown
        widgetMatrix[numOfRule][2] = QComboBox()
        widgetMatrix[numOfRule][2].addItems(["Sip", "Shot", "Cup"])
        
        # message stuff
        message.addWidget(widgetMatrix[numOfRule][3])
        message.addWidget(label1)
        message.addWidget(widgetMatrix[numOfRule][0])
        message.addWidget(label2)
        message.addWidget(widgetMatrix[numOfRule][1])
        message.addWidget(widgetMatrix[numOfRule][2])
        container.addLayout(message)

        # set values as currents
        if numOfRule == 3:
            widgetMatrix[numOfRule][3].setChecked(data["UserSettings"][3]["active"])
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "active")
            widgetMatrix[numOfRule][3].toggled.connect(changeVal)
            widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][3]["time"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "time")
            # connect the amount change signel to the function
            widgetMatrix[3][0].textChanged.connect(changeVal)
            widgetMatrix[numOfRule][1].setValue(int(data["UserSettings"][3]["drinkAmount"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "drinkAmount")
            # connect the amount change signel to the function
            widgetMatrix[3][1].textChanged.connect(changeVal)
            widgetMatrix[numOfRule][2].setCurrentIndex(int(data["UserSettings"][3]["size"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "size")
            # connect the amount change signel to the function
            widgetMatrix[3][2].currentIndexChanged.connect(changeVal)
        else:
            widgetMatrix[numOfRule][3].setChecked(data["UserSettings"][2]["active"])
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "active")
            widgetMatrix[numOfRule][3].toggled.connect(changeVal)
            widgetMatrix[numOfRule][0].setValue(int(data["UserSettings"][2]["time"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "time")
            # connect the amount change signel to the function
            widgetMatrix[2][0].textChanged.connect(changeVal)
            widgetMatrix[numOfRule][1].setValue(int(data["UserSettings"][2]["drinkAmount"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "drinkAmount")
            # connect the amount change signel to the function
            widgetMatrix[2][1].textChanged.connect(changeVal)
            widgetMatrix[numOfRule][2].setCurrentIndex(int(data["UserSettings"][2]["size"]))
            # set change val func to amount
            changeVal = partial(changeValue,data, numOfRule, "size")
            # connect the amount change signel to the function
            widgetMatrix[2][2].currentIndexChanged.connect(changeVal)
    return container
        
    


def addNewLine(data, numOfRule, list, editBox):
    if editBox.text().strip():
        list.addItem(editBox.text())

        # iteraste to make list
        items = []
        for x in range (list.count()):
            items.append(list.item(x).text())
        changeValue(data, numOfRule, "list", items)

def deleteItem(data, numOfRule, list):
    list.takeItem(list.currentRow())
    # iteraste to make list
    items = []
    for x in range (list.count()):
        items.append(list.item(x).text())
    changeValue(data, numOfRule, "list", items)