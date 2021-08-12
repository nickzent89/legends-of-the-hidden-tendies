import random
import pandas as pd
import time

class Character:
  def __init__(self):
    self.name = ""
    self.health = 1
    self.health_max = 1
  def do_damage(self, enemy):
    damage = min(
        max(random.randint(0, self.health) - random.randint(0, enemy.health), 0),
        enemy.health)
    enemy.health = enemy.health - damage
    if damage == 0: 
      print (f"{enemy.name} ducked {self.name}'s attack.")
    else: 
      print (f"{self.name} attempts an attack..")
    return enemy.health <= 0

class Enemy(Character):
  def __init__(self, player):
    Character.__init__(self)
    enemies = ['Neck Beard','Chad','Dew Master','Grog Neck','Chaos Mage']
    random_index = random.randint(0,len(enemies)-1)
    self.name = enemies[random_index]
    self.health = random.randint(1, player.health)

class Player(Character):
  def __init__(self):
    Character.__init__(self)
    self.state = 'normal'
    self.health = 10
    self.health_max = 10
    self.food = 1
  def quit(self):
    print (f"{self.name} can't find the way back to the corner market, and dies of tendie induced starvation.\nR.I.P.")
    self.health = 0
  def help(self): 
    command_df = pd.DataFrame.from_dict(Commands_Help,orient='index')
    command_df = command_df.reset_index()
    command_df.columns =['Command','Description']
    print(command_df)
  def status(self): 
    print (f"{self.name}'s health: {self.health}/{self.health_max}")
    print (f"{self.name}'s food: {self.food}")

  def tired(self):
    print (f"{self.name} feels tired AF, should have brought a dew.")
    self.health = max(1, self.health - 1)
  def rest(self):
    if self.state != 'normal': 
      print (f"{self.name} can't rest now!")
      self.enemy_attacks()
    else:
      print (f"{self.name} rests.")
      if random.randint(0, 1):
        self.enemy = Enemy(self)
        print (f"{self.name} is rudely awakened by {self.enemy.name}!")
        self.state = 'fight'
        self.enemy_attacks()
      else:
        if self.health < self.health_max:
          self.health = self.health + 1
        else: 
          print (f"{self.name} slept too much.")
          self.health = self.health - 1
  def explore(self):
    if self.state != 'normal':
      print (f"{ self.name} is too busy right now!")
      self.enemy_attacks()
    else:
      print (f"{ self.name} explores a twisty passage.")
      if random.randint(0, 1):
        self.enemy = Enemy(self)
        print (f"{ self.name} encounters {self.enemy.name}!")
        self.state = 'fight'
      else:
        if random.randint(0, 1): self.tired()
  def flee(self):
    if self.state != 'fight': 
      print (f"{self.name} runs in circles for a while.") 
      self.tired()
    else:
      if random.randint(1, self.health + 5) > random.randint(1, self.enemy.health):
        print (f"{self.name} runs the fuck away from {self.enemy.name}.")
        self.enemy = None
        self.state = 'normal'
      else: 
        print (f"{self.name} couldn't escape from {self.enemy.name}!")
        self.enemy_attacks()
  def attack(self):
    if self.state != 'fight': 
      print (f"{self.name} swats the air, and fucking fails so damn hard.")
      self.tired()
    else:
      if self.do_damage(self.enemy):
        print (f"{self.name} executes {self.enemy.name}!")
        self.enemy = None
        self.state = 'normal'
        if random.randint(0, self.health) < 10:
          self.health = self.health + 1
          self.health_max = self.health_max + 1
          print (f"{self.name} feels litty AF!") 
      else: 
        self.enemy_attacks()
  def enemy_attacks(self):
    if self.enemy.do_damage(self): 
      print (f"{self.name} was pwned by {self.enemy.name}!!!\nR.I.P.")
  def eat(self):
    if self.food >= 1:
      if self.state != 'normal':
        print (f"{ self.name} is too busy right now!")
        self.enemy_attacks()
      else:
        print (f"{ self.name} rested to eat some tendies and drink some dew.")
        if self.health < self.health_max:
          health_buff = self.health_max - self.health
          self.health = self.health + health_buff
          self.food = self.food - 1
        else:
          print('You are already full.')
    else:
      print('You dont have any food in your pack. You should forage.')
  def forage(self):
    if self.state != 'normal':
      print (f"{ self.name} is too busy right now!")
      self.enemy_attacks()
    else:
      print (f"{ self.name} forages for food.")
      if random.randint(0, 1):
        self.enemy = Enemy(self)
        print (f"{ self.name} finds tendies and dew!")
        self.food = self.food +1
      else:
        if random.randint(0, 1): self.tired()
Commands = {
  'quit': Player.quit,
  'help': Player.help,
  'status': Player.status,
  'rest': Player.rest,
  'explore': Player.explore,
  'run away': Player.flee,
  'fight': Player.attack,
  'eat':Player.eat,
  'forage':Player.forage
  }
Commands_Help = {
  'quit':  "Quits the game",
  'help': "Shows commands",
  'status': "Shows health and food levels",
  'rest': "Rest regens 1 hp",
  'explore': "Explore the area",
  'run away': "Attempt to run away from enemy",
  'fight': "Start fight with enemy",
  'eat': "If player has food, will refill health to full",
  'forage': "finds food for player to regain health"
  }

