from landscape import Landscape, complete_resources_if_possible
import pytest
import numpy as np


def test_landscape_creation():
    x = 10
    y = 10
    nb_patches = 3
    landscape = Landscape(x, y, nb_patches)
    assert landscape.land.shape == (x, y)
    assert (landscape.land > 0).sum() >= nb_patches

    too_many_patch = x * y + 1
    with pytest.raises(Exception):
        Landscape(x, y, too_many_patch)


def test_add_resources_as_patch():
    x = 10
    y = 10
    nb_patches = 0
    x_pos = 4
    y_pos = 6
    resource_dim = 75
    landscape = Landscape(x, y, nb_patches)
    landscape.add_resources_as_patch(x_pos, y_pos, resource_dim)
    assert landscape.land[x_pos, y_pos] == resource_dim
    assert (landscape.land[landscape.land != resource_dim] < resource_dim).all()
    assert (landscape.land[landscape.land != resource_dim] > 0).any()

    landscape.add_resources_as_patch(x_pos, y_pos, resource_dim)
    assert landscape.land[x_pos, y_pos] == Landscape.MAX_VALUE


def test_resources_which_can_be_eaten():
    x = 10
    y = 10
    nb_patches = 0
    x_pos = 4
    y_pos = 6
    resource_dim = 75
    landscape = Landscape(x, y, nb_patches)
    landscape.land[x_pos, y_pos] = resource_dim
    assert landscape.resources_which_can_be_eaten(x_pos, y_pos) == resource_dim


def test_eaten():
    x = 10
    y = 10
    nb_patches = 0
    x_pos = 4
    y_pos = 6
    resource_dim = 75
    landscape = Landscape(x, y, nb_patches)
    landscape.land[x_pos, y_pos] = resource_dim
    landscape.eaten(10, x_pos, y_pos)
    assert landscape.resources_which_can_be_eaten(x_pos, y_pos) == resource_dim - 10
    landscape.land[x_pos, y_pos] = resource_dim
    landscape.eaten(resource_dim+10, x_pos, y_pos)
    assert landscape.resources_which_can_be_eaten(x_pos, y_pos) == 0


def test_is_valid_position():
    x = 10
    y = 10
    nb_patches = 0
    landscape = Landscape(x, y, nb_patches)
    assert not landscape.is_valid_position(x, y-1)
    assert not landscape.is_valid_position(0, -1)
    assert landscape.is_valid_position(5, 5)


def test_complete_resources_if_possible():
    x = 10
    y = 10
    patch = np.zeros([x,y], dtype=int)
    x_pos = 4
    y_pos = 6
    resource_dim = 75
    patch = complete_resources_if_possible(patch, x_pos, y_pos, resource_dim)
    assert patch[x_pos, y_pos] == resource_dim
    assert (patch[patch != resource_dim] < resource_dim).all()
    assert (patch[patch != resource_dim] > 0).any()
