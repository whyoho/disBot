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
            
            balSend = f"Balance:\n\n👛  Wallet: {wallet} 🦦\n\n🏦  Bank: {bank} 🦦"

            if (wallet > 500):
                balSend += f"\n\n*wow, you're rich!*"
            elif (wallet <= 105 and wallet >= 0):
                balSend += f"\n\n*try using !earn to earn more otters!*"
            elif (wallet < 0):
                balSend += "\n\n*you're in debt...*\n*try using !earn to earn more otters!*"
            
            await message.channel.send(balSend)

            db.commit()
            cursor.close()
            db.close()

        # !earn: increases balance by a random int between 1 and 5
        elif (message.content.startswith('!earn')):
            author = message.author

            jackpot = random.randint(1, 1000)
            earnSend = ""

            # 1 in 1000 chance for jackpot
            if (jackpot == 1000):
                earnings = 5000
                earnSend += "You are minding your own business, sitting by the turtle pond, when you suddenly get swarmed by approximately 5000 otters. *Jackpot!!*\n\n"
            # 1 in 1000 chance of a Billy encounter
            elif (jackpot == 999):
                earnings = -3891
                earnSend += "You feel an ominous aura approaching you... *uh oh...*\nIt's Billy Bronco! His aura compels you to gift him 3891 of your otters.\n\n"
            # 99 in 1000 chance of Otter Pop
            elif (jackpot >= 900):
                earnings = random.randint(10, 20)
                earnSend += f"You unwrap an Otter Pop and {earnings} otters spawn in front of you. It sure is your lucky day!\n\n"
            # 150 in 1000 chance?  of tripping
            elif (jackpot >= 750):
                earnings = random.randint(5, 10)
                story = random.randint(1, 5)
                if (story == 1):
                    earnSend += f"You trip over a crack, and when you get up, {earnings} of your otters have mysteriously disappeared.\n\n"
                elif (story == 2):
                    earnSend += f"It looks like some of your otters want to go to Centerpointe... {earnings} of them, to be exact. You wave goodbye with a heavy heart.\n\n"
                elif (story == 3):
                    earnSend += f"You blink and suddenly {earnings} otters disappear. Maybe it was all a dream...\n\n"
                elif (story == 4):
                    earnSend += f"{earnings} of your otters have decided to go on vacation.\n\n"
                elif (story == 5):
                    earnSend += f"You stop to pet a cat, but when you look up again {earnings} of your otters have disappeared...\n\n"
                earnings *= -1
            # 799 in 1000 chance? of earning a tiny amount of otters
            else: 
                earnings = random.randint(1, 5)
                story = random.randint(1, 5)
                if (story == 1):
                    buildings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 17, 25, 28, 30, 31, 32, 45, 73, 74, 79, 98, 163, 164]
                    building = buildings[random.randint(0, len(buildings) - 1)]
                    earnSend += f"You take a walk and find {earnings} otter(s) near Building {building}.\n\n"
                elif (story == 2):
                    earnSend += f"There's free pizza at your club meeting today! As you raise your first slice to your mouth, you see {earnings} pair(s) of eyes looking at you.\n\n"
                elif (story == 3):
                    earnSend += f"You stop to tie your shoe and hear a squeak. You look up to see...otter... (hahaha, get it? sea otter...hahaha....).\n\n"
                elif (story == 4):
                    earnSend += f"You take a nap on the grass. When you wake up, you find something next to you...\n\n"
                elif (story == 5):
                    earnSend += f"You're studying in the library when a random person taps on your shoulder and bestows upon you the power of otter.\n\n"

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
            if (earnings >= 0):
                earnSend += f"You have earned {earnings} 🦦!"
            elif (earnings < 0):
                earnings *= -1
                earnSend += f"You have lost {earnings} 🦦!"
            
            await message.channel.send(earnSend)

            db.commit()
            cursor.close()
            db.close()

client = Client(command_prefix = '!', intents = intents)
# insert bot token here
client.run('discord bot token')