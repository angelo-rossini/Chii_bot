import os
import discord
import random
import socket
import wikipedia
import requests
from pytrends.request import TrendReq
from discord.ext import commands
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter

bot = commands.Bot('!')

@bot.event
async def on_ready():
    print('bom dia')

@bot.command(name='oi')
async def send_hi(ctx):
  await ctx.send('oii, espero que esteja bem')

@bot.command(name='manga')
async def Manga(ctx):
  await ctx.send('qual obra deseja procurar?')
  obra = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
  obra = str(obra.content)
  obra = obra.split()

  if obra[0] == 'chobits':
    link = ('https://mangalivre.net/manga/chobits/4954')
    await ctx.send(link)
  else:
    link = ('https://mangayabu.top/manga/')
    n = len(obra)
    for i in range (n):
      link = (link + obra[i] + '-')
    await ctx.send(link[:-1])

@bot.command(name='webtoon')
async def Webtoon(ctx):
  await ctx.send('qual obra deseja procurar?')
  obra = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
  obra = str(obra.content)
  obra = obra.split()
  link = ('https://yabutoons.com/webtoon/')
  n = len(obra)
  for i in range (n):
    link = (link + obra[i] + '-')
  await ctx.send(link[:-1])

@bot.command(name='pesquisa')
async def check_on_wikipedia(ctx):
  
  await ctx.send('qual a sua duvida?')
  query = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
  query = str(query.content)
  try:
    query = query.lower()
    query = query.replace("quem foi", "")
    query = query.replace("quem é", "")
    query = query.replace("o que é", "")
    query = query.replace("você sabe o que é", "")
    query = query.replace("me diga o que é", "")
    wikipedia.set_lang("pt")
    resumo = wikipedia.summary(query, sentences=3)
    await ctx.send(resumo)
  except:
    await ctx.send("desculpa, mas não foi possivel encontrar sobre ", query)

@bot.command(name='gato')
async def cat_fact(ctx):
  try:
    requisicao_gato = requests.get('https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=2').json()
    await ctx.send(requisicao_gato[1]['text'])
  except:
    await ctx.send("a api está com excesso de requisições no momento, peço desculpas por isso, tente mais tarde")

@bot.command(name='cachorro')
async def dog_fact(ctx):
  try:
    requisicao_cachorro = requests.get('https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1')
    curiosidade = requisicao_cachorro.json()
    await ctx.send(curiosidade[0]['fact'])
  except:
    await ctx.send("a api está com excesso de requisições no momento, peço desculpas por isso, tente mais tarde")

@bot.command(name='tendencia')
async def tendencia(ctx):
  pytrends = TrendReq(hl='en-US', tz=360)
  data = pytrends.trending_searches(pn='brazil')
  await ctx.send(data)

@bot.command(name='anime')
async def anime(ctx):
  try:
     computer_choice = random.randint(1, 9000)
     computer_url = 'https://api.jikan.moe/v3/anime/{}/'.format(computer_choice)
     computer_response = requests.get(computer_url)
     a = computer_response.json()['title']
     await ctx.send(a)
  except:
    await ctx.send("a api está com excesso de requisições no momento, peço desculpas por isso, tente mais tarde")

@bot.command(name='cotação')
async def moedas(ctx):
  try:
    await ctx.send("insira o código da moeda que deseja ver a conversão")
    moeda = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    moeda = str(moeda.content)
    if (moeda == 'BTC'):
      b = BtcConverter()
      b = b.get_latest_price('BRL')
      await ctx.send ('R$ {:.3}'.format(b))
    else:
      c = CurrencyRates()
      await ctx.send ('R$ {:.3}'.format(c.convert(moeda, 'BRL', 1)))
  except(KeyError):
    await ctx.send("chii:código inserido não é invalido, tente de novo")
  except:
    await ctx.send("a api atingiu o limite de requisições, por favor tente novamente quando renovar as requisições")

@bot.command(name='dado')
async def dado(ctx):
  await ctx.send("insira o numero maximo que se pode tirar no dado")
  n = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
  n = int(str(n.content))
  dado = random.randint(1, n)
  await ctx.send("que a sorte esteja com você")
  await ctx.send("o numero sorteado foi {}".format(dado))

bot.run(os.environ['TOKEN'])
