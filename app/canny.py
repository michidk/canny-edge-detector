import numpy as np
import imageio
import helper
import io

# contains the canny edge detector
class CannyEdge():

    def __init__(self):
        pass

    # expects a PNG
    # runs canny edge detection on it
    # returns the resulting png as io buffer
    def detect_edges(self, data):
        img = imageio.imread(data, as_gray =True)
        [rows, columns] = np.shape(img)

        Gx = np.array([[1.0, 0.0, -1.0], [2.0, 0.0, -2.0], [1.0, 0.0, -1.0]]) # sobel x
        Gy = np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]]) # sobel y
        sobel = np.zeros(shape=(rows, columns))
        dir = np.zeros(shape=(rows, columns))

        # calculate sobel (extracts edges)
        for x in range(rows - 2):
            for y in range(columns - 2):
                gx = np.sum(np.multiply(Gx, img[x:x + 3, y:y + 3]))
                gy = np.sum(np.multiply(Gy, img[x:x + 3, y:y + 3]))
                sobel[x + 1, y + 1] = np.hypot(gx, gy)
                dir[x + 1, y + 1] = helper.angle_to_direction(np.degrees(np.arctan2(gy,gx)))

        sobel = sobel / np.max(sobel) # normalize

        # non-max suppression (makes edges smaller)
        suppression = np.zeros(shape=(rows, columns))
        for x in range(1, int(rows) - 1):
            for y in range(1, int(columns) - 1):
                if (dir[x,y] == 0):
                    if((sobel[x,y] > sobel[x,y+1]) and (sobel[x,y] > sobel[x,y-1])):
                        suppression[x,y] = sobel[x,y]
                    else:
                        suppression[x,y] = 0
                if dir[x, y] == 1:
                    if((sobel[x,y] > sobel[x+1,y+1]) and (sobel[x,y] > sobel[x-1,y-1])):
                        suppression[x,y] = sobel[x,y]
                    else:
                        suppression[x,y] = 0
                if dir[x, y] == 2:
                    if((sobel[x,y] > sobel[x+1,y]) and (sobel[x,y] > sobel[x-1,y])):
                        suppression[x,y] = sobel[x,y]
                    else:
                        suppression[x,y] = 0
                if dir[x, y] == 3:
                    if((sobel[x,y] > sobel[x+1,y-1]) and (sobel[x,y] > sobel[x-1,y+1])):
                        suppression[x,y] = sobel[x,y]
                    else:
                        suppression[x,y] = 0

        suppression = suppression / np.max(suppression) # normalize

        # double threshold and hysteris (removes unconnected edges [weak gradient values])
        hysteresis = np.copy(suppression)
        high = 0.2
        low = 0.03

        sum = 0
        prev = 0
        while True: # perform blob analysis until no more strong edges are created
            for x in range(1, rows - 1):
                for y in range(1, columns - 1):
                    if hysteresis[x,y] < low:
                        hysteresis[x,y] = 0
                        continue;

                    if hysteresis[x,y] > high:
                        hysteresis[x,y] = 1
                        continue;

                    if hysteresis[x,y+1] > high or hysteresis[x+1,y-1] > high or hysteresis[x+1,y] > high or hysteresis[x+1,y+1] > high or hysteresis[x-1,y-1] > high or hysteresis[x-1,y] > high or hysteresis[x-1,y+1] > high or hysteresis[x,y-1] > high:
                        hysteresis[x,y] = 1

            prev = sum
            sum = np.sum(hysteresis == 1) # calc strong edges
            if prev != sum:
                break

        hysteresis[hysteresis < 1] = 0 # remove weak edges

        # invert colors
        res = 255 - hysteresis

        output = io.BytesIO()
        imageio.imwrite(output, res, "PNG-PIL")
        return output
