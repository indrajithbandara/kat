from disco.api.http import APIException
from disco.bot import Plugin
from disco.types import message
from disco.types import user
from kat import plugins
from kat.utils import helpers
from kat.utils import katconfig
from time import sleep
import random


class Me(Plugin):
    @Plugin.command('nick')
    @helpers.is_commander
    @helpers.is_in_guild
    def nick(self, event):
        """
        Changes my nickname on the current guild you run this from.

        This is only runnable by a valid commander.

        This is only runnable in a guild.
        """

        args = ' '.join(event.args) if event.args else None
        my_member = event.guild.get_member(self.state.me)

        # Delete the message
        self.log.info(f'Changing nickname in {event.guild.name} from {my_member.nick} to {args}')

        my_member.set_nickname(args)
        event.msg.delete()

    @Plugin.command('nickall')
    @helpers.is_commander
    def nick_all(self, event):
        """
        Changes my nickname on __all__ guilds I am in.

        This is only runnable by a valid commander.
        """

        # If not a commander.
        if event.author not in katconfig.config.commanders:
            return

        args = ' '.join(event.args) if event.args else None

        # Start typing to show working
        helpers.start_typing(self.bot, event.channel)

        successes = 0
        total = 0
        for guild in self.state.guilds.values():
            total += 1

            my_member = guild.get_member(self.state.me)
            self.log.info(f'Changing nickname in {guild.name} from {my_member.nick} to {args}')
            my_member.set_nickname(args)

            successes += 1

        reply_message = event.author.open_dm().send_message(f'Changed my nickname on {successes}/{total} guilds.')

        # Delete the command message
        event.msg.delete()

        sleep(10)

        reply_message.delete()

    @Plugin.command('whereami')
    @helpers.is_commander
    def where_am_i(self, event):
        """
        Shows a list of guilds I am a member in.

        This is only runnable by a valid commander.
        """

        guild_count = len(self.state.guilds.values())

        embed = message.MessageEmbed()

        embed.title = 'Guilds I am a member in'
        embed.description = ('These are all the guilds I am a member of. Run the `kick` command to '
                             'make me leave one of these guilds!\n\n'
                             f'I am currently in {guild_count} '
                             f'guild{"s" if len(self.state.guilds.values()) != 1 else ""}.')

        # Pull a random colour
        embed.color = random.randint(0x0, 0xFFFFFF)

        for guild in self.state.guilds.values():
            info_list = (f'- ID: `{guild.id}`\n'
                         f'- Owner: `{guild.owner}`\n'
                         f'- Channels¹: `{len(guild.channels)}`\n'
                         f'- Visible Members²: `{len(guild.members)}`\n'
                         f'- Total Members²: `{guild.member_count}`\n'
                         f'- Roles: `{len(guild.roles)}`\n'
                         f'- Region³: `{guild.region.upper()}`\n'
                         f'- Custom Emojis⁴: `{len(guild.emojis)}`\n'
                         f'- V\'fn Level⁵: `{guild.verification_level.name.upper()}`\n'
                         f'- MFA Level⁶: `{"NONE" if not guild.mfa_level else "2FA"}`')

            embed.add_field(name=guild.name, value=info_list, inline=True)

        embed.set_footer(text='1. These are the channels that you have access to. \n'
                              '2. These will be the same unless the server does not show offline members. \n'
                              '3. The voice region that is set. \n'
                              '4. This should be maximum of 50... but... Discord. \n'
                              '5. How strict the server settings are. \n'
                              '6. Whether multiple-factor authorisation is set or not.')

        try:
            event.channel.send_message(embed=embed)
        except APIException:  # e.g. missing permissions
            event.author.open_dm().send_message(embed=embed)
        finally:
            event.msg.delete()

    @Plugin.command('perms')
    @helpers.is_commander
    @helpers.is_in_guild
    def perms(self, event):
        """
        Shows the permissions for the guild you are calling this from for my user.

        If I don't have permission to send messages in the channel you call this from, I will just DM you instead
        (hopefully).

        This is only runnable by a valid commander.

        This is only runnable in a guild.
        """

        my_perms = event.guild.get_permissions(self.state.me)
        my_perms_dict = my_perms.to_dict()
        my_perms_value = my_perms.value

        role_ids = event.guild.get_member(self.state.me).roles
        roles = []
        for role_id in event.guild.roles.keys():
            if role_id in role_ids:
                roles.append(event.guild.roles[role_id])

        embed = message.MessageEmbed()

        embed.title = f'Permissions for {event.guild.name}'
        embed.description = 'The contents of this embed'
        embed.set_footer(text=f'Current bitfield permissions value: 2:{bin(my_perms_value)}; '
                              f'8:{oct(my_perms_value)}; 10:{my_perms_value}; 16:{hex(my_perms_value)}  .')

        # Pull a random colour
        embed.color = random.randint(0x0, 0xFFFFFF)

        main_perms_str = ''

        for key in my_perms_dict.keys():
            clean_key = key.title()
            clean_key = clean_key.replace('_', ' ')

            main_perms_str += (f'{":white_check_mark:" if my_perms_dict[key] else ":red_circle:"}'
                               f' {clean_key}\n')

        embed.add_field(name='Overall permissions', value=main_perms_str, inline=False)

        for key in my_perms_dict.keys():

            role_list = ''

            is_first = True

            for role in roles:
                if role.permissions.to_dict()[key]:
                    if is_first:
                        is_first = False
                    else:
                        role_list += '\n'

                    ''.title()

                    role_list += f'- {role.name}'

            if not role_list:
                role_list = '- @\u200beveryone'

            clean_key = key.title()
            clean_key = clean_key.replace('_', ' ')

            embed.add_field(name=f'{clean_key}', value=role_list, inline=True)

        try:
            event.channel.send_message(embed=embed)
        except APIException:  # e.g. missing permissions
            event.author.open_dm().send_message(embed=embed)
        finally:
            event.msg.delete()

    @Plugin.command('kick', '<guild:snowflake>')
    @helpers.is_commander
    def kick(self, event, *, guild):
        """
        Removes me from a given guild.

        You must provide the guild as a snowflake ID number for this to work, as the developer is too lazy to do it \\
        any other way.

        To find out the snowflake, you can run `whereami` and this will list the snowflakes for each guild I am in.

        This is only runnable by a valid commander.
        """
        try:
            if guild in self.state.guilds:
                guild_obj = self.state.guilds[guild]
                guild_obj.leave()
                event.author.open_dm().send_message(f'I successfully left {guild_obj.name}')
            else:
                event.author.open_dm().send_message(f'I could not find a guild with ID {guild}')
        except APIException as ex:
            event.author.open_dm().send_message(f'Something has gone wrong and a {ex} has occurred.')
        finally:
            event.msg.delete()

    @Plugin.command('invite')
    @helpers.is_commander
    def invite(self, event):
        """
        Generates a link to use to invite me to a new guild.

        This is sent to you via DM.

        This is only runnable by a valid commander.
        """
        url = helpers.generate_invite(katconfig.config.client_id, plugins.get_required_permissions())
        event.msg.delete()
        event.author.open_dm().send_message(f'Here is a link to invite me:\n\n{url}')

    @Plugin.command('status', '<status:str>')
    @helpers.is_commander
    def status(self, event, *, status):
        """
        Changes visibility of the bot.

        This can be one of four values:
        - `online` for Online (green).
        - `away` for Away/AFK (yellow).
        - `dnd` for Do Not Disturb (red).
        - `invisible` for Offline/Invisible (grey).

        This is only runnable by a valid commander, and will be reset if the bot is restarted.
        """

        uc_str_status = status.upper().strip()

        if uc_str_status not in ('ONLINE', 'AWAY', 'DND', 'INVISIBLE'):
            event.channel.send_message(f'{status} is an invalid visibility state.')
        else:
            self.client.update_presence(status=user.Status.get(uc_str_status))
            event.msg.delete()
