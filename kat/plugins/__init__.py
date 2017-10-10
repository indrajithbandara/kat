# This file is required for the module system to pick this directory up correctly...
# It does not need to contain anything, however.

from kat.utils import helpers
from kat.utils import katconfig
import logging

def get_required_permissions():
    """
    This holds the bitfield representation for the permissions needed to make the bot
    work on a guild. This can be provided as an argument when getting the invite
    URL from the client ID to enforce permissions explicitly.
    """

    return (
        0x00000040 |   # ADD_REACTIONS
        0x00000400 |   # READ_MESSAGES
        0x00000800 |   # SEND_MESSAGES
        0x00002000 |   # MANAGE_MESSAGES
        0x00008000 |   # ATTACH FILES
        0x00010000 |   # READ_MESSAGE_HISTORY
        0x00040000 |   # USE_EXTERNAL_EMOJIS
        0x04000000     # CHANGE_NICKNAME
    )


logging.getLogger('Kat plugins') \
       .info(f'Add me to a guild at {helpers.generate_invite(katconfig.config.client_id, get_required_permissions())}')
