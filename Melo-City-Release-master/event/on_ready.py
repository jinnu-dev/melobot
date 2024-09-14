# 봇이 로그인했을 때 이벤트

import os

from discord.ext.commands import Bot
from function import json

from event import on_component_interaction


def enable(bot: Bot):

    setting = json.get_data("setting.json")

    @bot.event
    async def on_ready():
        output_message = f"[{os.path.basename(__file__)}] 로그인 성공 => {bot.user}, 명령어 접두사 : {bot.command_prefix}"

        dev_channel = bot.get_channel(setting["Server"]["Channel"]["Development"])

        print(output_message)
        await dev_channel.send(output_message)

        while True:
            interaction = await bot.wait_for("button_click")
            if interaction is not None:
                await on_component_interaction.on_component_interaction(bot, interaction)

    print(f"[{os.path.basename(__file__)}] 활성화됨")
