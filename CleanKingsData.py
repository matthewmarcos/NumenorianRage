import csv
import re
from urllib.parse import unquote

INPUT_FILENAME = 'numenorians.psv'
INPUT_HEADERS = [
    'url',
    'referrer',
    'name',
    'other_names',
    'titles',
    'birth_year',
    'rule_start',
    'rule_end',
    'death_year',
    'notable_for'
]
OUTPUT_FILENAME = 'kings_clean.psv'
OUTPUT_HEADERS = [
    'url',
    'referrer',
    'name',
    'other_names',
    'titles',
    'birth_age',
    'birth_year',
    'death_age',
    'death_year',
    'rule_age',
    'rule_year'
]


def extract_date_of_birth(raw_birth_year):
    if(raw_birth_year == ''):
        return ('', '')
    else:
        birth_split = raw_birth_year.split(' ')[:2]
        match = re.match('[0-9]+', birth_split[1])
        return (birth_split[0], match[0] if match else '')


def extract_date_of_death(raw_death_year):
    if(raw_death_year == ''):
        return ('', '')
    else:
        death_split = raw_death_year.split(' ')[:2]
        match = re.match('[0-9]+', death_split[1])
        return (death_split[0], match[0] if match else '')


def extract_date_of_rule(raw_rule_start):
    if(raw_rule_start == ''):
        return ('', '')

    # Extract the age of the ruler
    rule_age = re.findall(
        r'(S\.A\.|T\.A\.|c\. Fo\.A\.)', raw_rule_start)[0]

    years_ruled = [
        int(s) for s in raw_rule_start.split() if s.isdigit()]

    return (rule_age, years_ruled[0] if len(years_ruled) > 0 else '')


def transform_king_data(king):
    birth_age, birth_year = extract_date_of_birth(king['birth_year'])
    death_age, death_year = extract_date_of_death(king['death_year'])
    rule_age, rule_year = extract_date_of_rule(king['rule_start'])

    king['birth_age'] = birth_age
    king['birth_year'] = birth_year
    king['death_age'] = death_age
    king['death_year'] = death_year
    king['rule_age'] = rule_age
    king['rule_year'] = rule_year
    king['url'] = unquote(king['url'])
    king['referrer'] = unquote(king['referrer'])

    return king


def get_king_data():
    with open(INPUT_FILENAME, 'r') as fp:
        reader = csv.reader(fp, delimiter='|')
        for row in reader:
            yield dict(zip(INPUT_HEADERS, row))


def save_profile(profile):
    to_save = {header: profile[header] for header in OUTPUT_HEADERS}

    with open(OUTPUT_FILENAME, 'a+') as fp:
        dict_writer = csv.DictWriter(
            fp, delimiter='|', fieldnames=OUTPUT_HEADERS)
        dict_writer.writerow(to_save)


def main():
    for king in get_king_data():
        # Drop non-kings. Analysis for other Numenorians will be done later.
        if(king['titles'] == ''):
            continue
        returned_king = transform_king_data(king)
        save_profile(returned_king)


if __name__ == '__main__':
    main()
