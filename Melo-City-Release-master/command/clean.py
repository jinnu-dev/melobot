import os

from discord.ext import commands


def enable(bot: commands.Bot):

    def is_message_manager(message) -> bool:
        return message.author.guild_permissions.manage_messages

    @bot.command()
    async def 청소(ctx, count: int):
        if not is_message_manager(ctx.message):
            return
        await ctx.channel.purge(limit=count+1)
        await ctx.send(f"메시지 {count}개 삭제함", delete_after=5)
        return

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
