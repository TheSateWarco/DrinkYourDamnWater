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

def getAvg(list): 
    return sum(list)/len(list)

def get_lastActiveWindow_title():
    window=win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def extract_website_from_title(title):
    #try to extract the website name from the browser title format
    match=re.search(r'(.+) - (Google Chrome|Mozilla Firefox|Microsoft Edge|DuckDuckGo|Safari)', title) # Regular expression to match the title format
    #print(match)
    # If the title matches the expected format, extract the website name
    # and return it without the browser name
    if match:
        return match.group(1)
    return None

def stopProgram(self):
    
    createMainScreen(self)
    changeStateThread = thread.Thread(target=changeState, args=[])
    changeStateThread.start()

def changeState():
    global state, lock
    lock.acquire() 
    state = 0
    lock.release()
    #print("state: " + str(state))


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
def startProgram(mainTimer, listOfWebsites, listOfApps, regularTimeActive,doomScrollActive,mainDSTimer):
    timer = 4*mainTimer
    doomScrollTimer = 4*mainDSTimer
    global state, lock, generalTimerNote,doomScrollNoteTimerNote,websiteNote,appTimerNote, faceMesh, connectionsFaceOval, connectionsIris
    # Initial active window title
    lastActiveWindow = get_lastActiveWindow_title()
    lock.acquire() 
    state = 1
    lock.release()
    try:
        while state == 1:
            if timer == 0:
                timer = 4*mainTimer
                if regularTimeActive:
                    generalTimerNote.send()
            else:
                time.sleep(1)
                #lock.acquire() 
                #print("state"+ str(state))
                #lock.release()
                current_window = get_lastActiveWindow_title()
                if doomScrollTimer == 0:
                    doomScrollTimer = 4*mainDSTimer
                    doomScrollNoteTimerNote.send()

                else:
                
                    if current_window != lastActiveWindow:

                        lastActiveWindow = current_window
                        activityName = extract_website_from_title(lastActiveWindow) or lastActiveWindow
                        # print("window: " + current_window)
                        # print("act: " + activity_name)
                        for app in listOfApps:
                            if app in lastActiveWindow:
                                appTimerNote.send()

                        for site in listOfWebsites:
                            #print(site + " = " + activityName)
                            if site in activityName:
                                websiteNote.send()
                    # check if doomscrolling is active
                    if doomScrollActive == True:
                        webcam= cv2.VideoCapture(0)
                    if webcam.isOpened():
                        success,img=webcam.read()
                        irisIndices = getUnique(connectionsIris)
                            
                        faceOvalIndices = getUnique(connectionsFaceOval)
                        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                        results =faceMesh.process(img)

                        if results.multi_face_landmarks:
                            for faceLandmark in results.multi_face_landmarks:
                                lms = faceLandmark.landmark
                                faceOvalDict={}
                                faceIrisDict={}
                                irisFaceRef=[]
                                for index in faceOvalIndices:
                                    x=int(lms[index].x *img.shape[1])
                                    y=int(lms[index].y *img.shape[0])
                                    faceOvalDict[index]=(x,y)
                                for index in irisIndices:
                                    x=int(lms[index].x *img.shape[1])
                                    y=int(lms[index].y *img.shape[0])
                                    faceIrisDict[index]=(x,y)
                                    irisFaceRef.append(y)
                                    
                                #irisFaceRef=[faceIrisDict[472][1],faceIrisDict[477][1]]
                                ovalFaceRef = [faceOvalDict[93][1],faceOvalDict[323][1]]
                                avgOval = getAvg(ovalFaceRef)
                                avgIris =  getAvg(irisFaceRef)
                                #print(str(avgOval - avgIris))
                                threshold = 30
                                #print(str(faceOvalDict[109][1]-faceOvalDict[148][1]))
                                if faceOvalDict[148][1]-faceOvalDict[109][1] <110:
                                    threshold=15
                                if (avgOval - avgIris)<threshold:
                                    print("doomscrolling")
                                    doomScrollTimer = doomScrollTimer -1

                                else:
                                    print("focused")
                                    doomScrollTimer = 4*mainDSTimer


                        

                    webcam.release()
                    cv2.destroyAllWindows()

            print(doomScrollTimer)
            timer = timer-1
    except KeyboardInterrupt:
        print("\n Tracking stopped.")