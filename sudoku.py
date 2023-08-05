import grid
import cli

# [!] needs an input manager alongside render component
#     that or merge render component with client
class Client():
    def __init__(self):
        self.grid = grid.Grid()
        self.renderer = None

        self.running = True
        self.max_mistakes = 3
        self.mistakes = 0

    def init(self, renderer=None):
        self.grid.init(9)
        if not renderer: renderer = cli.SudokuCLI
        self.renderer = renderer()
        self.mistakes = 0

    def check_state(self):
        if self.mistakes >= self.max_mistakes:
            # [!] move to render and input manager components
            # <move>
            print("you made too many mistakes, game over")
            user_in = input("sudoku(new game?)[y/n]>> ").lower()
            if user_in == "y": self.init()
            else: self.running = False
            # </move>

    # [!] move to input manager
    # [!] this is terrible. I don't like it
    #     needs calls to renderer instead of print
    #     needs a better input argument system
    #     needs error handling
    #     needs clean up
    def get_inputs(self):
        user_in = input("sudoku>> ").lower()
        args = user_in.strip().split(" ")
        
        if user_in == "exit":
            self.running = False
        elif user_in == "help":
            self.renderer.display_help()
        elif args[0] == "set":
            x, y = int(args[1]), int(args[2])
            value = int(args[3])
            all_values = self.grid.get_all_values()
            if (x > max(all_values) or x < min(all_values)) or (
                y > max(all_values) or y < min(all_values)
            ):
                print(f"x and y supports numbers from {min(all_values)}-{max(all_values)}")
                return None
            
            x-=1; y-=1
            available_values = self.grid.get_available_values(x, y)
            if value in available_values: 
                if not self.grid.set(x, y, value):
                    print("cannot change immutable value")
            else:
                self.mistakes +=1
                self.renderer.display_mistakes(
                    self.mistakes, 
                    self.max_mistakes
                )
        elif args[0] == "mistakes":
            self.renderer.display_mistakes(
                self.mistakes, 
                self.max_mistakes
            )
        elif user_in: 
            print(f"unrecognized command: {args[0]}")

    def mainloop(self):
        self.renderer.display_help()
        while self.running:
            self.renderer.display_grid(
                self.grid.get_data(),
                self.grid.get_dimension(),
                self.grid.get_square()
            )
            self.get_inputs()
            self.check_state()

