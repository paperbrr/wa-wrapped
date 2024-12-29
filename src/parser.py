from message import Message
import re


class Parser:

    _MESSAGE_CONTAINER = None
    _EXP_IOS = re.compile(r'(\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2}\u202F?(?:\s?[aApP][mM])?\]\s?~?\s?(?:\+?\d{1,3}\s?\d+|[^\:]+):)')
    _EXP_ANDROID = re.compile(r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\u202F?(?:[aApP][mM])?\s-\s(?:\+?\d{1,3}\s?\d+|[^\:]+):)')

    @staticmethod
    def parse_file(file_lines):

        l_file_lines = len(file_lines)
        for i in range(l_file_lines):
            line = file_lines[i]
            line = line.strip('\n')
            match_IOS = Parser._EXP_IOS.search(line)
            match_ANDROID = Parser._EXP_ANDROID.search(line)

            if match_IOS:
                info_end_index = match_IOS.end() + 1
                message_info = line[:info_end_index]
                message_content = line[info_end_index:]
                message = Message(message_info, message_content, os='IOS')
                Parser._MESSAGE_CONTAINER.add_message(message)

            elif match_ANDROID:
                info_end_index = match_ANDROID.end() + 1
                message_info = line[:info_end_index]
                message_content = line[info_end_index:]
                message = Message(message_info, message_content, os='ANDROID')
                Parser._MESSAGE_CONTAINER.add_message(message)

            else:
                if len(Parser._MESSAGE_CONTAINER._messages) > 0:
                    last_message = Parser._MESSAGE_CONTAINER._messages[-1]
                    last_message.content += f' {line} '

        return True