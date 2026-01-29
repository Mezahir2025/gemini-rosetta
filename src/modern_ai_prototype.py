"""
Modern DOOM AI Prototype (Behavior Tree Architecture)
------------------------------------------------------
This module modernizes the legacy AI logic from DOOM's p_enemy.c.
Legacy `goto` and `movecount` logic are replaced by a hierarchical 
Behavior Tree (BT) system.
"""

import enum
import random

class NodeStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"

# --- Behavior Tree Base Classes ---

class Node:
    def tick(self, actor):
        raise NotImplementedError

class CompositeNode(Node):
    def __init__(self, children):
        self.children = children

class Selector(CompositeNode):
    """Runs children until one succeeds (OR logic)"""
    def tick(self, actor):
        for child in self.children:
            if callable(child):
                status = child(actor)
            else:
                status = child.tick(actor)
                
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE

class Sequence(CompositeNode):
    """Runs children until one fails (AND logic)"""
    def tick(self, actor):
        for child in self.children:
            if callable(child):
                status = child(actor)
            else:
                status = child.tick(actor)
                
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS

# --- Custom DOOM-Inspired Nodes ---

class ConditionSeenPlayer(Node):
    def tick(self, actor):
        if actor.can_see_player:
            print(f"[AI] {actor.name} oyunçunu gördü (P_CheckSight success)")
            return NodeStatus.SUCCESS
        return NodeStatus.FAILURE

class ConditionHeardPlayer(Node):
    def tick(self, actor):
        if actor.has_heard_sound:
            print(f"[AI] {actor.name} səs eşitdi (P_NoiseAlert triggered)")
            return NodeStatus.SUCCESS
        return NodeStatus.FAILURE

class ActionSetTarget(Node):
    def tick(self, actor):
        actor.target_acquired = True
        return NodeStatus.SUCCESS

class ActionMoveTowards(Node):
    """Modernized 'movecount' logic"""
    def tick(self, actor):
        if actor.movecount > 0:
            actor.movecount -= 1
            print(f"[AI] {actor.name} hərəkət edir (Movecount: {actor.movecount})")
            return NodeStatus.RUNNING
        else:
            print(f"[AI] {actor.name} yeni istiqamət axtarır (P_NewChaseDir)")
            actor.movecount = random.randint(3, 5) # Simulating new path setup
            return NodeStatus.SUCCESS

class ActionPerformAttack(Node):
    def tick(self, actor):
        if actor.dist_to_player < 10:
            print(f"[AI] {actor.name} Yaxın döyüş! (A_MeleeAttack)")
        else:
            print(f"[AI] {actor.name} Raket atır! (A_MissileAttack)")
        return NodeStatus.SUCCESS

class ActionIdle(Node):
    def tick(self, actor):
        print(f"[AI] {actor.name} ətrafa baxır (A_Look/Idle)")
        return NodeStatus.SUCCESS

# --- The Actor (Monster) ---

class Monster:
    def __init__(self, name):
        self.name = name
        self.can_see_player = False
        self.has_heard_sound = False
        self.target_acquired = False
        self.dist_to_player = 100
        self.movecount = 0
        
        # Behavior Tree Logic
        self.brain = Selector([
            # Engagement Priority
            Sequence([
                Selector([
                    ConditionSeenPlayer(),
                    ConditionHeardPlayer()
                ]),
                ActionSetTarget(),
                Selector([
                    Sequence([
                        self._is_in_attack_range,
                        ActionPerformAttack()
                    ]),
                    ActionMoveTowards()
                ])
            ]),
            # Idle Priority
            ActionIdle()
        ])

    def _is_in_attack_range(self, actor):
        if actor.dist_to_player < 50:
            return NodeStatus.SUCCESS
        return NodeStatus.FAILURE

    def update(self):
        return self.brain.tick(self)

if __name__ == "__main__":
    # Quick manual test
    imp = Monster("Imp")
    imp.update()
    imp.can_see_player = True
    imp.update()
