import os

from discord import Embed, Colour
from discord.ext import commands

from function import json


def enable(bot: commands.Bot):

    setting = json.get_data("setting.json")

    def get_embed_color(color_name: str) -> Colour:
        color_list = json.get_data("color.json")
        color_rgb = color_list[color_name]
        return Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    @bot.command()
    async def 익명(ctx, *, content):

        channelType = str(ctx.message.channel.type)
        channelName = ctx.author

        anonymous = bot.get_channel(setting["Server"]["Channel"]["Anonymous"])
        log = bot.get_channel(setting["Server"]["Channel"]["Log"]["Anonymous"])

        if channelType == "text":
            await ctx.message.delete()
            channelName = ctx.channel.name
            await ctx.channel.send(content)

        if channelType == "private":
            await anonymous.send()

        embed_color = get_embed_color("Light_Blue")

        embed = Embed(description="전송하신 메시지는 관리 목적을 위하여 관리자 로그에 기록됩니다.\n절대 관리 이외의 용도로 사용되지 않습니다.", color=embed_color)
        await ctx.author.send(embed=embed)

        embed = Embed(color=embed_color)
        embed.set_author(name=f"{ctx.author}가 익명 기능 사용 || {channelName}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="💬 메시지 내용", value=content)
        await log.send(embed=embed)

        return

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
