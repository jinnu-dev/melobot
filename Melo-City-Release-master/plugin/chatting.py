from function import json


# 문자열을 입력받아서 특수 기호 및 공백 제거, 소문자로 변환
def delete_special_character(message: str) -> str:
    content = message.lower()
    return ''.join(filter(str.isalnum, content))


class badword:
    used = False
    message = "None"
    detect_type = "None"
    detect_word = "None"

    def __init__(self, message: str) -> None:
        self.message = delete_special_character(message)
        self.update(self.message)
        pass

    # 문자열을 받아서 클래스 상태 업데이트
    def update(self, message: str) -> None:
        badword_data = json.get_data('badword.json')

        for currentType in badword_data:
            if self.used:
                break
            for currrentWord in badword_data[currentType]:
                if currrentWord in message:
                    self.used = True
                    self.detect_type = currentType
                    self.detect_word = currrentWord
                    break


class long_sentence:
    longer = False
    message = "None"

    max_count = 150

    def __init__(self, message: str, max_count: int = 150) -> None:
        self.max_count = max_count  # 값을 전달 받지 않았으면 150
        self.message = message.replace(" ", "")
        self.update(message)
        pass

    # 문자열을 받아서 클래스 상태 업데이트
    def update(self, message: str) -> None:
        if self.max_count < len(message):
            self.longer = True
        else:
            self.longer = False
