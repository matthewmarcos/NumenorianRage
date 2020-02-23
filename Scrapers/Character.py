from collections import namedtuple

Character = namedtuple(
    'Character', 
    ' '.join([
        'url',
        'name',
        'birth_epoch',
        'birth_year',
        'rule_start_year',
        'rule_end_year',
        'death_epoch',
        'death_year',
        'notes']
        )
    )

x = Character(
    name="asd", url="ssss")

print(x)