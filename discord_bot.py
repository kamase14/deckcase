import discord
import asyncio
import sqlite3
import os
import re

path = "./deck.db"


conn = sqlite3.connect('deck.db')
c = conn.cursor()

#c.execute('''CREATE TABLE deck(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, recipe text, author text)''')

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author.bot:
        return


    if "/adddeck" in message.content:
        all_text = message.content.lstrip("/adddeck")

        name_start = all_text.find('###')
        recipe_start= all_text.find('```')

        if (name_start+1) and (recipe_start+1):
            deck_name = all_text[name_start:recipe_start]
            deck_name = deck_name.lstrip('###')
            deck_recipe = all_text[recipe_start:]
            deck = (deck_name, deck_recipe, message.author.name)
            print(c.execute('insert into deck(name, recipe, author) values (?,?,?)',deck))

            await message.channel.send("Add your deck successfully!")
            await message.channel.send("Deckname:"+deck_name)
            await message.channel.send("Deckrecipe:"+deck_recipe)
            conn.commit()
        else:
            await message.channel.send("invalid syntax!")

    if "/viewdeck" in message.content:
        if "-author" in message.content:

            param = message.content
            param = param.replace("/viewdeck","")
            param = param.replace("-author", "")
            param = param.strip()


            if param == "デブ":
                param = "さるばーれ"

            c.execute('SELECT id, author, name FROM deck where author = ? ',[param])

            row = c.fetchall()
            if (not(row)):
                string = "**" + param + "**さんが書いたデッキは見つかりませんでした。"
                await message.channel.send(string)
            else:
                for count in range(row[-1][0]):
                    string = "\nID : **  " + str(row[count][0]) + "     **Author :** " + str(row[count][1]) + "     **Deckname : **" + str(row[count][2]+ "**")
                    await message.channel.send(string)

        elif "-id" in message.content:

            param = message.content
            param = param.replace("/viewdeck","")
            param = param.replace("-id", "")
            param = param.strip()

            c.execute('SELECT author, recipe, name FROM deck where id = ? ',[param])
            tmp = c.fetchall()

            if(not(tmp)):
                string = "**" + param +"**番にはデッキは登録されてません。"
            else:
                string ="Deckname : **" + tmp[0][2]  + "**Author : **" +  tmp[0][0] + "**" + tmp[0][1]

            await message.channel.send(string)

        else :
            c.execute('SELECT id, author, name FROM deck')
            count = 0
            #await message.channel.send(c.fetchall())
            row  = c.fetchall()
            for count in range(row[-1][0]):
                string = "\nID : **  " + str(row[count][0]) + "     **Author :** " + str(row[count][1]) + "     **Deckname : **" + str(row[count][2]+ "**")
                await message.channel.send(string)

        return

    if "/removedeck" in message.content:
        ## WIP
        param = message.content
        param = param.replace("/removedeck","")
        param = param.strip()

        row = c.execute('SELECT id FROM deck WHERE id = ?',[param])
        tmp =c.fetchall()

        if (not(tmp)):
            string = "**" + param +"**番にはデッキは登録されてません。"
        else:
            c.execute('DELETE FROM DECK WHERE id=?',[param])
            string = "**" + param + "**番に登録されたデッキは削除されました。"

        await message.channel.send(string)
        return

    if "/updatedeck" in message.content:
        ## WIP
        return

    if "/deckcase_help" in message.content:
        await message.channel.send("https://github.com/kamase14/deck_case/blob/master/Readme.md　をご覧ください")



client.run("NTQ5ODc3NzIwNTgyOTc5NTg0.D1aT5g.vOrhCuAuyi3wydCFDiZGZzjvF1o")
