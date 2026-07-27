
from lib import *

notification = Notify(
    default_notification_title="Function Message",
    default_application_name="Great Application",
    default_notification_icon="hand-drawn-speech-bubble-cartoon-ah-shout-png-1343987513.png",
    default_notification_audio="freesound_community-ding-101492.wav"
)

def your_function():
    # stuff happening here.
    notification.message = "Function Result"
    notification.send()

your_function()