from disco.bot import Plugin
from kat.utils import katconfig

import random
import re


class React(Plugin):
    emote_names = katconfig.config.react_emotes
    trigger_words = []
    reaction_emotes = []

    def load(self, ctx):
        regex_list = katconfig.config.react_triggers
        for regex in regex_list:
            # Compile the regex, use multiline and case insensitive matching.
            self.trigger_words.append(re.compile(r'^.*\b%s\b.*?$' % regex, re.I | re.M))

    @Plugin.listen('Ready')
    def on_ready(self, _):
        """Once the bot connection is ready, cache the emotes."""
        self.__re_cache()

    @Plugin.listen('GuildEmojisUpdate')
    def on_emojis_update(self, _):
        """If a guild alters its emoji list, then recache the emotes."""
        self.__re_cache()

    @Plugin.listen('GuildCreate')
    def on_guild_join(self, _):
        """If a guild becomes available, then recache the emotes."""
        self.__re_cache()

    @Plugin.listen('GuildUpdate')
    def on_guild_update(self, _):
        """If a guild is updated, then recache the emotes."""
        self.__re_cache()

    @Plugin.listen('GuildDelete')
    def on_guild_leave(self, _):
        """If a guild is left, or deleted, then recache the emotes."""
        self.__re_cache()

    def __re_cache(self):
        """Regathers the list of emojis we can use."""
        emotes_to_find = []
        emotes_to_find.extend(self.emote_names)

        self.reaction_emotes.clear()

        for guild in self.state.guilds.values():
            for emoji in guild.emojis.values():
                if emoji.name in emotes_to_find:
                    emotes_to_find.remove(emoji.name)
                    self.reaction_emotes.append(emoji)
        self.log.debug(f'Cached {len(self.reaction_emotes)}/{len(self.emote_names)} emotes.')

    @Plugin.listen('MessageCreate')
    def on_message(self, event):
        if event.message.author != self.state.me:
            for regex in self.trigger_words:
                if regex.match(event.message.content):
                    self.log.debug(f'Matched message "{event.message.content}" on pattern "{regex}". Adding reaction.')

                    event.message.add_reaction(random.choice(self.reaction_emotes))
                    return


