import cv2
import math
from heapq import heappop, heappush
import copy


def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])



class Thing:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cx = x + (w / 2)
        self.cy = y + (h / 2)
        self.color = color


class RedZone:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.x = 0
        self.y = 0
        self.close_side = "n"
        self.points = []
        self.image = None
        self.finished = False

    def mouse_callback(self, e, x, y, m, n):
        if self.image is not None:
            if e == cv2.EVENT_LBUTTONDOWN:
                self.points.append((x, y))
            if len(self.points) == 2:
                self.finished = True

    def config(self, camera, ground):
        cv2.namedWindow("choose red zone", cv2.WINDOW_NORMAL)
        print "please crop your red zone in image"
        cv2.setMouseCallback("choose red zone", self.mouse_callback)
        while not self.finished:
            _, image = camera.read()
            (crop_p1, crop_p2) = ground.crop_points()
            image = image[crop_p1[0]:crop_p2[0], crop_p1[1]:crop_p2[1]]
            self.image = image
            cv2.imshow("choose red zone", image)
            cv2.waitKey(1)
        cv2.destroyWindow("choose red zone")
        self.x1 = self.points[0][0]
        self.y1 = self.points[0][1]
        self.x2 = self.points[1][0]
        self.y2 = self.points[1][1]
        self.x = self.x1 + (self.x2 - self.x1) / 2
        self.y = self.y1 + (self.y2 - self.y1) / 2

    def check_things(self, things):
        for i in things:
            if (self.x1 < i.cx <= self.x2) and (self.y1 < i.cy < self.y2):
                things.remove(i)
        return things

