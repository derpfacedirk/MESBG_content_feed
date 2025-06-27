import discord
from discord import app_commands, DMChannel
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents = intents, command_prefix = "$")

channels = []
creator_whitelist = []

DISCORDKEY = ""
PASSWORD = ""




@client.event
async  def on_ready():
    load_whitelist()
    load_channels()
    synched = await client.tree.sync()
    print(len(synched))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type is discord.ChannelType.private:
        print("DM detected")
        if message.author in creator_whitelist:
            print("Author whitelisted")
            for channel in channels:
                await channel.send(message.content)
        else:
            await message.channel.send("You haven't registered. Please register useing /register before sending messages")

@client.tree.command()
@app_commands.dm_only()
@app_commands.describe(password= "whitelist password. Ask Silfin if not known")
async def register(interaction: discord.Interaction, password: str):
    if password == PASSWORD:
        creator_whitelist.append(interaction.user)
        await interaction.response.send_message("Password correct, you can now send messages to be added to the feed")
    else:
        await interaction.response.send_message("Password incorrect, you have not been registered. Please ask Silfin for password")




@client.tree.command()
@app_commands.guild_only
@app_commands.default_permissions(discord.Permissions(administrator = True))
async def start_feed(interaction: discord.Interaction) -> None:
    channels.append(interaction.channel)
    save_channel(interaction.channel)
    await interaction.response.send_message(content= "Starting MESBG content feed in this channel")

@client.tree.command()
@app_commands.guild_only
@app_commands.default_permissions(discord.Permissions(administrator = True))
async def stop_feed(interaction: discord.Interaction) -> None:
    channels.remove(interaction.channel)
    save_channels()
    await interaction.response.send_message("Stopping MESBG content feed in this channel")


def load_keys():
    global DISCORDKEY
    global PASSWORD
    f = open("KEYS.txt", "r")
    DISCORDKEY = f.readline().strip()
    PASSWORD = f.readline().strip()

def save_channel(channel):
    f = open("feed_channels.txt", "a")
    f.write(str(channel.id) + "\n")
    f.close()

def save_channels():
    f = open("feed_channels.txt", "w")
    for channel in channels:
        f.write(str(channel.id) + "\n")
    f.close()

def load_channels():
    try:
        f = open("feed_channels.txt", "r")
        for line in f:
            channel_id = int(line.strip())
            channel = client.get_channel(channel_id)
            if channel is None:
                continue
            channels.append(client.get_channel(channel_id))
        save_channels()
    except IOError:
        print("No channels file yet")

def save_whitelist():
    try:
        f = open("creator_whitelist.txt", "w")
        for creator in creator_whitelist:
            f.write(str(creator.id) + "\n")
        f.close()
    except IOError:
        print("no whitelist file yet")

def save_creator(creator):
    try:
        f=open("creator_whitelist.txt", "a")
        f.write(str(creator.id) + "\n")
        f.close()
    except IOError:
        print("no whitelist file yet")

def load_whitelist():
    try:
        f = open("creator_whitelist.txt", "r")
        for line in f:
            creator_whitelist.append(client.get_user(int(line.strip())))
        f.close()
    except IOError:
        print("no whitelist file yet")

load_keys()
client.run(DISCORDKEY)