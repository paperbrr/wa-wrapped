import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud
from utils import merge_dicts_numeric


rcParams['font.family'] = 'Segoe UI Emoji'


class Visualiser:


        @staticmethod
        def plot_message_time_progression(_message_time_progression_map):

            plot_name = 'plots/message_time_progression'

            # message progression with months/years
            months = list(_message_time_progression_map.keys())
            values = list(_message_time_progression_map.values())

            plt.figure(figsize=(12, 7))
            plt.plot(months, values, marker='o', linestyle='-', color='b', label='Message Counts')
            plt.title("Monthly Message Count", fontsize=16)
            plt.xlabel("Month", fontsize=14)
            plt.ylabel("Message Count", fontsize=14)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(fontsize=12)
            plt.tight_layout()
            plt.savefig(plot_name)
            plt.close()

            return plot_name


        @staticmethod
        def plot_message_day(_message_day_map):
            
            plot_name = 'plots/message_day'

            # message counts on days of weeks
            values = list(_message_day_map.values())
            days = list(_message_day_map.keys())

            fig, axs = plt.subplots(1, 2, figsize=(12, 6))

            # Line chart
            axs[0].plot(days, values, marker='o', linestyle='-', color='b', label='Daily Values')
            axs[0].set_title("Messages on Days", fontsize=14)
            axs[0].set_xlabel("Days", fontsize=12)
            axs[0].set_ylabel("Messages", fontsize=12)
            axs[0].grid(axis='y', linestyle='--', alpha=0.7)
            axs[0].legend(fontsize=10)

            # Pie chart
            axs[1].pie(values, labels=days, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            axs[1].set_title("Messages on Days: %", fontsize=14)

            plt.tight_layout()
            plt.savefig(plot_name)
            plt.close()

            return plot_name


        @staticmethod
        def plot_message_hour(_message_day_map):

            plot_name = 'plots/message_hour'

            # Message counts on days of weeks
            values = list(_message_day_map.values())
            hours = list(_message_day_map.keys())
            hours_sorted = sorted(hours)
            all_hours = list(range(1, 25))
            all_values = [_message_day_map.get(hour, 0) for hour in all_hours]
            fig, ax1 = plt.subplots(figsize=(12, 6))

            # Line chart
            ax1.plot(all_hours, all_values, marker='o', color='b')
            ax1.set_xlabel("Hours", fontsize=14)
            ax1.set_ylabel("Message Count", fontsize=14)
            ax1.set_title("Messages Sent at Hours", fontsize=16)
            ax1.grid(axis='y', linestyle='--', alpha=0.7)

            # Bar graph
            ax1.bar(all_hours, all_values, alpha=0.5, color='orange')
            ax1.set_xticks(all_hours)
            ax1.legend(fontsize=12)

            plt.tight_layout()
            plt.savefig(plot_name)
            plt.close()

            return plot_name


        @staticmethod
        def plot_author_message_count(_author_message_count_map):

            plot_name = 'plots/author_message_count'

            # Message counts on days of weeks
            total_messages = sum(list(_author_message_count_map.values()))
            min_messages = 0.001 * total_messages
            trimmed_map = {k:v for k,v in _author_message_count_map.items() if v > min_messages}
            others_message_count = sum([i for i in _author_message_count_map.values() if i < min_messages])
            if others_message_count > 0: trimmed_map['Others'] = others_message_count

            users = list(trimmed_map.keys())
            message_counts = list(trimmed_map.values())

            # Horizontal bar graph
            plt.figure(figsize=(12, 8))
            plt.barh(users, message_counts, color='skyblue')
            plt.xlabel("Message Count", fontsize=14)
            plt.ylabel("Users", fontsize=14)
            plt.title("Message Count per User", fontsize=16)
            plt.grid(linestyle='--', alpha=0.7)
            x_tick = int(0.05*max(message_counts)) + 1
            plt.xticks(range(0, max(message_counts) + x_tick, x_tick), fontsize=7)
            plt.yticks(fontsize=12)
            plt.tight_layout()
            plt.savefig(plot_name)
            plt.close()

            return plot_name


        @staticmethod
        def plot_message_length_bins(_message_length_map):

            plot_name = 'plots/message_length_bins'

            # Message length in bins
            keys = list(_message_length_map.keys())
            sorted_keys = sorted(keys)
            values = [_message_length_map[i] for i in sorted_keys]
            for i in range(len(keys) - 1):
                sorted_keys[i] = f'{sorted_keys[i]}-{sorted_keys[i+1]}'
            sorted_keys[-1] = f'{sorted_keys[-1]}+'
            
            total = sum(values)
            percentages = [f"{cat} ({val / total * 100:.1f}%) W.P.M." for cat, val in zip(sorted_keys, values)]

            plt.figure(figsize=(12, 6))
            wedges, _= plt.pie(values, startangle=90)
            plt.legend(wedges, percentages, title="Words per Message", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12)
            plt.title('Message Length Distribution', fontsize=16)
            plt.tight_layout() 
            plt.savefig(plot_name)
            plt.close()
            
            return plot_name

        
        @staticmethod
        def plot_word_counts(_word_count_map, _special_searches_map):

            plot_name = 'plots/wordcloud'
             
            for k, v in _special_searches_map.items():
                _word_count_map[k] = v
            _word_count_map = dict(sorted(_word_count_map.items(), key=lambda x: x[1], reverse=True))
            freq_map = {k:_word_count_map[k] for k in list(_word_count_map.keys())[:len(_word_count_map)]} if len(_word_count_map) < 75 else {k:_word_count_map[k] for k in list(_word_count_map.keys())[:75]}
            
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_map)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(plot_name) 
            plt.close()

            return plot_name
        

        @staticmethod
        def plot_message_modulations(_message_modulation_map):

            plot_name = 'plots/message_modulations'
             
            formal_names = {'nomod': 'No modulation', 'edited': 'Message edited', 'deleted': 'Message deleted'}
            categories = [formal_names[i] for i in list(_message_modulation_map.keys())]
            counts = list(_message_modulation_map.values())

            total = sum(counts)
            percentages = [f'{(count / total) * 100:.1f}%' for count in counts]
            plt.figure(figsize=(12, 6))
            plt.pie(counts, startangle=140, colors=['blue', 'red', 'green'])
            plt.title('Message Modulation Distribution', fontsize=16)
            legend_labels = [f'{category}: {percentage}' for category, percentage in zip(categories, percentages)]
            plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)
            plt.tight_layout()
            plt.savefig(plot_name)
            plt.close()

            return plot_name


        @staticmethod
        def plot_emoji_count(_emoji_count_map):

            plot_name = 'plots/emoji_count'

            # Message counts on days of weeks
            total_occurences = sum(list(_emoji_count_map.values()))
            if total_occurences == 0: return None

            min_occurences = 0.009 * total_occurences
            trimmed_map = {k:v for k,v in _emoji_count_map.items() if v > min_occurences}
            others_occurences_count = sum([i for i in _emoji_count_map.values() if i < min_occurences])
            if others_occurences_count > 0: trimmed_map['Others'] = others_occurences_count

            users = list(trimmed_map.keys())
            occurence_counts = list(trimmed_map.values())

            # Horizontal bar graph
            plt.figure(figsize=(12, 8))
            plt.barh(users,  occurence_counts, color='skyblue')
            plt.xlabel("Occurrences", fontsize=14)
            plt.ylabel("Emojis", fontsize=14)
            plt.title("Emoji Occurrences", fontsize=16)
            plt.grid(linestyle='--', alpha=0.7)
            x_tick = int(0.05*max(occurence_counts)) + 1
            plt.xticks(range(0, max(occurence_counts) + x_tick, x_tick), fontsize=7)
            plt.yticks(fontsize=12)
            plt.tight_layout()
            plt.savefig(plot_name)
            plt.close()

            return plot_name
        

        @staticmethod 
        def plot_special_searches(_special_searches_map):

            plot_name = 'plots/special_searches'

            words = list(_special_searches_map.keys())
            frequencies = list(_special_searches_map.values())
            words_freq = [f'{words[i]} ({frequencies[i]})' for i in range(len(frequencies))]

            # Generate bar chart
            plt.figure(figsize=(10, 6))
            plt.barh(words_freq, frequencies, color='skyblue')
            plt.ylabel('Search Key')
            plt.xlabel('Frequency')
            plt.title('Special Search Frequencies')
            plt.gca().invert_yaxis()  # Invert y-axis to have the highest frequency on top
            plt.tight_layout()
            plt.savefig(plot_name)
            plt.close()

            return plot_name