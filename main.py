import requests
import json
import pickle
import os.path
from os import path

amountcurrency = "12"
fromcurrency = "USD"
tocurrency = "EUR"

def listOptions(recent):

    #for listing the currency options

    url = "https://fixer-fixer-currency-v1.p.rapidapi.com/symbols"

    headers = {
        'x-rapidapi-host': "fixer-fixer-currency-v1.p.rapidapi.com",
        'x-rapidapi-key': "1e9450041cmsha0ac4c5e02010e6p112bdajsn5f54dc2f2090"
        }

    response = requests.request("GET", url, headers=headers)
    text = json.dumps(response.json())
    data = json.loads(text)

    z = 0

    #displaying the five recently used currency and creating a listing everything else after them

    print(', '.join(recent))
    noclubs = [x for x in data["symbols"] if x not in recent]

    #just formatting so it doesn't take up too much space

    for i in noclubs:
        z+=1
        print(i, end=' ')
        if z % 10 == 0:
            print()

def convert(amountcurrency, tocurrency, fromcurrency):

    # prep for the get request for the API

    url = "https://fixer-fixer-currency-v1.p.rapidapi.com/convert"

    querystring = {"amount":amountcurrency,"to":tocurrency,"from":fromcurrency}

    headers = {
        'x-rapidapi-host': "fixer-fixer-currency-v1.p.rapidapi.com",
        'x-rapidapi-key': "1e9450041cmsha0ac4c5e02010e6p112bdajsn5f54dc2f2090"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # saving the json data

    text = json.dumps(response.json())
    data = json.loads(text)
    dict = {1: amountcurrency, 2: fromcurrency, 3: data["result"], 4: tocurrency , 5: data["date"]}

    # printing the convert results for the user

    print("Your", amountcurrency, fromcurrency, "is equal to", data["result"], tocurrency,"on this date!", data["date"])
    save = []

    # handling the database using pickle (if the file exists open it and load the data from it and append the new data then dump it back in it)

    if os.path.isfile('history.pickle'):
        with open("history.pickle", "rb") as lst:
            save = pickle.load(lst)
            save.append(dict)

        with open("history.pickle", "wb") as lst:
            pickle.dump(save, lst)   
    else:
        with open("history.pickle", "wb") as lst:
            save.append(dict)
            pickle.dump(save, lst)

#function for searching in the pickled save file

def searchHistory():

    #if statement to check if a save file is present then if it is loading it

    if os.path.isfile('history.pickle'):
        with open("history.pickle", "rb") as save:
            display = pickle.load(save)
    else:
        return("No save files exist!")

    # more user communication to search

    print("Search by date or currency?\n")
    a = input()

    if a =="date":
    
        print("Which date would you like to search? (yyyy-mm-dd)\n")
        date = input()

        #actually searching the save

        print([d for d in display if d[5] == date], end='\n') 
    
    elif a =="currency":
    
        print("Which currency would you like to search? \n")
        currency = input().upper()

        #actually searching the save

        print([d for d in display if d[2] == currency], end='\n')
        
        print([d for d in display if d[4] == currency], end='\n') 

    else:
        
        print("Please type either \"date\" or \"currency\"!")
        


recent = []
while True:

    # kind of a main menu for the app

    print("What would you like to do? convert/historySearch/exit")
    userinput = input()
    if userinput == "exit":
        print("Thanks for using my currency converter! Bye!")
        break
    elif userinput == "historySearch":
        searchHistory()
        continue
    elif userinput == "convert":

        while True:

            # fishing for user input (while under the impression that the user knows what is a valid input)
            # and a bonus feature to exit the loop whenever

            print("""What currency do you have?
            Options:""")
            print()

            #calling the currency options lister

            listOptions(recent) 
            print("""
            
            """)
            answer = str(input())
            if answer == "exit":
                break
            else:

                #setting the variables and appending the choice of currency to the recent list 

                fromcurrency = answer.upper()
                if answer not in recent: recent.append(answer.upper())  
                if len(recent) > 5: del recent[0]

            print("What is the amount?")
            print()
            answer = str(input())
            if answer =="exit":
                break
            else:
                amountcurrency = answer

            print("""What currency would you like to get?
            Options:""")
            print()
            listOptions(recent)
            print("""
            
            """)
            answer = str(input())
            if answer =="exit":
                break
            else:
                tocurrency = answer.upper()
                if answer not in recent: recent.append(answer.upper())
                if len(recent) > 5: del recent[0]

            convert(amountcurrency, tocurrency, fromcurrency)
    else:
        print("Please use the accepted inputs. \"convert\" or \"searchHistory\" or \"exit\"!")

    