from disco.bot import Plugin
from kat.utils import katconfig
from kat.utils import helpers
from time import sleep


class TalkBack(Plugin):

    prefix = katconfig.config.my_name
    commanders = katconfig.config.commanders

    @Plugin.listen('MessageCreate')
    def on_message(self, event):
        # If the author is not a commander, or the message is not in a guild, then ignore the message
        if event.message.author.id in self.commanders and event.channel.is_guild:

            content = event.message.content
            lower_content = content.lower()

            # Likewise if the message does not begin with the prefix and :, then ignore it.
            if lower_content.startswith(f'{self.prefix.lower()}:'):
                self.bot.log.info(f'Replying to commander on channel {event.channel} in {event.channel.guild.name}')

                # Remove the prefix from the start of the content
                content = content[len(self.prefix) + 1:].strip()

                # Give the client enough time to resync on mobile devices, otherwise messages will not delete.
                sleep(0.2)

                event.message.delete()

                helpers.start_typing(self.bot, event.channel)

                sleep(0.01 * len(content) + 1.2)

                event.channel.send_message(content)






