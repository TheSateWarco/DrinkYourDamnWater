# settings.py
# ui pyside
from lib import *

# write to the setting json
def changeConfig(instruction, data, settings, allRuleWidgets):
    if instruction == "restore":
        data["UserSettings"] = data["OGSettings"]

    for rule in Rule:
        widgets = allRuleWidgets[rule]
        record = data["UserSettings"][rule.value]

        if instruction == "apply":
            record["drinkAmount"] = widgets["amount"].value()
            record["size"] = widgets["unit"].currentIndex()
            if "itemList" in widgets:
                record["list"] = [widgets["itemList"].item(i).text()
                                for i in range(widgets["itemList"].count())]
            if "activeToggle" in widgets:
                record["active"] = widgets["activeToggle"].isChecked()
            if "timer" in widgets:
                record["time"] = widgets["timer"].value()

        elif instruction == "restore":
            widgets["amount"].setValue(int(record["drinkAmount"]))
            widgets["unit"].setCurrentIndex(int(record["size"]))
            if "itemList" in widgets:
                widgets["itemList"].clear()
                for item in record["list"]:
                    widgets["itemList"].addItem(item)
            if "activeToggle" in widgets:
                widgets["activeToggle"].setChecked(record["active"])
            if "timer" in widgets:
                widgets["timer"].setValue(int(record["time"]))

    with open('settings.json', "w") as json_file:
        json.dump(data, json_file, indent=2)

    settings.update()
# change the python dictionary
def changeValue(data, numOfRule, subpartOfRule, newValue):
        data["UserSettings"][numOfRule][subpartOfRule] = newValue
        

def makeRule(data, rule:Rule):
    spec =  RULE_SPECS[rule]
    container = QVBoxLayout()
    message = QHBoxLayout()
    widgets: dict[str, QWidget] = {}

    label = QLabel(spec.label)
    message.addWidget(label)


    if "itemList" in spec.features:
        widgets["itemList"] = QListWidget()
        for item in data["UserSettings"][rule.value]["list"]:
            widgets["itemList"].addItem(item)

    if "activeToggle" in spec.features:
        widgets["activeToggle"] = QCheckBox()
        widgets["activeToggle"].setChecked(data["UserSettings"][rule.value]["active"])
        message.addWidget(widgets["activeToggle"])

    if "timer" in spec.features:
        widgets["timer"] = QSpinBox()
        widgets["timer"].setRange(0, 600)
        widgets["timer"].setValue(int(data["UserSettings"][rule.value]["time"]))
        message.addWidget(widgets["timer"])

    if "deleteButton" in spec.features:
        widgets["deleteButton"] = QPushButton("-")
        widgets["deleteButton"].clicked.connect(
        lambda: deleteItem(data, rule.value, widgets["itemList"])
    )

        
    if "editBox" in spec.features:
        widgets["editBox"] = QLineEdit("New Item")
        

    if "addButton" in spec.features:
        widgets["addButton"] = QPushButton("+")
        widgets["addButton"].clicked.connect(
        lambda: addNewLine(data, rule.value, widgets["itemList"], widgets["editBox"])
    )
        


    # drinkAmount and size are unconditional — every rule gets these
    widgets["amount"] = QSpinBox()
    widgets["amount"].setRange(1, 10)
    widgets["amount"].setValue(int(data["UserSettings"][rule.value]["drinkAmount"]))
    widgets["unit"] = QComboBox()
    widgets["unit"].addItems(["Sip", "Shot", "Cup"])
    widgets["unit"].setCurrentIndex(int(data["UserSettings"][rule.value]["size"]))
    message.addWidget(widgets["amount"])
    message.addWidget(widgets["unit"])

    

    container.addLayout(message)
    if "itemList" in spec.features:
        container.addWidget(widgets["itemList"])
    if "insertLine" in spec.features:
        widgets["insertLine"] = QHBoxLayout()
        widgets["insertLine"].addWidget(widgets["editBox"])
        widgets["insertLine"].addWidget(widgets["addButton"])
        widgets["insertLine"].addWidget(widgets["deleteButton"])
        container.addLayout(widgets["insertLine"])
    return container, widgets  
    
def syncListToData(data, numOfRule, listWidget):
    items = [listWidget.item(i).text() for i in range(listWidget.count())]
    changeValue(data, numOfRule, "list", items)

def addNewLine(data, numOfRule, list, editBox):
    if editBox.text().strip():
        list.addItem(editBox.text())

        # iteraste to make list
        syncListToData(data, numOfRule, list)

def deleteItem(data, numOfRule, list):
    list.takeItem(list.currentRow())
    # iteraste to make list
    syncListToData(data, numOfRule, list)