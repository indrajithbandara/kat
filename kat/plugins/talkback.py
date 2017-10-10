from disco.api.http import APIException
from disco.bot import Plugin
from kat.utils import katconfig
from kat.utils import helpers
from time import sleep

import collections

# Maximum number of messages to remember.
MAX_QUEUE_SIZE = 100


class TalkBack(Plugin):
    prefix = katconfig.config.my_name
    commanders = katconfig.config.commanders
    message_dequeue = collections.deque()

    @Plugin.listen('MessageCreate')
    @helpers.is_in_guild
    @helpers.is_commander
    def on_message(self, event):
        """If we get a message and it is from a commander with our name prefix, parrot the message back to them."""
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

            sleep(0.05 * len(content) + 1.2)

            msg = event.channel.send_message(content)

            # Add this to our queue, this allows deletion later quickly!
            self.message_dequeue.append(msg)

            # Trim the queue
            if len(self.message_dequeue) > MAX_QUEUE_SIZE:
                # Remove the oldest message
                self.message_dequeue.popleft()

    @Plugin.listen('MessageDelete')
    def on_message_delete(self, event):
        """If a message is deleted and it is in our queue, remove it, this prevents errors later."""
        msg = helpers.find(lambda m: m.id == event.id, self.message_dequeue)

        # Todo, check
        if msg is not None:
            self.log.info('Someone deleted a message in my backqueue. I will remove it from the queue.')
            self.message_dequeue.remove(msg)

    @Plugin.command('delete')
    @helpers.is_commander
    def delete(self, event):
        """
        Deletes the most recent message I have sent using the `Name: text` syntax.

        I store up to the last 100 messages sent. If I shut down for any reason, this list is reset. Any messages that have had more than 100 messages sent since cannot be deleted by this command.

        This is only runnable by a valid commander.
        """
        if len(self.message_dequeue) > 0:
            self.log.info('Attempting to delete most recent message.')
            try:
                self.message_dequeue.append(self.message_dequeue.pop().delete())
                self.log.info('Deleted message successfully.')
            except APIException as ex:
                self.log.warning('I couldn\'t delete said message. I might not have permission, or the message may '
                                 f'have already been deleted. The error message was {ex.msg}.')
            finally:
                event.msg.delete()

    @Plugin.command('edit', '<text:str...>')
    @helpers.is_commander
    def edit(self, event, *, text):
        """
        Edits the most recent message I sent via the `Name: text` syntax. Whatever is given after this command will be interpreted as the replacement message. Be warned, this cannot be undone.

        I store up to the last 100 messages sent. If I shut down for any reason, this list is reset. Any messages that have had more than 100 messages sent since cannot be edited by this command.

        This is only runnable by a valid commander.
        """

        if len(self.message_dequeue) > 0:
            self.log.info('Attempting to edit most recent message.')
            try:
                self.message_dequeue.pop().edit(text)
                self.log.info('Edited message successfully.')
            except APIException as ex:
                self.log.warning('I couldn\'t edit said message. I might not have permission, or the message may '
                                 f'have already been deleted. The error message was {ex.msg}.')
            finally:
                event.msg.delete()



