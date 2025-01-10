from enum import Enum
import streamlit as st
from utils import Item, ItemType

class QuestType(Enum):
    KILL = "kill"           # Kill X number of specific enemies
    COLLECT = "collect"     # Collect X number of items
    EXPLORE = "explore"     # Visit specific areas
    UPGRADE = "upgrade"     # Upgrade equipment X times
    BOSS = "boss"          # Defeat specific boss enemies

class QuestStatus(Enum):
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    REWARDED = "rewarded"
    FAILED = "failed"

class Quest:
    def __init__(self, id, title, description, quest_type, requirements, rewards, area=None, min_level=1):
        self.id = id
        self.title = title
        self.description = description
        self.quest_type = quest_type
        self.requirements = requirements
        self.rewards = rewards
        self.status = QuestStatus.AVAILABLE
        self.progress = {}
        self.area = area
        self.min_level = min_level

    def update_progress(self, event_type, event_data):
        """Update quest progress based on events"""
        if self.status != QuestStatus.ACTIVE:
            return
            
        if self.quest_type == QuestType.KILL:
            if event_type == "enemy_killed" and event_data["enemy_name"] in self.requirements["enemies"]:
                enemy_name = event_data["enemy_name"]
                self.progress[enemy_name] = self.progress.get(enemy_name, 0) + 1
                st.toast(f"Quest progress: Killed {enemy_name} ({self.progress[enemy_name]}/{self.requirements['enemies'][enemy_name]})")
                
        elif self.quest_type == QuestType.COLLECT:
            if event_type == "item_collected" and event_data["item_name"] in self.requirements["items"]:
                item_name = event_data["item_name"]
                self.progress[item_name] = self.progress.get(item_name, 0) + 1
                st.toast(f"Quest progress: Collected {item_name} ({self.progress[item_name]}/{self.requirements['items'][item_name]})")
                
        elif self.quest_type == QuestType.EXPLORE:
            if event_type == "area_visited" and event_data["area"] in self.requirements["areas"]:
                area = event_data["area"]
                self.progress[area] = True
                st.toast(f"Quest progress: Explored {area}")
                
        elif self.quest_type == QuestType.BOSS:
            if event_type == "enemy_killed" and event_data["enemy_name"] == self.requirements["boss"]:
                self.progress["boss_killed"] = True
                st.toast(f"Quest progress: Defeated {self.requirements['boss']}!")
        
        # Check if quest is complete after progress update
        if self.is_complete():
            self.status = QuestStatus.COMPLETED
            st.toast(f"Quest completed: {self.title}! Return to quest board to claim rewards.")

    def check_requirements(self, warrior):
        """Check if warrior meets level and area requirements"""
        return warrior.level >= self.min_level

    def is_complete(self):
        """Check if all requirements are met"""
        if self.quest_type == QuestType.KILL:
            for enemy, required in self.requirements["enemies"].items():
                if self.progress.get(enemy, 0) < required:
                    return False
                    
        elif self.quest_type == QuestType.COLLECT:
            for item, required in self.requirements["items"].items():
                if self.progress.get(item, 0) < required:
                    return False
                    
        elif self.quest_type == QuestType.EXPLORE:
            for area in self.requirements["areas"]:
                if not self.progress.get(area, False):
                    return False
                    
        elif self.quest_type == QuestType.BOSS:
            if not self.progress.get("boss_killed", False):
                return False
                
        return True

    def check_completion(self):
        """Check if quest is complete but don't give rewards yet"""
        if self.status != QuestStatus.ACTIVE:
            return False
            
        if self.is_complete():
            self.status = QuestStatus.COMPLETED
            return True
        return False

    def claim_rewards(self, warrior):
        """Claim rewards for completed quest"""
        if self.status != QuestStatus.COMPLETED:
            return "Quest not ready for reward collection!"
        
        # Give rewards
        if "gold" in self.rewards:
            warrior.gold += self.rewards["gold"]
            st.toast(f"Received {self.rewards['gold']} gold!")
        
        if "xp" in self.rewards:
            warrior.experience += self.rewards["xp"]
            st.toast(f"Gained {self.rewards['xp']} experience!")
            
            # Check for level up
            xp_needed = warrior.calculate_xp_needed()
            if warrior.experience >= xp_needed:
                from encounters import level_up_warrior  # Import at function level to avoid circular imports
                level_up_warrior()
                
        if "items" in self.rewards:
            for item_name in self.rewards["items"]:
                item = create_reward_item(item_name)
                warrior.inventory.append(item)
                st.toast(f"Received {item_name}!")
        
        self.status = QuestStatus.REWARDED
        return "Rewards collected!"

    def get_progress_text(self):
        """Get formatted progress text"""
        if self.quest_type == QuestType.KILL:
            progress = []
            for enemy, required in self.requirements["enemies"].items():
                current = self.progress.get(enemy, 0)
                progress.append(f"{enemy}: {current}/{required}")
            return ", ".join(progress)
            
        elif self.quest_type == QuestType.COLLECT:
            progress = []
            for item, required in self.requirements["items"].items():
                current = self.progress.get(item, 0)
                progress.append(f"{item}: {current}/{required}")
            return ", ".join(progress)
            
        elif self.quest_type == QuestType.EXPLORE:
            areas_visited = sum(1 for area in self.requirements["areas"] if self.progress.get(area, False))
            return f"Areas explored: {areas_visited}/{len(self.requirements['areas'])}"
            
        elif self.quest_type == QuestType.BOSS:
            return "Boss killed" if self.progress.get("boss_killed", False) else "Boss not defeated"
        
        return "Unknown progress"
    
