import json
import os


# JSON파일의 경로를 받아서 JSON파일을 딕셔너리 형태의 데이터를 반환하는 함수
def get_data(url: str) -> dict:
    json_data = json.load(open(url, encoding="utf-8"))
    return dict(json_data)
