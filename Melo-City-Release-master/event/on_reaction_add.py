import discord
import os

from discord.ext import commands
from function import json


def enable(bot: discord.ext.commands.Bot):

    def is_vc_owner(voicechannel: discord.VoiceChannel, member: discord.member.Member):
        return str(member.id) in voicechannel.name

    def is_no_owner(voicechannel: discord.VoiceChannel):
        for member in voicechannel.members:
            if str(member.id) in voicechannel.name:
                return False
        return True

    remote_channel_id = json.get_data("setting.json")["Server"]["Channel"]["Voice"]["Remote"]
    remote_message_id = 944092392007561267
    remote_category_id = json.get_data("setting.json")["Server"]["Channel"]["Voice"]["Category"]

    remote_reaction = [
        "⬆",  # 인원 제한 한 명 업
        "⬇",  # 인원 제한 한 명 다운
        "🆓",  # 빠르게 인원 제한 제거
        "2️⃣", "3️⃣", "4️⃣", "5️⃣",  # 빠르게 인원 제한 (2~5)
        "🔒"  # 성인 전용 채널 전환
    ]

    @bot.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):

        vc_dashboard = bot.get_channel(remote_channel_id)
        remote_message = vc_dashboard.get_partial_message(remote_message_id)

        member = payload.member

        if member.bot:
            return

        if payload.message_id == remote_message_id:
            await remote_message.remove_reaction(emoji=payload.emoji, member=payload.member)

            if not member.voice:  # 음챗에 가입하지 않았다면 무시
                return
            if member.voice.channel.category_id != remote_category_id:  # 지정된 카테고리 채널이 아니라면 무시
                return
            if not is_vc_owner(member.voice.channel, member) and not is_no_owner(member.voice.channel):  # 음챗을 만든 사람이 아님과 동시에 혼자가 아니라면 무시
                return

            current_vc_limit = member.voice.channel.user_limit

            reactioned_emoji = str(payload.emoji)

            if reactioned_emoji == remote_reaction[0]:  # 인원 제한 한 명 업
                if 0 <= current_vc_limit < 99:
                    await member.voice.channel.edit(user_limit=current_vc_limit + 1, reason="사용자 지정 보이스채널")
                else:
                    return

            elif reactioned_emoji == remote_reaction[1]:  # 인원 제한 한 명 다운
                if 0 < current_vc_limit <= 99:
                    await member.voice.channel.edit(user_limit=current_vc_limit - 1, reason="사용자 지정 보이스채널")
                else:
                    return

            elif reactioned_emoji == remote_reaction[2]:  # 빠르게 인원 제한 제거
                await member.voice.channel.edit(user_limit=0, reason="사용자 지정 보이스채널")

            elif reactioned_emoji == remote_reaction[3]:  # 빠르게 인원 제한 (2)
                await member.voice.channel.edit(user_limit=2, reason="사용자 지정 보이스채널")

            elif reactioned_emoji == remote_reaction[4]:  # 빠르게 인원 제한 (3)
                await member.voice.channel.edit(user_limit=3, reason="사용자 지정 보이스채널")

            elif reactioned_emoji == remote_reaction[5]:  # 빠르게 인원 제한 (4)
                await member.voice.channel.edit(user_limit=4, reason="사용자 지정 보이스채널")

            elif reactioned_emoji == remote_reaction[6]:  # 빠르게 인원 제한 (5)
                await member.voice.channel.edit(user_limit=5, reason="사용자 지정 보이스채널")

            elif reactioned_emoji == remote_reaction[7]:  # 성인 제한 On / Off
                adult = member.guild.get_role(941497993897586739)
                if adult not in member.roles:
                    return

                resident = member.guild.get_role(913033296043192370)

                vc_permissions = member.voice.channel.overwrites
                resident_permissions = vc_permissions[resident]

                await member.voice.channel.set_permissions(resident,
                                                           connect=not resident_permissions.connect,
                                                           view_channel=True)

            else:
                return

    print(f"[{os.path.basename(__file__)}] 활성화됨")
