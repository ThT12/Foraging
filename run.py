import matplotlib.pyplot as plt
import matplotlib.animation as an
from forager import Forager
from landscape import Landscape
from foraging import foraging, display


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
