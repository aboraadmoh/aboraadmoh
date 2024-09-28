#Mohammed Murtadha Al-khulaidi
#محمد مرتضى الخليدي 
#تكليف الباصر
import random

class Card:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

    def numeric_value(self):
        if self.value in ["Jack", "Queen", "King"]:
            return 10
        elif self.value == "Ace":
            return 1
        else:
            return int(self.value)

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.captured_cards = []

    def draw(self, deck, num=4):
        for _ in range(num):
            self.hand.append(deck.draw_card())

    def play_card(self, index):
        return self.hand.pop(index)

    def capture_cards(self, cards):
        self.captured_cards.extend(cards)

    def has_cards(self):
        return len(self.hand) > 0

    def __repr__(self):
        return f"{self.name} has captured {len(self.captured_cards)} cards."

class Game:
    def __init__(self):
        self.deck = Deck()
        self.table = []
        self.player = Player("You")
        self.computer = Player("Computer")
        self._deal_initial_cards()

    def _deal_initial_cards(self):
        self.player.draw(self.deck)
        self.computer.draw(self.deck)
        for _ in range(4):
            self.table.append(self.deck.draw_card())

    def _check_capture(self, player, card_played):
        captured = []
        for card in self.table:
            if card_played.numeric_value() == card.numeric_value():
                captured.append(card)

        if captured:
            player.capture_cards(captured)
            self.table = [c for c in self.table if c not in captured]

    def play_round(self, player, card_index):
        card_played = player.play_card(card_index)
        print(f"\n{player.name} plays: {card_played}")
        self._check_capture(player, card_played)
        self.table.append(card_played)

    def play(self):
        while self.deck.cards or self.player.has_cards() or self.computer.has_cards():
            if not self.player.has_cards():
                self.player.draw(self.deck)
                self.computer.draw(self.deck)

            print(f"\nCards on the table: {self.table}")
            print(f"Your hand: {[f'{i}: {card}' for i, card in enumerate(self.player.hand)]}")

            # Choose a card to play
            while True:
                try:
                    card_index = int(input("Choose a card index from your hand (0-3): "))
                    if 0 <= card_index < len(self.player.hand):
                        break
                    else:
                        print("Invalid choice, try again.")
                except ValueError:
                    print("Please enter a valid number.")

            # Play player's card
            self.play_round(self.player, card_index)

            # Computer plays a card
            computer_card_index = random.randint(0, len(self.computer.hand) - 1)
            self.play_round(self.computer, computer_card_index)

            # Display the table and captured cards status
            print(f"\nCards on the table after this round: {self.table}")
            print(self.player)
            print(self.computer)

        # Determine the winner based on the number of captured cards
        if len(self.player.captured_cards) > len(self.computer.captured_cards):
            print("\nYou win the game!")
        else:
            print("\nComputer wins the game!")

# Start the game
game = Game()
game.play()