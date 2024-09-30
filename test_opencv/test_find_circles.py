import cv2
import pytest

TEST_IMAGE = "yellow-tennis-ball.jpg"


def test_open_image():
    cv_image = cv2.imread(TEST_IMAGE)
    cv2.imshow("Blur", cv_image)
    cv2.waitKey(0)
    assert cv_image.any()


def test_blur_image():
    cv_image = cv2.imread(TEST_IMAGE)
    working_image = cv2.blur(cv_image, (5, 5))
    cv2.imshow("Blur", working_image)
    cv2.waitKey(0)
    assert working_image.any()


def test_convert_br_2_hsv():
    cv_image = cv2.imread(TEST_IMAGE)
    working_image = cv2.blur(cv_image, (5, 5))
    working_image = cv2.cvtColor(working_image, cv2.COLOR_BGR2HSV)
    cv2.imshow("Blur", working_image)
    cv2.waitKey(0)
    assert working_image.any()


def test_apply_hsv_threshold():
    cv_image = cv2.imread(TEST_IMAGE)
    working_image = cv2.blur(cv_image, (5, 5))
    working_image = cv2.cvtColor(working_image, cv2.COLOR_BGR2HSV)
    thresh_min = (21, 153, 42)
    thresh_max = (255, 255, 255)
    working_image = cv2.inRange(working_image, thresh_min, thresh_max)
    cv2.imshow("Blur", working_image)
    cv2.waitKey(0)
    assert working_image.any()


def test_dilate_erode():
    cv_image = cv2.imread(TEST_IMAGE)
    working_image = cv2.blur(cv_image, (5, 5))
    working_image = cv2.cvtColor(working_image, cv2.COLOR_BGR2HSV)
    thresh_min = (21, 153, 42)
    thresh_max = (255, 255, 255)
    working_image = cv2.inRange(working_image, thresh_min, thresh_max)
    working_image = cv2.dilate(working_image, None, iterations=2)
    working_image = cv2.erode(working_image, None, iterations=2)
    working_image = 255 - working_image
    cv2.imshow("Blur", working_image)
    cv2.waitKey(0)
    assert working_image.any()

def test_blob_detector():
    cv_image = cv2.imread(TEST_IMAGE)
    working_image = cv2.blur(cv_image, (5, 5))
    working_image = cv2.cvtColor(working_image, cv2.COLOR_BGR2HSV)
    thresh_min = (21, 153, 42)
    thresh_max = (255, 255, 255)
    working_image = cv2.inRange(working_image, thresh_min, thresh_max)
    working_image = cv2.dilate(working_image, None, iterations=2)
    working_image = cv2.erode(working_image, None, iterations=2)
    working_image = 255 - working_image
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0
    params.maxThreshold = 100

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 30
    params.maxArea = 20000

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.5

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    detector = cv2.SimpleBlobDetector_create(params)

    # Run detection!
    keypoints = detector.detect(working_image)
    assert keypoints == ()