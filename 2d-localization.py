import numpy as np

# Initialize a 2D world with uniform distribution
def initialize_world_probabilites(world):
    (rows, columns) = world.shape
    return (1/(rows*columns)) * np.ones((rows, columns), dtype="float")

# Take measurement
def sense(sensor_right, world, measurement, p):
    pHit = sensor_right
    pMiss = 1 - sensor_right

    idxs_hit = np.where(world == measurement)
    idxs_miss = np.where(world != measurement)

    p[idxs_hit] *= pHit
    p[idxs_miss] *= pMiss

    p = p / np.sum(p)

    return p

# Move the robot
def move(p_move, world, movement, p):
    [vertical, horizontal] = movement
    if vertical:
        p = (p*(1-p_move)) + (np.roll(p, vertical, axis=0)*p_move)
    elif horizontal:
        p = (p*(1-p_move)) + (np.roll(p, horizontal, axis=1)*p_move)

    return p

# Localize robot
def localize(world, sensor_right, p_move, measurements, movements):
    world = np.array(world)
    p = initialize_world_probabilites(world)


    for i in range(len(movements)):
        p = move(p_move, world, movements[i], p)
        p = sense(sensor_right, world, measurements[i], p)

    return p

# 3X3
# world = [['G', 'G', 'G'],
#          ['G', 'R', 'R'],
#          ['G', 'G', 'G']]

# 4X5
world = [['R', 'G', 'G', 'R', 'R'],
         ['R', 'R', 'G', 'R', 'R'],
         ['R', 'R', 'G', 'G', 'R'],
         ['R', 'R', 'R', 'R', 'R']]

# Take measurement commands
measurements = ['G', 'G', 'G', 'G', 'G']

"""
Take motion commands
[0, 0] - no movement
[0, 1] - move right
[0, -1] - move left
[1, 0] - move down
[-1, 0] - move up
Cannot move diagonally
"""
movements = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]

# probability that sensor measurement is correct
sensor_right = 0.7

# probability that the robot moves
p_move = 0.8

p = localize(world, sensor_right, p_move, measurements, movements)
print(p)
