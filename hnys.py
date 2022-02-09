import os
from dotenv import load_dotenv
import discord
import random
import json
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button

load_dotenv()

# Oh boy, there's gonna be a lot of commented and leftover code.
# The original developers of this bot are much more competent than me.
# But hey, if it gets the job done.

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
EMOJI_CHECKMARK = "✅"
EMOJI_ENVELOPE = "✉️"
EMOJI_EYES = "👀"
EMOJI_DELETE = "❌"
EMOJI_MAIL = "📩" # Not confusing

# discord stuff
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

# VERIFIED_MESSAGE = (
#     "Your account has been verified and your access has been granted! Feel free to check "
#     "any of the verified channels now :-) "
# )
# FURTHER_VERIFICATION = (
#     "The mod team would like to ask a couple questions about your verification proof. "
#     "\nDon't worry! A mod will be with you soon.\n\nRemember, you can also dm the mods "
#     "with `$%s dm_mods` + the message you want to send! " % BOT_NAME
# )

# DOES_NOT_SATISFY = (
#     "Mods received your proof, but cannot verify you at this time. "
#     "REASON: *Please make sure you have accepted your offer __prior__ to verification and "
#     "that there is a checkmark for this on your new hire checklist.*"
# )

# DMing Bot
INITIAL_GREETING = """Hello! This is the discreet User-Mod communication bot for the NYU Discord.   

If you want to discuss something with the mods, such as advertising in the server or reporting a user,
please type `ticket [TOPIC]` here in this DM, where [TOPIC] is the subject of your message. I will
then create a private channel in the server for you to speak with the mods. If you type anything else,
I will send this message to you again!

The mod team wishes you the best and hopes you have a wonderful stay!"""

HELP_IS_ON_WAY = (
    "I've created a private channel in the NYU server for you to discuss your concerns with the mods. If I didn't, DM hnys because he programmed me poorly."
)

PROOF_RECEIVED = "Proof received. Mods will review it shortly :)"

COMMAND_HELP = (
    "Commands:  `$%s verify` to get verification instructions. `$%s dm_mods` to speak to a mod. You "
    "may choose to send a custom message to the mods by typing said message right after command "
    "`$%s dm_mods`. " % (BOT_NAME, BOT_NAME, BOT_NAME)
)

INVALID_COMMAND = "I'm sorry, I don't understand that command. All I know is beep boop, flowers, and `$%s ticket [TOPIC]`."

# Notifying mods about user
NOTIFICATION_VERIFY = (
    "<@%s> has asked for the above image to be used as proof of verification."
    "\n%s to approve the user"
    "\n%s to let them know you will be contacting them for further info"
    "\n%s if they have not yet accepted offer"
    "\n%s to delete message"
)

NOTIFICATION_HELP = (
    "User <@%s> has asked for a mod to contact them for further discussion.  "
)

BOT_JOKE_PHRASE = (
    "You'll have to pay for that. "
)

FLOWERS = ["🌸", "🌹", "🌺", "🌻", "🌼", "🌷"]


################################

def load_counters():
    with open('counter.json', 'r') as f: 
        counters = json.load(f)
    return counters


def save_counters(counters):
    with open('counter.json', 'w') as f:
        json.dump(counters, f)



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

@bot.command() # not really
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
    # interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "ticket")

# @client.event
# async def on_reaction_add(reaction, _user):
#     """
#     Help mods attribute "verified" role by simply clicking on a react button
#     :param _user: [unused param]
#     :param reaction: a reaction object to the message. Includes
#         - reaction.count , the amount of people having reacted with this emoji
#         - reaction.message , the message object within the reaction (see param of on_message for more info)
#             - reaction.message.mentions , helping us identify the user tagged in the message, if any
#     """
#     if (
#         reaction.count > 1
#         and reaction.message.mentions
#         and reaction.message.channel.id == MOD_CHANNEL_ID
#     ):
#         userino = reaction.message.mentions[0]
#         if str(reaction.emoji) == EMOJI_CHECKMARK:
#             role = discord.utils.get(reaction.message.guild.roles, name="verified")
#             await userino.add_roles(role)
#             await userino.send(VERIFIED_MESSAGE)
#             await reaction.message.delete()

#         elif str(reaction.emoji) == EMOJI_ENVELOPE:
#             await userino.send(FURTHER_VERIFICATION)

#         elif str(reaction.emoji) == EMOJI_EYES:
#             await userino.send(DOES_NOT_SATISFY)

#         elif str(reaction.emoji) == EMOJI_DELETE:
#             await reaction.message.delete()


