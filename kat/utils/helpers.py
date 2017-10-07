def start_typing(bot, channel):
    bot.client.api.channels_typing(channel.id)