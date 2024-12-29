from utils import add_to_dict_numeric, merge_dicts_numeric, SortedListFinite
from message import Message
import datetime
import matplotlib.pyplot as plt


class MessageContainer:

    # make these configurable
    _NUMBER_MAP = {}


    def __init__(self):
        
        self._messages = []

        # CONFIG
        self._search_after = (30, 4, 2020)

        # AGGREGATE STATS
        self._word_count_map = {}
        self._mention_count_map = {}
        self._emoji_count_map = {}
        self._special_searches_map = {}
        self._message_day_map = {}
        self._message_month_map = {}
        self._message_year_map = {}
        self._message_hour_map = {}
        self._message_time_progression_map = {}
        self._message_length_map = {}
        self._message_modulation_map = {}

        # USER STATS
        self._author_message_count_map = {}
        self._author_top3_active_hours_map = {}
        self._author_top3_active_days_map = {}
        self._author_top5_words_map = {}
        self._author_avg_message_len_map = {}


    def add_message(self, message:Message):
        
        # filter out messages before a set date
        filter_date = datetime.datetime(self._search_after[2], self._search_after[1], self._search_after[0])
        sent_date = message.date_sent
        if sent_date < filter_date: return

        self._messages.append(message)                                              # all messages


    def process_messages(self):

        for message in self._messages:
            
            merge_dicts_numeric(self._word_count_map, message.word_map)             # unique word counts
            merge_dicts_numeric(self._mention_count_map, message.mention_map)       # unique mention counts
            merge_dicts_numeric(self._emoji_count_map, message.emojis_map)          # unique emoji occurrences
            merge_dicts_numeric(self._special_searches_map, message.special_searches_map)

            add_to_dict_numeric(self._message_day_map, message.day_sent)            # message day counts
            add_to_dict_numeric(self._message_month_map, message.month_sent)        # message month counts
            add_to_dict_numeric(self._message_year_map, message.year_sent)          # message year counts
            add_to_dict_numeric(self._message_hour_map, message.hour_sent)          # message hour counts

            add_to_dict_numeric(self._message_length_map, 30 if message.length//10 >= 3 else (message.length//10)*10)        # message length bins
            
            key = f'{message.month_sent[:3]}{message.year_sent}'
            add_to_dict_numeric(self._message_time_progression_map, key)            # message progression with months/years

            if message.is_deleted: add_to_dict_numeric(self._message_modulation_map, 'deleted')                                     # message deleted
            if message.is_edited: add_to_dict_numeric(self._message_modulation_map, 'edited')                                       # message edited
            if (not message.is_deleted) and (not message.is_edited): add_to_dict_numeric(self._message_modulation_map, 'nomod')     # no message modulation

            if not message.is_deleted: add_to_dict_numeric(self._author_message_count_map, message.author)                           # author message count