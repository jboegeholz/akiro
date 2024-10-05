import cv2
import pytest

from src.ball_tracker.ball_tracker.blob_detector import BlobDetector


def test_blob_detector():
    image = cv2.imread("tennis-ball.jpg")
    blob_detector = BlobDetector()
    keypoints, image = blob_detector.detect_blob(image)
    assert keypoints[0].pt[0] == pytest.approx(326.7, 0.1)
    assert keypoints[0].pt[1] == pytest.approx(265.3, 0.1)