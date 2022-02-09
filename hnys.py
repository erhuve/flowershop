import os
from dotenv import load_dotenv
import discord
import random
import json
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button

load_dotenv()

################################
description = "A bot for discreet communication between users and mods. Under development."
TOKEN = str(os.getenv("DISCORD_TOKEN"))
GUILD_ID = str(os.getenv("DISCORD_GUILD"))
MOD_CHANNEL_ID = int(os.getenv("MOD_CHANNEL_ID"))
MOD_ROLE_ID = int(os.getenv("MOD_ROLE_ID"))
MOD_CATEGORY_ID = int(os.getenv("MOD_CATEGORY_ID"))
TICKET_CHANNEL_ID = int(os.getenv("TICKET_CHANNEL_ID"))
GUILD = None


# EMOJIS🥶🥶🥶🥶
EMOJI_MAIL = "📩" 

# discord stuff, some unnecessary, oh well
client = discord.Client()
Embed = discord.Embed
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
bot = ComponentsBot(command_prefix = "!")

################################
# MESSAGES #

# Reactions to verify user
BOT_NAME = "Flower Shop"

# @deprecated
INITIAL_GREETING = """Hello! This is the discreet User-Mod communication bot for the NYU Discord.   

If you want to discuss something with the mods, such as advertising in the server or reporting a user,
please type `ticket [TOPIC]` here in this DM, where [TOPIC] is the subject of your message. I will
then create a private channel in the server for you to speak with the mods. If you type anything else,
I will send this message to you again!

The mod team wishes you the best and hopes you have a wonderful stay!"""

# @deprecated
HELP_IS_ON_WAY = (
    "I've created a private channel in the NYU server for you to discuss your concerns with the mods. If I didn't, DM hnys because he programmed me poorly."
)

BOT_JOKE_PHRASE = (
    "You'll have to pay for that. "
)

FLOWERS = ["🌸", "🌹", "🌺", "🌻", "🌼", "🌷"]


#######################################
# Helper functions for ticket counter #
#######################################

def load_counters():
    with open('counter.json', 'r') as f: 
        counters = json.load(f)
    return counters


def save_counters(counters):
    with open('counter.json', 'w') as f:
        json.dump(counters, f)

#######################################
# The Meat                            #
#######################################

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    global GUILD
    GUILD = bot.get_guild(int(GUILD_ID))

@bot.event
async def on_button_click(interaction):
    if interaction.component.id == "ticket":
        counters = load_counters()
        counters["tickets"] += 1
        save_counters(counters)
        ind = random.randrange(0, len(FLOWERS))
        prefix = FLOWERS[ind]
        category = discord.utils.get(GUILD.categories, id=MOD_CATEGORY_ID)
        mod_role = discord.utils.get(GUILD.roles, id=MOD_ROLE_ID)
        overwrites = {
            GUILD.default_role: discord.PermissionOverwrite(read_messages=False),
            GUILD.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            mod_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        with open('counter.json', 'r') as f:
            counters1 = json.load(f) # Open and load the file
        new_channel = await GUILD.create_text_channel(prefix + str(interaction.user) + "-" + str(counters1), category=category, overwrites=overwrites)
        await new_channel.send("{} Thank you for opening a ticket. {} will be here to help you shortly.".format(interaction.user.mention, mod_role.mention))
        await interaction.respond()

# To initialize, type !button in intended ticket channel (then delete your message or edit it into something informational)
@bot.command() 
async def button(ctx):
    if ctx.channel.id != TICKET_CHANNEL_ID:
        return
    buttons = [Button(label="%s Open a Ticket" % EMOJI_MAIL, id="ticket")]
    embed = Embed(
            title="Tickets", 
            description="If you'd like to open a ticket to discuss something with the mods, such as advertising in the server or reporting a user, please click the button below. Have a wonderful day!",
            color=discord.Color.blue()
            )
    await ctx.send(
        embed=embed, components=buttons
    )

@bot.event
async def on_message(message):
    """
    Method of closing and archiving tickets.
    Type $archive in the ticket channel to archive the ticket.
    Sends a log of the message history as a txt and includes attached files.
    """
    mod_channel = bot.get_channel(MOD_CHANNEL_ID)

    if  message.channel.name[0] in FLOWERS or message.channel.name.startswith("flwr"):
        if str(message.content).lower().startswith("$archive"):
            msgs = []
            attachment_counter = 0
            attachment_string = ''
            # Because there would never be a correspondence that long, right?
            async for text in message.channel.history(limit=6969):
                if len(text.attachments) > 0:
                    for att in text.attachments:
                        attachment_counter += 1
                        attachment_string += '[Attachment-{}-{}]'.format(str(attachment_counter), att.filename)
                        await att.save(att.filename)
                        os.rename(att.filename, 'attachments/{}-{}'.format(attachment_counter, att.filename))
                msgs.append(str(text.author)+' ('+ str(text.created_at)+'): ' + str(text.content) + attachment_string + "\n")
                attachment_string = ''
            with open ("archive.txt", "w") as archive:
                for msg in reversed(msgs):
                    archive.write(msg)
            files = []
            for file in os.listdir('attachments'):
                files.append(file)
            await mod_channel.send("Archiving channel: " + message.channel.name)
            await mod_channel.send(file=discord.File("archive.txt"))
            for file in files:
                if file == '.gitignore' or file == 'gitignore':
                    continue
                file_path = os.path.join('attachments', file)
                await mod_channel.send("Attachment {}".format(file), file=discord.File(file_path))
            await message.channel.delete()
            # Clean up our attachments folder so I don't pass some limits on Heroku
            for filename in os.listdir('attachments'):
                file_path = os.path.join('attachments', filename)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
    await bot.process_commands(message)

bot.run(TOKEN)
