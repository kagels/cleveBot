import datetime
import logging
import requests
import json
from jsonpath_ng import jsonpath, parse
from os.path import dirname, join


def getId(searchType, name):
    parser = parse('$.results[0].mal_id')
    url = "https://api.jikan.moe/v3/search/{0}?q={1}".format(searchType, name)
    resp = requests.get(url)
    respJson = resp.json()
    seriesId = parser.find(respJson)
    return seriesId[0].value

def getSeries(searchType, id):
    url = "https://api.jikan.moe/v3/{0}/{1}".format(searchType, id)
    resp = requests.get(url)
    respJson = resp.json()
    return respJson['url']

def getSeason(year, season):
    url = "https://myanimelist.net/anime/season/{0}/{1}".format(year, season) ## very fuking simple atm
    return url

def getUser(username):
    url = "https://api.jikan.moe/v3/user/{0}".format(username)
    resp = requests.get(url)
    respJson = resp.json()
    try:
        return respJson['url']
    except KeyError:
        return("Username not found, check your spelling and try again.")

def getUserScores(username, score):
    url = "https://api.jikan.moe/v3/user/{0}/animelist/all".format(username)
    resp = requests.get(url)
    respJson = resp.json()
    scoreList = []
    try:
        for item in respJson['anime']:
            if item['score'] == int(score):
                scoreList.append(item['title'])
        return scoreList
    except KeyError:
        return None
