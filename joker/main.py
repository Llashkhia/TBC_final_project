from game import Game


def main():
    print("Welcome to the Card Game 'JOKER'!")
    print("Card colors: (SPADES -'S'; HEART - 'H'; DIAMOND - 'D'; CLUB - 'C') ")
    print("Card values: (JACK- 'J'; QUEEN - 'Q'; KING - 'K'; ACE -'A')")
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