def create_reward_item(item_name):
    """Create an item object from a reward item name"""
    reward_items = {
        "Forest Strength Potion": {
            "cost": 50,
            "effect_type": "strength",
            "effect_value": 2,
            "icon": "💪",
            "type": ItemType.CONSUMABLE,
            "description": "A potion that boosts strength temporarily"
        },
        "Giant's Belt": {
            "cost": 400,
            "effect_type": "strength",
            "effect_value": 8,
            "icon": "🎗️",
            "type": ItemType.ACCESSORY,
            "description": "A massive belt imbued with a giant's power"
        },
        # Add more reward items as needed
    }
    
    if item_name not in reward_items:
        # Default item if name not found
        return Item(
            name=item_name,
            cost=100,
            effect_type="strength",
            effect_value=1,
            icon="📦",
            item_type=ItemType.CONSUMABLE,
            description="A mysterious item"
        )
    
    item_data = reward_items[item_name]
    return Item(
        name=item_name,
        cost=item_data["cost"],
        effect_type=item_data["effect_type"],
        effect_value=item_data["effect_value"],
        icon=item_data["icon"],
        item_type=item_data["type"],
        description=item_data.get("description", "")
    )

# Example quests
FOREST_QUESTS = [
    Quest(
        id="forest_wolves",
        title="Wolf Pack Menace",
        description="Clear out the dangerous wolf pack threatening local travelers.",
        quest_type=QuestType.KILL,
        requirements={"enemies": {"Wolf": 5}},
        rewards={"gold": 100, "xp": 50},
        area="forest",
        min_level=2
    ),
    Quest(
        id="magic_herbs",
        title="Magical Herbs",
        description="Collect healing herbs from the deep forest.",
        quest_type=QuestType.COLLECT,
        requirements={"items": {"Leafy Health Potion": 3}},
        rewards={"gold": 75, "items": ["Forest Strength Potion"]},
        area="forest",
        min_level=1
    ),
    Quest(
        id="forest_exploration",
        title="Forest Explorer",
        description="Explore all areas of the forest to map the region.",
        quest_type=QuestType.EXPLORE,
        requirements={"areas": ["forest_easy", "forest_medium", "forest_hard"]},
        rewards={"gold": 200, "xp": 100},
        area="forest",
        min_level=1
    ),
]

MOUNTAIN_QUESTS = [
    Quest(
        id="frost_giant_hunt",
        title="Frost Giant Hunt",
        description="Track and defeat the mighty Frost Giant terrorizing the mountain passes.",
        quest_type=QuestType.BOSS,
        requirements={"boss": "Frost Giant"},
        rewards={"gold": 300, "xp": 150, "items": ["Giant's Belt"]},
        area="mountain",
        min_level=5
    ),
    # Add more mountain quests...
]