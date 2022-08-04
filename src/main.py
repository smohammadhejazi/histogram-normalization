import sys
import collections
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

width = 0
height = 0
size = 0


def rgbaToGray(image):
    pixels = np.array(image)
    newImage = np.empty(shape=(height, width))
    products = np.dot(pixels[..., :3], [0.2989, 0.5870, 0.1140])
    for i in range(height):
        for j in range(width):
            newImage[i, j] = round(products[i, j])
    return newImage


def readImage(path):
    global width
    global height
    global size
    try:
        image = Image.open(path)
        width, height = image.size
        size = width * height
        return rgbaToGray(image)
    except Exception as e:
        print('Error: ' + str(e))


def filter(image):
    # count colors
    count = {}
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i, j] in count:
                count[image[i, j]] += 1
            else:
                count[image[i, j]] = 1

    # cumulative sum on sorted colors
    sortedCount = collections.OrderedDict(sorted(count.items()))
    sortedCumulativeCount = collections.OrderedDict()
    csum = 0
    for key, value in sortedCount.items():
        csum += value
        sortedCumulativeCount[key] = csum

    # apply filter
    filteredImage = np.empty(shape=(height, width))
    for i in range(height):
        for j in range(width):
            filteredImage[i, j] = round(255 * sortedCumulativeCount[image[i, j]] / size)

    return filteredImage


def drawHistogram(imageRavel, name):
    plt.hist(imageRavel, bins=256, range=(0, 256))
    plt.title(name)
    plt.savefig(name)
    plt.show()


def cumulativeSum(imageRavel, name):
    plt.hist(imageRavel, bins=256, range=(0, 256), cumulative=True)
    plt.title(name)
    plt.savefig(name)
    plt.show()


def drawImage(image, name):
    plt.imshow(image, cmap='gray')
    plt.title(name)
    plt.savefig(name)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Error: Enter image path.')
    else:
        print('Loading image...')
        image = readImage(sys.argv[1])
        imageRavel = image.ravel()
        drawImage(image, 'Original Image')
        print('Image loaded')

        print('Drawing original image histogram...')
        drawHistogram(imageRavel, 'Original Histogram')
        print('Original Histogram done')

        print('Drawing original cumulative sum...')
        cumulativeSum(imageRavel, 'Original Cumulative')
        print('Original Cumulative sum done')

        # Filter

        print('Filtering Image')
        filteredImage = filter(image)
        filteredImageRavel = filteredImage.ravel()
        drawImage(filteredImage, 'Filtered Image')
        print('Filtering done')

        print('Drawing filtered image histogram...')
        drawHistogram(filteredImageRavel, 'Filtered Histogram')
        print('Filtered Histogram done')

        print('Drawing filtered cumulative sum...')
        cumulativeSum(filteredImageRavel, 'Filtered Cumulative')
        print('Filtered Cumulative sum done')