import numpy as np

class RedPixelMatcher:   
    def __init__(self, threshold):
        self.threshold = threshold

    def match_image(self, img):
        red_pixels = np.logical_and(img[:, :, 0] > self.threshold, img[:, :, 1] == 0, img[:, :, 2] == 0)

        if not np.any(red_pixels):
            return None

        return np.unravel_index(np.argmax(red_pixels), red_pixels.shape)