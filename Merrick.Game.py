def render_introduction():
    return '''Welcome to my world, you have entered into a town and plan on passing through, \nThough you have heard that bandits have been barricading the road onward\nAnd the current guard is unwilling to leave the town to deal with them..\n'''
    '''
    Create the message to be displayed at the start of your game.

    Returns:
        str: The introductory text of your game to be displayed.
    '''

def create_dialogue():
    return {
        'mayor':'Hello there traveller, it has been a while since we had a visitor, you must be a grand advernturer,\nWould you please get rid of the bandis? I will pay you well.',
        'blacksmith':'Hello, I am the town blacksmith, I make weapons and armor for the town\nYou seek to get a sword then, I am out of material currently, if you could retrieve some materials, I could make you a sword.\nIt there are sticks for handles in the forest and ore in the mine.',
        'blacksmith2':'you do not have the materials required',
        'blacksmith3':'Thank you for the materials, for this I will make you a sword.\nyou should probably practice at the town green.',
        'wizard':'Hello there adventurer, my name is Xanthis the Great, the almighty one, the greatest of the great.\nthat is of course, assuming that I had my wand, which I seem to have misplaced.\nif you could find it for me, it would be most gratifying',
        'wizard1':'Well, do you want my gift or not, go get it!',
        'wizard2':'Thank you so much for getting me my wand, I will repay you for this by giving you a magical gift.\nit could take a little getting used to, but that is what the town green is for.'


    }
def create_map():

    return{
            'town':{
                'about':'This is a small town with a couple neccesary buildings\n',
                'neighbors':[
                    'shrine',
                    'forest',
                    'smithy',
                    'orchard',
                    'inn',
                    'well',
                    'town green',
                    'bandit blockade'],
                'stuff':['mayor']
            },

            'wizard tower':{
                'about':'This is a tower to a "powerful" wizard.\n',
                'neighbors':['orchard'],
                'stuff':['wizard']
            },

            'well':{
                'about':'Ah well\n',
                'neighbors':['town'],
                'stuff':['']
            },

            'cavern':{
                'about':'it is a cave, that is about all you can tell\n',
                'neighbors':['mine'],
                'stuff':['chest']
            },

            'shrine':{
                'about':'this is a shrine to the lady of luck, a powerful goddess.\n',
                'neighbors':['town'],
                'stuff':['alter']
            },

            'forest':{
                'about':'This is a dense thicket of woods\n',
                'neighbors':['town','mine'],
                'stuff':['stick']
            },

            'smithy':{
                'about':'This is the town smithy, where the town blacksmith works.\nThe billows are running, the forge is hot.\n',
                'neighbors':['town'],
                'stuff':['blacksmith']
            },

            'orchard':{
                'about':'This is an apple orchard, with apples all over the ground.\n',
                'neighbors':['wizard tower','town'],
                'stuff':['apples']
            },

            'inn':{
                'about':'A town inn it is very small, with very few patrons.\n',
                'neighbors':['town'],
                'stuff':[]
            },

            'mine':{
                'about':'The mine is a glorified cave, deep down in the ground with a bunch of ore\n',
                'neighbors':['forest'],
                'stuff':['pickaxe','ore vein']
            },

            'town green':{
                'about':'The town green, a big open space with one hay stuffed humanoid for weapons practice\n',
                'neighbors':['town'],
                'stuff':[]
            },
            'bandit blockade':{
                'about':'The bandit blockade that has been blocking supplies from entering or exiting the city.\n',
                'neighbors':['town'],
                'stuff':[]
            }

    }


def create_player():
    return{
            'location':'town',
            'inventory':[],
            'resolve':False,
            'met blacksmith':False,
            'met wizard':False,
            'ready':False
        }

def create_world():
    return {
        "status":'playing',
        'map':create_map(),
        'player':create_player(),
        'dialogue':create_dialogue()
    }
def render(world):
    '''
    Consumes a world and produces a string that will describe the current state
    of the world. Does not print.

    Args:
        world (World): The current world to describe.

    Returns:
        str: A textual description of the world.
    '''
    def render_location(world):
        player_location  = world['player']['location']
        return world['map'][player_location]['about']

    def render_visible_stuff(world):
        player_location = world['player']['location']
        map_location = world['map'][player_location]
        stuff = map_location['stuff']
        inventory = world['player']['inventory']
        visible_stuff = []
        for item in stuff:
            visible_stuff.append(item)
        return("\nYou see: "+ " , ".join(visible_stuff)+'\n')
    if render_visible_stuff(world) != "\nYou see: \n":
        return render_location(world) + render_visible_stuff(world)
    else:
        return render_location(world)

