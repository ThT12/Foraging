import numpy as np
import random
import itertools
import matplotlib.pyplot as plt


class Landscape:
    MAX_VALUE = 100
    MIN_VALUE_TO_CONTINUE = 10
    MIN_INIT_VALUE = 50
    RATIO_DIRECT_EXPANSION = 1.5
    RATION_DIAGONAL_EXPANSION = 1.8

    def __init__(self, x_size: int, y_size: int, nb_patches):
        if nb_patches > x_size * y_size:
            raise ValueError('Too many patches')
        self.land = np.zeros([x_size, y_size], dtype=int)
        rand_pos = random.sample(list(itertools.product(*[range(x_size), range(y_size)])), nb_patches)
        for pos in rand_pos:
            self.add_resources_as_patch(pos[0], pos[1], random.randint(Landscape.MIN_INIT_VALUE, Landscape.MAX_VALUE))

    def add_resources_as_patch(self, x_loc: int, y_loc: int, resource_dim: int):
        patch = np.zeros(self.land.shape, dtype=int)
        resource_dim = min(resource_dim, Landscape.MAX_VALUE)
        patch = complete_resources_if_possible(patch, x_loc, y_loc, resource_dim)
        self.land = self.land + patch
        self.land[self.land > Landscape.MAX_VALUE] = Landscape.MAX_VALUE

    def display(self):
        plt.imshow(self.land)
        plt.show()


def complete_resources_if_possible(patch, x_loc: int, y_loc: int, resource_dim: int):
    if x_loc not in range(patch.shape[0]) or y_loc not in range(patch.shape[1]):
        return patch
    if patch[x_loc, y_loc] and patch[x_loc, y_loc] > resource_dim:
        return patch
    else:
        patch[x_loc, y_loc] = resource_dim
    resource_expansion_direct = int(resource_dim / Landscape.RATIO_DIRECT_EXPANSION)
    if resource_expansion_direct < Landscape.MIN_VALUE_TO_CONTINUE:
        return patch
    patch = complete_resources_if_possible(patch, x_loc + 1, y_loc, resource_expansion_direct)
    patch = complete_resources_if_possible(patch, x_loc - 1, y_loc, resource_expansion_direct)
    patch = complete_resources_if_possible(patch, x_loc, y_loc + 1, resource_expansion_direct)
    patch = complete_resources_if_possible(patch, x_loc, y_loc - 1, resource_expansion_direct)
    resource_expansion_diagonal = int(resource_dim / Landscape.RATION_DIAGONAL_EXPANSION)
    if resource_expansion_diagonal < Landscape.MIN_VALUE_TO_CONTINUE:
        return patch
    patch = complete_resources_if_possible(patch, x_loc + 1, y_loc + 1, resource_expansion_diagonal)
    patch = complete_resources_if_possible(patch, x_loc + 1, y_loc - 1, resource_expansion_diagonal)
    patch = complete_resources_if_possible(patch, x_loc - 1, y_loc + 1, resource_expansion_diagonal)
    patch = complete_resources_if_possible(patch, x_loc - 1, y_loc - 1, resource_expansion_diagonal)
    return patch


def main():
    x = 50
    y = 50
    nb_patches = 20
    landscape = Landscape(x, y, nb_patches)
    landscape.display()


if __name__ == "__main__":
    main()

