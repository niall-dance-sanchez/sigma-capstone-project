import random
from datetime import datetime

def age_calculator(dob):

    now = datetime.now()
    given_date = datetime.strptime(dob, "%d-%m-%Y")

    age_years = now.year - given_date.year

    if now.month - given_date.month < 0 or (now.month == given_date.month and now.day - given_date.day < 0):
        age_years -= 1

    return age_years


def player_selection(player_stats, player_type):
    '''
    DEFINITION
    '''
    while True: 
        player_names = [d.get("Name") for d in player_stats]
        player_names_str = ''
        for num, name in enumerate(player_names):
            player_names_str += f'{num+1}. {name} \n '

        try: 
            user_player = int(input(f"Choose your {player_type} (select to preview stats): \n {player_names_str}"))

            if 0 < user_player < len(player_names)+1:
                print(player_stats[user_player- 1])
                confirm = input("Type YES to confirm choice or anything else to go back: ").lower()
            else:
                raise Exception

            if confirm == 'yes':
                break 
        except:
            print("Input a valid number please.")

    return player_stats[user_player- 1]
 

def coin_toss():
    '''
    perform a coin toss to determine if the user or opponent takes the first penalty
    '''
    coin_choice = input("Heads (H) or Tails (T)? (To determine first taker): ").lower()
    outcomes = ['h', 't']
    flip = random.randint(0,1)
    if coin_choice == outcomes[flip]:
        print("Good choice! You're up first.")
        return True
    else: 
        print("Poor decision! You're taking second.")
        return False 
    
def penalty(keeper_stats_avg, taker_stats_avg, goalkeeper, first_taker):
    '''
    DEFINTION
    '''
    if goalkeeper: 
        phrases = ["dive", "Goal! Hang your head in shame.", "Penalty saved! The crowd goes wild." , "stood between the wrong goalposts, bad luck."]
    else: 
        phrases = ["shoot", "Oh no! Penalty saved.", "Goal! The crowd goes wild.", "felt too embarassed to take the penalty."]

    try: 
        user_choice = int(input(f"Where would you like to {phrases[0]}? \n ------------- \n | 1   2   3 | \n | 4   5   6 | \n"))
        if not 0 < user_choice < 7:
            raise Exception
        opponent = random.randint(1, 100) + int(not first_taker)*5
        #opponent_save = 2

        if (goalkeeper and opponent >= keeper_stats_avg) and (not goalkeeper and opponent >= taker_stats_avg): 
            print(f"{phrases[1]}")
            return False
        else:
            print(f"{phrases[2]}")
            return True
    except: 
        print(f"You {phrases[3]}")


def take_penalty(taker_stats_avg, first_taker):
    '''
    DEFINITION
    '''
    try:
        user_choice = int(input("Where would you like to shoot? \n ------------- \n | 1   2   3 | \n | 4   5   6 | \n"))
        if not 0 < user_choice < 7:
            raise Exception
        opponent_shot = random.randint(1, 100) + int(not first_taker)*5 
        print(opponent_shot, taker_stats_avg)
        #opponent_shot = 1
        int(not first_taker)
        if opponent_shot >= taker_stats_avg: 
            print("Oh no! Penalty saved.")
            return False
        else: 
            print("Goal! The crowd goes wild.")
            return True
    except: 
        print("You stood between the wrong goalpoasts, bad luck.")

def save_penalty(keeper_stats_avg, first_taker):
    '''
    DEFINITION
    '''
    try:
        user_choice = int(input("Where would you like to dive? \n ------------- \n | 1   2   3 | \n | 4   5   6 | \n"))
        if not 0 < user_choice < 7:
            raise Exception
        opponent_shot = random.randint(1, 100) + int(not first_taker)*5 
        print(opponent_shot, keeper_stats_avg)
        #opponent_shot = 1
        int(not first_taker)
        if opponent_shot <= keeper_stats_avg: 
            print("Penalty saved! The crowd goes wild.")
            return True
        else: 
            print("Goal! Hang your head in shame.")
            return False
    except: 
        print("You stood between the wrong goalpoasts, bad luck.")


    
