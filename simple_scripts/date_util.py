''' Usage Example

>>> from util import add_one_month
>>> dates_str =['1970/1/31', '2018/12/31']
>>> print('Input:', dates_str)
Input: ['1970/1/31', '2018/12/31']
>>> print('Output:', [add_one_month(d) for d in dates_str])
Output: ['1970/2/28', '2019/1/31']

'''

from datetime import datetime
from calendar import monthrange

def add_one_month(date_str, zero_pad=False):
    # Convert the string to a datetime object
    date = datetime.strptime(date_str, '%Y/%m/%d')

    # Calculate new values for the year, month and day
    new_year = date.year + date.month // 12
    new_month = date.month % 12 + 1
    new_day = min(date.day, monthrange(new_year, new_month)[1])
    new_date = date.replace(year= new_year, month= new_month, day= new_day)

    # Convert it back to string and return
    if zero_pad:
        return datetime.strftime(new_date, '%Y/%m/%d')
    else:
        return datetime.strftime(new_date, '%Y/%m/%d').replace('/0','/')

if __name__ == '__main__':
    dates_str =['1970/1/31', '2018/12/31']
    print('Input:', dates_str)
    print('Output:', [add_one_month(d) for d in dates_str])
