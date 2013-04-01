"""
Converts JSON data from http://www.yelp.com/dataset_challenge to CSV format.
To use, download the dataset_challenge data and make this repository a
subdirectory.  Then run:

    python yelp_to_csv.py

Output will be in ../yelp_academic_dataset_full.txt
"""
import csv
import json
from datetime import datetime

###
# Define the fields to output
# Column name : function that takes a "joined" review
##/
convert_fields = {
        'review_id': lambda r: r['review_id'],
        'stars': lambda r: r['stars'],
        'characters': lambda r: len(r['text']),
        'words': lambda r: len(r['text'].split()),
        'date': lambda r: datetime.strptime(r['date'], '%Y-%m-%d').strftime('%s'),
        'useful': lambda r: r['votes']['useful'],
        'funny': lambda r: r['votes']['funny'],
        'cool': lambda r: r['votes']['cool'],
        'user_review_count': lambda r: r['user'].get('review_count', 0),
        'user_average_stars': lambda r: r['user'].get('average_stars', 0),
        'user_useful': lambda r: r['user'].get('votes', {}).get('useful', 0),
        'user_funny': lambda r: r['user'].get('votes', {}).get('funny', 0),
        'user_cool': lambda r: r['user'].get('votes', {}).get('cool', 0),
        'biz_stars': lambda r: r['business']['stars'],
        'biz_review_count': lambda r: r['business']['review_count'],
        'biz_open': lambda r: int(r['business']['open'])}


def juxt(*fs):
    """Given a (splatted) list of functions as an argument, return a function
    which takes a single argument and returns a list of the results."""
    return lambda x: [f(x) for f in fs]

###
# main
# Load all of the data, join it, write out in CSV format
##/
print "loading reviews"
with open('../yelp_academic_dataset_review.json', 'rb') as rev_file:
    reviews = map(json.loads, rev_file)

print "loading users"
with open('../yelp_academic_dataset_user.json', 'rb') as rev_file:
    users = map(json.loads, rev_file)
user_by_id = dict((u['user_id'], u) for u in users)

print "loading businesses"
with open('../yelp_academic_dataset_business.json', 'rb') as rev_file:
    businesses = map(json.loads, rev_file)
business_by_id = dict((b['business_id'], b) for b in businesses)

print "joining"
full = (dict(r.items()
             + {'user': user_by_id.get(r['user_id'], {})}.items()
             + {'business': business_by_id.get(r['business_id'], {})}.items())
        for r in reviews)

print "writing result"
with open('../yelp_academic_dataset_full.txt', 'wb') as full_file:
    writer = csv.writer(full_file)
    writer.writerow(convert_fields.keys())
    converter = juxt(*convert_fields.values())
    writer.writerows(converter(r) for r in full)