@bot.event
async def on_message(message):
    """
    The core exchange between bot and a user
    :param message: the message object sent to the bot. Includes
        - message.channel
        - message.content (the string of a message)
        - message.attachments , a list of attachments such as a picture, a link, etc
        - message.author , the user object that sent the message
    """
    mod_channel = bot.get_channel(MOD_CHANNEL_ID)

    # if message.author == client.user:
    #     return
    # if message.content.startswith("$%s give me a flower" % BOT_NAME):  # little easter egg
    #     await message.channel.send(BOT_JOKE_PHRASE)
    # # This is how I sent the original message. Best practice, booyah
    # # if message.content.startswith("Flower Shop, I summon thee. Thoust willst dost myst biddingst sts tstst awawawawawa"):
        
    # elif isinstance(message.channel, discord.channel.DMChannel):
    #     if str(message.content).lower().startswith("ticket "):
    #         # send confirmation to user, then create a channel for the user to communicate with mods
    #         category = discord.utils.get(GUILD.categories, id=MOD_CATEGORY_ID)
    #         mod_role = discord.utils.get(GUILD.roles, id=MOD_ROLE_ID)
    #         print(category)
    #         print(mod_role)
    #         overwrites = {
    #             GUILD.default_role: discord.PermissionOverwrite(read_messages=False),
    #             GUILD.me: discord.PermissionOverwrite(read_messages=True),
    #             mod_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    #             message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    #         }
    #         print(overwrites)
    #         await message.channel.send(HELP_IS_ON_WAY)
    #         await GUILD.create_text_channel("flwr " +str(message.content)[7:], category=category, overwrites=overwrites)
    #     else:
    #         await message.channel.send(INITIAL_GREETING)
    # else:
    if  message.channel.name[0] in FLOWERS or message.channel.name.startswith("flwr"):
        if str(message.content).lower().startswith("$archive"):
            msgs = []
            attachment_counter = 0
            attachment_string = ''
            async for text in message.channel.history(limit=6969):
                if len(text.attachments) > 0:
                    for att in text.attachments:
                        attachment_counter += 1
                        attachment_string += '[Attachment-{}-{}]'.format(str(attachment_counter, att.filename))
                        await att.save(att.filename)
                        os.rename(att.filename, 'attachments/{}-{}'.format(attachment_counter, att.filename))
                msgs.append(str(text.author)+' ('+ str(text.created_at)+'): ' + str(text.content) + attachment_string + "\n")
            with open ("archive.txt", "w") as archive:
                for msg in reversed(msgs):
                    archive.write(msg)
            # messages = await message.channel.history(limit=6969).flatten() # Probs wont be that many messages, right??
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

        # send proof to mod channel, notify mods, and offer reaction options
        # if len(message.attachments) != 0:
        #     await message.channel.send(PROOF_RECEIVED)
        #     attachment = await message.attachments[0].to_file()
        #     last_message = await mod_channel.send(
        #         content=NOTIFICATION_VERIFY
        #         % (
        #             message.author.id,
        #             EMOJI_CHECKMARK,
        #             EMOJI_ENVELOPE,
        #             EMOJI_EYES,
        #             EMOJI_DELETE,
        #         ),
        #         file=attachment,
        #     )
        #     await last_message.add_reaction(EMOJI_CHECKMARK)
        #     await last_message.add_reaction(EMOJI_ENVELOPE)
        #     await last_message.add_reaction(EMOJI_EYES)
        #     await last_message.add_reaction(EMOJI_DELETE)

        # display info for user wanting to verify themselves or to message mods.
    #     elif str(message.content).lower().startswith("$%s verify" % BOT_NAME):
    #         await message.channel.send(INITIAL_GREETING)

    #     elif str(message.content).lower().startswith("$%s dm_mods" % BOT_NAME):
    #         await message.channel.send(HELP_IS_ON_WAY)
    #         await mod_channel.send(NOTIFICATION_HELP % message.author.id)
    #         if len(message.content.strip()) > len("$%s dm_mods") + 1:  
    #             # if user has attached an additional message
    #             await mod_channel.send(
    #                 'They also sent the following message: "%s"'
    #                 % message.content[len("$%s dm_mods" % BOT_NAME) + 1 :]
    #             )

    #     elif str(message.content).lower().startswith("$%s" % BOT_NAME) or not str(
    #         message.content
    #     ).lower().startswith("$%s" % BOT_NAME):
    #         if not str(message.content).lower().startswith("$%s" % BOT_NAME)
    #             or len(message.content) > len("$%s" % BOT_NAME) + 1:
    #             await message.channel.send(INVALID_COMMAND)
    #         await message.channel.send(COMMAND_HELP)

    # elif message.content.startswith(
    #     "$%s" % BOT_NAME
    # ):  # if users try to call it outside of DMs.
    #     await message.channel.send(
    #         "I do not [yet] respond to normal commands outside of DMs :("
    #     )


bot.run(TOKEN)
