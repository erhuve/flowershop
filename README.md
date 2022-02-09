# FLOWER SHOP: A Ticketing Bot for the NYUDiscord
![image](https://user-images.githubusercontent.com/59463268/152920000-be5430f7-cdd2-4694-905a-cc2ee0e686ee.png)
![image](https://user-images.githubusercontent.com/59463268/152920027-a400e19c-f82b-46c9-b52c-5b3aea095138.png)
Originally a fork of Zuckerbot, but ended up being a completely different bot!

Regardless, it was a great way to boostrap the project, kudos and thanks to my friends who developed it.

The guys who put that together are far more talented than me, check them out!


I made this for the NYU Discord server to let users open tickets with the mods without needing to broadcast it in a public bot command channel. 

Flower Shop creates a user-friendly experience with a single button users click to create a private channel with them and the moderators. 

For moderators, once they close a ticket, the log is saved, including any attached files such as images.
## Commands
* `!button`: Initializes the message with the button for users to click. You can delete your message with this command afterwards, or edit it to provide information to your users about the ticketing system.
* `$archive`: To be used by moderators in a created ticket channel when done. This will delete the channel and save a log of the messages and any attachments (this will be saved in a separate channel you have created to keep logs)
## Setup
You can set up this application for your own bot and your own server. Locally, you will need to replace these values in your `.env` file, or in Heroku, the `Config Vars` which can be found in `Settings` of your application.
* DISCORD_TOKEN="`YOUR DISCORD BOT'S TOKEN`"
* DISCORD_GUILD="`THE ID OF YOUR SERVER`"
* MOD_CHANNEL_ID="`THE ID OF THE CHANNEL YOU WILL STORE LOGS IN`"
* MOD_ROLE_ID="`THE ID OF THE MODERATOR ROLE IN YOUR SERVER`"
* MOD_CATEGORY_ID="`THE ID OF THE CATEGORY THAT WILL HOUSE TICKETS`"
* TICKET_CHANNEL_ID="`THE ID OF THE CHANNEL THAT YOU WILL INITIALIZE FLOWER SHOP'S TICKETING SYSTEM IN`"

Follow [these steps](https://medium.com/analytics-vidhya/how-to-host-a-discord-py-bot-on-heroku-and-github-d54a4d62a99e) for deploying your bot to Heroku to keep it always running. Unless you've made significant changes, you probably only need to start from `HOSTING ON HEROKU` (keeping in mind to change your `Config Vars` as mentioned above).
If you're confused about the IDs of channels, categories, roles, etc. follow [these steps](https://www.howtogeek.com/714348/how-to-enable-or-disable-developer-mode-on-discord/) to enable developer mode on your Discord so that you can copy IDs.
