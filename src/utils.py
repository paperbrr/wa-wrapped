def _12_to_24(hour):

    hour = hour + 12
    return hour


def add_to_dict_numeric(d, key):

    if key in d:
        d[key] += 1
    else:
        d[key] = 1


def merge_dicts_numeric(d1, d2):

    # merges d2 into d1, fix?!?

    for k, v in d2.items():
        if k in d1:
            d1[k] += v
        else:
            d1[k] = v


def get_day_from_num(n):

    days_num_map = {0 : 'Monday',
                    1 : 'Tuesday',
                    2 : 'Wednesday', 
                    3 : 'Thursday',
                    4 : 'Friday',
                    5 : 'Saturday',
                    6 : 'Sunday'}
    
    return days_num_map[n]


def get_month_from_num(n):

    months_num_map = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    return months_num_map[n]


class SortedListFinite:


    def __init__(self, length):

        self.length = length
        self.list = []


    def find_insert_index(self, val):

        left = 0
        i = -1
        right = len(self.list) - 1

        while left <= right:
            mid = int((left + right)/2)
            if self.list[mid] == val:
                i = mid
                break
            elif self.list[mid] < val:
                right = mid - 1
            elif self.list[mid] > val:
                left = mid + 1
            if left > right:
                i = right + 1

        return i


    def insert(self, val):

        if val in self.list: return
        insert_index = self.find_insert_index(val)
        self.list.insert(insert_index, val)
        if len(self.list) > self.length: self.list.pop()


    def print_list(self):

        print(self.list)


def add_to_dict_finite_sorted(d, k, v):

    if k in d:
        d[k].insert(v)
    else:
        d[k] = SortedListFinite(3)
