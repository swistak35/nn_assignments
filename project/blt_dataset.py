import numpy as np
import json
import string
import dateutil.parser
import operator
import warnings
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

events_file_name = "../datasets/events1.json"

CATEGORIES = [
    'music',
    'food',
    'entertainment',
    'nightlife',
    'theatre',
    'arts',
    'sports',
    'outdoors',
    'conferences',
    'courses',
    'charity',
    'attraction',
    'exhibition',
    'talks',
#     'other_stuff',
]

def flattener(left, right):
    try:
        res = reduce(flattener, right, left)
    except TypeError:
        left.append(right)
        res = left
    return res

def flatten(seq):
    return reduce(flattener, seq, [])

def cleanup_text(text):
    new_text = text.lower()
    new_text = BeautifulSoup(text, "lxml").get_text()
    new_text = ''.join(c for c in new_text if c not in string.punctuation)
    new_text = ''.join(c for c in new_text if c not in '0123456789')
    new_text = ' '.join(new_text.split())
    return new_text

def get_yday(date):
    return date.timetuple().tm_yday

def attrs_from_date(date):
    return [
        date.weekday(),
        # odleglosci tego dnia od najblizszego 1.01, 1.02, ...
        #
    ]

def is_weekend(date):
    return (date.weekday() in [5,6])

def export_events_json_data(infile, early_stop = None):
    events_json = []
    with open(infile, 'r') as reader:
        for line in reader:
            event = json.loads(line, encoding = 'utf-8')

            if (event['category'] in CATEGORIES):
                if event['state'] != 'draft':
                    events_json.append(event)

            if early_stop and len(events_json) > early_stop:
                break
    return events_json

def export_events_data(infile,
        early_stop = None):
    events_json = export_events_json_data(infile, early_stop = early_stop)
    events = []
    for event in events_json:
        category = event['category']
        created_at = dateutil.parser.parse(event['created_at'])
        starts_at = dateutil.parser.parse(event['starts_at'])
        ends_at = dateutil.parser.parse(event['ends_at'])
        tt_prices = [float(tt['price']) for tt in event['ticket_types_info']]
        tt_quantities = [float(tt['quantity']) for tt in event['ticket_types_info']]
        tt_types = [tt['type'] for tt in event['ticket_types_info']]

        events.append({
            'description': cleanup_text(event['description']),
            'title': cleanup_text(event['name']),
            'category': CATEGORIES.index(event['category']),
            'attrs_bool': [
                event['seating_enabled'],
                event['public'],
                is_weekend(created_at),
                is_weekend(starts_at),
                is_weekend(ends_at),
            ],
            'attrs_scale01': flatten([
                attrs_from_date(created_at),
                attrs_from_date(starts_at),
                attrs_from_date(ends_at),
                (ends_at - starts_at).days, # event's span in days
                len(tt_types),
                np.sum([typ == 'PayTicketType' for typ in tt_types]),
                np.sum([typ == 'FreeTicketType' for typ in tt_types]),
                np.sum([typ == 'AttendanceTicketType' for typ in tt_types]),
                np.sum([typ == 'DonationTicketType' for typ in tt_types]),
            ]),
            'attrs_logscale01': [
                event['seats'],
                (0.0 if tt_prices == [] else np.max(tt_prices)), # max_tt_price
                (0.0 if tt_prices == [] else np.min(tt_prices)), # min_tt_price
                (0.0 if tt_prices == [] else np.mean(tt_prices)), # avg_tt_price
                np.sum(tt_quantities),
            ],
        })

    return events
