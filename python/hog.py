from skimage import feature

# A small class for working with Histograms of Oriented Gradients (HOG) build on top of the
# skimage image library
class HOG:
    def __init__(self, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), normalize=False):
        self.orientations = orientations
        self.pixels_per_cell = pixels_per_cell
        self.cells_per_block = cells_per_block
        self.normalize = normalize

    def describe(self, image):
        histogram = feature.hog(image,
                                orientations=self.orientations,
                                pixels_per_cell=self.pixels_per_cell,
                                cells_per_block=self.cells_per_block,
                                normalise=self.normalize)
        return histogram