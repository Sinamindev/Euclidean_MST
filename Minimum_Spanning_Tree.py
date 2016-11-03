# constant parameters
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
CANVAS_MARGIN = 20
POINT_COLOR = 'gray'
MST_EDGE_COLOR = 'red'
TSP_EDGE_COLOR = 'navy'
POINT_RADIUS = 3
OUTLINE_WIDTH = 2

import enum, math, random, time, tkinter
from math import sqrt
import sys
import itertools

# Class representing one 2D point.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def dist(self, other):
        return sqrt((other.x - self.x) * (other.x - self.x) +
                (other.y - self.y) * (other.y - self.y))
    def __repr__(self):
        return "{} {}".format(self.x, self.y)

# Euclidean Minimum Spanning Tree (MST) algorithm
#
# input: a list of n Point objects
#
# output: a list of (p, q) tuples, where p and q are each input Point
# objects, and (p, q) should be connected in a minimum spanning tree
# of the input points
def euclidean_mst(points):
    K = []
    n = len(points)
    spanned = [False] * n

    # Mark a start vertex
    spanned[0] = True

    while len(K) < n - 1:
        # Find an edge with minimum weight
        b = None
        for v in range(0, n):
            for w in range(0, n):
                # Make sure (points[v], points[w]) is a bridge edge
                if spanned[v] != spanned[w]:
                    if b is None or points[v].dist(points[w]) < points[b[0]].dist(points[b[1]]):
                        b = (v, w)
        # Mark both points as spanned
        v, w = b[0], b[1]
        spanned[v] = spanned[w] = True
        K.append((points[v], points[w]))

    return K

# Euclidean Traveling Salesperson (TSP) algorithm
#
# input: a list of n Point objects
#
# output: a permutation of the points corresponding to a correct
# Hamiltonian cycle of minimum total distance
def euclidean_tsp(points):
    best = None

    for path in itertools.permutations(points):
        cycle = list(path)
        cycle.append(cycle[0])

        if verify_tsp(points, cycle):
            if best is None or cycle_weight(cycle) < cycle_weight(best):
                best = cycle
    return best

def cycle_weight(cycle):
    total = 0
    for i in range(len(cycle)-1):
        total += cycle[i].dist(cycle[i+1])
    return total

def verify_tsp(points, cycle):
    return True

###############################################################################
# The following code is responsible for generating instances of random
# points and visualizing them. You can leave it unchanged.
###############################################################################

# input: an integer n >= 0
# output: n Point objects with all coordinates in the range [0, 1]
def random_points(n):
    return [Point(random.random(), random.random())
            for i in range(n)]

# translate coordinates in [0, 1] to canvas coordinates
def canvas_x(x):
    return CANVAS_MARGIN + x * (CANVAS_WIDTH - 2*CANVAS_MARGIN)
def canvas_y(y):
    return CANVAS_MARGIN + y * (CANVAS_HEIGHT - 2*CANVAS_MARGIN)

# extract the x-coordinates (or y-coordinates respectively) from a
# list of Point objects
def xs(points):
    return [p.x for p in points]
def ys(points):
    return [p.y for p in points]

# input: a non-empty list of numbers
# output: the mean average of the list
def mean(numbers):
    return sum(numbers) / len(numbers)

# input: list of Point objects
# output: list of the same objects, in clockwise order
def clockwise(points):
    if len(points) <= 2:
        return points
    else:
        center_x = mean(xs(points))
        center_y = mean(ys(points))
        return sorted(points,
                      key=lambda p: math.atan2(p.y - center_y,
                                               p.x - center_x),
                      reverse=True)

# Run one trial of one or both of the algorithms.
#
# 1. Generates an instance of n random points.
# 2. If do_box is True, run the bounding_box algorithm and display its output.
# 3. Likewise if do_hull is True, run the convex_hull algorithm and display
#    its output.
# 4. The run-times of the two algorithms are measured and printed to standard
#    output.

def generate_points(n):
    print('generating n=' + str(n) + ' points...')
    return random_points(n)
   

def time_trial(message, points, func):
    print(message)

    start = time.perf_counter()
    output = func(points)
    end = time.perf_counter()

    print('elapsed time = ' + str(end - start) + ' seconds')

    return output

def setup_canvas(points):
    w = tkinter.Canvas(tkinter.Tk(),
                       width=CANVAS_WIDTH, 
                       height=CANVAS_HEIGHT)
    w.pack()

    for p in points:
        w.create_oval(canvas_x(p.x) - POINT_RADIUS,
                      canvas_y(p.y) - POINT_RADIUS,
                      canvas_x(p.x) + POINT_RADIUS,
                      canvas_y(p.y) + POINT_RADIUS,
                      fill=POINT_COLOR)

    return w

def draw_edge(w, p, q, color):
    w.create_line(canvas_x(p.x), canvas_y(p.y),
                  canvas_x(q.x), canvas_y(q.y),
                  fill=color)

def mst_trial(n):
    points = generate_points(n)
    edges = time_trial('minimum spanning tree...', points, euclidean_mst)

    w = setup_canvas(points)
    for (p, q) in edges:
        draw_edge(w, p, q, MST_EDGE_COLOR)

    tkinter.mainloop()

def tsp_trial(n):
    points = generate_points(n)
    cycle = time_trial('traveling salesperson...', points, euclidean_tsp)

    w = setup_canvas(points)
    for i in range(n):
        p = cycle[i]
        q = cycle[(i + 1) % n]

        draw_edge(w, p, q, TSP_EDGE_COLOR)

        w.create_text(canvas_x(p.x), canvas_y(p.y) - POINT_RADIUS,
                      text=str(i),
                      anchor=tkinter.S)

    tkinter.mainloop()

###############################################################################
# This main() function runs multiple trials of the algorithms to
# gather empirical performance evidence. You should rewrite it to
# gather the evidence you need.
###############################################################################
def main():
    runs = 10
    if len(sys.argv) > 1:
        runs = int(sys.argv[1])
    mst_trial(runs)
    tsp_trial(runs)

if __name__ == '__main__':
    main()
