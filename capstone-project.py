import random
from datetime import datetime


def age_calculator(dob):
    '''
    Calculate a person's age from their date of birth. 

    Args:
    dob (str): The user's date of birth.
    '''
    now = datetime.now()
    given_date = datetime.strptime(dob, "%d-%m-%Y")
    age_years = now.year - given_date.year

    # account for the fact the person's birthday may not have passed in the current year
    if now.month - given_date.month < 0 or (now.month == given_date.month and now.day - given_date.day < 0):
        age_years -= 1

    return age_years


def player_selection(player_stats, player_type, user_points):
    '''
    Display a selection of players and their statistics, prompting the user to select one.

    Args:
    player_stats (list): a list of dictionaries that contain statistics for each selectable player.
    player_type (str): selects the different player lists (goalkeepers or penalty takers).
    user_points (int): total points scored by the user which unlocks better players in the selection.
    '''
    # points required to unlock each goalkeeper and penalty taker
    if player_type == "goalkeeper":
        player_points = [0, 500, 1750, 3750, 7500]
    else:
        player_points = [0, 1000, 2500, 5000, 10000]

    while True:
        # display a numbered list of the player names for the user to select from
        player_names = [d.get("Name") for d in player_stats]
        player_names_str = ''
        for num, name in enumerate(player_names):
            player_names_str += f"{num+1}. {name} (Points required: {player_points[num]}) \n "

        try:
            user_player = int(input(
                f"Points = {user_points} \nChoose your {player_type} (select to preview stats): \n {player_names_str}"))

            # check that the user's input is valid and they have enough points to select the chosen player.
            # allow them to view the stats of their chosen player and either confirm or go back to re-select.
            if 0 < user_player < len(player_names)+1 and player_points[user_player-1] <= user_points:
                print(player_stats[user_player - 1])
                confirm = input(
                    "Type YES to confirm choice or anything else to go back: ").lower()
            elif player_points[user_player-1] >= user_points:
                print("You do not have enough points to select this player.")
                continue
            else:
                raise Exception

            if confirm == "yes":
                break
        except:
            print("Input a valid number please.")

    return player_stats[user_player-1]


def coin_toss():
    '''
    Perform a coin toss to determine if the user or opponent takes the first penalty.
    '''
    coin_choice = input(
        "Heads (H) or Tails (T)? (To determine first taker): ").lower()
    outcomes = ['h', 't']
    flip = random.randint(0, 1)
    if coin_choice == outcomes[flip]:
        print("Good choice! You're up first.")
        return True
    else:
        print("Poor decision! You're taking second.")
        return False


def penalty(keeper_stats_avg, taker_stats_avg, goalkeeper, first_taker, difficulty):
    '''
    Prompt the user to take/save a penalty by selecting where to shoot/dive. 

    args:
    keeper_stats_avg (int): Mean of the statistics of the user's chosen goalkeeper.
    taker_stats_avg (int): Mean of statistics of the user's chosen penalty taker.
    goalkeeper (bool): True if the user is saving a penalty, False if they are shooting.
    first_taker (bool): True if the user took the first penalty of the shootout, False if not.
    difficulty (int): User's selected difficulty for the shootout as an integer (1-Easy, 2-Intermediate, 3-Hard, 4-Very Hard).
    '''
    if goalkeeper:
        phrases = ["dive", "Penalty saved! The crowd goes wild.",
                   "Goal! Hang your head in shame.", "stood between the wrong goalposts, bad luck."]
    else:
        phrases = ["shoot", "Goal! The crowd goes wild.",
                   "Oh no! Penalty saved.", "felt too embarrassed to take the penalty."]

    try:
        user_choice = int(input(
            f"Where would you like to {phrases[0]}? \n ------------- \n | 1   2   3 | \n | 4   5   6 | \n"))
        if not 0 < user_choice < 7:
            raise Exception

        # the winner of the coin toss gets an 5% increase on their chances of scoring/saving each penalty to reflect the advantage of doing so in real life.
        # for each level of difficulty above Easy the opponent has a 10% greater chance of scoring/saving a penalty.
        buffer = int(not first_taker)*5 - \
            int(first_taker)*5 + (difficulty-1)*10
        opponent = random.randint(
            0+buffer, 99+buffer)

        if (goalkeeper and opponent <= keeper_stats_avg) or (not goalkeeper and opponent <= taker_stats_avg):
            print(f"{phrases[1]}")
            print(opponent, f"keeper = {keeper_stats_avg}",
                  f"taker = {taker_stats_avg}")
            return True
        else:
            print(f"{phrases[2]}")
            print(opponent, f"keeper = {keeper_stats_avg}",
                  f"taker = {taker_stats_avg}")
            return False
    except:
        print(f"You {phrases[3]}")


def check_score(user_score, opponent_score, shot_count, first_taker):
    '''
    Check the score of the shootout and return True if either player has won

    args:
    user_score (int): number of penalties scored by the user
    opponent_score (int): number of penalties scored by the opponent
    shot_count (int): total number of penalties taken in the shootout 
    first_taker (bool): True if the user took the first penalty of the shootout, False if not.
    '''
    if first_taker:
        user_shot_count = (shot_count+1) // 2
        opponent_shot_count = shot_count // 2
    else:
        opponent_shot_count = (shot_count+1) // 2
        user_shot_count = shot_count // 2

    user_remaining = 5 - user_shot_count
    opponent_remaining = 5 - opponent_shot_count

    if shot_count < 10 and (user_score > opponent_score + opponent_remaining or opponent_score > user_score + user_remaining):
        return True
    elif shot_count >= 10 and shot_count % 2 == 0 and user_score != opponent_score:
        return True

    return False


