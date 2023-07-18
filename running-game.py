import random
import requests

def generateCard():
    # Generating a random card ID.
    cardID = random.randint(1,151)

    # Calling the API
    pokemonURL = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(cardID)
    response = requests.get(pokemonURL)
    chosenPokemon = response.json()

    # There were multiple 'stats' keys, so we looped through until we found the hp stat.
    hp = 0
    for stat in chosenPokemon['stats']:
        if stat['stat']['name'] == 'hp':
            hp = stat['base_stat']
            break

    # Returning the stats as a dictionary.
    return {
        'id': chosenPokemon['id'],
        'name': chosenPokemon['name'],
        'weight': chosenPokemon['weight'],
        'height': chosenPokemon['height'],
        'base_experience': chosenPokemon['base_experience'],
        'hp': hp
    }

def gameScore(computerStat, userStat):
    userScore = 0
    computerScore = 0
    ties = 0
    roundWinner = ""

    if computerStat > userStat:
        computerScore+=1
        roundWinner = "computer"

    elif computerStat < userStat:
        userScore +=1
        roundWinner = "user"

    elif computerStat == userStat:
        ties +=1
        roundWinner = "tie"

    roundScore = {
        'user-score': userScore,
        'computer-score': computerScore,
        'ties': ties,
        'round-winner': roundWinner
    }

    return roundScore

def runningGame():
    numRounds = 10
    roundCount = 1

    userStat = 0;
    compStat = 0;

    validInput = False

    totalScore = {
        'computer':0,
        'user':0,
        'ties':0
    }

    while numRounds != 0:
        userCard = generateCard()
        compCard = generateCard()

        while userCard['id'] == compCard['id']:
            compCard = generateCard()

        weightString = f"Weight: {userCard['weight']}"
        baseXPString = f"Base XP: {userCard['base_experience']} "

        cardString = f"""--------------YOUR CARD--------------
Name: {userCard['name'].title()}

{weightString:<20}Height: {userCard['height']}
{baseXPString:<20}HP: {userCard['hp']}
-------------------------------------
        """
        print(f"\nROUND: {roundCount}")
        print(cardString)

        while validInput == False:
            statChoice = input("Would you like to choose Weight (w), Height (h), Base XP (b), or HP (hp)? ")

            if statChoice.lower().strip() == "w":
                userStat = userCard['weight']
                compStat = compCard['weight']
                break

            elif statChoice.lower().strip() == "h":
                userStat = userCard['height']
                compStat = compCard['height']
                break

            elif statChoice.lower().strip() == "b":
                userStat = userCard['base_experience']
                compStat = compCard['base_experience']
                break

            elif statChoice.lower().strip() == "hp":
                userStat = userCard['hp']
                compStat = compCard['hp']
                break

            else:
                print("Invalid input. Please try again.\n")

        roundScore = gameScore(compStat, userStat)

        totalScore['computer']= totalScore['computer'] + roundScore['computer-score']
        totalScore['user']= totalScore['user'] + roundScore['user-score']
        totalScore['ties']= totalScore['ties'] + roundScore['ties']

        if roundScore['round-winner'] == "computer":
            print(f"\nThe computer's stat was {compStat}. Your stat was {userStat}. The computer wins this round!")
        elif roundScore['round-winner'] == "user":
            print(f"\nThe computer's stat was {compStat}. Your stat was {userStat}. You win this round!")
        elif roundScore['round-winner'] == "tie":
            print(f"\nThe computer's stat was {compStat}. Your stat was {userStat}. This round is a tie.")

        print(f"\n---------- Computer: {totalScore['computer']} pts   User: {totalScore['user']} pts   Ties: {totalScore['ties']} ----------")

        if numRounds == 1:
            input("Please press enter to view the final results.\n\n")
        else:
            input("Please press enter to play the next round.\n\n")

        numRounds -= 1
        roundCount += 1

    print("\n\n-------------------------FINAL SCORE-------------------------\n")
    print(f"Computer: {totalScore['computer']} pts     User: {totalScore['user']} pts     Ties: {totalScore['ties']}")

    if totalScore['computer'] > totalScore['user']:
        print(f"The computer wins with {totalScore['computer']} points!")
    elif totalScore['computer'] < totalScore['user']:
        print(f"You win with {totalScore['user']} points!")
    elif totalScore['computer'] == totalScore['user']:
        print(f"Its a tie! You both scored {totalScore['user']} points!")

    print("\n------------------Thank you for playing!----------------------")

runningGame()