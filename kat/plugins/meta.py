import platform
import disco
from disco.bot import Plugin
from disco.types import message

from kat import __version__
from kat import __revision__
from kat import __license__
from kat import __author__
from kat import __copyright__
from kat import __credits__
from kat import __maintainer__
from kat import __email__
from kat import __status__
from kat import __date__
from kat import __repository__
from kat.utils import katconfig

version_meta = {
    'License': __license__,
    'Author': __author__,
    'Copyright': __copyright__,
    'Credits': ', '.join(__credits__),
    'Maintainer': __maintainer__,
    'Email': __email__
}

system_meta = {
    'Processor': platform.processor(),
    'Machine': platform.machine(),
    'System': f'{platform.system()} {platform.release()} {platform.version()}',
    'Platform': platform.platform(),
    'disco-py library version': disco.VERSION,
    'Python version': platform.python_version(),
    'Python implementation': platform.python_implementation()
}


class Meta(Plugin):
    @Plugin.command('version')
    def version(self, event):
        """
        Shows versioning information for this bot.
        """

        embed = message.MessageEmbed()

        embed.title = f'{katconfig.config.my_name.title()} is brought to you by:'

        embed.description = (f'Katherine v{__version__}r{__revision__} {__status__}.\n\nReleased on {__date__}.\n\n'
                             f'Repository: {__repository__}')

        embed.set_image(url=self.state.me.avatar_url)

        for key in version_meta.keys():
            value = version_meta[key]
            if not value:
                value = '_Not specified_'
            embed.add_field(name=key, value=value, inline=False)

        for key in system_meta.keys():
            value = system_meta[key]
            if not value:
                value = '_Not specified_'
            embed.add_field(name=key, value=value, inline=True)

        # Purrloin purple.
        embed.color = 0xD200FF

        event.channel.send_message(embed=embed)
        event.msg.delete()
