import os

# from discord import Embed, Colour
from discord.ext import commands
# from discord_components import Button, Select, SelectOption

# from function import json


def enable(bot: commands.Bot):

    @bot.command()
    async def set_permission(ctx):
        role = ctx.guild.roles[0]  # everyone
        for channel in ctx.guild.channels:
            await channel.set_permissions(
                role,
                create_instant_invite=True
            )
            print(channel.name, f"초대 링크 생성 권한 허용 완료 ({role})")
        print("모두 처리 완료")

    # color 중 color_name의 색을 임베드에 사용 가능한 변수로 반환
    # def get_embed_color(color_name: str) -> Colour:
    #     color_list = json.get_data("color.json")
    #     color_rgb = color_list[color_name]
    #     return Colour.from_rgb(
    #         r=color_rgb[0],
    #         g=color_rgb[1],
    #         b=color_rgb[2]
    #     )

    # @bot.command()
    # async def setremote(ctx):
    #
    #     embed_color = get_embed_color("Light_Yellow")
    #
    #     embed = Embed(title="VoiceChannel 대시보드",
    #                   description="이 곳에서 음성채널을 관리할 수 었어요",
    #                   color=embed_color)
    #     embed.set_image(url="https://cdn.discordapp.com/attachments/939797813250883594/939804741226090496/15e81451c9648c5f36abbe630518b24d.gif")
    #
    #     await ctx.send(
    #         embed=embed,
    #         components=[
    #             [
    #                 Button(label="인원 제한 +1", custom_id="plus_limit", style=1, emoji="⬆"),
    #                 Button(label="인원 제한 -1", custom_id="minus_limit", style=4, emoji="⬇"),
    #                 Button(label="인원 제한 제거", custom_id="free_limit", style=3, emoji="🆓")
    #             ],
    #             Select(
    #                 placeholder="빠른 인원 제한",
    #                 options=[
    #                     SelectOption(label="1", value=1),
    #                     SelectOption(label="2", value=2),
    #                     SelectOption(label="3", value=3),
    #                     SelectOption(label="4", value=4),
    #                     SelectOption(label="5", value=5)
    #                 ]
    #             ),
    #             Select(
    #                 placeholder="성인 제한 On / Off",
    #                 options=[
    #                     SelectOption(label="On", value=1),
    #                     SelectOption(label="Off", value=0)
    #                 ]
    #             )
    #         ]
    #     )

    print(f"[{os.path.basename(__file__)}] 활성화됨")
