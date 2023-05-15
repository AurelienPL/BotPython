import discord 
from discord.ext import commands
from liste import historique_commandes
from fonction import citations
from fonction import blagues
import random
import asyncio
from collections import deque


intents = discord.Intents.all()
History = historique_commandes()
client = commands.Bot(command_prefix="!", intents = intents)
last_command = ''   


@client.event
async def on_ready():
   print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
   message.append(message)



historique_queue = asyncio.Queue()
historique = deque(maxlen=10) 


@client.command(name="record")
async def record(ctx, command):
    await historique_queue.put(command)
    try:
        await historique_queue.get()
        historique.append(command)
        await ctx.send("Commande enregistrée dans l'historique.")
    finally:
        historique_queue.task_done()


@client.command(name="history")
async def history(ctx):
    if historique_queue.empty() or historique_queue._get()[0] == ctx.author.id:
        if not historique:
            await ctx.send("Aucun historique de commandes trouvé.")
        else:
            await ctx.send(f"Historique des commandes : {', '.join(historique)}")
        historique_queue.task_done()
    else:
        await ctx.send("Désolé, seul le prochain utilisateur dans la file peut accéder à l'historique.")


@client.command(name="next")
async def next(ctx):
    if not historique_queue.empty() and historique_queue._get()[0] == ctx.author.id:
        historique_queue.task_done()
        await ctx.send("Passé au prochain utilisateur dans la file.")
    else:
        await ctx.send("Tu dois attendre a ton tour")



@client.command(name="del")
async def delete(ctx, number):
    await ctx.channel.purge(limit=int(number))
    History.add_command("!del")

@client.command(name="historique")
async def full_history(ctx):
   all_commands = History.get_all_commands()
   for command in all_commands:
      await ctx.channel.send(command)
   History.add_command("!full_history")

@client.command(name="last_command")
async def last_command(ctx):
    last_command = History.get_last_command()
    if last_command:
        await ctx.channel.send(last_command)
    else:
        await ctx.channel.send("Aucune commande n'a été trouvée dans l'historique.")
    History.add_command("!last_command")


@client.command(name="add_command")
async def add_command(ctx):
    command = "!add_command"
    History.add_command(command)


@client.command(name="clear_history")
async def clear_history(ctx):
    History.clear_history()
    await ctx.channel.send("L'historique des commandes a été effacé.")

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_typing(channel, user, when):
     await channel.send(user.name+" écris a une vitesse faramineuse")

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(977137496720826368)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name)

@client.event
async def on_message(message):
  if message.author == client.user:
    return   

  if message.content.startswith("hello"):
    await message.channel.send("Salutation")
  if message.content.startswith("ca va et toi"):
      await message.channel.send("Je n'ai pas d'âme donc je ne ressens pas d'émotion")
  if message.content.startswith("un peu triste ton histoire"):
      await message.channel.send("je m'en moque")
  

  await client.process_commands(message)

@client.command(name = "citations")
async def citation(ctx):
    citation = random.choice(citations)
    command = "!citation"
    History.add_command(command)
    await ctx.send(citation)


@client.command(name = "blagues")
async def blague(ctx):
    blague = random.choice(blagues)
    command = "!blagues"
    History.add_command(command)
    await ctx.send(blague)


@client.command(name = "sondage")
async def poll(ctx, question, *options):
    command = "!sondage"
    History.add_command(poll)
    if len(options) < 2:
        await ctx.send("Veuillez fournir au moins deux options pour le sondage.")
        return
    
    embed = discord.Embed(title="Sondage", description=question, color=discord.Color.blue())
    for i, option in enumerate(options):
        emoji = chr(0x1f1e6 + i) 
        embed.add_field(name=f"{emoji} Option {i+1}", value=option, inline=False)

    sondage_message = await ctx.send(embed=embed)
    for i in range(len(options)):
        emoji = chr(0x1f1e6 + i)
        await sondage_message.add_reaction(emoji)

@client.command()
async def countdown(ctx, seconds: int, *, role: discord.Role):
    if seconds <= 0:
        await ctx.send("Veuillez fournir un nombre de secondes valide (supérieur à zéro).")
        return
    
    message = await ctx.send(f"Décompte : {seconds} secondes.")
    
    while seconds > 0:
        await asyncio.sleep(1)
        seconds -= 1
        await message.edit(content=f"Décompte : {seconds} secondes.")
    
    await message.edit(content=f"{role.mention}Décompte terminé!")
    await ctx.send("Le décompte est terminé.")

@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        message = f"La france te souhaite la bienvenue {member.mention} !"
        await channel.send(message)

@client.command()
async def greet(ctx):
    message = f"Salut {ctx.author.mention} ! Comment ça va ?"
    await ctx.send(message)

@client.command(name = "ping_bot")
async def ping(ctx):
    command = "!ping_bot"
    History.add_command(command)
    latency = round(client.latency * 1000)  # Convertir en millisecondes
    await ctx.send(f"Pong! Latence : {latency}ms")

@client.command()
async def botinfo(ctx):
    bot_name = client.user.name
    bot_id = client.user.id
    bot_created_at = client.user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    bot_owner = "Ambilieu"

    embed = discord.Embed(title="Informations sur le bot", color=discord.Color.blue())
    embed.add_field(name="Nom", value=bot_name, inline=True)
    embed.add_field(name="ID", value=bot_id, inline=True)
    embed.add_field(name="Date de création", value=bot_created_at, inline=True)
    embed.add_field(name="Propriétaire", value=bot_owner, inline=True)

    await ctx.send(embed=embed)



@client.command()
async def commands(ctx):
    prefix = "!"  # Remplacez par le préfixe de votre bot
    command_list = []

    for command in client.commands:
        command_list.append(f"{prefix}{command.name}")

    command_list_str = "\n".join(command_list)
    await ctx.send(f"Liste des commandes disponibles:\n```\n{command_list_str}\n```")

@client.command(name="assign_role")
async def assign_role(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
        await ctx.send(f"Le rôle {role.name} a été attribué à {member.display_name}.")
    except discord.Forbidden:
        await ctx.send("Je n'ai pas les permissions nécessaires pour attribuer ce rôle.")
    except discord.HTTPException:
        await ctx.send("Une erreur s'est produite lors de l'attribution du rôle.")

@client.command(name="remove_role")
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.remove_roles(role)
        await ctx.send(f"Le rôle {role.name} a été retiré à {member.display_name}.")
    except discord.Forbidden:
        await ctx.send("Je n'ai pas les permissions nécessaires pour attribuer ce rôle.")
    except discord.HTTPException:
        await ctx.send("Une erreur s'est produite lors de l'attribution du rôle.")

@client.command()
async def disconnect(ctx):
    if ctx.author.id == 201301810407800832:
        await ctx.send("Je vais me coucher bonne nuit et à très vite")
        await client.close()
    else:
        await ctx.send("Vous n'êtes pas autorisé à effectuer cette commande.")

@client.command(name="talk")
async def talk(ctx):
    pass



client.run("Your Token")




          
  