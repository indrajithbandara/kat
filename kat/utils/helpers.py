from kat.utils import katconfig
import logging
import re

__logger = logging.getLogger('helpers')


###############################################################################
#                                                                             #
# DEOBFUSCATOR HELPER FUNCTIONS FOR OTHERWISE ABSTRACT OR "LENGTHY"           #
#   GENERIC ROUTINE OPERATIONS                                                #
#                                                                             #
###############################################################################


def find(predicate, collection):
    """
    Attempts to find a match for the given predicate function in a given collection.

    We return the first match only, or None if no match exists.
    """
    for item in collection:
        if predicate(collection):
            return item
    return None


def find_all(predicate, collection):
    """
    Attempts to find matches for a given predicate across a given collection, yielding
    any results in a generator function that can be cast to a List/Tuple, or iterated
    across.
    """

    for item in collection:
        if predicate(collection):
            yield item


def is_valid_identifier(string: str):
    """
    Determines whether the given string is a valid python identifier or not. If it is,
    we return True, otherwise, we return False.
    """
    valid_first_character = r'[A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02B8]'
    valid_rest = r'[0-9_$A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02B8]*'
    regex = f'^{valid_first_character}{valid_rest}$'

    invalid_tokens = ('False', 'class', 'finally', 'is', 'return', 'None', 'continue',
                      'for', 'lambda', 'try', 'True', 'def', 'from', 'nonlocal', 'while',
                      'and', 'del', 'global', 'not', 'with', 'as', 'elif', 'if', 'or',
                      'yield', 'assert', 'else', 'import', 'pass', 'break', 'except',
                      'in', 'raise', '_', '__',
                      re.compile(f'^__{valid_first_character}{valid_rest}__$', re.U)
                      )

    # Ensure it is a correctly formatted identifier first.
    if not re.match(regex, string, re.U):
        return False

    def pred(x):
        if str(type(x)) == '<class \'_sre.SRE_Pattern\'>':
            return re.match(x, string)
        else:
            return x == string

    return not any(pred(x) for x in invalid_tokens)


def start_typing(bot, channel):
    """Starts the bot typing."""
    bot.client.api.channels_typing(channel.id)


###############################################################################
#                                                                             #
# DECORATORS FOR EVENT HANDLERS                                               #
#                                                                             #
###############################################################################


def is_commander(func):
    """
    Decorator that will only invoke the given event if the context's author is
    in the commanders list of the bot.
    """

    def pred(self=None, event=None, *args, **kwargs):
        author = None

        if hasattr(event, 'author'):
            author = event.author
        elif hasattr(event, 'message'):
            author = event.message.author
        elif hasattr(event, 'msg'):
            author = event.msg.author
        else:
            __logger.error(f'Could not get an author attribute from the event in {func.__name__}. '
                           f'This event interface provides the following members: {dir(event)}. '
                           'Aborting for safety.')
            return

        if author in katconfig.config.commanders:
            __logger.debug(f'In is_commander decorator for {func.__name__}; author {author} IS commander.')
            func(self, event, *args, **kwargs)
        else:
            __logger.debug(f'In is_commander decorator for {func.__name__}; author {author} IS NOT commander.')

    return pred


def is_in_guild(func):
    """
    Decorator that will only invoke the given event if the context is from a valid
    guild, i.e. not from a direct message.
    """

    def pred(self=None, event=None, *args, **kwargs):
        if not hasattr(event, 'guild'):
            __logger.error(f'Could not get guild attribute from the event in {func.__name__}. '
                           f'This event interface provides the following members: {dir(event)}. '
                           'Aborting for safety.')
            return

        if event.guild is not None:
            __logger.debug(f'In is_guild decorator for {func.__name__}; message WAS in valid guild.')
            func(self, event, *args, **kwargs)
        else:
            __logger.debug(f'In is_guild decorator for {func.__name__}; message WAS NOT in valid guild.')

    return pred
