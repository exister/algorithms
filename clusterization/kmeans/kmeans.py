# -*- coding: utf-8 -*-
from random import sample
import Image
import math
from matplotlib.collections import PatchCollection
import os
import matplotlib.pyplot as plt
from matplotlib.patches import  Rectangle

class Point(object):
    def __init__(self, *args):
        if len(args) != self.dimensions:
            raise TypeError()
        self.coordinates = args

    @property
    def dimensions(self):
        return 2

    def distance(self, point):
        if not isinstance(point, self.__class__):
            raise TypeError()
        if point.dimensions != self.dimensions:
            raise TypeError()
        return self._distance(point)

    def _distance(self, point):
        return math.sqrt(reduce(lambda x, p: x + pow(point.coordinates[p] - self.coordinates[p], 2), xrange(self.dimensions), 0.0))

class ColorPoint(Point):
    def __init__(self, *args):
        super(ColorPoint, self).__init__(*args)

    @property
    def r(self):
        return self.coordinates[0]

    @property
    def g(self):
        return self.coordinates[1]

    @property
    def b(self):
        return self.coordinates[2]

    @property
    def dimensions(self):
        return 3


class Cluster(object):
    def __init__(self, points):
        if not points:
            raise ValueError()
        self.point_class = type(points[0])
        self.dimensions = points[0].dimensions
        self.points = points
        self.mean = self.centroid()

    def centroid(self):
        return self.point_class(*[reduce(lambda x, p: x + p.coordinates[i], self.points, 0.0) / len(self.points) for i in xrange(self.dimensions)])

    def update(self, points):
        old_mean = self.mean
        self.points = points
        self.mean = self.centroid()
        return old_mean.distance(self.mean)


class Clustering(object):
    _point_class = Point

    def __init__(self, *args, **kwargs):
        self.clusters = []

    def __call__(self, amount, max_iters, min_shift):
        self._analyze(amount, max_iters, min_shift)
        print ['#%s' % ''.join(['%02x' % p for p in c.mean.coordinates]) for c in self.clusters]

    def _analyze(self, amount, max_iters, min_shift):
        self._random_clusters(amount)
        iters = 0
        run = True
        while run:
            clusters = self._assign()
            shift = self.update(clusters)
            iters += 1
            run = iters < max_iters and shift > min_shift

    def _random_clusters(self, amount):
        for p in sample(self._points, amount):
            self.clusters.append(Cluster([p]))

    @property
    def _points(self):
        return []

    def _assign(self):
        tmp_clusters = [[] for x in self.clusters]
        for p in self._points:
            min_distance = None
            cluster_index = None
            for ci, c in enumerate(self.clusters):
                distance = p.distance(c.mean)
                if min_distance is None:
                    min_distance = distance
                    cluster_index = ci
                elif distance < min_distance:
                    min_distance = distance
                    cluster_index = ci
            tmp_clusters[cluster_index].append(p)
        return tmp_clusters

    def update(self, clusters):
        return max(0.0, *[c.update(clusters[i]) for i, c in enumerate(self.clusters)])


class ColorClustering(Clustering):
    _point_class = ColorPoint

    def __init__(self, *args, **kwargs):
        super(ColorClustering, self).__init__(*args, **kwargs)
        self.path = kwargs.get('path')
        self.load_image()

    def load_image(self):
        if self.path and os.path.exists(self.path) and os.path.isfile(self.path):
            self.image = Image.open(self.path)
            if self.image.size[0] > 200 or self.image.size[1] > 200:
                self.image.thumbnail((200, 200))
            self.pixels = [self._point_class(*p) for c, p in self.image.getcolors(self.image.size[0] * self.image.size[1])]

    @property
    def _points(self):
        return self.pixels

    def __call__(self, amount, max_iters, min_shift):
        super(ColorClustering, self).__call__(amount, max_iters, min_shift)

        fig = plt.figure()
        ax = fig.add_subplot(211, frameon=False, xticks=[], yticks=[])
        ax2 = fig.add_subplot(212, frameon=False, xticks=[], yticks=[])

        ax.imshow(self.image)

        patches = []
        for i, c in enumerate(self.clusters):
            rec = Rectangle((0.07 + 0.11*i, 0.05), 0.1, 0.1, color=map(lambda x: x / 256, c.mean.coordinates))
            patches.append(rec)
        p = PatchCollection(patches, match_original=True)
        ax2.add_collection(p)
        plt.show()


if __name__ == '__main__':
    path = raw_input('Enter image path: ')
    ColorClustering(path=path)(3, 200, 0.5)