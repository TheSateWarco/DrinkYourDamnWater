# ui pyside
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox, QComboBox, QListWidget, QLineEdit, QCheckBox, QSpacerItem,QMessageBox,QColorDialog

from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

# settings
import json

# lambda for button functions
from functools import partial

# time 
import time

# threading 
import threading as thread

# notify 
from notifypy import Notify

# tracking
import win32gui
import re

# webcam and mediapipe
import cv2
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import mediapipe as mp

# data related
from enum import Enum
from dataclasses import dataclass

class Rule(Enum):
    APPLICATION = 0
    WEBSITE = 1
    TIMER = 2
    DOOMSCROLL_TIMER = 3

@dataclass
class RuleSpec:
    label: str
    features: set[str]

# checks the optional ones based on type of rule
RULE_SPECS: dict[Rule, RuleSpec] = {
    Rule.APPLICATION:      RuleSpec("Following applications will require ", {"itemList", "addButton", "deleteButton", "editBox", "insertLine"}),
    Rule.WEBSITE:          RuleSpec("Following websites will require ", {"itemList", "addButton", "deleteButton", "editBox", "insertLine"}),
    Rule.TIMER:            RuleSpec("After ", {"activeToggle", "timer"}),
    Rule.DOOMSCROLL_TIMER: RuleSpec("After ", {"activeToggle", "timer"}),
}

# for widgets
FIELD_MAP = [
    ("amount", "drinkAmount", "value", "setValue"),
    ("unit", "size", "currentIndex", "setCurrentIndex"),
    ("timer", "time", "value", "setValue"),
    ("activeToggle", "active", "isChecked", "setChecked"),
]

# thrweading
eventState = thread.Event()
stopFlag = thread.Event()

# notification settings
LOGO_PATH = "Logo.png"
def makeNotifier(title):
    return Notify(
        default_notification_title=title,
        default_application_name= "Drink Your Damn Water",
        default_notification_icon= LOGO_PATH,
        default_notification_audio= "freesound_community-ding-101492.wav"
    )

generalTimerNotification = makeNotifier("Water Timer!")
doomScrollTimerNotification = makeNotifier("Doomscroll Timer!")
websiteNotification = makeNotifier("Website Notification")
appTimerNotification = makeNotifier("Application Notification")

NOTIFIERS: dict[Rule, Notify] = {
    Rule.APPLICATION:      appTimerNotification,
    Rule.WEBSITE:          websiteNotification,
    Rule.TIMER:            generalTimerNotification,
    Rule.DOOMSCROLL_TIMER: doomScrollTimerNotification,
}

# mediaPipe settings
mediaPipeFaceMesh = mp.solutions.face_mesh
faceMesh = mediaPipeFaceMesh.FaceMesh(
        static_image_mode = False,
        max_num_faces = 2,
        refine_landmarks = True,
        min_detection_confidence = 0.5
        )

connectionsFaceOval = mediaPipeFaceMesh.FACEMESH_FACE_OVAL
connectionsIris = mediaPipeFaceMesh.FACEMESH_IRISES

