import logging
import os
from enum import Enum, unique
from random import randint

import tdl  # import tcod as libtcod
import tcod.path
import numpy as np

from app import colors
from app.map import Map, TileId
from app.entity import (
    move_towards,
    Entity,
    EntityId,
)
from app.render import (
    render_bar,
    render_blit,
    render_clear_all,
    render_entities,
    render_entity,
    random_font_path,
    render_text,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

FOV_ALGO = 'BASIC'
FOV_LIGHT_WALL = True
DEBUG_VISUALS = False


def random_percent():
    return randint(0, 100)


@unique
class InputMode(Enum):
    GAME = 0
    EDITOR = 1


class Console:
    pass

class Game:
    """
    note: see `init()`, definitions are not duplicated between it and `__init__()`

    methods:
        spawn -- ['player'|'monster'|'item'] factory constructor

    members:
        root_console --  main screen surface
        con -- 2nd surface, back-buffer to render to root_console
        map -- actual Map instance
        entities -- list of `Entity()s`
        is_done -- causes game to exit

    """
    def __init__(self, root_path):
        self.root_path = root_path
        self.limit_fps = 60
        self.is_done = False
        self.MAP_TILES_X = 80
        self.MAP_TILES_Y = 50
        self.SCREEN_TILES_X = self.MAP_TILES_X
        self.SCREEN_TILES_Y = self.MAP_TILES_Y
        self.entities = []
        self.player = None
        self.map = Map(self.MAP_TILES_X, self.MAP_TILES_Y, self)
        self.map.debug_show_colors = True
        self.input_mode = InputMode.GAME
        self.panel_height = 7
        self.bar_width = 20
        self.panel_y = self.SCREEN_TILES_Y - self.panel_height

        self.fov_recompute = True
        self.update_sim = True
        self.visible_tiles = [] # todo: move to map
        self.use_fog_of_war = False
        self.torch_radius = 10
        self.draw_hp = False

        self.init()
        path = os.path.join(self.root_path, 'fonts', 'arial12x12.png')
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(self.SCREEN_TILES_X, self.SCREEN_TILES_Y, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(self.SCREEN_TILES_X, self.SCREEN_TILES_Y)
        self.con_console = tdl.Console(self.SCREEN_TILES_X, self.panel_height)
        tdl.setFPS(self.limit_fps)
        logger.debug("FPS: {}".format(self.limit_fps))

    def re_init_font(self):
        # allows reloading of font
        path = random_font_path(PATH_APP_ROOT)
        logger.debug("font: ", path)
        tdl.set_font(path, greyscale=True, altLayout=True)
        self.root_console = tdl.init(self.SCREEN_TILES_X, self.SCREEN_TILES_Y, title='tcod demo', fullscreen=False)
        self.con = tdl.Console(self.SCREEN_TILES_X, self.SCREEN_TILES_Y)
        tdl.setFPS(LIMIT_FPS)

    def init(self):
        # reset for next round, and first-time init.
        self.fov_recompute = True
        self.update_sim = True
        self.visible_tiles = []  # todo: move to map
        self.is_done = False
        self.MAP_TILES_X = 80
        self.MAP_TILES_Y = 50
        self.SCREEN_TILES_X = self.MAP_TILES_X
        self.SCREEN_TILES_Y = self.MAP_TILES_Y
        self.entities = []
        self.map.reset(self.MAP_TILES_X, self.MAP_TILES_Y)
        self.player = self.spawn("player")
        self.input_mode = InputMode.GAME
        # self.use_fog_of_war = True
        self.torch_radius = 10
        self.panel_height = 7
        self.bar_width = 20
        self.panel_y = self.SCREEN_TILES_Y - self.panel_height

        self.map.gen_random_map()

    def spawn(self, name, **kwargs):
        if name == 'player':
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            hp = kwargs.get('hp', 15)

            kwargs = {
                'entity_id': EntityId.PLAYER,
                'hp': hp,
                'can_hurt_monsters': True,
                'name': 'Player',
                'blocking': True,
            }
            spawn = Entity(x, y, '@', colors.white, self, **kwargs)

            if self.player and self.player in self.entities:
                self.entities.remove(self.player)

            self.entities.append(spawn)
            self.player = spawn

            logger.debug("Spawn('player') = {}".format(str(spawn)))
            return spawn
        elif name == 'monster':
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            hp = kwargs.get('hp', 1)
            # char = str(kwargs.get('char','X'))
            color = colors.yellow
            name = "Nobody"

            chance = random_percent()
            if chance <= 30:
                # orc
                char = 'o'
                color = colors.orc
                name = 'Orc'
            elif chance <= 60:
                char = 'T'
                color = colors.troll
                name = 'Troll'
                hp = 2
            else:
                char = 'r'
                color = colors.rat
                name = 'Rat'

            kwargs = {
                'entity_id': EntityId.MONSTER,
                'hp': hp,
                'can_hurt_monsters': False,
                'name': name,
                'blocking': True,
            }
            spawn = Entity(x, y, char, color, self, **kwargs)

            logger.info("Spawn('monster') = {}".format(str(spawn)))
            self.entities.append(spawn)
        else:
            raise ValueError("Unknown spawn() type: {}".format(name))

    def draw(self):
        # map
        for y in range(self.SCREEN_TILES_Y):
            for x in range(self.SCREEN_TILES_X):
                # check for both fog of war, and tile visibility/LOS

                tile_id = self.map.at(x, y).tile_id
                visible = (x, y) in self.visible_tiles
                explored = self.map.at(x, y).explored

                if not visible and not explored and self.use_fog_of_war:
                    continue

                if visible and not explored:
                    self.map.at(x, y).explored = True

                color = colors.white
                if tile_id == TileId.WALL:
                    if visible:
                        color = colors.lit_dark_wall
                    else:
                        color = colors.dark_wall
                elif tile_id == TileId.FLOOR:
                    if visible:
                        color = colors.lit_dark_floor
                    else:
                        color = colors.dark_floor

                self.con.draw_char(x, y, None, fg=None, bg=color)

        # entities
        render_entities(self, self.con, self.entities)

        # this does draw player a 2nd time but then I don't have to worry about
        # entity order (to always be on top)
        render_entity(self.con, self.player)

        # if DEBUG_VISUALS and self.debug_path:
        if DEBUG_VISUALS:
            # if self.debug_path:
            #     for x, y in self.debug_path:
            #         self.con.draw_rect(x, y, width=1, height=1, string='.', bg=colors.red)

            for monster in self.get_monsters_only():
                if monster.path:
                    for x, y in monster.path:
                        if self.map.in_bounds(x + 1, y + 1):
                            self.con.draw_rect(x, y, width=1, height=1, string='.', bg=colors.green)

        # HP bar GUI


        # render_bar(self.con_console,

        # self.con.draw
        # def _render_bar(x, y, total_width, name, val, max, bg_bar, bg_back):
        #     bar_width = int(float(self.player.hp) / self.player.hp_max)
        #     self.con_panel.draw_rect(x, y, total_width, 1, None, bg=bg_back)
        #
        #     self.con_panel.draw_rect(x, y, total_width, 1, None, bg=bg_back)
        #     # now render the bar on top
        #     if bar_width > 0:
        #         self.con_panel.draw_rect(x, y, bar_width, 1, None, bg=bg_bar)
        #
        #     # todo: health numbers

        # BAR_WIDTH = 20
        # PANEL_HEIGHT = 7
        # PANEL_Y = self.TILES_Y - PANEL_HEIGHT
        # self.con_panel.clear(fg=colors.white, bg=colors.black)
        # _render_bar(1, 1, BAR_WIDTH, 'hp', self.player.hp, self.player.hp_max, colors.light_red, colors.dark_red)

        # TextGUI
        # # Todo: call render.draw_str which does bound checking
        # try:
        #     self.con.draw_str(0, self.map.tiles_y - 2, "Player HP: {hp}/15hp, loc={loc}  -- Ents: monster={monster}, total={total}".format(
        #         loc="({},{})".format(self.player.x, self.player.y),
        #         hp=self.player.hp,
        #         monster=len(self.get_monsters_only()),
        #         total=len(self.entities)),
        #         fg=colors.gray_80,
        #         bg=colors.gray_20)
        # except tdl.TDLError:
        #     pass

        # self.con.blit(self.con_panel, 0, PANEL_Y, self.TILES_X, PANEL_HEIGHT, 0, 0)
        # swap buffers
        render_blit(self.root_console, self.con, self.SCREEN_TILES_X, self.SCREEN_TILES_Y)

        # lazy, full clear.
        tdl.flush()
        render_clear_all(self.con, fg=colors.black, bg=colors.black)

    def update(self):
        if self.update_sim:
            self.update_ai()
            self.update_sim = False
            if self.player.hp <= 0:
                print("Player dies")
                self.init()

        if self.fov_recompute:
            self.fov_recompute = False
            self.visible_tiles = tdl.map.quickFOV(
                self.player.x,
                self.player.y,
                self.map.tile_is_visible,
                fov=FOV_ALGO,
                radius=self.torch_radius,
                lightWalls=FOV_LIGHT_WALL
            )

    def get_monsters_only(self):
        return self.get_entities(entity_id=EntityId.MONSTER)

    def get_entities(self, entity_id=None):
        if entity_id is None:
            entity_id = EntityId.MONSTER

        entities = []
        for entity in self.entities:
            if entity.entity_id == entity_id:
                entities.append(entity)

        return entities

    def get_entities_at(self, x, y):
        entities = []
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                entities.append(entity)

        return entities

    def update_ai(self):
        # update deaths
        for entity in self.get_entities(entity_id=None):
            if entity.hp <= 0:
                self.entities.remove(entity)
                print("{} dies".format(entity.name))

        for monster in self.get_monsters_only():
            # if not monster.path:
            #     monster.path = self.astar_path(monster.x, monster.y, self.player.x, self.player.y)

            if False:
                print(monster.path)
                print(monster.x, monster.y)
                if monster.path:
                    next = monster.path[0]
                    # monster.move_towards(*next)
                    mod = (next[0] - monster.x, next[1] - monster.y)
                    monster.move_or_attack(*mod)

                    if next == (monster.x, monster.y):
                        monster.path.pop(0)
            else:
                move = move_towards(monster, self.player)
                monster.move_or_attack(*move)

            # if False:
                #
                # if not monster.path:
                #     # monster.path = []
                #     # print(self.map.as_raw_list())
                #     map_data = np.array(self.map.as_raw_list(), dtype=np.int8)
                #     # print(map_data)
                #     astar = tcod.path.AStar(map_data)
                #     monster.path = astar.get_path(monster.x, monster.y, self.player.x, self.player.y)
                #     # print(monster.path)
                # else:
                #     # print(monster.path)
                #     # todo: only pop *if* move was successful
                #     # raise NotImplementedError()
                #     next = monster.path.pop(0)
                #     monster.teleport_to(*next)

    def loop(self):
        while not self.is_done and not tdl.event.is_window_closed():
            self.update()
            self.draw()
            self.input()

    def input(self):
        for event in tdl.event.get():
            action = self.handle_input(event)

            if action:
                if action.get('move'):
                    self.player.move_or_attack(*action.get('move'))
                if action.get('rest'):
                    self.update_sim = True
                if action.get('exit'):
                    self.is_done = True
                if action.get('open'):
                    print("Example of a command that does **not** update simulation")
                if action.get('fullscreen'):
                    tdl.set_fullscreen(not tdl.get_fullscreen())

    def handle_input(self, event):
        # Movement keys
        if self.input_mode == InputMode.GAME:
            return self.handle_input_game(event)
        elif self.input_mode == InputMode.EDITOR:
            return self.handle_input_editor(event)
        else:
            raise Exception("Unknown game mode: {}".format(self.input_mode))

    def handle_input_game(self, event):
        RECOMPUTE_LOS_KEYS = ["UP", "DOWN", "LEFT", "RIGHT", "SPACE"]
        UPDATE_SIM_KEYS = RECOMPUTE_LOS_KEYS

        if event.type == 'KEYDOWN':
            # debug for key names
                # print(event.key)
                # print('%s event - char=%s key=%s alt=%i control=%i shift=%i' % (
                # event.type.ljust(7), repr(event.char), repr(event.key), event.alt, event.control, event.shift))

            if event.key in RECOMPUTE_LOS_KEYS:
                self.fov_recompute = True

            if event.key in UPDATE_SIM_KEYS:
                self.update_sim = True

            # keys using char
            if event.key == 'CHAR':
                if event.char == 'l' or event.char == 'z':
                    print("load_json")
                    self.map.load_json("map.json")
                elif event.char == 's':
                    print("save_json")
                    self.map.save_json("map.json")
                elif event.char == 'i':
                    raise NotImplementedError("Inventory does not exist yet")
                    return {'open': 'inventory'}

            # player
            if event.key == 'UP':
                return {'move': (0, -1)}
            elif event.key == 'DOWN':
                return {'move': (0, 1)}
            elif event.key == 'LEFT':
                return {'move': (-1, 0)}
            elif event.key == 'RIGHT':
                return {'move': (1, 0)}

            # keys that do not use .char
            elif event.key == 'TAB':
                if self.input_mode == InputMode.GAME:
                    self.input_mode = InputMode.EDITOR
                else:
                    self.input_mode = InputMode.GAME
                print(self.input_mode)

            elif event.key == '1':
                self.map.room_gen_padding -= 1
                self.map.room_gen_padding = max(self.map.room_gen_padding, 0)
                logger.info("room padding: {}".format(self.map.room_gen_padding))
                self.init()
            elif event.key == '2':
                self.map.room_gen_padding += 1
                logger.info("room padding: {}".format(self.map.room_gen_padding))
                self.init()

            elif event.key == 'F1':
                self.init()
            elif event.key == 'F2':
                self.use_fog_of_war = not self.use_fog_of_war
                print("Fog: {}".format(self.use_fog_of_war))
                self.init()
            elif event.key == 'F3':
                global DEBUG_VISUALS
                DEBUG_VISUALS = not DEBUG_VISUALS
            elif event.key == 'F4':
                self.draw_hp = not self.draw_hp
            elif event.key == 'PAGEUP':
                self.re_init_font()
            elif event.key == 'PAGEDOWN':
                self.re_init_font()
            elif event.key == 'SPACE':
                return {'rest': True}
            elif event.key == 'ESCAPE':
                return {'exit': True}
            elif event.key == 'ENTER' and event.alt:
                return {'fullscreen': True}

        # mice
        elif event.type == 'MOUSEDOWN':
            if event.button == 'LEFT':
                self.player.teleport_to(*event.cell)
                self.fov_recompute = True

                # self.debug_path = self.astar_path(0, 0, self.player.x, self.player.y)
                # print("map: {}".format(self.debug_path))
                # for m in self.get_monsters_only():
                #     m.path = None

                logger.info("LMB Cell: {}".format(event.cell))

        return {}

    def astar_path(self, x1, y1, x2, y2):
        # todo: move to map
        path = None

        map_data = np.array(self.map.as_raw_list_cost(), dtype=np.int8)
        astar = tcod.path.AStar(map_data)
        path = astar.get_path(x1, y1, x2, y2)
        return path

    def handle_input_editor(self, event):
        RECOMPUTE_LOS_KEYS = ["UP", "DOWN", "LEFT", "RIGHT"]

        if event.type == 'KEYDOWN':
            # print(event)

            if event.key in RECOMPUTE_LOS_KEYS:
                self.fov_recompute = True

            elif event.key == 'TAB':
                if self.input_mode == InputMode.GAME:
                    self.input_mode = InputMode.EDITOR
                else:
                    self.input_mode = InputMode.GAME
                print(self.input_mode)

            # player
            if event.key == 'UP':
                return {'move': (0, -1)}
            elif event.key == 'DOWN':
                return {'move': (0, 1)}
            elif event.key == 'LEFT':
                return {'move': (-1, 0)}
            elif event.key == 'RIGHT':
                return {'move': (1, 0)}

            elif event.key == 'SPACE':
                return {'rest': True}
            elif event.key == 'ESCAPE':
                return {'exit': True}

        # mice
        elif event.type == 'MOUSEDOWN':
            if event.button == 'LEFT':
                (x, y) = event.cell
                tile_id = self.map.at(x, y).tile_id
                if tile_id == TileId.WALL:
                    self.map.at(x, y).set_type(TileId.FLOOR)
                else:
                    self.map.at(x, y).set_type(TileId.WALL)
                self.fov_recompute = True

        return {}
