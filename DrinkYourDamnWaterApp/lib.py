# ui pyside
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox, QComboBox, QListWidget, QLineEdit, QCheckBox, QSpacerItem,QMessageBox,QColorDialog

from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

import json

from functools import partial

# time 
import time

# threding 
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
state = 0

eventState = thread.Event()

stopFlag = thread.Event()

lock = thread.Lock()

LOGO_PATH = "Logo.png"
def makeNotifier(title):
    return Notify(
        default_notification_title=title,
        default_application_name= "Drink Your Damn Water",
        default_notification_icon= LOGO_PATH,
        default_notification_audio= "freesound_community-ding-101492.wav"
    )

generalTimerNote = makeNotifier("Water Timer!")
doomScrollNoteTimerNote = makeNotifier("Doomscroll Timer!")
websiteNote = makeNotifier("Website Notification")
appTimerNote = makeNotifier("Application Notification")

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(
        static_image_mode = False,
        max_num_faces = 2,
        refine_landmarks = True,
        min_detection_confidence = 0.5
        )

connectionsFaceOval = mpFaceMesh.FACEMESH_FACE_OVAL
connectionsIris = mpFaceMesh.FACEMESH_IRISES
