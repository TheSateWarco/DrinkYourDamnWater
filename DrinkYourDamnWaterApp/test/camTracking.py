import cv2
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import mediapipe as mp


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

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(
        static_image_mode = False,
        max_num_faces = 2,
        refine_landmarks = True,
        min_detection_confidence = 0.5
        )
connectionsFaceOval = mpFaceMesh.FACEMESH_FACE_OVAL
connectionsIris = mpFaceMesh.FACEMESH_IRISES
# mpDrawing= mp.solutions.drawing_utils
# mpDrawingStyles= mp.solutions.drawing_styles
webcam= cv2.VideoCapture(0)
while webcam.isOpened():
    success,img=webcam.read()


    # # apply media pipe
    # img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # #results =mpFaceMesh.FaceMesh(refine_landmarks=True).process(img)
    # results =mpFaceMesh.FACEMESH_IRISES
    irisIndices = getUnique(connectionsIris)
    
    faceOvalIndices = getUnique(connectionsFaceOval)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results =faceMesh.process(img)


    # print(?)
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
            print(str(faceOvalDict[109][1]-faceOvalDict[148][1]))
            if faceOvalDict[148][1]-faceOvalDict[109][1] <100:
                threshold=15
            if (avgOval - avgIris)<threshold:
                print("doomscrolling")
            else:
                print("focused")


    cv2.imshow("Koolac",img)
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()