taker_stats = [{"Name": "Alvaro Morata", "Age": f"{age_calculator('23-10-1992')}", "Shot power": 60, "Accuracy": 53, "Composure": 37,
                "Special ability": None},
               {"Name": "Scott McTominay",
                   "Age": f"{age_calculator('08-12-1996')}", "Shot power": 68, "Accuracy": 57, "Composure": 55, "Special ability": None},
               {"Name": "Bruno Fernandes", "Age": f"{age_calculator('08-09-1994')}", "Shot power": 62,
                "Accuracy": 73, "Composure": 75, "Special ability": "Hop penalty"},
               {"Name": "Andrea Pirlo", "Age": f"{age_calculator('19-05-1979')}", "Shot power": 53,
                "Accuracy": 94, "Composure": 93, "Special ability": "Panenka penalty"},
               {"Name": "Cristiano Ronaldo", "Age": f"{age_calculator('05-02-1985')}", "Shot power": 95, "Accuracy": 84, "Composure": 91, "Special ability": "Volley penalty"}]

keeper_stats = [{"Name": "Kepa Arrizabalaga", "Age": f"{age_calculator('03-10-1994')}", "Diving": 53, "Handling": 45, "Reflexes": 52,
                 "Special ability": None},
                {"Name": "David Marshall",
                    "Age": f"{age_calculator('05-03-1985')}", "Diving": 63, "Handling": 60, "Reflexes": 42, "Special ability": None},
                {"Name": "Unai Simon", "Age": f"{age_calculator('11-06-1997')}", "Diving": 68,
                 "Handling": 53, "Reflexes": 74, "Special ability": "Early read"},
                {"Name": "Petr Cech", "Age": f"{age_calculator('20-05-1982')}", "Diving": 78,
                 "Handling": 85, "Reflexes": 62, "Special ability": "Safe hands"},
                {"Name": "Iker Casillas", "Age": f"{age_calculator('20-05-1981')}", "Diving": 87, "Handling": 73, "Reflexes": 95, "Special ability": "Cat spring"}]


def penalty_shootout():
    '''
    Run the penalty shootout game between the user and the opponent (the computer).

    This function allows the user to play as many shootouts as they like through which they earn points and unlock players. 
    The previously defined functions are integrated to determine the order of the shootout and perform user player selection, user shots and saves, and score checking.
    At the end of game, the user's score will be reported along with the number of shootouts played.   
    '''
    points = 0
    round_points = 0
    plays = 0

    print("#"*28 + "\nWelcome to Penalty Shootout!\n" + "#"*28)

    while True:

        points += round_points

        if points < 0:
            points = 0

        # prompt the user to play again or exit the game after they have played more than one shootout
        if plays:
            play_again = input(
                f"Total points = {points} \n Would you like to play again? (Type YES to continue or anything else to finish) ").lower()
            if play_again != "yes":
                break

        difficulty = int(input(
            "What difficulty would you like to play on:\n1. Easy (200 point win)\n2. Intermediate (400 point win)\n3. Hard (600 point win)\n4. Very Hard (800 point win)\n"))

        round_points -= round_points

        # prompt user to select their penalty taker and goalkeeper
        user_taker = player_selection(taker_stats, "penalty taker", points)
        user_keeper = player_selection(keeper_stats, "goalkeeper", points)

        # initialise the score and perform the coin toss to decide if the user takes first
        user_score = 0
        opponent_score = 0
        shot_count = 0
        first_taker = coin_toss()

        taker_stats_avg = sum(list(user_taker.values())[2:5]) // 3
        keeper_stats_avg = sum(list(user_keeper.values())[2:5]) // 3
        list(user_taker.values())[5]

        while True:

            # prompt the user to take first penalty if they won the coin toss,
            # if not skip this code once as the user is taking second
            if (not first_taker and shot_count != 0) or first_taker:
                if penalty(keeper_stats_avg, taker_stats_avg, False, first_taker, difficulty):
                    round_points += 50
                    user_score += 1
                shot_count += 1
                print(f"You {user_score} - {opponent_score} Opp")
                if check_score(user_score, opponent_score, shot_count, first_taker):
                    break

            if not penalty(keeper_stats_avg, taker_stats_avg, True, first_taker, difficulty):
                opponent_score += 1
            shot_count += 1
            print(f"You {user_score} - {opponent_score} Opp")

            if check_score(user_score, opponent_score, shot_count, first_taker):
                break

        # determine the winner of the shootout
        scores = [user_score, opponent_score]
        winner = scores.index(max(scores))
        plays += 1

        if winner == 0:
            round_points += 200 + (difficulty-1)*200
            print(f"You win!!! \nRound points: {round_points}")
        else:
            round_points -= 100 * (difficulty-1)
            print(f"You lose!!! \nRound points: {round_points}")

    print(
        f"After {plays} shootout{'s' * bool(plays-1)} you scored {points} points!")


penalty_shootout()
