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
    @helpers.Debugging.dump_args
    def perms(self, event):
        pass#me = event.me



