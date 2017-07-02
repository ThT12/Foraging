from forager import Forager
from landscape import Landscape
from foraging import eat, is_moving, move, foraging


x = 2
y = 2
nb_patches = 0
x_forager = 0
y_forager = 0
landscape = Landscape(x, y, nb_patches)
forager = Forager(x_forager, y_forager)


def test_eat():
    forager.stock = Forager.STOCK_MAX - Forager.EAT_MAX_BY_DAY + 2
    landscape.land[x_forager, y_forager] = Forager.EAT_MAX_BY_DAY
    eat(landscape, forager)
    assert landscape.land[x_forager, y_forager] == 2
    assert forager.stock == Forager.STOCK_MAX
    forager.stock = Forager.STOCK_MAX - Forager.EAT_MAX_BY_DAY - 2
    landscape.land[x_forager, y_forager] = Forager.EAT_MAX_BY_DAY
    eat(landscape, forager)
    assert landscape.land[x_forager, y_forager] == 0
    assert forager.stock == Forager.STOCK_MAX - 2


def test_is_moving():
    landscape.land[x_forager, y_forager] = 0
    assert is_moving(landscape, forager)
    landscape.land[x_forager, y_forager] = Forager.EAT_MAX_BY_DAY - 1
    forager.stock = 0
    assert is_moving(landscape, forager)
    landscape.land[x_forager, y_forager] = Forager.EAT_MAX_BY_DAY
    assert not is_moving(landscape, forager)


def test_move():
    forager.x_pos = x_forager
    forager.y_pos = y_forager
    forager.stock = Forager.STOCK_MAX
    move(landscape, forager)
    assert (forager.x_pos, forager.y_pos) != (x_forager, y_forager)
    forager.x_pos = x_forager
    forager.y_pos = y_forager
    forager.stock = Forager.STOCK_MAX
    forager.memory_position = [(x_forager - 1, y_forager), (x_forager, y_forager - 1), (x_forager + 1, y_forager)]
    move(landscape, forager)
    assert (forager.x_pos, forager.y_pos) == (x_forager, y_forager+1)
    forager.x_pos = x_forager
    forager.y_pos = y_forager
    forager.stock = Forager.STOCK_MAX
    forager.memory_position = [(x_forager - 1, y_forager), (x_forager, y_forager - 1), (x_forager + 1, y_forager),
                               (x_forager, y_forager + 1)]
    move(landscape, forager)
    assert (forager.x_pos, forager.y_pos) != (x_forager, y_forager)


def test_foraging(mocker):
    mocker.patch('foraging.is_moving', return_value=True)
    forager.x_pos = x_forager
    forager.y_pos = y_forager
    forager.stock = Forager.STOCK_MAX
    foraging(landscape, forager)
    assert (forager.x_pos, forager.y_pos) != (x_forager, y_forager)
    assert forager.stock == Forager.STOCK_MAX - Forager.EAT_BY_MOVE - Forager.EAT_BY_DAY
    mocker.patch('foraging.is_moving', return_value=False)
    forager.x_pos = x_forager
    forager.y_pos = y_forager
    forager.stock = Forager.STOCK_MAX
    foraging(landscape, forager)
    assert (forager.x_pos, forager.y_pos) == (x_forager, y_forager)
    assert forager.stock == Forager.STOCK_MAX - Forager.EAT_BY_DAY
