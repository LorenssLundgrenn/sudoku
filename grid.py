import numpy as np
import random

class Grid():
    def __init__(self):
        self.__dimension = 9
        self.__square = None
        self.__data = None
        self.__immutable_mask = None
        self.__density_range = (20, 30) # starting density (%)

    def init(self, set_dim=None):
        if set_dim: self.__dimension = set_dim
        # dimension must be a number that is divisible with
        # the nearest square number because it just works
        self.__square = np.sqrt(self.__dimension)
        self.__square = np.round(self.__square).astype(int)
        self.__dimension -= self.__dimension % self.__square
        self.__data = [
            [None]*self.__dimension for _ in range(self.__dimension)
        ]
        self.__immutable_mask = [
            [0]*self.__dimension for _ in range(self.__dimension)
        ]
        # fill grid with random starting values
        rnd = random.Random()
        density = rnd.randint(*self.__density_range)/100
        starting_density = int(self.__dimension**2 * density)
        for _ in range(starting_density):
            rndx = rnd.randrange(self.__dimension)
            rndy = rnd.randrange(self.__dimension)
            available = self.get_available_values(rndx, rndy)
            value = available[rnd.randrange(len(available))]
            self.__data[rndy][rndx] = value
            self.__immutable_mask[rndy][rndx] = 1

    def get_dimension(self): return self.__dimension
    def get_square(self): return self.__square
    def get_data(self): return self.__data

    def get_all_values(self):
        return [x+1 for x in range(self.__dimension)]

    # find the quadrant in the grid the x, y
    # values correspond to
    def get_quadrant_from_pos(self, x, y):
        return (x//self.__square, y//self.__square)

    # find all available values for a position
    # using standard sudoku rules
    def get_available_values(self, x, y, p=True):
        qx, qy = self.get_quadrant_from_pos(x, y)
        return list(
            self.row_capacity(y) &
            self.col_capacity(x) & 
            self.quadrant_capacity(qx, qy)
        )

    def set(self, x, y, value): 
        if not self.__immutable_mask[y][x]:
            self.__data[y][x] = value
            return True
        return False

    # calculate available values in row
    def row_capacity(self, y):
        values = []
        for value in self.__data[y]:
            if value: values.append(value)
        all_values = self.get_all_values()
        return set(all_values)^set(values)

    # calculate available values in column
    def col_capacity(self, x):
        values = []
        for y in range(self.__dimension):
            value = self.__data[y][x]
            if value: values.append(value)
        all_values = self.get_all_values()
        return set(all_values)^set(values)

    # calculate available values withn a quadrant
    def quadrant_capacity(self, qx, qy):
        values = []
        for dy in range(self.__square):
            for dx in range(self.__square):
                x = qx*self.__square+dx
                y = qy*self.__square+dy
                value = self.__data[y][x]
                if value: values.append(value)
        all_values = self.get_all_values()
        return set(all_values)^set(values)