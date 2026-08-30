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

        for widgetKey, jsonKey, readMethod, writeMethod in FIELD_MAP:
            if widgetKey not in widgets:
                continue  # this rule doesn't have this field

            if instruction == "apply":
                value = getattr(widgets[widgetKey], readMethod)()
                record[jsonKey] = value

            elif instruction == "restore":
                value = record[jsonKey]
                if widgetKey in ("timer", "amount"):  # needs int() cast, like your original code
                    value = int(value)
                getattr(widgets[widgetKey], writeMethod)(value)

        # itemList still needs its own handling since it's a list, not a single value
        if "itemList" in widgets:
            if instruction == "apply":
                record["list"] = [widgets["itemList"].item(i).text()
                                for i in range(widgets["itemList"].count())]
            elif instruction == "restore":
                widgets["itemList"].clear()
                for item in record["list"]:
                    widgets["itemList"].addItem(item)

    with open('settings.json', "w") as json_file:
        json.dump(data, json_file, indent=2)

    settings.update()
# change the python dictionary
def changeValue(data, rule: Rule, subpartOfRule, newValue):
    data["UserSettings"][rule.value][subpartOfRule] = newValue   

def makeRule(data, rule:Rule):
    spec =  RULE_SPECS[rule]
    container = QVBoxLayout()
    message = QHBoxLayout()
    widgets: dict[str, QWidget] = {}
    if "activeToggle" in spec.features:
            widgets["activeToggle"] = QCheckBox()
            widgets["activeToggle"].setChecked(data["UserSettings"][rule]["active"])
            message.addWidget(widgets["activeToggle"])

    label = QLabel(spec.label)
    message.addWidget(label)


    if "itemList" in spec.features:
        widgets["itemList"] = QListWidget()
        for item in data["UserSettings"][rule.value]["list"]:
            widgets["itemList"].addItem(item)


    if "timer" in spec.features:
        widgets["timer"] = QSpinBox()
        widgets["timer"].setRange(0, 600)
        widgets["timer"].setValue(int(data["UserSettings"][rule.value]["time"]))
        message.addWidget(widgets["timer"])
        message.addWidget(QLabel(" minutes, take "))

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
    
def syncListToData(data, rule: Rule, listWidget):
    items = [listWidget.item(i).text() for i in range(listWidget.count())]
    changeValue(data, rule, "list", items)

def addNewLine(data, rule: Rule, list, editBox):
    if editBox.text().strip():
        list.addItem(editBox.text())
        syncListToData(data, rule, list)

def deleteItem(data, rule: Rule, list):
    list.takeItem(list.currentRow())
    syncListToData(data, rule, list)