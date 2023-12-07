def render_introduction():
     return '''                      == Humane Problem ==
                     = By Chris Cleverly =

        You wake up next to your friend in an unknown house. You've been told
        that your friend has been poisoned and the only antidote is inside your stomach.
        You can choose to save your friend, or save yourself. What will it be?
        '''


def create_player():
    return {
        'location': 'bedroom',
        'inventory': [],
    }

def create_map():
    return {
        'bedroom': {
            'neighbors': ['living room'],
            'about': "You woke up in this bedroom with your friend. Rather small and plain.",
            'stuff': ["antidote"],
        },
        'living room': {
            'neighbors': ['bedroom', 'kitchen', 'closet', 'front door'],
            'about': "A dimly lit and poorly decorated room.",
            'stuff': []
        },
        'kitchen': {
            'neighbors': ['living room'],
            'about': "A mostly white kitchen with the smell of rotting food.",
            'stuff': ["knife"]
        },
        'closet': {
            'neighbors': ['living room'],
            'about': "A closet full of dusty cleaning supplies.",
            'stuff': ["key"]
        },
        'front door': {
            'neighbors': ['living room'],
            'about': "There is a locked door.",
            'stuff': ["key"]
        }
    }

def create_world():
    return {
        'map': create_map(),
        'player': create_player(),
        'status': "playing"
    }

def render(world):

    players_location = world['player']['location']
    return world['map'][players_location]['about']

world = create_world()
print(render(world))


def get_options(world):

    options = ['quit']
    players_location = world['player']['location']
    movements = world['map'][players_location]['neighbors']
    inventory = world['player']['inventory']
    for loc in movements:
        options.append(f'go to {loc}')
    if players_location == "bedroom":
        if "knife" in inventory:
            for thing in world['map'][players_location]['stuff']:
                options.append(f'pick up {thing}')
    else:
        for thing in world['map'][players_location]['stuff']:
                options.append(f'pick up {thing}')
    if "key" in inventory:
        if players_location == "front door":
            options.append("use key")
    return options


def update(world, command):
    
    inventory = world['player']['inventory']
    if command == "use key":
        if world['player']['location'] == "front door":
            world['status'] = 'lost'
            return "Congrats! You've gotten the Abandonment Ending. You used the key to escape, leaving your poisoned friend to die alone. Was it worth it? Because to some you lose this game, but to others you've won. Which is it to you?"
        else:
            return "You can't use this here."
    if command == "quit":
        world['status'] = 'quit'
        return "You just couldn't decide who should die. Fair enough. It is a rather difficult decision to make."
    if command.startswith("go to "):
        world['player']['location'] = command[6:]
        return f"You are now in {world['player']['location']}"
    if command.startswith("pick up "):
        for item in inventory:
            if command[8:] == item:
                return "You've already picked this item up"
        if command == "pick up antidote":
            world['status'] = 'won'
            return "Congrats! You've gotten the Sacrificial Ending. You used the knife on yourself to get the antidote and save your friend! However, you bled to death in the process. Do you find this to be a win? Some may not think so."
        else:
            world['player']['inventory'].append(command[8:])
            return f"You have picked up the {command[8:]}"
    if command.startswith("use "):
        return f"You used the {command[4:]}"


def render_ending(world):

    if world['status'] == 'quit':
        return "Thanks for playing"
    if world['status'] == 'won':
        return "Thanks for playing"
    if world['status'] == 'lost':
        return "Thanks for playing"


def choose(options):

    print("You can: ")
    for option in options:
        print(f"- {option}")

    cmd = input("What will you do?")
    while cmd not in options:
        cmd = input("What will you do?")
    return cmd

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
    while world['status'] == 'playing':
        print(render(world))
        options = get_options(world)
        command = choose(options)
        print(update(world, command))
    print(render_ending(world))

if __name__ == '__main__':
    main()
    pass
