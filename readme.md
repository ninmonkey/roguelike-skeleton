# about

code mostly based on http://rogueliketutorials.com/libtcod/

# test

- prevent monster spawns on top of each other.
    either re-rand or attempt to nudge both away.
     
 - **edit events** to be turn-based
    - pull loop_ai() outside recompute 

# next
    text
        - render monster count
        - render HP values of monsters
        
    - pathfind
        1. hardcode works, **monsters** don't.
        2. walls are currently walkable even when value=999 ?
            use walkable array
        2. always use np arrays (or else cache)
    
    - autowrite Enum in json saves:
        https://stackoverflow.com/a/24482806
        https://hynek.me/articles/serialization/
        

# todo:

- when fog_of_war=False, explored tiles need to be darker.
- switch to logging (redirect to console)
    - https://docs.python.org/3/howto/logging.html#configuring-logging 
    - rotate logs:
        https://pymotw.com/3/logging/
        https://docs.python.org/3.1/library/logging.html
    - separate log file for Map
    
- todo: disable input event auto-repeat
    - make key input based on state? 
- # todo: find a better way to serialize to/from 'automagically'

- separate screen_tiles_x from map_tiles_x for scrolling
- text: player loc, monster count, fps.
- weightedChoice: https://gamedev.stackexchange.com/a/20929 

# real-time vs turn-based


## async / real-time

    key = tcod.console_check_for_keypress()
        is async
       
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            break
    else:
        user_input = None
               
## blocking / sync / turn-based
       
    key = tcod.console_wait_for_keypress(True)
        is blocking                   
    
# tdl / libtcod docs and references

line of sight options:
    http://www.roguebasin.com/index.php?title=Comparative_study_of_field_of_view_algorithms_for_2D_grid_based_worlds

fonts:
    https://github.com/libtcod/python-tcod/tree/master/fonts/libtcod
        
colors:
    http://roguecentral.org/doryen/data/libtcod/doc/1.5.1/html2/color.html?c=false&cpp=false&cs=false&py=true&lua=false
    
examples:
    py3 http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod,_part_1
    http://rogueliketutorials.com/libtcod/1
    https://github.com/libtcod/python-tcod/tree/master/examples

tilesets:
    https://www.reddit.com/r/roguelikedev/comments/436sop/roguelike_tilesets/?utm_source=reddit&utm_medium=usertext&utm_name=roguelikedev&utm_content=t5_2si41

tdl docs:
    https://python-tdl.readthedocs.io/en/latest/tdl.html
    
tcod docs:
    http://roguecentral.org/doryen/data/libtcod/doc/1.5.1/index2.html?c=false&cpp=false&cs=false&py=true&lua=false
    
key constants:
    https://pythonhosted.org/tdl/tdl.event.KeyEvent-class.html#key
    