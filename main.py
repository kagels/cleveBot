import json
from os.path import dirname, join
import discord
from discord.ext import commands
import re
from urllib import parse, request
import datetime
import logging
import requests
import requs

current_dir = dirname(__file__)
filePath = join(current_dir, "./config.json")
with open(filePath, 'r') as file:
    data = json.load(file)

## clientId = data.get('clientId')
## clientSecret = data.get('clientSecret')

token = data.get('token')

bot = commands.Bot(command_prefix='!', description="cleve bot ver 0.1")

@bot.command()
async def anime(ctx, *argv): ## gets anime url, parses args together in case of spaced name
    seriesName = ""
    for arg in argv:
        seriesName+=(arg + " ")
    seriesId = requs.getId("anime", seriesName)
    url = requs.getSeries("anime", seriesId)
    await ctx.send(url)

@bot.command()
async def manga(ctx, *argv): ## gets manga url, same shit as above
    seriesName = ""
    for arg in argv:
        seriesName+=(arg + " ")
    seriesId = requs.getId("manga", seriesName)
    url = requs.getSeries("manga", seriesId)
    await ctx.send(url)

@bot.command()
async def seasonal(ctx, year=None, season=None): ## defaults to current season with option to give year/season for historic urls
    if year is None:
        year = str(datetime.date.today().year)
    if season is None:
        month = int(datetime.date.today().month)
        if month in range(1,4):
            season = "winter"
        elif month in range(4,7):
            season = "spring"
        elif month in range(7,10):
            season = "summer"
        elif month in range(10,13): ## +1 added to range so it doesnt just stop at eg. 11
            season = "fall"
    url = requs.getSeason(year, season)
    await ctx.send(url)

@bot.command()
async def user(ctx, username): ## literally just get user url
   url = requs.getUser(username)
   await ctx.send(url)

@bot.command()
async def scores(ctx, username, score): ## gets specified scores from users animulist
    scores = requs.getUserScores(username, score)
    scoresString = "User {0} has given {1}s to: ".format(username, score)
    for x in range(len(scores)): ## add scores to a string along with some simple formatting
        if x != len(scores)-1:
            scoresString+=(scores[x] + ", ")
        else:
            scoresString+=(scores[x] + ".") 
    if not scores:
        scoresString+="fucking nothing." ## pretty self explanatory but this is all we add if the list is empty
    await ctx.send(scoresString)


bot.run(token)