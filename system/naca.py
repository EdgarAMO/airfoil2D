
#: NAME:        naca
#: DESCRIPTION: Builds upper and lower list of points 
#: DATE:        28 / 07 / 2020
#: AUTHOR:      Edgar A. Martínez Ojeda

import numpy as np
from math import radians
from math import degrees
from math import cos
from math import sin
from math import pi
import copy

def makeAirfoil(digits, noOPoints, chord):

    """
    - digits............MPXX,
    - noOPoints.........number of points along each surface
    - chord.............airfoil's chord

    - returns merged upper and lower list of points
    """

    if len(digits) != 4:
        raise Exception('NACA airfoil must be a four-digit string')

    M = float(int(digits[0])) / 100         # max camber
    P = float(int(digits[1])) / 10          # max camber position
    t = float(int(digits[2:])) / 100        # thickness

    b = np.linspace(0, np.pi, noOPoints)    # 0 <= b <= pi
    x =  chord * (1 - np.cos(b)) / 2        # scale to chord's size

    # M != 0 and P != 0 for non-symmetrical  airfoils
    if (M != 0 and P != 0):

        # camber y array & camber gradient array
        yc = np.zeros((x.size, ), dtype=float)
        dycdx = np.zeros((x.size, ), dtype=float)

        # camber y before P location
        ybp = lambda x : (M / P ** 2) * (2 * P * x - x ** 2)
        ybpVector = np.vectorize(ybp)

        # camber gradient before P location
        gbp = lambda x: ((2 * M) / (P ** 2)) * (P - x)
        gbpVector = np.vectorize(gbp)

        # camber y after P location
        yap = lambda x : (M / ((1 - P) ** 2)) * (1 - 2 * P + 2 * P * x - x ** 2)
        yapVector = np.vectorize(yap)

        # camber gradient after P location
        gap = lambda x: ((2 * M) / ((1 - P) ** 2)) * (P - x)
        gapVector = np.vectorize(gbp)

        # apply functions accordingly
        yc[x < P] = ybpVector(x[x < P])
        yc[x >= P] = yapVector(x[x >= P])
        dycdx[x < P] = gbpVector(x[x < P])
        dycdx[x >= P] = gapVector(x[x >= P])

    # else, M = 0 and P = 0 for symmetrical afoils
    else:

        yc = np.zeros((x.size, ), dtype=float)
        dycdx = np.zeros((x.size, ), dtype=float)

    #  thickness distribution
    a0 = 0.29690
    a1 = -0.1260
    a2 = -0.3516
    a3 = 0.28430
    a4 = -0.1036

    yt = ( (5 * t) *
         ( (a0 * np.sqrt(x)) +
           (a1 * x) +
           (a2 * (x**2)) +
           (a3 * (x**3)) +
           (a4 * (x**4))
         ) )

    theta = np.arctan(dycdx)

    # upper surface
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)

    # lower surface
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    # displace trailing edge to (0, 0)
    xl -= chord
    xu -= chord
    
    # pack points into nested lists
    upper = []
    lower = []

    for x, y in zip(xu, yu):
        upper.append([x, y])

    for x, y in zip(xl, yl):
        lower.append([x, y])
    
    # write(copy.deepcopy(upper), copy.deepcopy(lower))   

    return upper, lower

def write(upper, lower):

    # concatenate upper and lower, L.E. and T.E. are not repeated:
    upper.extend(list(reversed(lower[1:-1])))

    # rename it:
    points = upper

    file = open('{}.asc'.format('airfoil'), 'w')

    for point in points:
        file.write('{0:.5f}\t{1:.5f}\t0.00000\n'.format(point[0], point[1]))

    file.close()




