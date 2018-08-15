from enum import Enum, unique
import logging


@unique
class EntityId(Enum):
    PLAYER = 0
    MONSTER = 1
    ITEM = 2
    DEBUG = 9999


def move_towards(entity, other):
    x, y = 0, 0
    if entity.x < other.x:
        x = 1
    elif entity.x > other.x:
        x = -1
    else:
        x = 0

    if entity.y < other.y:
        y = 1
    elif entity.y > other.y:
        y = -1
    else:
        y = 0

    return x, y


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
        # logging.info("{} .move(dx={}, dy={})".format(self, dx, dy))

        entities = self.game.get_entities_at(new_x, new_y)

        if not entities:
            self.move(dx, dy)
            return

        # todo: allow/prohibit multiple attacks if they are stacked?
        for entity in entities:
            if self == entity:
                continue

            if entity.entity_id == EntityId.MONSTER and not self.can_hurt_monsters:
                continue

            self.attack_entity(entity)

    def attack_entity(self, other):
        print("{name} attacks {other}; {hp}HP - {damage} damage".format(
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
        return "Entity(id={id}, type={char} name={name}, pos=({x}, {y}))".format(
            id=self.entity_id,
            char=self.char,
            name=self.name,
            x=self.x,
            y=self.y
        )