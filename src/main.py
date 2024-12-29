from parser import Parser
from messageContainer import MessageContainer
from visualiser import Visualiser
from message import Message
from config import config


def initialise_message_container(file_data):

    mc = MessageContainer()
    Parser._MESSAGE_CONTAINER = mc
    Parser.parse_file(file_data)
    mc.process_messages()

    return mc


def generate_plots(mc):

    progression_stats = mc._message_time_progression_map
    progression_stats_file_name = Visualiser.plot_message_time_progression(progression_stats)

    message_day_map = mc._message_day_map
    message_day_plot_file_name = Visualiser.plot_message_day(message_day_map)

    message_hour_map = mc._message_hour_map
    message_hour_plot_file_name = Visualiser.plot_message_hour(message_hour_map)

    author_message_map = mc._author_message_count_map
    message_author_plot_file_name = Visualiser.plot_author_message_count(author_message_map)

    message_length_map = mc._message_length_map
    messae_length_plot_file_name = Visualiser.plot_message_length_bins(message_length_map)

    mod_map = mc._message_modulation_map
    message_mod_plot_file_name = Visualiser.plot_message_modulations(mod_map)

    emoji_map = mc._emoji_count_map
    message_emoji_plot_file_name = Visualiser.plot_emoji_count(emoji_map)

    special_searches_map = mc._special_searches_map
    if len(special_searches_map) > 0: special_searches_file_name = Visualiser.plot_special_searches(special_searches_map)

    word_map = mc._word_count_map
    message_wordcloud_file_name = Visualiser.plot_word_counts(word_map, special_searches_map)


if __name__ == '__main__':

    file_name = input('file name: ')
    file_data, min_word_len, special_search_words, case_sensitive_search, blacklisted_words = config(file_name)

    Message._MINIMUM_WORD_LENGTH = min_word_len
    Message._SPECIAL_SEARCHES = special_search_words
    Message._SPECIAL_SEARCH_CASE_SENSITIVE = case_sensitive_search
    Message._BLACKLISTED_WORDS = blacklisted_words

    mc = initialise_message_container(file_data)
    generate_plots(mc)