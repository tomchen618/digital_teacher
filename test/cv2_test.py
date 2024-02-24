import cv2
import numpy as np
from PIL import Image
from torchvision import transforms
from matplotlib import pyplot as plt


def concatenate():
    a1 = np.array([[[1, 2], [3, 4]]])
    a2 = np.array([[[5, 6], [7, 8]]])
    print('Rave：\n', a1[:, :, 0].ravel())
    print('concatenate：\n', np.concatenate((a1, a2), axis=0))


def image_transforms():
    data = np.random.randint(0, 255, size=30000)
    img = data.reshape(100, 100, 3)
    print(img.shape)
    img_tensor = transforms.ToTensor()(img)  # 转换成tensor
    print(img_tensor)
    plt.imshow(img, interpolation='nearest')
    plt.show()


if __name__ == '__main__':
    # concatenate()
    image_transforms()
    f1 = np.zeros((810, 1440, 3), dtype=np.uint8)

    height_diff, width_right, _ = f1.shape
    h = int(height_diff / 2)
    f2 = np.zeros((h, width_right, 3), dtype=np.uint8)
    # f1 = [
    #     [[3, 4, 6], [5, 6, 7], [88, 99, 100], [3, 4, 6], [5, 6, 7], [88, 99, 100], [3, 4, 6], [5, 6, 7], [88, 99, 100],
    #      [3, 4, 6], [5, 6, 7], [88, 99, 100]]]
    #
    # f2 = [
    #     [[3, 4, 6], [5, 6, 7], [88, 99, 100], [3, 4, 6], [5, 6, 7], [88, 99, 100], [3, 4, 6], [5, 6, 7], [88, 99, 100],
    #      [3, 4, 6], [5, 6, 7], [88, 99, 100]]]

    height_1, width_1, _ = f1.shape
    height_2, width_2, _ = f2.shape

    print(str(width_1) + "," + str(height_1))
    print(str(width_2) + "," + str(height_2))

    new_f = cv2.vconcat([f1, f2])
    height_new, width_new, _ = new_f.shape

    print("new: " + str(width_new) + "," + str(height_new))
