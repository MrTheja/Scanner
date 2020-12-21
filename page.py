import numpy as np
import cv2

PAGE_SIZE = 1024

orb = cv2.ORB_create()

#Creating the class page to store a page and other required variables
#and perform all the necessary actions
class Page:
    
    def __init__(self, location):
        
        self.page = cv2.imread(location)
        
        displayRatio = PAGE_SIZE / max(self.page.shape)
        
        #Page is resized so as to fit the screen
        #to alter the image ratio, tweak PAGE_SIZE
        self.page = cv2.resize(self.page, None,
                                   fx = displayRatio, fy = displayRatio,
                                   interpolation = cv2.INTER_AREA if displayRatio > 1 else cv2.INTER_CUBIC
                                   )
        #Detecting keypoints, to get the features
        self.keyPoints, self.distance = orb.detectAndCompute(self.page,None)
        #initialising the edge points
        SetSelectedPoints()
    
    #This function is to initialise the edge points
    def SetSelectedPoints(self):
        #to be removed and substituted by a ML algorithm to detect Edges
        self.selectedPoints = [[12, 22], [480, 19], [42, 99], [43, 477]]
    
    #This fuction is written inorder to have the selected edge points sorted
    #So that the lines will not cross while drawing the polygon
    def SortPoints(self):
        
        self.selectedPoints = sorted(self.selectedPoints)
        
        if self.selectedPoints[0][1] > self.selectedPoints[1][1]:
            self.selectedPoints[1], self.selectedPoints[0] = self.selectedPoints[0], self.selectedPoints[1]
        
        if self.selectedPoints[2][1] < self.selectedPoints[3][1]:
            self.selectedPoints[3], self.selectedPoints[2] = self.selectedPoints[2], self.selectedPoints[3]
    
    #This function is for the User to change the points,
    #When the predictions are inaccurate
    def EditSelectedPoints(self):
        #this function is to change the display image to redraw the polygon
        #at every callback
        def DisplayImage():
            
            displayImage = self.page.copy()
            points = self.selectedPoints.copy()
            
            #Drawing circles to indicate points
            for point in points:
                cv2.circle(displayImage, tuple(point), 8, (255, 0, 0), -1)
            
            #drawing the polygon to join the points
            points = np.int32(points).reshape((-1,1,2))
            displayImage = cv2.polylines(displayImage, [points], True, (255, 0, 0))
            
            return displayImage
            
        #call back function at mouse-click event
        def read(event,x,y,flags,param):
            
            if event==cv2.EVENT_LBUTTONDOWN:
                self.AlterPoints([x, y])
                cv2.imshow('Image', DisplayImage())
            
        
        cv2.imshow('Image', DisplayImage())
        cv2.setMouseCallback('Image',read)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    #Function to replace the closest point for each point selected by the User
    def AlterPoints(self, newPoint):
        minDistance = float('inf')
        position = None
        
        for index, point in enumerate(self.selectedPoints):
            distance = abs((point[0] - newPoint[0])**2 + (point[1] - newPoint[1])**2)
            if distance < minDistance:
                minDistance = distance
                position = index
            
        self.selectedPoints[position] = newPoint
        self.SortPoints()
                
    #Function to apply perspective transform to the page
    #with respect to the selected points
    def PerspectiveTransform(self, transformedPoints):
        
        perspectiveTransform = cv2.getPerspectiveTransform(imagePoints, transformedPoints)
        self.transformedImage = cv2.warpPerspective(self.page,
                                                    perspectiveTransform,
                                                    tuple(transformedPoints[-1])
                                                    )