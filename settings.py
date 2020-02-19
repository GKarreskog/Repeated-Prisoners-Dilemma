from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.02,
    'initial_points': 50,
    'participation_fee': 1.,
    'min_players_start': 6,
    'num_interactions': 4,
    "wait_to_skip": 180,
    "timeout":20,
    "timeout_mins":20,
    'compensation_units': 50,
    'pay_for_waiting': 7/3600,
    'max_pay_for_waiting': 5.,
    'REAL_WORLD_CURRENCY_DECIMAL_PLACES': 2,
    'quiz_bonus': 0.,
    'base_points': 2,
    'doc': "",
    "mturk_hit_settings": {
        'keywords': ['bonus', 'study', 'experiment'],
        'title': 'Multiperson decision making experiment with large bonus',
        'description': 'Earn a large bonus, in this 20-50 minute experiment. Total hourly wage has been between $11-$17/hour in previous sessions.',
        'frame_height': 700,
        'template': 'global/mturk_template.html',
        'minutes_allotted_per_assignment': 100,
        'expiration_hours': 2,
        'grant_qualification_id': '3EZ90CUA4RK0VSYFM17NZ8UO4BLIWL',
        'qualification_requirements': [
            {
                'QualificationTypeId': '3EZ90CUA4RK0VSYFM17NZ8UO4BLIWL',
                'Comparator': 'DoesNotExist',
            },
            # {
            #     'QualificationTypeId': "000000000000000000L0",
            #     'Comparator': "GreaterThan",
            #     'IntegerValues': [95]
            # },
            # {
            #     'QualificationTypeId': "00000000000000000071",
            #     'Comparator': "EqualTo",
            #     'LocaleValues': [{
            #         'Country': "US",
            #     }]
            # }
        ]
    }
}


SESSION_CONFIGS = [
    {
       'name': 'full',
       'display_name': "Full experiment",
       'num_demo_participants': 6,
       'min_players_start': 4,
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
        'num_demo_participants': 8,
        "timeout_mins":0.1,
        'min_players_start': 6,
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
