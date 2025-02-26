import json
import argparse
from typing import Dict

# ELO Constants
INITIAL_ELO = 1500
K_FACTOR = 32

class BadmintonLeague:
    def __init__(self):
        self.players: Dict[str, float] = {}

    def add_player(self, name: str, rating: float = INITIAL_ELO):
        if name in self.players:
            print(f"Player '{name}' already exists.")
        else:
            self.players[name] = rating
            print(f"Player '{name}' added with ELO {rating}.")

    def remove_player(self, name: str):
        if name in self.players:
            del self.players[name]
            print(f"Player '{name}' removed.")
        else:
            print(f"Player '{name}' does not exist.")

    def expected_score(self, rating_a: float, rating_b: float) -> float:
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_elo(self, player1: str, player2: str, score1: int, score2: int):
        if player1 not in self.players or player2 not in self.players:
            raise ValueError("Both players must be registered.")

        rating1 = self.players[player1]
        rating2 = self.players[player2]

        expected1 = self.expected_score(rating1, rating2)
        expected2 = self.expected_score(rating2, rating1)

        if score1 > score2:
            score1_result, score2_result = 1, 0
        elif score1 < score2:
            score1_result, score2_result = 0, 1
        else:
            score1_result, score2_result = 0.5, 0.5

        self.players[player1] += K_FACTOR * (score1_result - expected1)
        self.players[player2] += K_FACTOR * (score2_result - expected2)
        print(f"Updated ELO: {player1} ({self.players[player1]:.2f}), {player2} ({self.players[player2]:.2f})")

    def show_leaderboard(self):
        sorted_players = sorted(self.players.items(), key=lambda x: x[1], reverse=True)
        print("\nLeaderboard:")
        for rank, (name, rating) in enumerate(sorted_players, 1):
            print(f"{rank}. {name} - ELO: {rating:.2f}")

    def save_data(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.players, f)
        print(f"Data saved to {filename}.")

    def load_data(self, filename: str):
        try:
            with open(filename, 'r') as f:
                self.players = json.load(f)
            print(f"Data loaded from {filename}.")
        except FileNotFoundError:
            print(f"File '{filename}' not found. Starting with a new league.")


def main():
    parser = argparse.ArgumentParser(description="Badminton League ELO Manager")
    parser.add_argument('--add-player', '-a', nargs='+', help="Add players with default rating.")
    parser.add_argument('--remove-player', '-r', nargs='+', help="Remove players from the league.")
    parser.add_argument('--leaderboard', '-ls', action='store_true', help="Show the leaderboard.")
    parser.add_argument('--record', action='store_true', help="Record a match result.")

    args = parser.parse_args()
    league = BadmintonLeague()
    league.load_data("badminton_league.json")

    if args.add_player:
        for player in args.add_player:
            league.add_player(player)

    if args.remove_player:
        for player in args.remove_player:
            league.remove_player(player)

    if args.leaderboard:
        league.show_leaderboard()

    if args.record:
        try:
            player1 = input("Enter Player 1 Name: ").strip()
            score1 = int(input(f"Enter {player1}'s Score: "))
            player2 = input("Enter Player 2 Name: ").strip()
            score2 = int(input(f"Enter {player2}'s Score: "))
            league.update_elo(player1, player2, score1, score2)
        except ValueError as e:
            print(f"Error: {e}")

    league.save_data("badminton_league.json")

if __name__ == "__main__":
    main()
