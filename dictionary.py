# Method 1: Json
# In this json document, words are case-sensitive. For example, you cannot get the definition of America when you input "america". 
# So I consider different occasions in order to get the correct result.

import json
from difflib import get_close_matches

data = json.load(open("data.json"))

def translate(w):
    w = w.lower()
    if w in data:
        return data[w]
    elif w.upper() in data:
        return data[w.upper()]
    elif w.title() in data:
        return data[w.title()]
    # the word that user input is not in the dictionary, check if there's a similar word
    elif len(get_close_matches(w,data.keys())) > 0:
        # get the most similar word
        similar_w = get_close_matches(w,data.keys())[0]
        # ask user if he wants the definition of the similar word
        yn = input(f"Do you mean {similar_w} instead? Enter Y if yes, enter N if no: ")
        yn = yn.upper().strip()
        while yn != "Y" and yn != "N":
            yn = input("Please enter a valid letter(Y/N): ")
        if yn == "Y":
            return data[similar_w]
        elif yn == "N":
            return "The word doesn't exist. Please double check it."
    else:
        return "The word doesn't exist. Please double check it."

while True:
    word = input("Please enter a word (press '\exit' to exit): ")
    if word == "\exit":
        break

    output = translate(word)  # the result is stored in a list (one word might have more than one definition)
    # if the input is available, print the definition line by line
    if isinstance(output,list):
        for line in output:
            print(line)
    else:
        print(output)


        
# Method 2: mysql.connetor
# Unlike previous example, words are not case-sensitive in the database.
# So, there's no need to lower/upper/title user's input. We just jump to look for similar words.

import mysql.connector
from difflib import get_close_matches

con = mysql.connector.connect(
    user = "ardit700_student",
    password = "ardit700_student",
    host = "108.167.140.122",
    database = "ardit700_pm1database"
)

cursor = con.cursor()

def translate(w):
    # The table we use is called "Dictionary".The results is: [(expression,definition),...]
    query = cursor.execute(f"SELECT * FROM Dictionary WHERE Expression = '{w}'")
    results = cursor.fetchall()

    if results:
        # store only the definition elements
        results = [result[1] for result in results]
        return results
    else:
        # get all expressions
        query = cursor.execute("SELECT Expression FROM Dictionary")
        total_ws = cursor.fetchall()
        # the formation is [(definition,),...], exert the first element
        total_ws = [total_w[0] for total_w in total_ws]

        if len(get_close_matches(w,total_ws)) > 0:
            similar_w = get_close_matches(w,total_ws)[0]
            yn = input(f"Do you mean {similar_w} instead? Enter Y if yes, enter N if no: ")
            yn = yn.upper().strip()
            while yn != "Y" and yn != "N":
                yn = input("Pleae input a valid letter: ")
                yn = yn.upper().strip()
            if yn == "Y":
                return translate(similar_w)
            else:
                return "The word doesn't exist."

while True:
    word = input("Please enter a word(press '\exit' to exit): ")
    if word == '\exit':
        break

    output = translate(word)
    if isinstance(output,list):
        for line in output:
            print(line)
    else:
        print(output)


