from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'initial_points': 50,
    'participation_fee': 0.25,
    'min_players_start': 4,
    'num_interactions': 4,
    "wait_to_skip": 30,
    "timeout":30,
    'compensation_units': 50,
    'pay_for_waiting': 7/3600,
    'max_pay_for_waiting': 3.,
    'REAL_WORLD_CURRENCY_DECIMAL_PLACES': 2,
    'quiz_bonus': 0.5,
    'doc': "",
}

mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Multiplayer decision making experiment',
    'description': 'Earn a bonus ($2-$3 on average) in this 10 to 20 minute experiment.',
    'frame_height': 700,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 40,
    'expiration_hours': 2,
    'qualification_requirements': [
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThan",
            'IntegerValues': [95]
        },
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{
                'Country': "US",
            }]
        }
    ]
}

SESSION_CONFIGS = [
    {
       'name': 'full',
       'display_name': "Full experiment",
       'num_demo_participants': 6,
       'app_sequence': ['lobby', 'waiting', 'pd'],
    },
    {
       'name': 'only_games',
       'display_name': "Only Games",
       'num_demo_participants': 6,
       'min_players_start': 4,
       'app_sequence': ['waiting', 'pd'],
    },
    {
        'name': 'bots',
        'display_name': "Bots",
        'user_browser_bots': True,
        'num_demo_participants': 4,
        'min_players_start': 4,
        'app_sequence': ['lobby', 'waiting', 'pd'],
    }
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '!8=wtrajrj+gu-=pg6wd^!f-^rk$mj%$dob)yvl+0s+b#80vm_'

DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
