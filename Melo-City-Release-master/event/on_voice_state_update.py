import discord
import os

from discord.ext import commands
from function import json

"""
1. 유저가 음챗에 있다가 다른 음챗으로 이동하는 건 None으로 인식 안됨
2. 유저가 나가면 member.voice None
"""


def enable(bot: discord.ext.commands.Bot):

    voice = json.get_data("setting.json")["Server"]["Channel"]["Voice"]
    new_channels = []

    @bot.event
    async def on_voice_state_update(
            member: discord.member.Member,
            before: discord.member.VoiceState,
            after: discord.member.VoiceState
    ):

        if member.bot:
            return

        def is_user_joined():
            if member.voice is None:
                return False
            else:
                return True

        def is_autochannel_category_channel():
            channel_ids = voice["State_IDs"]  # 순서대로 0, adult
            try:
                return member.voice.channel.id in channel_ids
            except:
                return False

        """def get_user_joined_vc():
             유저가 입장한 음챗 반환
                유저가 퇴장할 시 None 반환
            if is_user_joined():
                return after.channel
            else:
                return None"""

        def get_user_left_vc():
            """ 유저가 퇴장한 음챗 반환
                유저가 입장할 시 None 반환 """
            if is_user_joined():
                return None
            else:
                return before.channel

        async def clone_channel():
            vc_name = f"💬 {member.display_name} ({member.id})"
            return await member.voice.channel.clone(name=vc_name)

        async def delete_no_user_channel():
            for channel in new_channels:
                if not channel.members:
                    try:
                        await channel.delete()
                    except:
                        new_channels.remove(channel)

        user_joined = is_user_joined()
        left_vc = get_user_left_vc()

        await delete_no_user_channel()

        if user_joined:
            vc_role = member.guild.get_role(940447541617639475)
            try:
                await member.add_roles(vc_role, reason="사용자 지정 보이스채널")
            except:
                pass

            if not is_autochannel_category_channel():  # 지정된 채널이 아닐 경우 무시
                return

            new_channel = await clone_channel()

            await member.move_to(new_channel)
            new_channels.append(new_channel)
        else:
            vc_role = member.guild.get_role(940447541617639475)
            try:
                await member.remove_roles(vc_role, reason="사용자 지정 보이스채널")
            except:
                pass

            if left_vc.category.id != voice["Category"]:
                # 음챗 카테고리 속 채널이 아닐 경우 무시
                return

            if not left_vc.members:  # 아무도 없다면
                if is_autochannel_category_channel():
                    return
                try:
                    if not is_autochannel_category_channel():
                        await left_vc.delete()
                except:
                    pass
                try:
                    new_channels.remove(left_vc)
                except:
                    pass

    print(f"[{os.path.basename(__file__)}] 활성화됨")
