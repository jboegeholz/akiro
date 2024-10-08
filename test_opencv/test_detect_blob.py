import cv2
import pytest

from src.ball_tracker.ball_tracker.blob_detector import BlobDetector


def test_blob_detector():
    image = cv2.imread("tennis-ball.jpg")
    blob_detector = BlobDetector()
    keypoints, image = blob_detector.detect_blob(image)
    assert keypoints[0].pt[0] == pytest.approx(326.7, 0.1)
    assert keypoints[0].pt[1] == pytest.approx(265.3, 0.1)

def test_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
