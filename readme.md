# about

code mostly based on http://rogueliketutorials.com/libtcod/

# todo:

- refactor tiles[x][y] to fail when out of bounds


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

fonts:
    https://github.com/libtcod/python-tcod/tree/master/fonts/libtcod
    
    better fonts:
        arial10x10.png
        arial12x12.png
        lucida12x12_gs_tc.png
    
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
    