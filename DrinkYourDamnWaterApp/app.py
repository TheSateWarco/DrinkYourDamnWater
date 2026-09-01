# ui pyside
from lib import *


# get unique index
def getUnique(connections):
    # smake a temp list (to save og)
    tempList = list(connections)
    # set for getting one instance of index
    tempSet = set()
    # go though all indecies
    for t in tempList:
        # add both indecies
        tempSet.add(t[0])
        tempSet.add(t[1])
    return list(tempSet)

# get avg number
def getAvg(list): 
    return sum(list)/len(list)

# checks Gets the title of the last foreground title 
# Note: ONLY AVAILIABLE ON WINDOWS
def getLastActiveWindowTitle():
    window=win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

# get website from the title of application
def extractWebsiteFromTitle(title):
    #try to extract the website name from the browser title format
    match=re.search(r'(.+) - (Google Chrome|Mozilla Firefox|Microsoft Edge|DuckDuckGo|Safari)', title) # Regular expression to match the title format
    # If the title matches the expected format, extract the website name
    # and return it without the browser name
    if match:
        # gets the title of the first part of the website line
        return match.group(1)
    return None

# stop main program
def stopProgram(self):
    global stopFlag
    stopFlag.set()    
    eventState.set()  
    # get the thread ready for the stop input
    changeStateThread = thread.Thread(target=changeState, args=[self])
    changeStateThread.start()

# change state of the program (from working to stopping)
def changeState(self):
    global eventState
    # check the state of the program every two seconds
    while self.workerThread.is_alive():
        time.sleep(2)
    # connect threads
    self.workerThread.join()
    self.returnToMain.emit()
    eventState.set()
    eventState.clear()

# create the main menu (start, help, credits, settings)
def createMainScreen(self):
        # start button
        startBtn = QPushButton("Start")
        startBtn.clicked.connect(self.startClicked)
        # help button
        helpBtn = QPushButton("Help")
        helpBtn.clicked.connect(self.helpClicked)
        #credits button
        creditBtn = QPushButton("Credits")
        creditBtn.clicked.connect(self.creditsClicked)
        # settings button
        settingsBtn = QPushButton("Settings")
        settingsBtn.clicked.connect(self.settingsClicked)
        # layout stuff
        layout = QVBoxLayout()
        layout.addWidget(startBtn)
        layout.addWidget(helpBtn)
        layout.addWidget(creditBtn)
        layout.addWidget(settingsBtn)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
# check the size of the amount in settings
def checkSize(amount, number):
    size = ""
    match number:
        case 0:
            size = "sip"
        case 1:
            size = "shot"
        case 2:
            size = "cup"
    #print(size)
    if int(amount) > 1:
        size = size + "s"
    return size

# start the water reminders
def startProgram(mainTimer, listOfWebsites, listOfApps, regularTimeActive,doomScrollActive,mainDSTimer):
    timer = 4*mainTimer
    doomScrollTimer = 4*mainDSTimer
    global eventState, generalTimerNotification,doomScrollTimerNotification,websiteNotification,appTimerNotification, faceMesh, connectionsFaceOval, connectionsIris, stopFlag
    stopFlag.clear()
    # Initial active window title
    lastActiveWindow = getLastActiveWindowTitle()
    # attempt to continue app enless keyboard interupt
    try:
        # loop indefinately
        while True:
            # check if stop was requested
            if stopFlag.is_set():  
                break
            # check if general timer is out
            if timer == 0:
                # 4 * 15 sec = 1 min (see line 123)
                timer = 4*mainTimer
                if regularTimeActive:
                    # notify
                    generalTimerNotification.send()
            # still waiting for next timer
            else:
                # 4 * 15 sec = 1 min (see line 115)
                eventState.wait(15)
                eventState.clear()
                # check again after wait
                if stopFlag.is_set():  
                    break
                # current window
                currentWindow = getLastActiveWindowTitle()

                # check doom scroll timer
                if doomScrollTimer == 0:
                    doomScrollTimer = 4*mainDSTimer
                    doomScrollTimerNotification.send()

                else:

                    # compare current window to last opened window
                    if currentWindow != lastActiveWindow:
                        # set new current widow
                        lastActiveWindow = currentWindow
                        # find the name of web/app
                        activityName = extractWebsiteFromTitle(lastActiveWindow) or lastActiveWindow
                        # compare with list of apps
                        for app in listOfApps:
                            if app in lastActiveWindow:
                                appTimerNotification.send()
                        # compare of list of websites
                        for site in listOfWebsites:
                            if site in activityName:
                                websiteNotification.send()
                    # check if doomscrolling is active
                    if doomScrollActive == True:
                        # turn on camera
                        webcam= cv2.VideoCapture(0)
                        if webcam.isOpened():
                            # reate the camera
                            success,img=webcam.read()
                            # get the indicies of the eyes
                            irisIndices = getUnique(connectionsIris)
                            # get indicies of the face shape
                            faceOvalIndices = getUnique(connectionsFaceOval)
                            # change color because the mesh needs this to compare
                            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                            results =faceMesh.process(img)
                            # if there are landmards
                            if results.multi_face_landmarks:
                                for faceLandmark in results.multi_face_landmarks:
                                    lms = faceLandmark.landmark
                                    # put respective indices into dictionary
                                    faceOvalDict={}
                                    faceIrisDict={}
                                    irisFaceRef=[]
                                    # get the image position of face shape indecies
                                    for index in faceOvalIndices:
                                        x=int(lms[index].x *img.shape[1])
                                        y=int(lms[index].y *img.shape[0])
                                        faceOvalDict[index]=(x,y)
                                    # get the image position of iris indices
                                    for index in irisIndices:
                                        x=int(lms[index].x *img.shape[1])
                                        y=int(lms[index].y *img.shape[0])
                                        faceIrisDict[index]=(x,y)
                                        irisFaceRef.append(y)

                                    # get the two indecies of the face shape right next to eyes
                                    ovalFaceRef = [faceOvalDict[93][1],faceOvalDict[323][1]]
                                    # get the average of position of indecies
                                    avgOval = getAvg(ovalFaceRef)
                                    avgIris =  getAvg(irisFaceRef)
                                    # max difference in eye position vs face position
                                    threshold = 30
                                    # if the face is closer to the camera, change threshold
                                    if faceOvalDict[148][1]-faceOvalDict[109][1] <110:
                                        threshold=15
                                    # compare face and iris positions
                                    if (avgOval - avgIris)<threshold:
                                        # start doomscroller timer
                                        doomScrollTimer = doomScrollTimer -1

                                    else:
                                        # reset doomscroller timer
                                        doomScrollTimer = 4*mainDSTimer

                        webcam.release()
                        cv2.destroyAllWindows()
            # general timer in use
            timer = timer-1
    except KeyboardInterrupt:
        print("\n Tracking stopped.")