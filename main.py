import discord
from discord.ext import commands
import requests
import io
import json
from datetime import timezone, timedelta, datetime
import os
from credit_manager import CreditManager
import time
import difflib
claim_cooldown = {}


activity_type = discord.ActivityType.streaming, discord.ActivityType.playing
activity = discord.activity
presence_type = discord.Status.idle
credit_manager = CreditManager()

bot = commands.Bot(command_prefix="-", intents=discord.Intents.all(), help_command=None, activity=discord.Streaming(name="Snusbot by xDatabase", url="https://www.twitch.tv/rickyrollstar"), status=presence_type)

@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    member = ctx.author

    balance_text = credit_manager.get_balance(user_id)

    embed = discord.Embed(title=f"Salut {member.display_name}!", color=0x000000)
    embed.description = f"Tu as {balance_text} crédit(s)"

    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    else:
        embed.set_thumbnail(url=member.default_avatar)

    await ctx.send(embed=embed)


def update_balance(ctx, user_id, amount):
    member = bot.get_guild(ctx.guild.id).get_member(user_id)
    
   
    
    current_balance = credit_manager.get_balance(str(user_id))
    new_balance = current_balance + amount
    
    if new_balance < 0:
        new_balance = 0
    
    credit_manager.set_balance(str(user_id), new_balance)
    
    return f"L'utilisateur <@{user_id}> a maintenant {new_balance} crédit(s)."

@bot.command()
async def claim(ctx):

    
    
    user_id = str(ctx.author.id)
    

    if user_id in claim_cooldown:
        last_claim_time = claim_cooldown[user_id]
        if time.time() - last_claim_time < 86400:  # 86400 secondes = 24 heures
            await ctx.send("Vous avez déjà utilisé cette commande récemment. Veuillez réessayer plus tard.")
            return
    

    credit_manager.add_balance(user_id, 10)
    

    claim_cooldown[user_id] = time.time()
    

    embed = discord.Embed(title="Récompense de réclamation", color=0x000000)
    embed.add_field(name="Utilisateur", value=ctx.author.mention, inline=False)
    embed.add_field(name="Crédits ajoutés", value="10", inline=False)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def addcr(ctx, user: discord.Member, amount: int):
    if is_admin(ctx):
        await ctx.send(update_balance(ctx, user.id, amount))
    else:
        embed = discord.Embed(
            title="❌ Permission refusée ❌",
            description=f"{ctx.author.mention}"
        ).set_footer(text=f"{ctx.guild.name} - Gestion, dev by xDatabase")
        await ctx.send(embed=embed)


def load_admins():
    with open('admin.json', 'r') as f:
        data = json.load(f)
    return data["admins"]


def save_admins(data):
    with open('admin.json', 'w') as f:
        json.dump(data, f, indent=4)




admins = load_admins()



DATA_FILE = "user_stats.json"


if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

previous_invites = {}

@bot.event
async def on_member_join(member):
    guild = member.guild
    now = int(datetime.now().timestamp())  
    created_at_timestamp = int(member.created_at.timestamp())  
    invite_channel = discord.utils.get(guild.channels, name="génénral")  

    
    if str(member.id) in user_data:
        user_data[str(member.id)]["join_count"] += 1
    else:
        user_data[str(member.id)] = {
            "join_count": 1,
            "created_at": created_at_timestamp
        }
    
    join_count = user_data[str(member.id)]["join_count"]

   
    new_invites = await guild.invites()
    used_invite = None

    for invite in previous_invites[guild.id]:
        for new_invite in new_invites:
            if invite.code == new_invite.code and invite.uses < new_invite.uses:
                used_invite = new_invite
                break
        if used_invite:
            break

    previous_invites[guild.id] = new_invites  

    if used_invite:
        inviter_info = f"Il/Elle a été invité(e) par **{used_invite.inviter}** avec le lien **{used_invite.code}**."
    else:
        inviter_info = "Il/Elle a rejoint par un lien d'invitation inconnu ou direct."

    if invite_channel:
        
        message = (
            f"<@{member.id}> vient de nous rejoindre pour la {join_count}e fois, "
            f"son compte a été créé <t:{created_at_timestamp}:R>. "
            f"{inviter_info} "
            f"Nous sommes désormais {guild.member_count} !"
        )
        await invite_channel.send(message)

   
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4)


def is_admin(ctx):
    return str(ctx.author.id) in admins


@bot.event
async def on_ready():

    print(f"Snusbot remade by xDatabase est prêt\nNom : {bot.user}\nId : {bot.user.id}")
    
    for guild in bot.guilds:
        previous_invites[guild.id] = await guild.invites()
