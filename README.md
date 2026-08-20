# DrinkYourDamnWater
A background reminder app that notifies you to drink water using timers, app/website triggers, and (experimental) webcam detection.
---

## Why
This app will help you build this habit so you don’t have to depend on it for the rest of your life. It leans on classical conditioning: each notification pairs an everyday trigger, like opening a specific app or website or simply a set amount of time passing, with the same simple action of drinking water. Repeat that pairing enough times, and the trigger itself starts to carry the cue on its own. Eventually, opening YouTube or noticing an hour's gone by prompts you to drink even before the app has a chance to remind you, no notification needed. The app runs quietly in the background whether you're watching a show, doing homework, or gaming, doing the pairing work until you don't need it anymore. 
---

## Features
- Regular timer — get reminded every X minutes, no matter what you're doing
- App/website triggers — get notified when specific apps or websites open (e.g. YouTube, Spotify, VS Code)
- Simple interface — fully customizable notification settings (drink amount, unit, timing, active/inactive)
- Experimental doomscroll detection — (off by default) uses your webcam and on-device facial tracking (MediaPipe) to detect when you're looking down for an extended period, as if scrolling on your phone, and reminds you to drink

> Privacy note: the doomscroll detection feature processes webcam frames locally on your machine; nothing is uploaded or sent anywhere. It's off by default and must be explicitly enabled in Settings.
---

## Installation

> Windows only for now (uses pywin32 for active-window tracking).

1. Download on STEAM $0.99 **(WIP)**
2. Download on Itch.io $0.99 **(WIP)**
3. Clone Repo
- Make sure you have Python 3.11 installed
- Clone the repo:
```
git clone https://github.com/TheSateWarco/DrinkYourDamnWater.git
cd DrinkYourDamnWater
```
- Install dependencies:
```
pip install -r requirements.txt
```
- Run the app or get .exe file:
  - python main.py (run app)
  - python pyside6 (get exe)
---

## Dependencies
- PySide6
- notify-py
- opencv-python
- mediapipe
- pywin32
---

## Usage
1. Launch the app and hit Start
2. Customize your reminders under Settings:
3. Add/remove tracked apps and websites
4. Set your regular reminder interval and drink amount
5. Optionally enable experimental doomscroll detection
6. Hit Stop at any time to pause reminders
7. Download

Prefer not to build from source? The packaged app will soon be on STEAM and Itch.io for $0.99
---

## Contributing
Issues and pull requests are welcome. This project is still in active development. Contributions are unpaid and volunteer-based, though all contributors will be credited (in the application and ReadMe Credits Section).
---

## License
MIT — see LICENSE for details. 
---

## Credits
Main Programmer: TheSateWarco

