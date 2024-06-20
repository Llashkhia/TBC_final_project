import random

class Player:
    def __init__(self, name):
        self.name = name

    def get_players_name(self) -> list:
        names = []
        for i in range(4):
            name = input("Please enter name: ").strip().title()
            while not name or name in names:
                if not name:
                    print("Name cannot be empty")
                if name in names:
                    print("This name already exists")
                name = input("Please enter name: ").strip().title()
            names.append(name)
        random.shuffle(names)
        return [Player(name) for name in names]
        