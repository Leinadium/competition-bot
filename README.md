# competition-bot
A python script for notifications via reddit of new WCA (World Cube Association) competitions, used in r/Cubers

## How it works:
There are two run python scripts. 

run_users.py will update all the users, checking for messages of u/WCACompetitionsBot,
and it updates the users.json file.

run_competitions.py will update all competitions, checking the website of wca, and then for all new competitions
it will send notifications for all users that wants that competitions

This script doesn't have the users.json, competitions.json and credentials.json file, for security reasons.

## Modules used:
praw, io, json, requests, beautifulsoup, datetime, geopy

