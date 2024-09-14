# 데이터베이스 관련 함수

import discord
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class warning:

    database_token = credentials.Certificate('plugin/database_token.json')
    firebase_admin.initialize_app(database_token, {
        'databaseURL': 'https://tidocity-486f5-default-rtdb.firebaseio.com/'
    })

    user_id = 000000000000

    def __init__(self, user: discord.User):
        print(f"[{os.path.basename(__file__)}] {user.display_name}({user.id})의 경고 데이터 요청")
        self.user_id = user.id

    def get_info(self) -> dict:
        database = db.reference(f"Users/{self.user_id}/Warning")
        if database.get() is None:  # 경고 데이터가 없다면 기본값으로 초기화
            self.clear_data()
            database = db.reference(f"Users/{self.user_id}/Warning")
        return dict(database.get())

    def get_value(self) -> int:
        data = self.get_info()
        return data["Point"]

    def get_all_reason(self) -> list:
        data = self.get_info()
        return data["Reason"]

    def get_last_reason(self) -> str:
        data = self.get_info()
        reasons = data["Reason"]
        return reasons[len(reasons)-1]

    def add(self, value: int, reason: str) -> None:
        current_warn_value = self.get_value()
        new_warn_value = current_warn_value + value

        reasons = self.get_all_reason()
        reasons.append(f"({value}) {current_warn_value}P -> {new_warn_value}P : {reason}")

        new_data = {
            "Point": new_warn_value,
            "Reason": reasons
        }

        database = db.reference(f"Users/{self.user_id}/Warning")
        database.update(new_data)
        return

    def clear_data(self) -> None:
        database = db.reference(f"Users/")
        default_data = {
            f"{self.user_id}": {
                "Warning": {
                    "Point": 0,
                    "Reason": ["None"]
                }
            }
        }
        database.update(default_data)
        return
