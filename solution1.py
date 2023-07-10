import pandas as pd
from copy import deepcopy
from tabulate import tabulate


processed = {
    'welcome': 0,
    'score_increased': 0,
    'score_decreased': 0,
    'constant_score': 0
}

delivery_rate = deepcopy(processed)
open_rate = deepcopy(processed)
click_rate = deepcopy(processed)


# Read data.csv file
df = pd.read_csv('task/data.csv')[['user_id', 'message_id', 'event', 'subject']]

# Filtering data by user column
df = df.dropna(subset=['user_id'])

# Filtering data by the necessary categories of mails
df = df[df['event'].isin(['processed', 'delivered', 'open', 'click'])]

# Array of unique mails
messages_dict = df.groupby('message_id')[['subject']].first()


def message_to_category(message: str) -> str:
    """The function replaces the text of the mail with its category"""
    if 'scorul tău este' in message:
        return 'constant_score'
    elif 'crescut' in message:
        return 'score_increased'
    elif 'scăzut' in message:
        return 'score_decreased'
    else:
        return 'welcome'


# Replacing text with a category
messages_dict['subject'] = messages_dict['subject'].apply(message_to_category)

# Dictionary of message categories
messages_category = messages_dict['subject'].to_dict()


# Data collection
users_data = {}
for row in df[['user_id', 'message_id', 'event']].itertuples():
    user = row.user_id
    message_id = row.message_id
    event = row.event
    category = messages_category[message_id]
    if not users_data.get(user):
        users_data[user] = {message_id: {'events': {event}, 'category': category}}
    if not users_data[user].get(message_id):
        users_data[user][message_id] = {'events': {event}, 'category': category}
    else:
        users_data[user][message_id]['events'].add(event)


def category_calculator(categ, ev_count):
    """The function calculates the number of categories"""
    match ev_count:
        # corresponds to the category "processed"
        case 1:
            processed[categ] += 1
        # corresponds to the category "delivered"
        case 2:
            processed[categ] += 1
            delivery_rate[categ] += 1
        # corresponds to the category "open"
        case 3:
            processed[categ] += 1
            delivery_rate[categ] += 1
            open_rate[categ] += 1
        # corresponds to the category "click"
        case 4:
            processed[categ] += 1
            delivery_rate[categ] += 1
            open_rate[categ] += 1
            click_rate[categ] += 1


# Parse data
for user in users_data.values():
    for message_id in user.values():
        category = message_id['category']
        event_count = len(message_id['events'])
        match category:
            case 'welcome':
                category_calculator('welcome', event_count)
            case 'score_increased':
                category_calculator('score_increased', event_count)
            case 'score_decreased':
                category_calculator('score_decreased', event_count)
            case 'constant_score':
                category_calculator('constant_score', event_count)

# Create result DataFrame
result_df = pd.DataFrame({'processed': processed,
                          'delivery_rate': delivery_rate,
                          'open_rate': open_rate,
                          'click_rate': click_rate})

# Percentage calculation by category
result_df['delivery_rate'] = round(result_df['delivery_rate'] / result_df['processed'] * 100, 2)
result_df['open_rate'] = round(result_df['open_rate'] / result_df['processed'] * 100, 2)
result_df['click_rate'] = round(result_df['click_rate'] / result_df['processed'] * 100, 2)

# Result table
print(tabulate(result_df, headers='keys', tablefmt='fancy_grid'))
