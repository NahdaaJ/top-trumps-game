import random
import requests
import datetime
import os
import config

SUPERHERO_API_KEY = config.SUPERHERO_API_KEY

def generateCard(gameTheme):
    if gameTheme == "Pokemon":
        # Generating a random card ID.
        cardID = random.randint(1, 151)

        # Calling the API
        pokemonURL = "https://pokeapi.co/api/v2/pokemon/{}/".format(cardID)
        response = requests.get(pokemonURL)
        chosenPokemon = response.json()

        # There were multiple 'stats' keys, so we looped through until we found the hp stat.
        hp = 0
        attack = 0
        defence = 0
        speed = 0

        for stat in chosenPokemon['stats']:
            if stat['stat']['name'] == 'hp':
                hp = stat['base_stat']
            if stat['stat']['name'] == 'attack':
                attack = stat['base_stat']
            if stat['stat']['name'] == 'defense':
                defence = stat['base_stat']
            if stat['stat']['name'] == 'speed':
                speed = stat['base_stat']


        # Returning the stats as a dictionary.
        return {
            'id': chosenPokemon['id'],
            'name': chosenPokemon['name'],
            'stat1': attack,
            'stat2': defence,
            'stat3': speed,
            'stat4': hp
        }
    elif gameTheme == "Superhero":
        isNull = True

        while (isNull):
            cardID = random.randint(1, 732)
            superheroURL = "https://superheroapi.com/api/{}/{}".format(SUPERHERO_API_KEY,cardID)
            response = requests.get(superheroURL)
            chosenHero = response.json()

            if chosenHero['name'] == "null" or chosenHero['powerstats']['intelligence'] == "null" or \
                    chosenHero['powerstats']['strength'] == "null" or chosenHero['powerstats']['speed'] == "null" or \
                    chosenHero['powerstats']['durability'] == "null":
                continue
            else:
                hero = {
                    'id': chosenHero['id'],
                    'name': chosenHero['name'],
                    'stat1': int(chosenHero['powerstats']['intelligence']),
                    'stat2': int(chosenHero['powerstats']['strength']),
                    'stat3': int(chosenHero['powerstats']['speed']),
                    'stat4': int(chosenHero['powerstats']['durability'])
                }
                return hero
    elif gameTheme == "Starships":
        isNull = True

        while (isNull):
            listID = [2, 3, 5, 10, 11, 12, 13, 17]
            randomID = random.choice(listID)

            starshipURL = "https://swapi.dev/api/starships/{}/".format(randomID)
            response = requests.get(starshipURL)
            chosenStarship = response.json()

            starship = {
                'id': randomID,
                'name': chosenStarship['name'].title(),
                'stat1': float(chosenStarship['length'].replace(',','')),
                'stat2': int(chosenStarship['max_atmosphering_speed'].replace('km','')),
                'stat3': float(chosenStarship['hyperdrive_rating']),
                'stat4': int(chosenStarship['cargo_capacity'])
            }
            return starship

def gameScore(computerStat, userStat):
    userScore = 0
    computerScore = 0
    ties = 0

    roundWinner = ""

    if computerStat > userStat:
        computerScore += 1
        roundWinner = "computer"

    elif computerStat < userStat:
        userScore += 1
        roundWinner = "user"

    elif computerStat == userStat:
        ties += 1
        roundWinner = "tie"

    roundScore = {
        'user-score': userScore,
        'computer-score': computerScore,
        'ties': ties,
        'round-winner': roundWinner
    }

    return roundScore

def recordGame(gameTheme, computerScore, userScore):
    currentDateTime = datetime.datetime.now()
    formattedDateTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
    fileName = "TopTrumpsRecord.txt"

    if computerScore > userScore:
        gameOutcome = "Loss"
    elif computerScore < userScore:
        gameOutcome = "Win"
    elif computerScore == userScore:
        gameOutcome = "Tie"


    if os.path.exists(fileName) == False:
        file = open(fileName, 'w')
        file.close()

    with open(fileName,'r') as file:
        toAppend = file.read()

    compScoreString = f"{computerScore} pts"
    userScoreString = f"{userScore} pts"

    with open(fileName,'w+') as file:
        newGame = f"{gameTheme:<20}{gameOutcome:<15}{userScoreString:<10}{compScoreString:<10}{formattedDateTime}\n"

        file.write(newGame)
        file.write(toAppend)

def viewGameHistory():
    fileName = "TopTrumpsRecord.txt"

    if os.path.exists(fileName) == False:
        print("\nYou have no previous games to view.")
        input("Please press enter to return to Main Menu.\n\n")
        return False

    with open(fileName, 'r') as file:
        gameHistory = file.read()

    return gameHistory

