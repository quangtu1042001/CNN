import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy.random

# numpy.random.seed(5)

img = cv2.imread('img/tu.jpg')
img = cv2.resize(img, (200, 200))

#
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) / 255



class Conv2d:
    def __init__(self, input, kernelSize, padding=1):
        self.input = np.pad(input, (padding, padding), 'constant')

        self.kernel = np.random.rand(kernelSize, kernelSize)

        self.Result = np.zeros(
            (self.input.shape[0] - self.kernel.shape[0] + 1, self.input.shape[1] - self.kernel.shape[1] + 1))
        print(self.kernel.shape)

    def getRoi(seft):
        # vi tri cua hinh
        for row in range(int((seft.input.shape[0] - seft.kernel.shape[0])) + 1):
            for col in range(int((seft.input.shape[1] - seft.kernel.shape[1])) + 1):
                # kich thuoc cua dong cot de nhan vs kernel
                roi = seft.input[row: row + seft.kernel.shape[0],
                      col:col + seft.kernel.shape[1]]
                yield row, col, roi

    def operate(seft):
        for row, col, roi in seft.getRoi():
            seft.Result[row, col] = np.sum(roi * seft.kernel)
        return seft.Result


conv2d = Conv2d(img_gray, 3, )
img_123 = conv2d.operate()

plt.imshow(img_123, cmap='gray')

plt.show()