def get_options(world):
    location = player_location  = world['player']['location']
    map_location = world['map'][location]
    neighbors = map_location['neighbors']
    inventory = world['player']['inventory']
    stuff = map_location['stuff']
    commands = ["quit",  "inventory"]
    magic = 'magic' in inventory or 'magic stick' in inventory
    if neighbors:
        for place in neighbors:
            commands.append("go to " + place)
    if location == 'forest' and 'stick' in stuff and 'stick' not in inventory:
        commands.append("pick up stick")
    if location == 'cavern' and 'chest' in stuff and not 'magic stick' in inventory:
        commands.append("open chest")
    if location == 'well':
        commands.append('jump in well')
    if location == 'town green' and 'sword' in inventory and world['player']['ready'] == False:
        commands.append('practice with sword')
    if location == 'town green' and magic and world['player']['ready'] == False:
        commands.append('practice with magic')
    if location == 'mine' and 'pickaxe' in stuff:
        commands.append("pick up pickaxe")
    if location == 'mine' and 'ore vein' in stuff and 'pickaxe' in inventory:
        commands.append("mine ore")
    if location == 'shrine' and 'alter' in stuff and 'blessing' not in inventory:
        commands.append("pray at alter")
    if location == 'town' and 'mayor' in stuff:
        commands.append("talk to mayor")
    if location == 'smithy' and 'blacksmith' in stuff and not 'sword' in inventory and not 'magic' in inventory:
        commands.append("talk to blacksmith")
    if location == 'wizard tower' and 'wizard' in stuff and not 'sword' in inventory and not 'magic' in inventory:
        commands.append("talk to wizard")
    '''
    Consumes a world and produces a list of strings representing the options
    that are available to be chosen given this state.

    Args:
        world (World): The current world to get options for.

    Returns:
        list[str]: The list of commands that the user can choose from.
    '''



    return commands

def goto(world, command):
    new_location = command[len('go to '):]
    player_location =  world['player']['location']
    world['player']['location'] = new_location
    if new_location in world['map'][player_location]['neighbors']:
        return "You went to " + new_location + "\n"
def pickup(world, command):
    player_location  = world['player']['location']
    place = world['map'][player_location]
    item = command.lower()[len('pick up '):]
    world['player']['inventory'].append(item)
    place['stuff'].remove(item)
    return "\n" + item + " added to Inventory\n"
def talkto(world, command):
    person = command[len('talk to '):]
    player_location =  world['player']['location']
    if person in world['map'][player_location]['stuff']:
        return world['dialogue'][person]
def update(world, command):
    '''
    Consumes a world and a command and updates the world according to the
    command, also producing a message about the update that occurred. This
    function should modify the world given, not produce a new one.

    Args:
        world (World): The current world to modify.

    Returns:
        str: A message describing the change that occurred in the world.
    '''
    # world['player']['resolve'] = False
    inventory = world["player"]['inventory']
    location = world['player']['location']
    command = command.lower()
    if command == ('go to bandit blockade') and world['player']['resolve'] == True:
        if world['player']['ready']:
            world['status'] = 'won'
        else:
            if not 'blessing' in world['player']['inventory']:
                world['status'] = 'lost'
            else:
                world['player']['location'] = 'shrine'
                world['player']['inventory'].remove('blessing')
                return '''
you die and return to the shrine
                '''
    elif command == ('go to bandit blockade') and world['player']['resolve'] == False:
        world['player']['resolve'] = True
        return "The Guard at the gate comes up to you and says:\nAre you sure you want to go there? the bandits have been barricading the road to Emon,\nif you want to travel this path, be sure you are ready.\nYou'll know when you are ready.\n"
    if command.startswith('go to '):
        return goto(world, command)
    if command == 'jump in well':
        world['player']['location'] = 'cavern'
        return 'you jumped into a well'
    if command == 'open chest':
        inventory.append('magic stick')
        return 'You open the chest and find a very magic looking stick.\n\nMagic stick added to inventory\n'
    if command == 'quit':
        world['status'] = 'quit'
        return ''
    if command == 'practice with sword':
        world['player']['resolve'] = True
        world['player']['ready'] = True
        return 'You train with your new sword, old training being renewed.'
    if command == 'practice with magic':
        world['player']['resolve'] = True
        world['player']['ready'] = True
        return 'You train and practice until you feel ready to face whatever is up ahead.'
    if command == 'inventory':
        return inventory
    if command == 'mine ore':
        inventory.append('ore')
        world['map'][location]['stuff'].remove('ore vein')
        return '''You take a bit of time and effort and mine the ore and pick it up'''
    if command.startswith('pick up '):
        return pickup(world, command)
    if command == 'talk to blacksmith':
        if not world['player']['met blacksmith']:
            world['player']['met blacksmith'] = True
            return world['dialogue']['blacksmith']
        if not 'ore' in inventory or not 'stick' in inventory:
            return world['dialogue']['blacksmith2']
        if 'ore' in inventory and 'stick' in inventory:
            inventory.remove('stick')
            inventory.remove('ore')
            inventory.append('sword')
            return world['dialogue']['blacksmith3']
    elif command == 'talk to wizard':
        if not world['player']['met wizard']:
            world['player']['met wizard'] = True
            return world['dialogue']['wizard']
        if not 'magic stick' in inventory:
            return world['dialogue']['wizard1']
        if 'magic stick' in inventory:
            inventory.remove('magic stick')
            inventory.append('magic')
            return world['dialogue']['wizard2']
    elif command.startswith('talk to '):
        return talkto(world, command)
    if command == 'pray at alter':
        inventory.append('blessing')
        return '''
You pray to the goddess of luck, she favors you with a response:

You my child, I sense great potential for misfortune in your future.
For you, I will give you my blessing.
If trial ever befall you, you will be taken but once,
back to this shrine of mine.
        '''