def gameMenu():
    gameTheme = ""
    roundNumbers = 0
    validInput = False;

    while validInput == False:
        userInput1 = input("""Welcome to Top Trumps! Would you like to:
1 - Play a new game.
2 - View previous games.
3 - Exit.
""")
        if userInput1 == "1":
            break
        elif userInput1 == "2":
            gameHistory = viewGameHistory()

            if gameHistory != False:
                print("\nGame Theme          Outcome        Player     CPU        Date       Time")
                print("-----------        ---------      --------  --------  ----------- ---------")
                print(gameHistory)
                print("---------------------------------------------------------------------------")
                input("Press enter to return to Main Menu.\n\n")
            continue
        elif userInput1 == "3":
            print("Thanks for playing!")
            return
        else:
            print("Please enter a valid input.\n")


    while validInput == False:
        userInput = input("""\n\nPlease choose a game theme:
1 - Pokemon
2 - Superheroes
3 - Starwars Starships\n""")

        if userInput == "1":
            gameTheme = "Pokemon"
            break

        elif userInput == "2":
            gameTheme = "Superhero"
            break

        elif userInput == "3":
            gameTheme = "Starships"
            break

        else:
            print("\nPlease enter a valid choice.\n")

    while validInput == False:
        userInput2 = input("\nHow many rounds would you like to play?\nMaximum number of rounds: 30\n")

        if userInput2.isdigit() and int(userInput2) > 0 and int(userInput2) <= 30:
            roundNumbers = int(userInput2)
            break
        else:
            print("\nPlease enter a valid number.\n")

    print(f"\nYou have chosen the game theme '{gameTheme}' with {roundNumbers} round(s)!")
    input("Please press enter to begin the game. ")

    runningGame(gameTheme, roundNumbers)

