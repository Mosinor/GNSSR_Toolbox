import matplotlib.pyplot as plt
import numpy as np
from geopy.distance import geodesic

array = np.array([
    [ 21.06826401, 328.7328186,    6.,    0.],
    [ 15.96437073, 330.087677,     6.,    0.],
    [ 18.06357384, 330.99157715,   6.,    0.],
    [ 21.09316826, 328.77407837,   6.,    0.83333349],
    [ 15.98845768, 330.12765503,   6.,    0.83333349],
    [ 18.08806229, 331.03213501,   6.,    0.83333349],
    [ 16.01494217, 330.17166138,   6.,    1.75000023],
    [ 21.12055588, 328.81948853,   6.,    1.75000023],
    [ 18.11645126, 331.07922363,   6.,    1.80000018],
    [ 18.14434624, 331.12548828,   6.,    2.75000023],
    [ 21.15042114, 328.86901855,   6.,    2.75000047],
    [ 16.04381752, 330.21966553,   6.,    2.75000047],
    [ 21.18027878, 328.9185791,    6.,    3.75000023],
    [ 16.07266426, 330.26766968,   6.,    3.75000023],
    [ 18.17369461, 331.17422485,   6.,    3.75000047],
    [ 18.20302582, 331.22296143,   6.,    4.74999999],
    [ 21.21012306, 328.96813965,   6.,    4.75000023],
    [ 16.10149574, 330.31570435,   6.,    4.75000023],
    [ 16.13030624, 330.36373901,   6.,    5.74999999],
    [ 18.23234367, 331.27172852,   6.,    5.74999999],
    [ 21.23995209, 329.0177002,    6.,    5.74999999],
    [ 18.26164436, 331.32049561,   6.,    6.74999999]
])

example = array[0]

track_list = []
track = []


for index, measure in enumerate(array[0:len(array)-10]):
    if measure[2] != 0:
        track.append(measure)
        measure[2] = 0
        coord1 = (measure[0], measure[1])
        candidates = []

        # Checks 6 next measures for distance
        for x in range(1, 6):
            coord2 = (array[index+x][0], array[index+x][1])
            a = geodesic(coord1, coord2).m
            if a < 15000 and a != 0:  # if d is less than 15km its a candidate
                candidates.append([a, index+x])

        # smallest candidate is selected, else we start new track
        if len(candidates) > 0:
            next = min(candidates)[1]
            track.append(array[next])
            array[next][2] = 0
        else:
            track_list.append(track)
            track = []
        print(track)

print(track_list)
