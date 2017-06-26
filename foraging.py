import random
import matplotlib.pyplot as plt
import matplotlib.animation as an
import numpy as np
from forager import Forager
from landscape import Landscape


def eat(landscape, forager):
    want_to_eat = forager.quantity_which_can_be_eaten
    can_be_eaten = landscape.resources_which_can_be_eaten(forager.x_pos, forager.y_pos)
    will_be_eat = min(want_to_eat, can_be_eaten)
    forager.eat(will_be_eat)
    landscape.eaten(will_be_eat, forager.x_pos, forager.y_pos)


def is_moving(landscape, forager):
    if not landscape.resources_which_can_be_eaten(forager.x_pos, forager.y_pos):
        return True
    if landscape.resources_which_can_be_eaten(forager.x_pos, forager.y_pos) < Forager.EAT_BY_DAY:
        return True
    return False


def move(landscape, forager):
    rand_pos = random.sample([[0, 1], [1, 0], [-1, 0], [0, -1]], 4)
    i = 0
    while not landscape.is_valid_position(forager.x_pos + rand_pos[i][0], forager.y_pos + rand_pos[i][1]) or \
            not forager.is_valid_position(forager.x_pos + rand_pos[i][0], forager.y_pos + rand_pos[i][1]) or \
            i == 4:
        i = i + 1
    if i == 4:
        i = 0
        while not landscape.is_valid_position(forager.x_pos + rand_pos[i][0], forager.y_pos + rand_pos[i][1]):
            i = i + 1
    forager.move(forager.x_pos + rand_pos[i][0], forager.y_pos + rand_pos[i][1])


def foraging(landscape, forager):
    if is_moving(landscape, forager):
        move(landscape, forager)
    else:
        eat(landscape, forager)
    forager.sustain()


def display(landscape, forager):
    land = np.copy(landscape.land)
    land[forager.x_pos, forager.y_pos] = 150
    return plt.imshow(land)


def update(_):
    global l, f
    if not f.is_dead:
        foraging(l, f)
    return display(l, f),


l = Landscape(30, 30, 15)
f = Forager(0, 0)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)

animation = an.FuncAnimation(fig, update, interval=1, blit=True, frames=200)
plt.show()

print('Total move = %d' % f.total_move)
print('Total eaten = %d' % f.total_eaten)
