import os
import numpy as np
import cv2
import page

class Scanner:
    
    def __init__(self, location):
        os.chdir(location)
        location += '/'
        pageNames = [name for name in os.listdir() if name.endswith('.jpg')]
        
        self.pages = [page.Page(pageName) for pageName in pageNames]
        
#a = Scanner('/home/thejus/Downloads')