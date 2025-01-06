# region_configs.py

FOREST_CONFIG = {
    "name": "forest",
    "required_level": 1,
    "welcome_messages": [
        "*You enter a lush green forest with towering trees and a gentle breeze.*",
        "*Birds sing in the canopy above as you make your way deeper into the forest.*",
    ],
    "areas": [
        ("Sunlit glade", "easy"),
        ("Mossy cave", "medium"),
        ("Steaming forest fissure", "hard")
    ],
    "area_messages": {
        "easy": "*You venture into the peaceful sunlit glade...*",
        "medium": "*You carefully enter the dark mossy cave...*",
        "hard": "*You approach the dangerous steaming fissure...*"
    },
    "side_image": "images/forest_side.png",
    "area_image_prefix": "forest"
}

MOUNTAIN_CONFIG = {
    "name": "mountain",
    "required_level": 5,
    "welcome_messages": [
        "*The air grows thin as you climb higher into the treacherous mountains.*",
        "*Snow crunches under your feet as you navigate the treacherous peaks.*",
    ],
    "areas": [
        ("Craggy slopes", "easy"),
        ("Ice caves", "medium"),
        ("Peak summit", "hard")
    ],
    "area_messages": {
        "easy": "*You begin climbing the rocky slopes...*",
        "medium": "*You enter a freezing ice cave...*",
        "hard": "*You approach the dangerous peak summit...*"
    },
    "side_image": "images/mountain_side.png",
    "area_image_prefix": "mountain"
}