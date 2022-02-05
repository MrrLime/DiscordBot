# this is a python file
import discord, json, urllib, asyncio, random
from discord.ext import commands
from urllib import request
from datetime import datetime as dt
from keep_alive import keep_alive as ka
from functions import taint

colours = {"Black": 0x000000, "Blue": 0x0000FF, "Brown": 0x800000, "Cyan": 0x00FFFF, "Gray": 0x808080,
           "Green": 0x008000, "Lime": 0x00FF00, "Magenta": 0xFF00FF, "Navy": 0x000080, "Orange": 0xFF6600,
           "Purple": 0x800080, "Red": 0xFF0000, "Silver": 0xC0C0C0, "White": 0xFFFFFF, "Yellow": 0xFFFF00}

api = {"api_raw_dis": "https://api.corona-zahlen.org/districts", "api_raw_sta": "https://api.corona-zahlen.org/states",
       "api_raw_ger": "https://api.corona-zahlen.org/germany"}

date_today = dt.today().strftime('%d-%m-%y')

prefix = "m." 
#prefix = input("[+]prefix: ")

VIPs = ["awa", "bot", "emil"]

insult_list = []
insult_path = "Insults.txt"
# insult_lists = []
# insult_lists.append(("[~] Input listpath: "))


bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("ready")
    bot.loop.create_task(status_task())


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(f"{prefix}help"), status=discord.Status.online)

@bot.command(name="help")
async def help(ctx):
  embed = discord.Embed(title="Help",url="https://BotCollection.rexy27t.repl.co", description="All commands and their usage", color=colours.get("Green"))
  embed.add_field(name=f"➤ **{prefix}** (prefix)", value="used before every command, Basti", inline=False)
  embed.add_field(name="➤ **corona** (command)", value="is able to show the incidences of each state in germany(send msp afterwards for msp incidence)", inline=False)
  embed.add_field(name="➤ **insult** (command)", value="is able to insult the person you wish to insult with a variety of isults", inline=False)
  await ctx.send(embed=embed, delete_after=60)
  await ctx.message.delete()


@bot.command(name="corona")
async def corona(ctx):
    def check(m):
        return m.author == ctx.author

    states = {'Berlin': 'BE', 'Bayern': 'BY', 'Niedersachsen': 'NI', 'Baden-Württemberg': 'BW',
              'Rheinland-Pfalz': 'RP', 'Sachsen': 'SN', 'Thüringen': 'TH', 'Hessen': 'HE', 'Nordrhein-Westfalen': 'NW',
              'Sachsen-Anhalt': 'ST', 'Brandenburg': 'BB', 'Mecklenburg-Vorpommern': 'MV', 'Hamburg': 'HH',
              'Schleswig-Holstein': 'SH', 'Saarland': 'SL', 'Bremen': 'HB'}
    with request.urlopen(api.get("api_raw_ger")) as api_fetched:
      inz_ger = str(round(json.loads(api_fetched.read())['weekIncidence']))
    colour = taint.colour(inz_ger, colours)
    embed = discord.Embed(title="Corona", url="https://github.com/MrrLime/DiscordBot", description="**Inzidenz**", color=colour)
    embed.add_field(name=f"➤ ***Deutschland***", value=f"   • {inz_ger}", inline=False)
    for key in states:
      with request.urlopen(api.get("api_raw_sta")) as api_fetched:
        value = str(round(json.loads(api_fetched.read())['data'][states[key]]['weekIncidence']))
      embed.add_field(name=f"➤ **{key}**", value=f"   • {value}", inline=False)
    embed.set_footer(text="®by MrrLime")
    await ctx.send(embed=embed, delete_after=60)
    await ctx.message.delete()
    try:
      message = await bot.wait_for("message", check=check, timeout=20)
      message_id = message.id
    except TimeoutError:
        await ctx.send(":Timeout:", delete_after=5)
    else:
      if "msp" in message.content.lower():
        with request.urlopen(api.get("api_raw_dis")) as api_fetched:
          inz_msp = str(round(json.loads(api_fetched.read())["data"]["09677"]["weekIncidence"]))
        await ctx.send(f"➤ Inzidenz Main-Spessart: **{inz_msp}**", delete_after=60)
      msg = await ctx.fetch_message(message_id)
      await msg.delete()

@bot.command(name="insult")
async def on_message(ctx):
    count = 1
    with open(insult_path, "r") as file:
        index = random.randint(0, 189)
        for line in file.readlines():
            insult_list.append(line.strip("\n"))

    def check(m):
        return m.author == ctx.author
    
    bot_message = await ctx.send("What's your name?", delete_after=10)
    message_id_bot = bot_message.id
    msg_bot = await ctx.fetch_message(message_id_bot)
    await msg_bot.delete()
    try:
        message = await bot.wait_for("message", check=check, timeout=10)
        message_id = message.id
        msg = await ctx.fetch_message(message_id)
        await msg.delete()
    except TimeoutError:
        await ctx.send(":Timeout:", delete_after=5)
    else:
      await ctx.message.delete()
      for word in VIPs:
        if word in message.content.lower():
          count = 0
      if count == 0:
        await ctx.send(f"{ctx.author} sucks!", delete_after=20)
      if count == 1:
        await ctx.send(f"{message.content}, {insult_list[index].lower()}", delete_after=20)
      
      


ka()

bot.run("")
