
#: NAME:        splines
#: DESCRIPTION: Builds lists of splines
#: DATE:        13 / 08 / 2020
#: AUTHOR:      Edgar A. Martínez Ojeda

import sys

def ensemble(NACA, NPOINTS):

	from naca import makeAirfoil

	upper, lower = makeAirfoil(NACA, NPOINTS, 1.00)

	# pairs of point labels:
	pairs = [[0, 1], [9, 10], [0, 8], [9, 17]]

	# list of third coordinates:
	depths = [-0.5, 0.5, -0.5, 0.5]

	# list of interpolation points lists:
	splines = [upper, upper, lower, lower]

	# open file:
	file = open('chunk2', 'w')
	for pair, depth, spline in zip(pairs, depths, splines):
	    file.write('\tspline {0:2d} {1:2d}\n'.format(*pair))
	    file.write('\t(\n')
	    for point in spline:
	        file.write('\t\t({0:6.4f} {1:6.4f} {2:6.4f})\n'.
	                   format(point[0], point[1], depth))
	    file.write('\t)\n\n')
	file.close()

	# ensemble the three chunks
	filenames = ['chunk1', 'chunk2', 'chunk3']
	with open('blockMeshDict', 'w') as outfile:
	    for fname in filenames:
	        with open(fname) as infile:
	            outfile.write(infile.read())


arg1 = str(sys.argv[1])
arg2 = int(sys.argv[2])

ensemble(arg1, arg2)


    
