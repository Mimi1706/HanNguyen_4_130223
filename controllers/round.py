from views.round import RoundView
from models.match import MatchModel
from tinydb import TinyDB, where
from tinydb.operations import add
import random

db_players = TinyDB('db_players.json').table("players").all()
db_tournaments = TinyDB('database.json').table("tournaments")

class RoundController:
    def __init__(self):
        self.view = RoundView()

    def display_menu(self):
        while True:
            user_input = self.view.user_choice()

            if user_input == "1":
                self.create_match()
                break

            if user_input == "2":
                break

            if user_input == "3":
                break

            else: 
                self.view.custom_print("Erreur de sélection, veuillez sélectionner une option valide.")
                self.display_menu()

    def pair_players(self):
        tournament_players = list(db_tournaments.get(doc_id=1)["players"])
        tournament_current_round = db_tournaments.get(doc_id=1)["current_round"]
        all_players_chessIds = [r['chess_id'] for r in tournament_players]
        all_paired_players = []

        if(tournament_current_round == 0):
            while len(all_players_chessIds) > 0:
                randomized_pair = random.sample(all_players_chessIds, 2)
                all_players_chessIds.remove(randomized_pair[0])
                all_players_chessIds.remove(randomized_pair[1])  
                all_paired_players.append(randomized_pair)

        return all_paired_players

    def create_match(self):
        all_paired_players = self.pair_players()
        created_match = []

        for index, paired_players in enumerate(all_paired_players):
            match = MatchModel(f"Match_{index+1}", paired_players)
            created_match.append(match.serializer())

        db_tournaments.update(add("rounds_list",created_match),where("name")=="test")
    
    def update_round(self):
        tournaments = db_tournaments.search(where("name")=="test")[0]
        current_match = self.create_match()
        previous_matches = list(tournaments.get("rounds_list"))
        previous_matches.extend(current_match)

        db_tournaments.update({"current_round":1},where("name")=="test")
        db_tournaments.update({"rounds_list":previous_matches},where("name")=="test")