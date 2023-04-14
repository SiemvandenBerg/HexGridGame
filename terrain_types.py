# terrain_types.py
terrain_types = {
    'grassland': {
        'resources': {
            'wood': 1,
            'food': 2,
            'stone': 0
        },
        'color': (0, 128, 0), # green
        'passable': True,
        'movement_cost': 1
    },
    'swamp': {
        'resources': {
            'wood': 2,
            'food': 1,
            'stone': 0
        },
        'color': (0, 128, 128), # teal
        'passable': True,
        'movement_cost': 1
    },
    'forest': {
        'resources': {
            'wood': 3,
            'food': 1,
            'stone': 0
        },
        'color': (0, 64, 0), # dark green
        'passable': True,
        'movement_cost': 1
    },
    'dark forest': {
        'resources': {
            'wood': 4,
            'food': 0,
            'stone': 0
        },
        'color': (0, 32, 0), # very dark green
        'passable': True,
        'movement_cost': 1
    },
    'hills': {
        'resources': {
            'wood': 1,
            'food': 1,
            'stone': 2
        },
        'color': (128, 128, 0), # olive
        'passable': True,
        'movement_cost': 1
    },
    'mountains': {
        'resources': {
            'wood' :0,
            'food': 0,
            'stone': 3
        },
        'color': (128, 128, 128), # gray
        'passable': False,
        'movement_cost': 999
    },
    'water': {
        'resources': {
            'wood': 0,
            'food': 0,
            'stone': 0
        },
        'color': (0, 0, 128), # blue
        'passable': False,
        'movement_cost': 999
    },
}
