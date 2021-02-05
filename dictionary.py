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
        yn = yn.strip()
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
