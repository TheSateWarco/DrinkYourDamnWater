# ui pyside
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox, QComboBox, QListWidget, QLineEdit, QCheckBox, QSpacerItem,QMessageBox,QColorDialog

from PySide6.QtGui import QIcon, Qtimer
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

state = 1

lock = thread.Lock()

generalTimerNote = Notify(
    default_notification_title="Water Timer!",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="Logo.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)
doomScrollNoteTimerNote = Notify(
    default_notification_title="Doomscroll Timer!",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="Logo.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)

websiteNote = Notify(
    default_notification_title="Website Notification",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="Logo.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)

appTimerNote = Notify(
    default_notification_title="Application Notification",
    default_application_name="Drink Your Damn Water",
    default_notification_icon="Logo.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)


mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(
        static_image_mode = False,
        max_num_faces = 2,
        refine_landmarks = True,
        min_detection_confidence = 0.5
        )

connectionsFaceOval = mpFaceMesh.FACEMESH_FACE_OVAL
connectionsIris = mpFaceMesh.FACEMESH_IRISES
