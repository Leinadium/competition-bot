# WCACompetitionsBot (v2.4)

This is a script to get new competitions at worldcubeassociation.org website, and send new ones to all users
that subscribed via Reddit.

To subscribe, send a private message to u/WCACompetitionsBot with the title "Subscribe", and on the body message,
one of the following:

City, Country (Radius)  # I want all competitions within a radius of this city.    
City, Country  # I want all competitions in this city.    
Country  # I want all competitions in this country.    

To unsubscribe, send a private message to u/WCACompetitionsBot with the title "Unsubscribe", and anything on the body message.

## How it works:
There are two run python scripts. 

run_users.py will update all the users, checking for messages of u/WCACompetitionsBot,
and it updates the users.json file.

run_competitions.py will update all competitions, checking the website of wca, and then for all new competitions
it will send notifications for all users that wants that competitions

This github page doesn't have the users.json, competitions.json and credentials.json file, for security reasons.

## Modules required:
praw (to interact with reddit), geopy (to get coordinates of users and competitions), 
besides io, json, requests and datetime.

## Contact at:
u/Leinadium

