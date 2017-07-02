from forager import Forager
import pytest


forager = Forager(0, 0)


def test_is_dead():
    forager.stock = 1
    assert not forager.is_dead
    forager.stock = 0
    assert forager.is_dead


def test_quantity_which_can_be_eat():
    forager.stock = Forager.STOCK_MAX - 2
    assert forager.quantity_which_can_be_eaten == 2
    forager.stock = Forager.STOCK_MAX - Forager.EAT_MAX_BY_DAY * 2
    assert forager.quantity_which_can_be_eaten == Forager.EAT_MAX_BY_DAY


def test_eat():
    forager.stock = Forager.STOCK_MAX - 10
    forager.total_eaten = 10
    forager.eat(5)
    assert forager.stock == Forager.STOCK_MAX - 5
    assert forager.total_eaten == 15
    forager.stock = Forager.STOCK_MAX - 10
    forager.total_eaten = 10
    forager.eat(15)
    assert forager.stock == Forager.STOCK_MAX
    assert forager.total_eaten == 20


def test_sustain():
    forager.stock = Forager.EAT_BY_DAY * 2
    assert forager.sustain()
    assert forager.stock == Forager.EAT_BY_DAY
    assert not forager.sustain()
    assert forager.stock == 0


def test_move():
    with pytest.raises(Exception):
        forager.move(Forager.MOVE_MAX_BY_DAY * 2, 0)
    with pytest.raises(Exception):
        forager.move(0, Forager.MOVE_MAX_BY_DAY * 2)
    assert forager.move(0, 0)
    assert forager.y_pos == 0
    assert forager.stock == 0
    assert forager.total_move == 0
    forager.stock = Forager.EAT_BY_MOVE
    assert not forager.move(1, 0)
    forager.stock = Forager.EAT_BY_MOVE * Forager.MOVE_MAX_BY_DAY + 1
    forager.total_move = 0
    assert forager.move(Forager.MOVE_MAX_BY_DAY, 0)
    assert forager.x_pos == Forager.MOVE_MAX_BY_DAY
    assert forager.y_pos == 0
    assert forager.stock == 1
    assert forager.total_move == Forager.MOVE_MAX_BY_DAY
    forager.stock = Forager.EAT_BY_MOVE * Forager.MOVE_MAX_BY_DAY + 1
    assert forager.move(Forager.MOVE_MAX_BY_DAY, Forager.MOVE_MAX_BY_DAY)
    assert forager.x_pos == Forager.MOVE_MAX_BY_DAY
    assert forager.y_pos == Forager.MOVE_MAX_BY_DAY
    assert forager.stock == 1
    assert forager.total_move == Forager.MOVE_MAX_BY_DAY * 2


def test_add_pos_to_memory():
    forager.memory_position = [(0, 1)]
    forager.y_pos = 1
    forager.x_pos = 1
    forager.add_pos_to_memory()
    assert forager.memory_position == [(0, 1), (1, 1)]
    pos = [(0, 1) for _ in range(Forager.MEMORY_SIZE)]
    forager.memory_position = pos
    forager.add_pos_to_memory()
    pos2 = pos[:-1]
    pos2.append((1, 1))
    assert forager.memory_position == pos2


def test_is_valid_position():
    forager.memory_position = []
    assert forager.is_valid_position(1, 1)
    forager.memory_position = [(1, 0), (0, 0), (0, 1)]
    assert forager.is_valid_position(1, 1)
    assert not forager.is_valid_position(0, 0)
