import datetime
import sys
import disnake as discord
from disnake.ext import commands
import json


class info(commands.Cog):
    """
    `With those commands you almost can stalk a user`
    """

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def getRoles(roles):
        roles.reverse()
        roles = [f'{role.mention}' for role in roles if not role.is_default()]
        thing = ''

        for role in roles:
            if len(thing + str(role)) > 800:
                thing += '...'
                break
            thing += f'{role} '
        else:
            return thing

    @commands.command(name='user', aliases=['userinfo', 'info'])
    async def user(self, ctx, member: discord.Member = None):
        """
        Get an info about a specific user or yourself
        - **?user [`member`]**
        """

        with open('utils/json/active_check.json', 'r') as f:
            data = json.load(f)

        if data[str(ctx.guild.id)]["Info"] == 'false':
            embed = discord.Embed(
                description=f'Diese **Extension (Info) ist momentan deaktiviert!** Wende dich bitte an **den Owner vom Bot** (LookAtYourSkill#8691)',
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if not member:
                member = ctx.author
            days = (datetime.datetime.utcnow() - member.created_at).days
            days2 = (datetime.datetime.utcnow() - member.joined_at).days
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            roles = self.getRoles(member.roles)
            embed = discord.Embed(title=f'> Userinfo für {member.display_name}',
                                  color=0x4cd137,
                                  timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.add_field(name='**Name**',
                            value=f'```Name: {member.name}#{member.discriminator}\n'
                                  f'ID: {member.id}\n'
                                  f'Nick: {(member.nick if member.nick else "Nein")}\n```',
                            inline=False)
            embed.add_field(name='**Account**',
                            value=f'```Discord Beigetreten: {member.created_at.strftime("%d.%m.%Y")}\n'
                                  f'Vor {days} Tagen erstellt\n'
                                  f'Bot : {("Ja" if member.bot else "Nein")}\n'
                                  f'Farbe : {member.color}\n'
                                  f'Status : {member.status}\n'
                                  f'Join Position : {str(members.index(member) + 1)}```',
                            inline=False)
            embed.add_field(name='**Server**',
                            value=f'```Server Beigetreten : {member.joined_at.strftime("%d.%m.%Y")}\n'
                                  f'Vor {days2} Tagen beigetreten\n'
                                  f'Booster: {("Ja" if member.premium_since else "Nein")}```',
                            inline=False)
            embed.add_field(name=f'**Rollen [{len(member.roles) - 1}]**',
                            value=f'{(roles if roles else f"```Der Member noch hat keine Rollen!```")}',
                            inline=False)
            embed.set_footer(text=f'Angefordert von {ctx.author.name}#{ctx.author.discriminator}',
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name='server', aliases=['serverinfo', 'guild'])
    async def server(self, ctx):
        """
        Get multiple infos about a server
        - **?server**
        """

        with open('utils/json/active_check.json', 'r') as f:
            data = json.load(f)

        if data[str(ctx.guild.id)]["Info"] == 'false':
            embed = discord.Embed(
                description=f'Diese **Extension (Info) ist momentan deaktiviert!** Wende dich bitte an **den Owner vom Bot** (LookAtYourSkill#8691)',
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            roles = self.getRoles(ctx.guild.roles)
            days = (datetime.datetime.utcnow() - ctx.guild.created_at).days
            statuses = [
                len(list(filter(lambda m: str(m.status) == 'online', ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == 'idle', ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == 'dnd', ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == 'offline', ctx.guild.members)))
            ]
            embed = discord.Embed(color=0x4cd137,
                                  timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
            embed.add_field(name=f'> Info für {ctx.guild.name}',
                            value=f'```Name : {ctx.guild.name}\n'
                                  f'ID : {ctx.guild.id}\n'
                                  f'Owner : {ctx.guild.owner}\n'
                                  f'Owner ID : {ctx.guild.owner_id}\n'
                                  f'Region : {ctx.guild.region}```',
                            inline=False)
            embed.add_field(name='**Daten**',
                            value=f'```Erstellt: {ctx.guild.created_at.strftime("%d.%m.%Y")}\n'
                                  f'Vor {days} Tagen Erstellt\n'
                                  f'Member : {ctx.guild.member_count}\n'
                                  f'Boost Status : {ctx.guild.premium_subscription_count}/30```',
                            inline=False)
            embed.add_field(name='**Members**',
                            value=f'```Statuses:\n'
                                  f'🟢 {statuses[0]} | 🟡 {statuses[1]} | 🔴 {statuses[2]} | 🔘 {statuses[3]} \n'
                                  f'User:\n'
                                  f'{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}\n'
                                  f'Bots:\n'
                                  f'{len(list(filter(lambda m: m.bot, ctx.guild.members)))}```',
                            inline=False)
            embed.add_field(name='**Channel**',
                            value=f'```Insgesamt : {len(ctx.guild.channels)}\n'
                                  f'Textchannel : {len(ctx.guild.text_channels)}\n'
                                  f'Voicechannel : {len(ctx.guild.voice_channels)}\n'
                                  f'Kategorien : {len(ctx.guild.categories)}```')
            embed.add_field(name=f'**Rollen[{len(ctx.guild.roles) - 1}]**',
                            value=f'{roles}',
                            inline=False)
            embed.set_footer(text=f'Angefordert von {ctx.author.name}#{ctx.author.discriminator}',
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name='members')
    async def members(self, ctx):
        """
        Check all members on the discord server
        - **?members**
        """

        with open('utils/json/active_check.json', 'r') as f:
            data = json.load(f)

        if data[str(ctx.guild.id)]["Info"] == 'false':
            embed = discord.Embed(
                description=f'Diese **Extension (Info) ist momentan deaktiviert!** Wende dich bitte an **den Owner vom Bot** (LookAtYourSkill#8691)',
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**Member Count**',
                                  description=f'Auf diesem Server sind `{ctx.guild.member_count}` Mitglieder!')
            await ctx.send(embed=embed)

    @commands.command(name='joined')
    async def joined(self, ctx, member: discord.Member = None):
        """
        Give you the position, at which place you joined the server and when you joined
        - **?joined [member]**
        """

        with open('utils/json/active_check.json', 'r') as f:
            data = json.load(f)

        if data[str(ctx.guild.id)]["Info"] == 'false':
            embed = discord.Embed(
                description=f'Diese **Extension (Info) ist momentan deaktiviert!** Wende dich bitte an **den Owner vom Bot** (LookAtYourSkill#8691)',
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if not member:
                member = ctx.author
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            embed = discord.Embed(title='**Member joined**',
                                  description=f'You joined at the `{member.joined_at.strftime("%d.%m.%Y")}`\n'
                                              f'Join Position : `{str(members.index(member) + 1)}`')
            await ctx.send(embed=embed)

    @commands.command(name='bot', aliases=['botinfo'])
    async def bot(self, ctx):
        """
        Give a little info about the bot
        - **?bot**
        """

        with open('utils/json/active_check.json', 'r') as f:
            data = json.load(f)

        if data[str(ctx.guild.id)]["Info"] == 'false':
            embed = discord.Embed(
                description=f'Diese **Extension (Info) ist momentan deaktiviert!** Wende dich bitte an **den Owner vom Bot** (LookAtYourSkill#8691)',
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            BOT_VERSION = 'v1.3'
            PREFIX = '?'
            python_version = '{}.{}.{}'.format(*sys.version_info[:3])
            embed = discord.Embed(title=f'> Bot Info ',
                                  description='',
                                  color=0x4cd137,
                                  timestamp=datetime.datetime.utcnow())

            embed.add_field(name='**Besitzer**',
                            value='```LookAtYourSkill#6822\nID: 493370963807830016```',
                            inline=True)
            embed.add_field(name='Versionen',
                            value=f'```Python: {python_version}\nDiscord: {discord.__version__}```',
                            inline=True)
            embed.add_field(name='**Other**',
                            value=f'```Bot Version: {BOT_VERSION}\nBot Prefix: {PREFIX}```\n',
                            inline=True)
            embed.set_footer(text=f'Angefordert von {ctx.author.name}#{ctx.author.discriminator}',
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['av'])
    async def avatar(self, ctx, member: discord.Member = None):
        """
        Give back the profile picture from a user or yourself
        - **?avatar [`member`]**
        """

        with open('utils/json/active_check.json', 'r') as f:
            data = json.load(f)

        if data[str(ctx.guild.id)]["Info"] == 'false':
            embed = discord.Embed(
                description=f'Diese **Extension (Info) ist momentan deaktiviert!** Wende dich bitte an **den Owner vom Bot** (LookAtYourSkill#8691)',
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if not member:
                member = ctx.author
            icon = member.avatar_url
            embed = discord.Embed(title='',
                                  color=0x123456,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f'{member}',
                             icon_url=icon)
            embed.set_image(url=icon)
            embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=f'Angefordert von {ctx.author}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
