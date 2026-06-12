from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ActionType(Enum):
    ATTACK = "attack"
    HEAL = "heal"

@dataclass
class Action:
    agent_id: int
    target_id: int
    action_type: ActionType
    value: int

class GameState:
    def __init__(self):
        # agents: id -> health
        self.agents = {
            0: {"name": "Warrior", "health": 100},
            1: {"name": "Mage", "health": 80},
            2: {"name": "Archer", "health": 90},
            3: {"name": "Cleric", "health": 70},
        }
    
    def resolve_turn(self, actions_by_agent: list[Optional[Action]]):
        """
        actions_by_agent: array indexed by agent ID
        None means agent didn't act this turn
        """
        print("\n" + "="*50)
        print("TURN START - Current Health:")
        self.print_status()
        
        # ========== PHASE 1: Action submission (already in array form) ==========
        # actions_by_agent is our array indexed by agent ID
        print("\n[PHASE 1] Actions submitted:")
        for agent_id, action in enumerate(actions_by_agent):
            if action:
                print(f"  Agent {agent_id} ({self.agents[agent_id]['name']}) -> {action}")
        
        # ========== PHASE 2: Conflict grouping (hash map!) ==========
        # target_id -> list of actions affecting that target
        conflict_map = defaultdict(list)
        
        for agent_id, action in enumerate(actions_by_agent):
            if action:
                conflict_map[action.target_id].append((agent_id, action))
        
        print("\n[PHASE 2] Conflict grouping (target -> actions):")
        for target_id, actions in conflict_map.items():
            target_name = self.agents[target_id]['name']
            print(f"  Target {target_id} ({target_name}): {len(actions)} action(s)")
        
        # ========== PHASE 3: Resolution ==========
        print("\n[PHASE 3] Resolving conflicts...")
        
        # First, calculate all effects without applying them (simultaneous!)
        pending_changes = defaultdict(int)  # agent_id -> health change
        
        for target_id, actions in conflict_map.items():
            for agent_id, action in actions:
                if action.action_type == ActionType.ATTACK:
                    pending_changes[target_id] -= action.value
                    print(f"    Agent {agent_id} attacks {self.agents[target_id]['name']} for {action.value}")
                elif action.action_type == ActionType.HEAL:
                    pending_changes[target_id] += action.value
                    print(f"    Agent {agent_id} heals {self.agents[target_id]['name']} for {action.value}")
        
        # Apply all changes simultaneously
        print("\n[RESOLUTION] Applying simultaneous effects:")
        for agent_id, change in pending_changes.items():
            old_health = self.agents[agent_id]["health"]
            new_health = max(0, old_health + change)
            self.agents[agent_id]["health"] = new_health
            print(f"    Agent {agent_id} ({self.agents[agent_id]['name']}): {old_health} -> {new_health} ({change:+d})")
        
        print("\nTURN END - Final Health:")
        self.print_status()
        print("="*50)
    
    def print_status(self):
        for agent_id, data in self.agents.items():
            print(f"  {agent_id}: {data['name']} - HP: {data['health']}")

# ========== SIMULATION ==========
if __name__ == "__main__":
    game = GameState()
    
    # Array indexed by agent ID (dirty list - some None entries)
    # Format: actions_by_agent[agent_id] = Action or None
    actions_by_agent = [None] * len(game.agents)
    
    # Warrior (0) attacks Mage (1) for 30 damage
    actions_by_agent[0] = Action(0, 1, ActionType.ATTACK, 30)
    
    # Mage (1) attacks Warrior (0) for 25 damage
    actions_by_agent[1] = Action(1, 0, ActionType.ATTACK, 25)
    
    # Archer (2) attacks Mage (1) for 20 damage (conflicts with Warrior!)
    actions_by_agent[2] = Action(2, 1, ActionType.ATTACK, 20)
    
    # Cleric (3) heals Warrior (0) for 15
    actions_by_agent[3] = Action(3, 0, ActionType.HEAL, 15)
    
    # Agent 4 doesn't exist, but we have 4 agents (0-3)
    
    # Resolve the turn
    game.resolve_turn(actions_by_agent)