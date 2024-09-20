import aiohttp
import discord

from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter


def enable(bot: discord.ext.commands.Bot):

    @bot.event
    async def on_message_delete(message: discord.Message):

        def message_has_file(msg: discord.Message):
            if len(msg.attachments) >= 1:
                return True
            else:
                return False

        def message_has_embed(msg: discord.Message):
            if len(msg.embeds) >= 1:
                return True
            else:
                return False

        async def logging_message(channel: str, user: discord.User, text: str, file: discord.File, embed: discord.Embed):

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
                await webhook.send(
                    content=text,
                    username=f"{user}({user})      {channel}",
                    avatar_url=user.avatar_url,
                    file=file,
                    embed=embed
                )
            return 0

        no_log_channel = [
            843629350892208148,  # 관리팀 공지방
            782796263175225374,  # 모더팀 채팅방
            808953456589013002,  # 스태프팀 채팅방
            872806233202122763   # 메시지 삭제 로그 채널
        ]

        # 만일 봇이 보낸 메시지거나 .pick 메시지라면 무시
        if message.author.bot or ".pick" in message.content:
            return

        # 만일 로그를 안할 채널이라면 무시
        if message.channel.id in no_log_channel:
            return 0

        webhook_url = " "

        author = message.author
        channel = message.channel
        content = message.content

        file = None
        embed = None

        if message_has_file(message):
            file = await message.attachments[0].to_file(spoiler=True)

        if message_has_embed(message):
            embed = message.embeds[0]

        await logging_message(
            channel=channel,
            user=author,
            text=content,
            file=file,
            embed=embed
        )

        return 0
