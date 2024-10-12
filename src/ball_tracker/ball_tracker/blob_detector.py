import cv2

class BlobDetector:
    def __init__(self):
        self.params = cv2.SimpleBlobDetector_Params()
        self.params.filterByArea = True
        self.params.minArea = 7000
        self.params.maxArea = 25000
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.5
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.9
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.5
        self.hsv_thresh_min = (35, 31, 18)
        self.hsv_thresh_max = (74, 255, 255)
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def detect_blob(self, image):
        image = cv2.blur(image, (5, 5))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = cv2.inRange(image, self.hsv_thresh_min, self.hsv_thresh_max)
        image = 255 - image  # invert color white -> black
        keypoints = self.detector.detect(image)
        return keypoints, image