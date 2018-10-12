import pygame
import random
import math


size = 20
obstacleSize = 5


def createObstacle(num, grid):
    obs = []
    for i in range(0, num):
        ranx = random.uniform(0, len(grid[0]))
        rany = random.uniform(0, len(grid[1]))
        ranxlen = random.uniform(0, obstacleSize)
        ranylen = random.uniform(0, obstacleSize)
        obs.append([ranx, rany, ranxlen, ranylen])

