import discord
import sqlite3
import random

intents = discord.Intents.all()
intents.messages = True

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try:
            # MAKE SURE YOU REPLACE main.sqlite WITH THE FILE PATH!
            db = sqlite3.connect("main.sqlite", timeout = 5.0)
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS main(
                user_id INTEGER, wallet INTEGER, bank INTEGER
            )''')

            db.commit()
        except sqlite3.Error as error:
            print(f'Failed to insert data into sqlite table: {error}')
            cursor.close()
            db.close()

    async def on_message(self, message):
        if message.author == self.user:
            return

        # this is for debugging
        # print(f'Message from {message.author}: {message.content}')

        author = message.author
        db = sqlite3.connect("main.sqlite", timeout = 5.0)
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM main WHERE user_id = {author.id}")
        result = cursor.fetchone()
        db.commit()
        # if the user doesn't already have a balance
        if result is None:
            sql = ("INSERT INTO main(user_id, wallet, bank) VALUES (?, ?, ?)")
            # initialize user's wallet with 100 coins and an empty bank
            val = (author.id, 100, 0)
            cursor.execute(sql, val)
            db.commit()

        cursor.close()
        db.close()
    
        # commands (they're a little wacky)
        # !balance / !bal: displays current balance
        if (message.content.startswith('!balance') or message.content.startswith('!bal')):
            author = message.author
            db = sqlite3.connect("main.sqlite", timeout = 5.0)
            cursor = db.cursor()

            cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {author.id}")
            bal = cursor.fetchone()
            try:
                wallet = bal[0]
                bank = bal[1]
            except:
                wallet = 0
                bank = 0
            
            balSend = f"Balance:\n\n👛  Wallet -- {wallet} 🦦\n\n🏦  Bank -- {bank} 🦦"

            if (wallet > 500):
                balSend += f"\n\n*wow, you're rich!*"
            elif (wallet <= 105):
                balSend += f"\n\n*try using !earn to earn more otters!*"
            
            await message.channel.send(balSend)

            db.commit()
            cursor.close()
            db.close()

        # !earn: increases balance by a random int between 1 and 5
        elif (message.content.startswith('!earn')):
            author = message.author

            earnings = random.randint(1, 5)
            jackpot = random.randint(1, 1000)
            earnSend = ""

            if (jackpot == 1000):
                earnSend = "*Jackpot!!*\n"
                earnings = 100

            db = sqlite3.connect("main.sqlite", timeout = 5.0)
            cursor = db.cursor()

            cursor.execute(f"SELECT wallet FROM main WHERE user_id = {author.id}")
            wallet = cursor.fetchone()

            try:
                wallet = int(wallet[0])
            except:
                wallet = 0
            
            sql = ("UPDATE main SET wallet = ? WHERE user_id = ?")

            val = (wallet + int(earnings), author.id)
            cursor.execute(sql, val)
            earnSend += f"You have earned {earnings} 🦦!"
            await message.channel.send(earnSend)

            db.commit()
            cursor.close()
            db.close()

client = Client(command_prefix = '!', intents = intents)
# insert hash thing here!!
client.run('discord bot token')