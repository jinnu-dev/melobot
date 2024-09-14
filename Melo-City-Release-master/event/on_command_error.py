import discord

from discord.ext import commands
from function import json


def enable(bot: discord.ext.commands.Bot):

    @bot.event
    async def on_command_error(ctx: discord.ext.commands.Context, error):

        # color 중 color_name의 색을 임베드에 사용 가능한 변수로 반환
        def get_embed_color(color_name: str) -> discord.Colour:
            color_list = json.get_data("color.json")
            color_rgb = color_list[color_name]
            return discord.Colour.from_rgb(
                r=color_rgb[0],
                g=color_rgb[1],
                b=color_rgb[2]
            )

        embed_color = get_embed_color("Light_Red")

        embed = discord.Embed(color=embed_color)
        embed.set_author(name="⛔ 명령어 오류 Command Error")
        embed.add_field(name="💬 사용된 명령어", value=ctx.message.content)
        embed.add_field(name="📝 오류 코드", value=error)
        embed.set_footer(text="개발자 채널에 해당 오류가 전송되었습니다.")

        await ctx.send(embed=embed,
                       delete_after=10)

        embed.set_footer(text=f"{ctx.author}({ctx.author.display_name}) / {ctx.channel}")

        setting = json.get_data("setting.json")
        dev_channel = bot.get_channel(setting["Server"]["Channel"]["Development"])

        await dev_channel.send(embed=embed)

        return 0
