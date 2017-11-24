import random

from disco.bot import Plugin
from disco.types import message
from kat.utils import helpers


class Help(Plugin):

    @Plugin.command('help')
    def help(self, event):
        """
        `help <command>`
        Shows help for a given command.

        `help`
        Lists all available commands. These will likely include commands that you __do not__ have access to.

        This command is runnable by any user.
        """

        if event.args:
            self.__help_detail(event, ' '.join(event.args))
        else:
            self.__help_outline(event)

        event.msg.delete()

    def __help_outline(self, event):
        self.log.debug('Outlining help.')

        embed = message.MessageEmbed()
        embed.title = 'Available commands'
        embed.description = ('These commands may not be accessible by you.\n\n' 
                             'To find out more, run `help <command>` where `<command>` is a valid command name.')

        command_list = ''

        for command in sorted(self.bot.commands, key=lambda c: c.name):
            command_list += f'- `{command.name}`\n'

        if not command_list.strip():
            command_list = 'No commands implemented or found!'

        embed.add_field(name='Commands', value=command_list)

        # Add random accent colour.
        embed.color = random.randint(0x0, 0xFFFFFF)

        event.channel.send_message(embed=embed)

    def __help_detail(self, event, command):
        self.log.debug(f'Detailing help for command {command}.')

        actual_command = helpers.find(lambda c: c.name.lower() == command.lower(), self.bot.commands)

        if actual_command is None:
            event.channel.send_message(f'Could not find any command named `{command}`')
        else:
            embed = message.MessageEmbed()
            embed.title = f'Documentation for `{command}`'

            description = ''

            # Removes the shit indentation that the docstrings create... Stupid python.
            for line in actual_command.get_docstring().split('\n'):
                strip_ln = line.strip()

                # Allows us to put '\' at the end of a line to escape the newline. We instead append a space.
                if strip_ln.endswith('\\'):
                    # Remember to r-strip any spaces away after removing the delimiter
                    description += strip_ln[:-1].rstrip()
                    description += ' '
                else:
                    description += strip_ln
                    description += '\n'

            embed.description = description

            # Add random accent colour.
            embed.color = random.randint(0x0, 0xFFFFFF)

            event.channel.send_message(embed=embed)
