from enum import Enum, unique
import logging


@unique
class EntityId(Enum):
    PLAYER = 0
    MONSTER = 1
    ITEM = 2
    DEBUG = 9999


class Entity:
    """Base class for game units/monsters/player

    blocking -- is walking on this blocked?
    can_hurt_monsters -- enables monster friendly fire
    """
    def __init__(self, x, y, char, color, game, entity_id, damage=1, hp=1, can_hurt_monsters=False, name=None, blocking=True):
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.char = char
        self.color = color
        self.game = game
        self.map = game.map
        self.blocking = blocking
        if name is None:
            name = "Nobody"
        self.name = name
        self.can_hurt_monsters = can_hurt_monsters
        self.entity_id = entity_id

    def move(self, dx, dy):
        if not self.map.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_or_attack(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        logging.info("{} .move(dx={}, dy={})".format(self, dx, dy))

        # blocking entity at target?
        # for i, monster in enumerate(self.game.get_monsters_only()):
        #     print(i, monster)

        monsters = self.game.get_monsters_at(new_x, new_y)

        if not monsters:
            self.move(dx, dy)
            return

        # todo: allow/prohibit multiple attacks if they are stacked?
        for monster in monsters:
            if self == monster:
                continue

            if self.entity_id == EntityId.MONSTER and monster.entity_id == EntityId.MONSTER:
                if not self.can_hurt_monsters:
                    continue

                print("{name} attacks {monster} -- stack={stack}".format(
                    name=self.name,
                    monster=monster.name,
                    stack=len(monsters)))

            # if not self.can_hurt_monsters:
            #     continue

            self.attack_entity(monster)

    def attack_entity(self, other):
        print("{name} attacks {other} HP {hp} - {damage}".format(
            name=self.name,
            other=other.name,
            hp=other.hp,
            damage=self.damage,
        ))
        other.hp -= self.damage

    def teleport_to(self, x, y):
        if self.map.in_bounds(x, y):
            self.x = x
            self.y = y

    def __str__(self):
        return "Entity(type={char} name={name}, pos=({x}, {y}))".format(
            char=self.char,
            name=self.name,
            x=self.x,
            y=self.y
        )