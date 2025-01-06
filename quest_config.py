# quest_config.py
from enum import Enum

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
    FAILED = "failed"

class Quest:
    def __init__(self, id, title, description, quest_type, requirements, rewards, area=None, min_level=1):
        self.id = id
        self.title = title
        self.description = description
        self.quest_type = quest_type
        self.requirements = requirements  # Dict with requirements
        self.rewards = rewards          # Dict with rewards
        self.status = QuestStatus.AVAILABLE
        self.progress = {}             # Track progress for each requirement
        self.area = area               # Required area for quest
        self.min_level = min_level     # Minimum level requirement
        
    def check_requirements(self, warrior):
        """Check if warrior meets level and area requirements"""
        if warrior.level < self.min_level:
            return False
        return True
    
    def update_progress(self, event_type, event_data):
        """Update quest progress based on events"""
        if self.status != QuestStatus.ACTIVE:
            return
            
        if self.quest_type == QuestType.KILL:
            if event_type == "enemy_killed" and event_data["enemy_name"] in self.requirements["enemies"]:
                enemy_name = event_data["enemy_name"]
                self.progress[enemy_name] = self.progress.get(enemy_name, 0) + 1
                
        elif self.quest_type == QuestType.COLLECT:
            if event_type == "item_collected" and event_data["item_name"] in self.requirements["items"]:
                item_name = event_data["item_name"]
                self.progress[item_name] = self.progress.get(item_name, 0) + 1
                
        elif self.quest_type == QuestType.EXPLORE:
            if event_type == "area_visited" and event_data["area"] in self.requirements["areas"]:
                area = event_data["area"]
                self.progress[area] = True
                
        elif self.quest_type == QuestType.UPGRADE:
            if event_type == "item_upgraded":
                self.progress["upgrades"] = self.progress.get("upgrades", 0) + 1
                
        elif self.quest_type == QuestType.BOSS:
            if event_type == "enemy_killed" and event_data["enemy_name"] == self.requirements["boss"]:
                self.progress["boss_killed"] = True
        
        self.check_completion()
    
    def check_completion(self):
        """Check if quest is completed based on progress"""
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
                    
        elif self.quest_type == QuestType.UPGRADE:
            if self.progress.get("upgrades", 0) < self.requirements["count"]:
                return False
                
        elif self.quest_type == QuestType.BOSS:
            if not self.progress.get("boss_killed", False):
                return False
        
        self.status = QuestStatus.COMPLETED
        return True
    
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
            
        elif self.quest_type == QuestType.UPGRADE:
            current = self.progress.get("upgrades", 0)
            return f"Upgrades: {current}/{self.requirements['count']}"
            
        elif self.quest_type == QuestType.BOSS:
            return "Boss killed" if self.progress.get("boss_killed", False) else "Boss not defeated"
        
        return "Unknown progress"

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
        min_level=1
    ),
    Quest(
        id="magic_herbs",
        title="Magical Herbs",
        description="Collect healing herbs from the deep forest.",
        quest_type=QuestType.COLLECT,
        requirements={"items": {"Health Potion": 3}},
        rewards={"gold": 75, "items": ["Strength Potion"]},
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
        min_level=2
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