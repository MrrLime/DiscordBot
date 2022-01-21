# this is a python file
import discord, json, urllib, asyncio, random
from discord.ext import commands
from urllib import request
from datetime import datetime as dt
from keep_alive import keep_alive as ka

colours = {"Black": 0x000000, "Blue": 0x0000FF, "Brown": 0x800000, "Cyan": 0x00FFFF, "Gray": 0x808080,
           "Green": 0x008000, "Lime": 0x00FF00, "Magenta": 0xFF00FF, "Navy": 0x000080, "Orange": 0xFF6600,
           "Purple": 0x800080, "Red": 0xFF0000, "Silver": 0xC0C0C0, "White": 0xFFFFFF, "Yellow": 0xFFFF00}

api = {"api_raw_dis": "https://api.corona-zahlen.org/districts", "api_raw_sta": "https://api.corona-zahlen.org/states",
       "api_raw_ger": "https://api.corona-zahlen.org/germany"}

date_today = dt.today().strftime('%d-%m-%y')

prefix = input("[+]prefix: ")

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
  embed = discord.Embed(title="Help",url="https://github.com/MrrLime/DiscordBot", description="All commands and their usage", color=colours.get("Green"))
  embed.add_field(name="➤ **corona** ", value="is able to show the incidences of each state in germany", inline=False)
  embed.add_field(name="➤ **insult** ", value="is able to insult the person you wish to insult with a variety of isults", inline=False)
  await ctx.send(embed=embed)

@bot.command(name="corona")
async def corona(ctx):
    def check(m):
        return m.author == ctx.author

    states = {'Berlin': 'BE', 'Bayern': 'BY', 'Niedersachsen': 'NI', 'Baden-Württemberg': 'BW',
              'Rheinland-Pfalz': 'RP', 'Sachsen': 'SN', 'Thüringen': 'TH', 'Hessen': 'HE', 'Nordrhein-Westfalen': 'NW',
              'Sachsen-Anhalt': 'ST', 'Brandenburg': 'BB', 'Mecklenburg-Vorpommern': 'MV', 'Hamburg': 'HH',
              'Schleswig-Holstein': 'SH', 'Saarland': 'SL', 'Bremen': 'HB'}

    value = '➤ Berlin\n ➤ Bayern\n ➤ Niedersachsen\n ➤ Baden-Württemberg\n ➤ Rheinland-Pfalz\n ➤ Sachsen\n ➤ Thüringen\n ➤ Hessen\n ➤ Nordrhein-Westfalen\n ➤ Sachsen-Anhalt\n ➤ Brandenburg\n ➤ Mecklenburg-Vorpommern\n ➤ Hamburg\n ➤ Schleswig-Holstein\n ➤ Saarland\n ➤ Bremen'

    with urllib.request.urlopen(api.get("api_raw_ger")) as api_fetched:
        inz_ger = str(round(json.loads(api_fetched.read())['weekIncidence']))
    colour = colours.get("Magenta")
    if int(inz_ger) < 50:
      colour = colours.get("Lime")
    elif int(inz_ger) in range(50,200):
      colour = colours.get("Green")
    elif int(inz_ger) in range(200,400):
      colour = colours.get("Yellow")
    elif int(inz_ger) in range(400,600):
      colour = colours.get("Orange")
    elif int(inz_ger) in range(600, 800):
       colour = colours.get("Red")
    elif int(inz_ger) > 800:
      colour = colours.get("Black")

    embed = discord.Embed(title="corona", url="https://github.com/MrrLime/DiscordBot",
                          description=" Alle 16 Bundesländer und deren Rechtschreibung.", color=colours.get("Cyan"))

    embed.add_field(name="  Bitte gib das gewünschte Bundesland ein.", value=value, inline=False)
    embed.set_footer(text="®by MrrLime")
    await ctx.send(embed=embed)
    try:
        message = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.send(":Timeout:")
    else:
        state_short = states.get(message.content)
        with urllib.request.urlopen(api.get("api_raw_sta")) as api_fetched:
            inz_sta = str(round(json.loads(api_fetched.read())['data'][state_short]['weekIncidence']))
        if state_short == "BY":
            with request.urlopen(api.get("api_raw_dis")) as api_fetched:
                inz_dis = str(round(json.loads(api_fetched.read())['data']['09677']['weekIncidence']))
        state_short = states.get(message.content)
        embed = discord.Embed(title="Inzidenzen", url="https://github.com/MrrLime/DiscordBot",
                              description="Inzidenzen für ganz Deutschland", color=colour)
        embed.add_field(name="➤ Inzidenz Deutschland: ", value=f"• {inz_ger}", inline=False)
        embed.add_field(name=f"➤ Inzidenz {message.content}: ", value=f"• {inz_sta}", inline=False)
        if state_short == "BY":
            embed.add_field(name="➤ Inzidenz Main-Spessart:", value=f"• {inz_dis}", inline=False)
        embed.set_footer(text="®by MrrLime")
        await ctx.send(embed=embed)


@bot.command(name="insult")
async def on_message(ctx):
    with open(insult_path, "r") as file:
        index = random.randint(0, 189)
        for line in file.readlines():
            insult_list.append(line.strip("\n"))

    def check(m):
        return m.author == ctx.author

    await ctx.send("Wie heist du?")
    try:
        message = await bot.wait_for("message", check=check, timeout=20)
    except TimeoutError:
        await ctx.send(":Timeout:")
    else:
        await ctx.send(f"{message.content}, {insult_list[index].lower()}")


ka()

bot.run("")