def runningGame(gameTheme, roundNumbers):
    roundCount = 1
    userStat = 0;
    compStat = 0;
    validInput = False
    numRounds = roundNumbers

    totalScore = {
        'computer':0,
        'user':0,
        'ties':0
    }

    while roundNumbers != 0:
        userCard = generateCard(gameTheme)
        compCard = generateCard(gameTheme)

        while userCard['id'] == compCard['id']:
            compCard = generateCard(gameTheme)

        print(f"\n\n\nROUND: {roundCount}")

        if gameTheme == "Pokemon":
            nameString = f"Name: {userCard['name'].title()}"
            attackString = f"Attack: {userCard['stat1']}"
            defenceString = f"Defence: {userCard['stat2']}"
            speedString = f"Speed: {userCard['stat3']}"
            hpString = f"HP: {userCard['stat4']}"

            cardString = f"""--------------YOUR CARD--------------
Name: {userCard['name'].title()}

{attackString:<20}{defenceString}
{speedString:<20}{hpString}
-------------------------------------
"""
            compAttack = f"Attack: {compCard['stat1']}"
            compDefence = f"Defence: {compCard['stat2']}"
            compSpeed = f"Speed: {compCard['stat3']}"
            compHP = f"HP: {compCard['stat4']}"

            comparisonCardString = f"""\n\n--------------YOUR CARD--------------          --------------CPU CARD--------------
{nameString:<48}Name: {compCard['name'].title()}

{attackString:<20}{defenceString:<28}{compAttack:<20}{compDefence}
{speedString:<20}{hpString:<28}{compSpeed:<20}{compHP}
-------------------------------------          ------------------------------------"""
            print(cardString)

            while validInput == False:
                statChoice = input("Would you like to choose Attack (a), Defence (d), Speed (s), or HP (h)? ")

                if statChoice.lower().strip() == "a":
                    userStat = userCard['stat1']
                    compStat = compCard['stat1']
                    break

                elif statChoice.lower().strip() == "d":
                    userStat = userCard['stat2']
                    compStat = compCard['stat2']
                    break

                elif statChoice.lower().strip() == "s":
                    userStat = userCard['stat3']
                    compStat = compCard['stat3']
                    break

                elif statChoice.lower().strip() == "h":
                    userStat = userCard['stat4']
                    compStat = compCard['stat4']
                    break

                else:
                    print("Invalid input. Please try again.\n")

            roundScore = gameScore(compStat, userStat)


        elif gameTheme == "Superhero":
            nameString = f"Name: {userCard['name'].title()}"
            intelligenceString = f"Intelligence: {userCard['stat1']}"
            strengthString = f"Strength: {userCard['stat2']}"
            speedString = f"Speed: {userCard['stat3']}"
            durabilityString = f"Durability: {userCard['stat4']}"


            cardString = f"""--------------YOUR CARD--------------
Name: {userCard['name'].title()}

{intelligenceString:<20}{strengthString}
{speedString:<20}{durabilityString}
-------------------------------------"""

            compIntelligenceString = f"Intelligence: {compCard['stat1']}"
            compStrengthString = f"Strength: {compCard['stat2']}"
            compSpeedString = f"Speed: {compCard['stat3']}"
            compDurabilityString = f"Durability: {compCard['stat4']}"

            comparisonCardString = f"""\n\n--------------YOUR CARD--------------          --------------CPU CARD--------------
{nameString:<48}Name: {compCard['name'].title()}

{intelligenceString:<20}{strengthString:<28}{compIntelligenceString:<20}{compStrengthString}
{speedString:<20}{durabilityString:<28}{compSpeedString:<20}{compDurabilityString}
-------------------------------------          ------------------------------------"""
            print(cardString)

            while validInput == False:
                statChoice = input("Would you like to choose Intelligence (i), Strength (s), Speed (sp), or Durability (d)? ")

                if statChoice.lower().strip() == "i":
                    userStat = userCard['stat1']
                    compStat = compCard['stat1']
                    break

                elif statChoice.lower().strip() == "s":
                    userStat = userCard['stat2']
                    compStat = compCard['stat2']
                    break

                elif statChoice.lower().strip() == "sp":
                    userStat = userCard['stat3']
                    compStat = compCard['stat3']
                    break

                elif statChoice.lower().strip() == "d":
                    userStat = userCard['stat4']
                    compStat = compCard['stat4']
                    break

                else:
                    print("\nInvalid input. Please try again.\n")

            roundScore = gameScore(compStat, userStat)


        elif gameTheme == "Starships":
            nameString = f"Name: {userCard['name'].title()}"
            lengthString = f"Length: {userCard['stat1']}"
            speedString = f"Max Speed: {userCard['stat2']}"
            hdString = f"Hyper-Drive Rating: {userCard['stat3']} "
            cargoString = f"Cargo Capacity: {userCard['stat4']}"

            cardString = f"""-----------------------YOUR CARD-----------------------
Name: {userCard['name'].title()}

{lengthString:<30}{speedString}
{hdString:<30}{cargoString}
-------------------------------------------------------"""

            compLengthString = f"Length: {compCard['stat1']}"
            compSpeedString = f"Max Speed: {compCard['stat2']}"
            compHDString = f"Hyper-Drive Rating: {compCard['stat3']} "
            compCargoString = f"Cargo Capacity: {compCard['stat4']}"

            comparisonCardString = f"""\n\n----------------------YOUR CARD----------------------          -------------------------CPU CARD-------------------------
{nameString:<65}Name: {compCard['name'].title()}

{lengthString:<30}{speedString:<35}{compLengthString:<30}{compSpeedString}
{hdString:<30}{cargoString:<35}{compHDString:<30}{compCargoString}
-----------------------------------------------------          ----------------------------------------------------------"""

            print(cardString)

            while validInput == False:
                statChoice = input(
                    "Would you like to choose Length (l), Max Speed (s), Hyper-Drive Rating (h), or Cargo Capacity (c)? ")

                if statChoice.lower().strip() == "l":
                    userStat = userCard['stat1']
                    compStat = compCard['stat1']
                    break

                elif statChoice.lower().strip() == "s":
                    userStat = userCard['stat2']
                    compStat = compCard['stat2']
                    break

                elif statChoice.lower().strip() == "h":
                    userStat = userCard['stat3']
                    compStat = compCard['stat3']
                    break

                elif statChoice.lower().strip() == "c":
                    userStat = userCard['stat4']
                    compStat = compCard['stat4']
                    break

                else:
                    print("\nInvalid input. Please try again.\n")

            roundScore = gameScore(compStat, userStat)


        totalScore['computer']= totalScore['computer'] + roundScore['computer-score']
        totalScore['user']= totalScore['user'] + roundScore['user-score']
        totalScore['ties']= totalScore['ties'] + roundScore['ties']

        print(comparisonCardString)

        if roundScore['round-winner'] == "computer":
            print(f"\nThe computer's stat was {compStat}. Your stat was {userStat}. The computer wins this round!")
        elif roundScore['round-winner'] == "user":
            print(f"\nThe computer's stat was {compStat}. Your stat was {userStat}. You win this round!")
        elif roundScore['round-winner'] == "tie":
            print(f"\nThe computer's stat was {compStat}. Your stat was {userStat}. This round is a tie.")

        print(f"\n---------- Computer: {totalScore['computer']} pts   User: {totalScore['user']} pts   Ties: {totalScore['ties']} ----------")

        if roundNumbers == 1:
            input("Please press enter to view the final results.\n\n")
        else:
            input("Please press enter to play the next round.\n\n")

        roundNumbers -= 1
        roundCount += 1

    print("\n\n-------------------------FINAL SCORE-------------------------\n")
    print(f"Computer: {totalScore['computer']} pts     User: {totalScore['user']} pts     Ties: {totalScore['ties']}")

    if totalScore['computer'] > totalScore['user']:
        print(f"The computer wins with {totalScore['computer']} point(s)!")
    elif totalScore['computer'] < totalScore['user']:
        print(f"You win with {totalScore['user']} point(s)!")
    elif totalScore['computer'] == totalScore['user']:
        print(f"Its a tie! You both scored {totalScore['user']} point(s)!")

    print("\n------------------Thank you for playing!----------------------")
    recordGame(gameTheme, totalScore['computer'], totalScore['user'])

    input("Press enter to return to the Main Menu.\n\n")
    gameMenu()

gameMenu()