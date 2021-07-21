from GetData import *
from DataBaseManager import *
from discord import Client, Colour, File, Embed, Game
from requests import get
from os import remove


client = Client()

token = ''


@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="!commands"))
    print('bot is on!')


@client.event
async def on_message(message):
    reactions_caracters = ['❤️', '📌', '✅','🕑']
    if not message.author.bot:
        if message.content.lower() == '!commands':
            msg = '!get <nome do manga> => manda esse maga para você\n!get <nome do manga> capitulo <N do capitulo> => mada o capitulo em especifico\n!my favorites => mostra o seus favoritos\n!my readed => mostra seus lidos\n!my read_later => manda os marcados para ler depois'
            style = Embed(title='menssagem de ajuda', description=f'olá, <@{message.author.id}> aqui está uma ajudinha :>, obrigada por me usar <3\n{msg}', color=Colour.random())
            await message.channel.send(embed=style)
        if '!get' in message.content and 'capitulo' in message.content:
            footer = '❤️ para adicionar aos favoritos\n📌 para ler agora\n✅ para marcar como lido\n🕑 para ler mais tarde'
            name = message.content[:message.content.find(" capitulo")]
            chapter = message.content[message.content.find('capitulo '):]
            name = CleanCaracters(name.replace('!get ', ''))
            page = get(f'https://www.supermangas.site/manga/{name}/{chapter[len("capitulo "):]}')
            try:
                if page.raise_for_status() is None:
                    style = Embed(title=f'{name} {chapter}', color=Colour.random())
                    style.set_footer(text=footer)
                    bot_message = await message.channel.send(f'<@{message.author.id}> {name} {chapter}', embed=style)
                    for react in reactions_caracters:
                        await bot_message.add_reaction(react)
                else:
                    style = Embed(title='Infelizmente não tenho esse ai :(', colour=Colour.random())
                    await message.channel.send(f'<@{message.author.id}> {name} {chapter}', embed=style)
            except:
                style = Embed(title='desculpa :( ocorreu um erro no meu banco de dados :(, tente mais tarde.)', colour=Colour.random())
                await message.channel.send(f'<@{message.author.id}> {name} {chapter}', embed=style)


        elif '!get' in message.content:
            footer = '❤️ para adicionar aos favoritos\n📌 para ler agora\n✅ para marcar como lido\n🕑 para ler mais tarde'
            manga = message.content.replace('!get ', '')
            Data = GetDataInfo(manga)
            style = Embed(title=manga, description=Data["Info"], colour=Colour.random())
            style.set_image(url=Data["image"])
            style.set_footer(text=footer)
            bot_message = await message.channel.send(f'<@{message.author.id}> {manga}', embed=style)
            for react in reactions_caracters:
                await bot_message.add_reaction(react)


        elif '!my ' in message.content:
            tables = ['favorites', 'readed', 'read_later']
            for i in tables:
                if i in message.content:
                    msg = maneger(i, message.author.id, Value=True)
                    style = Embed(title=i, description=msg, colour=Colour.random())
                    await message.channel.send(f'<@{message.author.id}>', embed=style)



@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        reactions_caracters = ['❤️', '✅','🕑']
        tables = ['favorites', 'readed', 'read_later']
        if str(reaction) in reactions_caracters:
            index = tables[reactions_caracters.index(str(reaction))]
            message = reaction.message.content.lower()
            tables = ['favorites', 'readed', 'read_later']
            maneger(tables[reactions_caracters.index(str(reaction))], user.id, message[message.find('> ')+len('> '):])

        elif str(reaction) == "📌":
            message = reaction.message.content[reaction.message.content.find('> ')+len('> '):]
            if 'capitulo' in message:
                chapter = message[message.find('capitulo ')+len('capitulo '):]
                arc = GetImageData(message[:message.find(' capitulo')])
            else:
                arc = GetImageData(message)
            await reaction.message.channel.send(f'aqui está <@{user.id}>', file=File(arc))
            remove(arc)


client.run(token)
