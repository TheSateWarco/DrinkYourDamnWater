# ui pyside
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox, QComboBox, QListWidget, QLineEdit, QCheckBox, QSpacerItem,QMessageBox
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

state = 1

lock = thread.Lock()

generalTimerNote = Notify(
    default_notification_title="Water Timer!",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="hand-drawn-speech-bubble-cartoon-ah-shout-png-1343987513.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)
doomScrollNoteTimerNote = Notify(
    default_notification_title="Doomscroll Timer!",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="hand-drawn-speech-bubble-cartoon-ah-shout-png-1343987513.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)

websiteNote = Notify(
    default_notification_title="Website Notification",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="hand-drawn-speech-bubble-cartoon-ah-shout-png-1343987513.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)

appTimerNote = Notify(
    default_notification_title="Application Notification",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="hand-drawn-speech-bubble-cartoon-ah-shout-png-1343987513.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)