@bot.command()
async def snusbase(ctx, query):
        blacklist = ["1059179993051172914"]
        if any(word in query.lower() for word in blacklist):
            await ctx.reply("## > ❌ Blackliste.")
            await ctx.message.delete()
            return
        if credit_manager.get_balance(str(ctx.author.id)) < 1:
            await ctx.send("Vous n'avez pas assez de crédits pour effectuer une recherche ping un Créateur.")
            return
        remaining_credits = credit_manager.get_balance(str(ctx.author.id))
        credit_manager.remove_balance(str(ctx.author.id), 1)
        bonjour = await ctx.send(f'Veuillez patienter pendant que je rassemble les informations...')
        snusbase_auth = 'sbyjthkoft4yaimbwcjqpmxs8huovd'
        snusbase_api = 'https://api-experimental.snusbase.com'

        url = f"{snusbase_api}/data/search"
        headers = {
            'auth': snusbase_auth,
            'Content-Type': 'application/json',
        }
        body = {
            'terms': [query],
            'types': ["email", "username", "lastip", "hash", "password", "name"],
            'wildcard': False,
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            result = response.json()
            
            if result['size'] == 0:
                await ctx.send(f"Aucun résultat trouvé pour : {query}")
            else:
                formatted_response = json.dumps(result, indent=2)

                
                output = io.BytesIO(formatted_response.encode())
                
               
                file = discord.File(output, filename="snusbase_response.txt")

               
                await ctx.author.send(file=file, content=f'Voici les résultats pour votre recherche. "**{query}**"')
                embed = discord.Embed(

                )
                
            embed = discord.Embed(
                title="🔮 Recherche envoyée 🔮", 
                description=f"Votre recherche a été envoyée à vos DM, {ctx.author.mention}.",
                color=discord.Color.purple() 
            )
            embed.set_footer(text=f"by xDatabase | 💵 {remaining_credits} crédit(s) restant(s)")
    
            await ctx.send(embed=embed)
            await bonjour.delete()
            await ctx.message.delete()
        else:
            await ctx.send(f'Erreur lors de la recherche pour : {query}')
            await bonjour.delete()
            await ctx.message.delete()
    



status_fr = {
    discord.Status.online: 'En ligne',
    discord.Status.offline: 'Hors ligne',
    discord.Status.idle: 'Inactif',
    discord.Status.dnd: 'Ne pas déranger',
    discord.Status.do_not_disturb: 'Ne pas déranger',
    discord.Status.invisible: 'Invisible'
}


emoji_fr = {
    False: '❌',
    True: '✅'
}


@bot.command()
async def userinfo(ctx, id: int):
    if is_admin(ctx):
        blacklist = [1059179993051172914, 909455566756249621, 1096447502049353849, 1113897602975531118, 711951673559482389, 607812110860419082, 1227734338888532019]
        if id in blacklist:
            await ctx.reply("## > ❌ Blackliste.")
            await ctx.message.delete()
            return
        url = f'https://discord.com/api/v9/users/{id}'
        headers = {
            'Authorization': f'Bot ',
            'Content-Type': 'application/json',
        }

        
        result = requests.get(url, headers=headers)

        
        if result.status_code != 200:
            await ctx.send("L'utilisateur n'existe pas.")
            return

        rjson = result.json()
        print(rjson)
        thumbnail = rjson.get('avatar')
        deco_avatar = rjson.get('avatar_decoration_data')
        banner = rjson.get('banner')
        nomutilisateur = rjson.get('username')
        nickname = rjson.get('global_name')
        is_bot = emoji_fr.get(rjson.get('bot', False), '❌')  

        user_status = "Inconnu"
        join_date = "Inconnue"
        roles = "Aucun"  
        user = ctx.guild.get_member(id) 
        if user:
            user_status = status_fr.get(user.status, "Inconnu")
            join_date = user.joined_at.strftime("%d %B %Y à %H:%M:%S") if user.joined_at else "Inconnue"
            roles = ', '.join([role.name for role in user.roles if role.name != "@everyone"])  

        
        discord_epoch = 1420070400000
        user_id_timestamp = ((id >> 22) + discord_epoch) / 1000
        account_creation_date = datetime.utcfromtimestamp(user_id_timestamp).strftime('%d %B %Y à %H:%M:%S')

        
        public_flags = rjson.get('public_flags', 0)

        
        badges = {
            1: 'Staff',
            2: 'Partner',
            4: 'HypeSquad Events',
            8: 'Bug Hunter Niveau 1',
            64: 'HypeSquad Bravery',
            128: 'HypeSquad Brilliance',
            256: 'HypeSquad Balance',
            512: 'Supporter Précoce',
            16384: 'Bug Hunter Niveau 2',
            131072: 'Développeur de Bot Vérifié',
            4194304: 'Développeur Actif'
        }

        user_badges = [name for bit, name in badges.items() if public_flags & bit]

        

        

        embed = discord.Embed(title=f"Lookup de {nomutilisateur}",
                            url=(f"https://cdn.discordapp.com/avatars/{id}/{thumbnail}"))
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{id}/{thumbnail}")
        if banner:
            embed.set_image(url=f'https://cdn.discordapp.com/banners/{id}/{banner}?size=1024')
            embed.add_field(name="__Informations de l'utilisateur__", value=f"**Nom d'utilisateur** : `{nomutilisateur}` \n**Nom** : `{nickname}` \n**Id** : `{id}` \n**Bot** : `{is_bot}` \n**Date de création du compte** : `{account_creation_date}` \n**Date d'arrivée sur le serveur** : `{join_date}` \n**Statut** : `{user_status}` \n**Badges** : `{', '.join(user_badges) if user_badges else 'Aucun'}` \n**Rôles** : `{roles}` \n**Bannière** : [Bannière](https://cdn.discordapp.com/banners/{id}/{banner})", inline=False)
        else:
            embed.add_field(name="__Informations de l'utilisateur__", value=f"**Nom d'utilisateur** : `{nomutilisateur}` \n**Nom** : `{nickname}` \n**Id** : `{id}` \n**Bot** : `{is_bot}` \n**Date de création du compte** : `{account_creation_date}` \n**Date d'arrivée sur le serveur** : `{join_date}` \n**Statut** : `{user_status}` \n**Badges** : `{', '.join(user_badges) if user_badges else 'Aucun'}` \n**Rôles** : `{roles}` \n**Bannière** : `❌`", inline=False)

        if deco_avatar:
            embed.add_field(name="Décoration d'avatar ", value=deco_avatar, inline=False)
        else:
            embed.add_field(name="Décoration d'avatar", value=("Aucune."), inline=False)

        embed.set_footer(text="By xDatabase")
        await ctx.send(embed=embed)

        channel = bot.get_channel(1288938486371454976)
        await channel.send(f"Lookup de **{nomutilisateur}** effectué par **{ctx.author.name}**")
    else:
        embed = discord.Embed(
            title="❌ Permission refusée ❌",
            description=f"{ctx.author.mention}"
        ).set_footer(text=f"{ctx.guild.name} - Gestion, dev by xDatabase")
        await ctx.send(embed=embed)



commandes_admin = {
    "👑 Commandes Admins": [
        ("addcr", "`<user>` `<nombre>` - Ajoute des crédits à un utilisateur"),
        ("userinfo", "`<id>` - Donne des informations sur l'utilisateur")
        
    ]
}

commandes_users = {
    "📂 Commandes Utiles": [
        ("snusbase", "`<query>` - Rechercher avec Snusb@se"),
        ("balance", "Affiche vos crédits"),
        ("claim", "Reçevoir vos crédits journaliers")
    ]
}



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        
        invalid_command = str(ctx.message.content).split()[0][1:] 
      
        available_commands = [command.name for command in bot.commands]

        
        closest_matches = difflib.get_close_matches(invalid_command, available_commands, n=1, cutoff=0.5)

        if closest_matches:

            await ctx.send(f"Commande non trouvée. Vouliez-vous dire : `-{closest_matches[0]}` ?")
        else:
           
            await ctx.send("Commande non trouvée.")
    else:
       
        raise error



class HelpSelect(discord.ui.Select):
    def __init__(self, commandes):
        options = [discord.SelectOption(label=category, emoji=category.split()[0]) for category in commandes.keys()]
        self.commandes = commandes
        super().__init__(placeholder="Choisis une catégorie", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(title=f"Commandes - {category}", color=discord.Color.blurple(), description=f"Préfix actuel : -")
        
        for command, description in self.commandes[category]:
            embed.add_field(name=command, value=description, inline=False)
        
  
        total_commands = sum(len(commands) for commands in self.commandes.values())
        
        
        embed.set_footer(text=f"Total des commandes : {total_commands}")

        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self, commandes):
        super().__init__()
        self.add_item(HelpSelect(commandes))


@bot.command()
async def help(ctx):
    if is_admin(ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name} - Aide Admin",
            description="Les paramètres entre `< >` sont obligatoires et ceux entre `[ ]` sont facultatifs.",
            color=discord.Color.blurple()
        ).set_footer(text="by xDatabase")
        view = HelpView(commandes_admin)
    else:
        embed = discord.Embed(
            title=f"{ctx.guild.name} - Aide",
            description="Les paramètres entre `< >` sont obligatoires.",
            color=discord.Color.blurple()
        ).set_footer(text="by xDatabase")
        view = HelpView(commandes_users)
    
   
    total_commands = sum(len(commands) for commands in commandes_users.values()) + sum(len(commands) for commands in commandes_admin.values())
    
  
    embed.set_footer(text=f"Total des commandes : {total_commands}")
    
    await ctx.send(embed=embed, view=view)




bot.run("Ton token")