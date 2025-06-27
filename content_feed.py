import discord

intents = discord.Intents.default()
intents.message_content = True

channels = []

client = discord.Client(intents = intents)

@client.event
async  def on_ready():
    print(f'We have logged in as {client.user}')




def save_channel(channel):
    f = open("feed_channels.txt", "a")
    f.write(str(channel.guild.id) + "," + str(channel.id) + "\n")
    f.close()

def save_channels():
    f = open("feed_channels.txt", "w")
    for channel in channels:
        f.write(str(channel.guild.id) + "," + str(channel.id) + "\n")
    f.close()

def load_channels():
    f = open("feed_channels.txt", "r")
    for line in f:
        a = line.split(",")
        guild_id = a[0]
        channel_id = a[1]
        channels.append(client.guilds)



client.run()