def check_score(user_score, opponent_score, shot_count):
        '''
        DEFINITION
        '''
        score_dif = abs(user_score-opponent_score)
        if shot_count // 2 == 3 and score_dif == 3: 
            return True
        elif shot_count // 2 == 4 and score_dif >= 2:
            return True
        elif shot_count // 2 >= 5 and score_dif >= 1 and shot_count % 2 == 0:
            return True

taker_stats = [{"Name": "Alvaro Morata", "Age": f"{age_calculator("23-10-1992")}", "Shot power": 55, "Accuracy": 48, "Composure": 27, "Special ability": None},
                {"Name": "Scott McTominay", "Age": f"{age_calculator("08-12-1996")}", "Shot power": 58, "Accuracy": 42, "Composure": 50, "Special ability": None},
                {"Name": "Bruno Fernandes", "Age": f"{age_calculator("08-09-1994")}", "Shot power": 60, "Accuracy": 56, "Composure": 64, "Special ability": "Hop penalty"},
                {"Name": "Andrea Pirlo", "Age": f"{age_calculator("19-05-1979")}", "Shot power": 46, "Accuracy": 75, "Composure": 90, "Special ability": "Panenka penalty"},
                {"Name": "Crisiano Ronaldo", "Age": f"{age_calculator("05-02-1985")}", "Shot power": 85, "Accuracy": 73, "Composure": 82, "Special ability": "Volley penalty"}]

keeper_stats = [{"Name": "Kepa Arrizabalaga", "Age": f"{age_calculator("03-10-1994")}", "Diving": 70, "Handling": 58, "Reflexes": 32, "Special ability": None},
                {"Name": "David Marshall", "Age": f"{age_calculator("05-03-1985")}", "Diving": 70, "Handling": 58, "Reflexes": 32, "Special ability": None},
                {"Name": "Unai Simon", "Age": f"{age_calculator("11-06-1997")}", "Diving": 70, "Handling": 58, "Reflexes": 32, "Special ability": "Early read"},
                {"Name": "Petr Cech", "Age": f"{age_calculator("20-05-1982")}", "Diving": 70, "Handling": 58, "Reflexes": 32, "Special ability": "Safe hands"},
                {"Name": "Iker Casillas", "Age": f"{age_calculator("20-05-1981")}", "Diving": 70, "Handling": 58, "Reflexes": 32, "Special ability": "Cat spring"}]

def penalty_shootout():
    '''
    DEFINITION
    '''

    # prompt user to select their penalty taker and goalkeeper
    user_taker = player_selection(taker_stats, 'penalty taker')
    user_keeper = player_selection(keeper_stats, 'goalkeeper')

    # initialise the score and perform the coin toss to decide who takes first
    user_score = 0
    opponent_score = 0
    shot_count = 0
    first_taker = coin_toss()

    taker_stats_avg = sum(list(user_taker.values())[2:5]) // 3
    keeper_stats_avg = sum(list(user_keeper.values())[2:5]) // 3
    list(user_taker.values())[5]

    while True: 

        # take first penalty if the player won the coin toss, 
        # if not skip this code once as the player is taking second    
        if (not first_taker and shot_count != 0) or first_taker: 
            #if penalty(keeper_stats_avg, taker_stats_avg, False, first_taker):    
            if take_penalty(taker_stats_avg, first_taker):
                user_score += 1

            shot_count += 1
            print(f'You {user_score} - {opponent_score} Opp')

            if check_score(user_score, opponent_score, shot_count):
                break
        
        #if penalty(keeper_stats_avg, taker_stats_avg, True, first_taker):
        if not save_penalty(keeper_stats_avg, first_taker):
            opponent_score += 1 

        shot_count += 1
        print(f'You {user_score} - {opponent_score} Opp')

        if check_score(user_score, opponent_score, shot_count):
            break
    
    # determine the winner of the shootout
    scores = [user_score, opponent_score]
    winner = scores.index(max(scores))

    if winner == 0: 
        return print("You win!!!")
    else:
        return print("You lose!!!")
    
penalty_shootout()