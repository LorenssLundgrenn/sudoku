import numpy as np

class SudokuCLI():
    def __init__(self):
        pass

    # why did this take me an hour to write
    def set_text_padding(self, text, spacing):
        dif = spacing - len(text)
        pad_left = dif//2
        pad_right = np.ceil(dif/2).astype(int)
        return pad_left*' ' + text + pad_right*' '

    def display_grid(self, data, dimension, square):
        # convert to str matrix
        data = [list(map(str, row)) for row in data]
        #add vertical bars
        for row in data:
            for x in range(dimension//square+1):
                row.insert(x*(square+1), "│")

        # add padding to list elements, longest characters must
        # be one whitespace apart from neighbors
        for y in range(len(data)):
            row = data[y]
            for x in range(len(row)):
                char = row[x]
                if char == "None": char = "."
                spacing = len(str(dimension))
                char = self.set_text_padding(char, spacing)
                data[y][x] = char

        # flatted to 1d list
        data = [" ".join(map(str, row)) for row in data]
        # add horizontal bars
        for y in range(dimension//square+1):
            data_width = len("".join(data[y]).strip())
            data.insert(y*(square+1), "─"*data_width)
        data = "\n".join(data)
        print(data)

    def display_mistakes(self, mistakes, max_mistakes):
        print(f"mistakes: ({mistakes}/{max_mistakes})")

    def display_help(self):
        print("classic sudoku")
        print("this is the CLI version of the sudoku program")
        print("by Lorenss Teo Lundgrenn\n")
        print("commands:")
        print("exit\t\t\t- terminate program")
        print("help\t\t\t- display this menu")
        print("set <x> <y> <value>\t- set the value of a cell on the grid")
        print("mistakes\t\t- display mistakes")
        print("\nindev notice: the set command is unstable and")
        print("lacks error handling. Make sure you get it right")