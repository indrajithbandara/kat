from disco.api.http import APIException
from disco.bot import Plugin
from disco.types import message
from kat.utils import helpers
from kat.utils import katconfig
from time import sleep
import random


class Me(Plugin):
    @Plugin.command('nick')
    @helpers.is_commander
    @helpers.is_in_guild
    def nick(self, event):
        """Changes my nickname on the current guild you run this from."""

        args = ' '.join(event.args) if event.args else None
        my_member = event.guild.get_member(self.state.me)

        # Delete the message
        event.msg.delete()

        self.log.info(f'Changing nickname in {event.guild.name} from {my_member.nick} to {args}')

        my_member.set_nickname(args)

    @Plugin.command('nickall')
    @helpers.is_commander
    def nick_all(self, event):
        """Changes my nickname on all guilds I am in."""

        # If not a commander.
        if event.author not in katconfig.config.commanders:
            return

        args = ' '.join(event.args) if event.args else None

        # Delete the message
        event.msg.delete()

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

        reply_message = event.channel.send_message(f'Changed my nickname on {successes}/{total} guilds.')

        sleep(10)

        reply_message.delete()

    @Plugin.command('whereami')
    @helpers.is_commander
    def where_am_i(self, event):
        """Shows a list of guilds I am a member in."""

        event.msg.delete()

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

        event.channel.send_message(embed=embed)

    @Plugin.command('perms')
    @helpers.is_commander
    @helpers.is_in_guild
    def perms(self, event):
        """
        Shows the permissions for the guild you are calling this from for my user.

        If I don't have permission to send messages in the channel you call this from, I will just DM you
        instead (hopefully).
        """

        event.msg.delete()

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