def render_ending(world):
    if world['status'] == 'won':
        if 'sword' in world['player']['inventory']:
            return '''
You walk up to the bandit blockade, sword out, and one calls out to you:
"Give us all of your money, or face one of us in single combat, Its your choice."

it is at this moment you realize, the bandits are wearing armor that was not put
together, these are not trained bandits.

You yell out:
I challenge you to single combant!

they look supprised, you don't think they have anyone accept single combat.
You draw your sword, and walk forward as one of them shakily walks up to you.
They, shaking from apperent nerves say, challenge accepted

over the course of 2 minutes you proceed to win the fight, going on to Imohn to live out your life


You Win'''
        elif ('magic' in world['player']['inventory'] or 'magic stick' in world['player']['inventory']):
            return '''
You are walking down the road to the town, magic crackling in your veins.
Or that's what you feel.
You walk up to the bandit blockade, and a voice yells:
"Give us all of your money, or face one of us in single combat, Its your choice."
You yell out with your magically enhanced voice:
LET   ME   PASS
the ground rattles as your voice booms out, the barricade shaking.
They scatter and you walk through unscathed.


You win
'''
    if world['status'] == 'lost':
        return'''
You walk up to the bandit blockade, and a voice yells:
"Give us all of your money, or face one of us in single combat, Its your choice."
You unsure of weather to give up what you have or not.
They yell:
"Time is up"
They beat you up and take all of your possesions, leaving you battered bruised and dying.


You lose
'''
    if world['status'] == 'quit':
        return "you quit"
    '''
    Create the message to be displayed at the end of your game.

    Args:
        world (World): The final world state to use in describing the ending.

    Returns:
        str: The ending text of your game to be displayed.
    '''

def choose(options):
    '''
    Consumes a list of commands, prints them for the user, takes in user input
    for the command that the user wants (prompting repeatedly until a valid
    command is chosen), and then returns the command that was chosen.

    Note:
        Use your answer to Programming Problem #42.3

    Args:
        options (list[str]): The potential commands to select from.

    Returns:
        str: The command that was selected by the user.
    '''
    inp = ""
    repeating = True
    while repeating:
        print('You can:')
        print("")
        for item in options:
            print (("-")+item)
        print("")
        inp = input("What will you do? ")
        inp = inp.lower()
        if inp in options:
            repeating = False
        # elif inp.startswith('go to ') and 'go to ' + inp[len('go to '):] in options:
        #     repeating = False
    return inp
############# Main Function ##############
# Do not modify anything below this line #
##########################################
def main():
    '''
    Run your game using the Text Adventure console engine.
    Consumes and produces nothing, but prints and indirectly takes user input.
    '''
    print(render_introduction())
    world = create_world()
    # print(get_options(world))
    while world['status'] == 'playing':
        print(render(world))
        options = get_options(world)
        command = choose(options)
        print(update(world, command))
    print(render_ending(world))

if __name__ == '__main__':
    main()
