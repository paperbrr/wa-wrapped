import re
from utils import add_to_dict_numeric, _12_to_24, get_day_from_num, get_month_from_num
import datetime


class Message:


    _SPECIAL_SEARCHES = []
    _SPECIAL_SEARCH_CASE_SENSITIVE = False
    _BLACKLISTED_WORDS = []
    _MINIMUM_WORD_LENGTH = 5
    _DATE_FORMAT = 'DDMM' 
    

    def __init__(self, info, content, os='ANDROID'):

        self.is_deleted = False
        self.is_edited = False
        self.has_media = False

        self.info = info
        self.content = content

        self.date_sent, self.day_sent, self.month_sent, self.year_sent, self.hour_sent, self.minute_sent, self.author = self.extract_info(os=os)
        self.word_map, self.mention_map, self.emojis_map, self.special_searches_map, self.length = self.parse_content()
        self.emoji_counts = {}


    def extract_info(self, os='ANDROID'):

        _INFO_EXP_IOS = re.compile(r'\[(\d{1,2})/(\d{1,2})/(\d{2,4}), (\d{1,2}):(\d{2}):\d{2}\u202F?(?:\s?([aApP][mM]))?\]\s?~?\s?([^\:]+):')
        _INFO_EXP_ANDROID = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{2,4}), (\d{1,2}):(\d{2})\u202F?(?:([APap][mM]))?\s-\s([^\:]+):')
        _INFO_EXP = _INFO_EXP_ANDROID if os == 'ANDROID' else _INFO_EXP_IOS

        match = _INFO_EXP.search(self.info)
        day, month, year, hour, minute, am_pm, author = match.groups()
        day, month, year, hour, minute = int(day), int(month), int(year), int(hour), int(minute)
        if year < 100: year += 2000

        if Message._DATE_FORMAT == 'MMDD': day, month = month, day              #fix this?
        if am_pm == 'PM' or am_pm == 'pm': hour = _12_to_24(hour)
        
        try:
            date = datetime.datetime(year, month, day)
        except ValueError:
            Message._DATE_FORMAT = 'MMDD'
            day, month = month, day
            date = datetime.datetime(year, month, day)

        day_name = get_day_from_num(date.weekday())
        month_name = get_month_from_num(month)

        return date, day_name, month_name, year, hour, minute, author
    

    def parse_content(self):

        _MEDIA_EXP = r'(?i)\b(?:sticker|image|media|video|document)\s+omitted\b'
        media = re.search(_MEDIA_EXP, self.content)
        if media: 
            self.has_media = True
            return {}, {}, {}, {}, 0

        _DELETE_EXP = r'(?i)\s*(?:<\s*)?This\s+message\s+was\s+deleted\s*(?:\.\s*|\s*)?(?:\s*>)?'
        delete_check = re.search(_DELETE_EXP, self.content)
        if delete_check:
            self.is_deleted = True
            return {}, {}, {}, {}, 0

        _EDIT_EXP = r'(?i)\s*(?:<\s*)?This\s+message\s+was\s+edited\s*(?:\.\s*|\s*)?(?:\s*>)?'
        edit_check = re.search(_EDIT_EXP, self.content)
        if edit_check:
            edit_index = edit_check.start()
            self.content = self.content[:edit_index]
            self.is_edited = True
        
        words = self.content.split()
        length = len(words)
        words_count_map = {}
        for word in words:
            word = word.strip()
            word = word.strip('\',".!-:()_<>[]\/?')
            word = word.lower()
            if ((len(word) >= Message._MINIMUM_WORD_LENGTH) and (word[0] != '@')) and (word not in Message._BLACKLISTED_WORDS):
                add_to_dict_numeric(words_count_map, word)

        mentions_map = {}
        _MENTION_EXP = re.compile(r'@(\+?\d{10,15})')
        mentions = _MENTION_EXP.findall(self.content)
        for mention in mentions:
            mention = mention.strip()
            mention = mention.strip('(),.:/\[];<>!')
            add_to_dict_numeric(mentions_map, mention)

        emojis_map = {}
        _EMOJI_EXP = re.compile(r'[\U0001F600-\U0001F64F' r'\U0001F300-\U0001F5FF' ']', flags=re.UNICODE)
        emojis = _EMOJI_EXP.findall(self.content)
        for emoji in emojis:
            add_to_dict_numeric(emojis_map, emoji)

        special_searches_map = {}
        for search_key in Message._SPECIAL_SEARCHES:
            _SEARCH_EXP = r'\b' + f'{search_key}' +r'\b'
            if not Message._SPECIAL_SEARCH_CASE_SENSITIVE: _SEARCH_EXP = r'(?i)' + _SEARCH_EXP
            # print(_SEARCH_EXP)
            occurrences = re.findall(_SEARCH_EXP, self.content)
            l_occurrences = len(occurrences)
            for i in range(l_occurrences):
                add_to_dict_numeric(special_searches_map, search_key)


        return words_count_map, mentions_map, emojis_map, special_searches_map, length