p = Player()
print("  ██▓    ▓█████   ▄████ ▓█████  ███▄    █ ▓█████▄   ██████")
print(" ▓██▒    ▓█   ▀  ██▒ ▀█▒▓█   ▀  ██ ▀█   █ ▒██▀ ██▌▒██    ▒")
print(" ▒██░    ▒███   ▒██░▄▄▄░▒███   ▓██  ▀█ ██▒░██   █▌░ ▓██▄")
print(" ▒██░    ▒▓█  ▄ ░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒░▓█▄   ▌  ▒   ██▒")
print(" ░██████▒░▒████▒░▒▓███▀▒░▒████▒▒██░   ▓██░░▒████▓ ▒██████▒▒")
print(" ░ ▒░▓  ░░░ ▒░ ░ ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒▓  ▒ ▒ ▒▓▒ ▒ ░")
print(" ░ ░ ▒  ░ ░ ░  ░  ░   ░  ░ ░  ░░ ░░   ░ ▒░ ░ ▒  ▒ ░ ░▒  ░ ░")
print("   ░ ░      ░   ░ ░   ░    ░      ░   ░ ░  ░ ░  ░ ░  ░  ░")
print("    ░  ░   ░  ░      ░    ░  ░         ░    ░          ░")
print("                                           ░")
print("  ▒█████    █████▒   ▄▄▄█████▓ ██░ ██ ▓█████")
print(" ▒██▒  ██▒▓██   ▒    ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀")
print(" ▒██░  ██▒▒████ ░    ▒ ▓██░ ▒░▒██▀▀██░▒███")
print(" ▒██   ██░░▓█▒  ░    ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄")
print(" ░ ████▓▒░░▒█░         ▒██▒ ░ ░▓█▒░██▓░▒████▒")
print(" ░ ▒░▒░▒░  ▒ ░         ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░")
print("   ░ ▒ ▒░  ░             ░     ▒ ░▒░ ░ ░ ░  ░")
print(" ░ ░ ░ ▒   ░ ░         ░       ░  ░░ ░   ░")
print("     ░ ░                       ░  ░  ░   ░  ░")
print("")
print("  ██░ ██  ██▓▓█████▄ ▓█████▄ ▓█████  ███▄    █    ▄▄▄█████▓▓█████  ███▄    █ ▓█████▄  ██▓▓█████   ██████ ")
print(" ▓██░ ██▒▓██▒▒██▀ ██▌▒██▀ ██▌▓█   ▀  ██ ▀█   █    ▓  ██▒ ▓▒▓█   ▀  ██ ▀█   █ ▒██▀ ██▌▓██▒▓█   ▀ ▒██    ▒ ")
print(" ▒██▀▀██░▒██▒░██   █▌░██   █▌▒███   ▓██  ▀█ ██▒   ▒ ▓██░ ▒░▒███   ▓██  ▀█ ██▒░██   █▌▒██▒▒███   ░ ▓██▄   ")
print(" ░▓█ ░██ ░██░░▓█▄   ▌░▓█▄   ▌▒▓█  ▄ ▓██▒  ▐▌██▒   ░ ▓██▓ ░ ▒▓█  ▄ ▓██▒  ▐▌██▒░▓█▄   ▌░██░▒▓█  ▄   ▒   ██▒")
print(" ░▓█▒░██▓░██░░▒████▓ ░▒████▓ ░▒████▒▒██░   ▓██░     ▒██▒ ░ ░▒████▒▒██░   ▓██░░▒████▓ ░██░░▒████▒▒██████▒▒")
print("  ▒ ░░▒░▒░▓   ▒▒▓  ▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒░   ▒ ▒      ▒ ░░   ░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒▓  ▒ ░▓  ░░ ▒░ ░▒ ▒▓▒ ▒ ░")
print("  ▒ ░▒░ ░ ▒ ░ ░ ▒  ▒  ░ ▒  ▒  ░ ░  ░░ ░░   ░ ▒░       ░     ░ ░  ░░ ░░   ░ ▒░ ░ ▒  ▒  ▒ ░ ░ ░  ░░ ░▒  ░ ░")
print("  ░  ░░ ░ ▒ ░ ░ ░  ░  ░ ░  ░    ░      ░   ░ ░      ░         ░      ░   ░ ░  ░ ░  ░  ▒ ░   ░   ░  ░  ░  ")
print("  ░  ░  ░ ░     ░       ░       ░  ░         ░                ░  ░         ░    ░     ░     ░  ░      ░  ")
print("            ░       ░                                                       ░")
print("")
time.sleep(1)
print("What is your name, Tendie seeker? You are new to these parts. ")
p.name = input("Enter name: ")
time.sleep(1)
print("")
print("[-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-]")
print (f"Hello...{p.name}")
time.sleep(1)
print("...Welcome to Legends of the Hidden Tendies...")
print("[-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-]")
time.sleep(1)
print("")
print (f" {p.name} enters a dark cave in search of chicken tendies, mountain dew, and m'lady's. Unaware of the evils that lie ahead.")
time.sleep(.5)
print("")
print("------------------------NOTE-----------------------")
print("during the game, type help to get a list of actions")
print("---------------------------------------------------")
print("")
while(p.health > 0):
  line = input("> ")
  args = line.split()
  if len(args) > 0:
    commandFound = False
    for c in Commands.keys():
      if args[0] == c[:len(args[0])]:
        Commands[c](p)
        commandFound = True
        break
    if not commandFound:
      print (f"{p.name} doesn't understand the suggestion.")