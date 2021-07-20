from GetData import *
from discord import Client, Colour, File
import discord
from requests import get

client = Client()

token = 'NzEwNDg0NTQzOTM2NjU5NTU4.Xr1ISw.WQBvwHi3qor_QYsECT5u9lpO71I'


@client.event
async def on_ready():
    print('bot is on!')


@client.event
async def on_message(message):
    reactions_caracters = ['❤️', '📌', '✅','🕑']
    if not message.author.bot:
        if '!get' in message.content and 'capitulo' in message.content:
            footer = '❤️ para adicionar aos favoritos\n📌 para ler agora\n✅ para marcar como lido\n🕑 para ler mais tarde'
            name = message.content[:message.content.find(" capitulo")]
            chapter = message.content[message.content.find('capitulo '):]
            name = CleanCaracters(name.replace('!get ', ''))
            page = get(f'https://www.supermangas.site/manga/{name}/{chapter[len("capitulo "):]}')
            try:
                if page.raise_for_status() is None:
                    style = discord.Embed(title=f'{name} {chapter}', color=Colour.random())
                    style.set_footer(text=footer)
                    bot_message = await message.channel.send(f'<@{message.author.id}> {name} {chapter}', embed=style)
                    for react in reactions_caracters:
                        await bot_message.add_reaction(react)
                else:
                    style = discord.Embed(title='Infelizmente não tenho esse ai :(', colour=Colour.random())
                    await message.channel.send(f'<@{message.author.id}> {name} {chapter}', embed=style)
            except:
                style = discord.Embed(title='desculpa :( ocorreu um erro no meu banco de dados :(, tente mais tarde.)', colour=Colour.random())
                await message.channel.send(f'<@{message.author.id}> {name} {chapter}', embed=style)


        elif '!get' in message.content:
            footer = '❤️ para adicionar aos favoritos\n📌 para ler agora\n✅ para marcar como lido\n🕑 para ler mais tarde'
            manga = message.content.replace('!get ', '')
            Data = GetDataInfo(manga)
            style = discord.Embed(title=manga, description=Data["Info"], colour=Colour.random())
            style.set_image(url=Data["image"])
            style.set_footer(text=footer)
            bot_message = await message.channel.send(f'<@{message.author.id}> {manga}', embed=style)
            for react in reactions_caracters:
                await bot_message.add_reaction(react)

@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        reactions_caracters = ['❤️', '✅','🕑']
        tables = ['favorites', 'readed', 'read_later']
        if str(reaction) in reactions_caracters:
            index = tables.index(str(reaction))
            message = reaction.message.content.lower()
            #make later

        elif str(reaction) == "📌":
            message = reaction.message.content[reaction.message.content.find('> ')+len('> '):]
            if 'capitulo' in message:
                chapter = message[message.find('capitulo ')+len('capitulo '):]
            arc = GetImageData(message[:message.find(' capitulo')])
            await reaction.message.channel.send(f'aqui está <@{user.id}>', file=File(arc))


client.run(token)
