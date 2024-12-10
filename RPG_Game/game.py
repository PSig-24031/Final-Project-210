import pygame  
import os  
from collections import deque  
  
pygame.init()  
  
screen_width = 800  
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("Turn-Based Strategy Game")  
  
map_image_path = 'image/map/map3.jpg'  
map_image = pygame.image.load(map_image_path).convert_alpha()  
map_image = pygame.transform.scale(map_image, (screen_width, screen_height))  
  
dialogue_box_image_path = 'image/icon/dilaoguebox.png'  
dialogue_box_image = pygame.image.load(dialogue_box_image_path).convert_alpha()  
dialogue_box_image = pygame.transform.scale(dialogue_box_image, (720, 80))
  
combat_background_image_path = 'image/background/battleback1.png'  
combat_background_image = pygame.image.load(combat_background_image_path).convert_alpha()  
combat_background_image = pygame.transform.scale(combat_background_image, (screen_width, screen_height))  
  
main_screen_image_path = 'image/MainScreen/main.jpg'
main_screen_image = pygame.image.load(main_screen_image_path).convert_alpha()
main_screen_image = pygame.transform.scale(main_screen_image, (screen_width, screen_height))

pygame.font.init()  
font = pygame.font.Font(None, 24) 
skill_tree_font = pygame.font.Font(None, 24) 

def draw_main_menu():
    screen.blit(main_screen_image, (0, 0))

    button_width = 200
    button_height = 50
    play_button_x = screen_width // 2 - button_width // 2
    play_button_y = screen_height // 2 - button_height // 2 - 30
    quit_button_x = screen_width // 2 - button_width // 2
    quit_button_y = screen_height // 2 - button_height // 2 + 30

    pygame.draw.rect(screen, (0, 255, 0), (play_button_x, play_button_y, button_width, button_height))
    play_text = font.render("Play", True, (0, 0, 0))
    screen.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))

    pygame.draw.rect(screen, (255, 0, 0), (quit_button_x, quit_button_y, button_width, button_height))
    quit_text = font.render("Quit", True, (0, 0, 0))
    screen.blit(quit_text, (quit_button_x + button_width // 2 - quit_text.get_width() // 2, quit_button_y + button_height // 2 - quit_text.get_height() // 2))
    return play_button_x, play_button_y, button_width, button_height, quit_button_x, quit_button_y

def draw_map():  
   screen.blit(map_image, (0, 0))  
  
def draw_dialogue_box(text):  
   screen.blit(dialogue_box_image, (screen_width // 2 - dialogue_box_image.get_width() // 2, screen_height - dialogue_box_image.get_height() - 10))
   lines = split_text_into_lines(text, font, dialogue_box_image.get_width() - 20) 
   for i, line in enumerate(lines):  
      text_surface = font.render(line, True, (0, 0, 0)) 
      
      text_rect = text_surface.get_rect(topleft=(screen_width // 2 - dialogue_box_image.get_width() // 2 + 10, screen_height - dialogue_box_image.get_height() - 10 + 10 + i * 24))  
      screen.blit(text_surface, text_rect)  
  
def split_text_into_lines(text, font, max_width):  
   words = text.split(' ')  
   lines = []  
   current_line = ''  
   for word in words:  
      test_line = current_line + word + ' '  
      if font.size(test_line)[0] <= max_width:  
        current_line = test_line  
      else:  
        lines.append(current_line)  
        current_line = word + ' '  
   lines.append(current_line)  
   return lines  
  
def draw_health_bar(current_hp, max_hp, x, y, width, height, color):  
   ratio = current_hp / max_hp  
   pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height)) 
   pygame.draw.rect(screen, color, (x, y, width * ratio, height)) 
  
def draw_skill_tree(node, x, y, depth=0):  
   text_surface = skill_tree_font.render(node.name, True, (255, 255, 255))  
   text_rect = text_surface.get_rect(center=(x, y + depth * 20))  
   screen.blit(text_surface, text_rect)  
   for i, child in enumerate(node.children):  
      draw_skill_tree(child, x + (i - len(node.children) // 2) * 100, y, depth + 1)  
  
def draw_inventory(player):  
   x = 10  
   y = 10  
   for item in player.inventory:  
      text_surface = font.render(item, True, (255, 255, 255)) 
      screen.blit(text_surface, (x, y))  
      y += 30 
  
def draw_stats_skill_tree(player, node, depth=0, y_offset=0):
    text_surface = skill_tree_font.render(node.name, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    screen.blit(text_surface, text_rect)
    for i, child in enumerate(node.children):
        draw_stats_skill_tree(player, child, depth + 1, y_offset + (i + 1) * 40)
    
    points_text = f"Upgrade Points: {player.upgrade_points}"
    points_surface = skill_tree_font.render(points_text, True, (255, 255, 255))
    points_rect = points_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 60))
    screen.blit(points_surface, points_rect)

def draw_abilities_skill_tree(node, depth=0, y_offset=0):
    text_surface = skill_tree_font.render(node.name, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    screen.blit(text_surface, text_rect)
    for i, child in enumerate(node.children):
        draw_abilities_skill_tree(child, depth + 1, y_offset + (i + 1) * 40)

def handle_stats_skill_tree_input(player, node):
    keys = pygame.key.get_pressed()
    if player.upgrade_points > 0:
        if keys[pygame.K_1] and node.children:
            node.children[0].upgrade_function(player)
            player.upgrade_points -= 1
        elif keys[pygame.K_2] and len(node.children) > 1:
            node.children[1].upgrade_function(player)
            player.upgrade_points -= 1
        elif keys[pygame.K_3] and len(node.children) > 2:
            node.children[2].upgrade_function(player)
            player.upgrade_points -= 1

def handle_abilities_skill_tree_input(player, node):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1] and node.children:
        node.children[0].upgrade_function(player)
    elif keys[pygame.K_2] and len(node.children) > 1:
        node.children[1].upgrade_function(player)
    elif keys[pygame.K_3] and len(node.children) > 2:
        node.children[2].upgrade_function(player)

def draw_player_stats(player):
    player.rect.center = (screen_width // 2, screen_height // 2 - 100)
    player.set_action('idle')
    player.update()
    player.draw()

    stats_box_x = screen_width // 2 - 150
    stats_box_y = screen_height // 2
    stats_box_width = 430
    stats_box_height = 200
    pygame.draw.rect(screen, (0, 0, 0), (stats_box_x, stats_box_y, stats_box_width, stats_box_height))
    pygame.draw.rect(screen, (255, 255, 255), (stats_box_x, stats_box_y, stats_box_width, stats_box_height), 2)

    stats_text = [
        f"Name: {player.name}",
        f"HP: {player.hp}/{player.max_hp}",
        f"Strength: {player.strength}",
        f"Defense: {player.defense}",
        f"Potions: {player.inventory.get('potion', 0)}",
        f"Abilities: {', '.join(player.abilities.keys())}"
    ]
    for i, line in enumerate(stats_text):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (stats_box_x + 10, stats_box_y + 10 + i * 30))

class Player:
    def __init__(self, x, y, name, max_hp, strength, defense, potions, scale, flip=False, can_run=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.defense = defense
        self.potions = potions
        self.alive = True
        self.inventory = {'sword': 1, 'potion': 1, 'shield': 1}  
        self.abilities = {'fireball': 10, 'ice shard': 15, 'lightning strike': 20} 
        self.power_points = 0
        self.upgrade_points = 5 

        self.animation_list = {'idle': [], 'run': []} 
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 'idle'
        self.flip = flip


        self.load_animation('idle', scale, flip)
        if can_run:
            self.load_animation('run', scale, flip)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def load_animation(self, action, scale, flip):
        image_path = f'image/{self.name}/{action}/{action.capitalize()}-Sheet.png'
        sprite_sheet = pygame.image.load(image_path).convert_alpha()

        frame_count = sprite_sheet.get_width() // sprite_sheet.get_height()
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()

        frames = []
        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
            if flip:
                frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)
        self.animation_list[action] = frames

    def update(self):
        animation_cooldown = 150 
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

        self.image = self.animation_list[self.action][self.frame_index]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self):
        screen.blit(self.image, self.rect)

    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, target):
        damage = self.strength + self.inventory.get('sword', 0) * 10
        target.hp -= max(0, damage - target.defense)
        if target.hp <= 0:
            target.hp = 0
            target.alive = False

    def use_potion(self):
        if self.inventory.get('potion', 0) > 0:
            self.hp = min(self.max_hp, self.hp + 20)
            self.inventory['potion'] -= 1
            if self.inventory['potion'] == 0:
                del self.inventory['potion']

    def use_ability(self, ability, target):
        damage = self.abilities[ability]
        target.hp -= max(0, damage - target.defense)

    def add_item(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1

    def remove_item(self, item):
        if self.inventory.get(item, 0) > 0:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
        return item
  
class SkillTreeNode:  
   def __init__(self, name, upgrade_function=None):  
      self.name = name  
      self.upgrade_function = upgrade_function  
      self.children = []  
  
   def add_child(self, child_node):  
      self.children.append(child_node)  
  
root_stats = SkillTreeNode("Root")  
attack_node = SkillTreeNode("Upgrade Attack", lambda player: setattr(player, 'strength', player.strength + 5))  
defense_node = SkillTreeNode("Upgrade Defense", lambda player: setattr(player, 'defense', player.defense + 5))  
vitality_node = SkillTreeNode("Upgrade Vitality", lambda player: setattr(player, 'max_hp', player.max_hp + 20))  
  
root_stats.add_child(attack_node)  
root_stats.add_child(defense_node)  
root_stats.add_child(vitality_node)  
  
root_abilities = SkillTreeNode("Root")  
fireball_node = SkillTreeNode("Upgrade Fireball", lambda player: player.abilities.update({'fireball': player.abilities['fireball'] + 5}))  
ice_shard_node = SkillTreeNode("Upgrade Ice Shard", lambda player: player.abilities.update({'ice shard': player.abilities['ice shard'] + 5}))  
lightning_strike_node = SkillTreeNode("Upgrade Lightning Strike", lambda player: player.abilities.update({'lightning strike': player.abilities['lightning strike'] + 5}))  
  
root_abilities.add_child(fireball_node)  
root_abilities.add_child(ice_shard_node)  
root_abilities.add_child(lightning_strike_node)  

scale = 1.5 
  
player_x = screen_width // 2  
player_y = screen_height // 2 + 50  
Kebin = Player(player_x, player_y, 'player', 100, 25, 15, 3, scale, can_run=True)  
  
mob_x = screen_width - 140   
mob_y = screen_height - 128 
mob = Player(mob_x, mob_y, 'mob', 200, 10, 15, 0, scale, flip= False, can_run=False)  

mob_list = [mob]

dialogue_texts = [  
   "Mamma mia! Why am I here? I can't remember a thing! Did I hit my head or am I just sleep-deprived?",  
   "Oh yeah, those Typhlosion! They're like walking fire hazards! How do they even get so strong?! What is this skeleton thing? Is it a Halloween decoration gone rogue? And why is it moving?!",  
   "Well, guess I'm fighting this... Can it get any weirder than this?!"  
]  
dialogue_index = 0  

clock = pygame.time.Clock()
run = True
show_dialogue = False
in_combat = False
player_turn = True
combat_over = False
combat_message_time = 0
combat_message_duration = 2000
show_skill_tree = False
show_abilities = False
show_skill_tree_upgrade = False
show_player_stats = False
show_main_menu = True 

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if show_main_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                play_button_x, play_button_y, button_width, button_height, quit_button_x, quit_button_y = draw_main_menu()
                if play_button_x <= mouse_x <= play_button_x + button_width and play_button_y <= mouse_y <= play_button_y + button_height:
                    show_main_menu = False 
                elif quit_button_x <= mouse_x <= quit_button_x + button_width and quit_button_y <= mouse_y <= quit_button_y + button_height:
                    run = False 
        else:
            if event.type == pygame.KEYDOWN and show_dialogue:
                if event.key == pygame.K_RETURN:
                    dialogue_index += 1
                    if dialogue_index >= len(dialogue_texts):
                        show_dialogue = False
                        in_combat = True
                        dialogue_index = 0
            if event.type == pygame.KEYDOWN and show_skill_tree:
                handle_stats_skill_tree_input(Kebin, root_stats)
                if Kebin.upgrade_points == 0:
                    show_skill_tree = False
                    show_skill_tree_upgrade = True
            if event.type == pygame.KEYDOWN and show_skill_tree_upgrade:
                handle_abilities_skill_tree_input(Kebin, root_abilities)
                show_skill_tree_upgrade = False
                show_player_stats = True

    if show_main_menu:
        screen.fill((0, 0, 0))
        draw_main_menu()
    else:
        screen.fill((0, 0, 0))
        draw_map()
        draw_inventory(Kebin)

        if not in_combat and not combat_over and not show_skill_tree and not show_abilities and not show_skill_tree_upgrade and not show_player_stats:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT]:
                dx = -3  
                Kebin.set_action('run')
                Kebin.flip = True
            elif keys[pygame.K_RIGHT]:
                dx = 3 
                Kebin.set_action('run')
                Kebin.flip = False
            if keys[pygame.K_UP]:
                dy = -3 
                Kebin.set_action('run')
            elif keys[pygame.K_DOWN]:
                dy = 3  
                Kebin.set_action('run')
            if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                Kebin.set_action('idle')

            Kebin.move(dx, dy)

            for mob in mob_list:
                if Kebin.rect.colliderect(mob.rect):
                    show_dialogue = True

            Kebin.update()
            Kebin.draw()
            for mob in mob_list:
                mob.update()
                mob.draw()

            if show_dialogue:
                draw_dialogue_box(dialogue_texts[dialogue_index])
        elif in_combat:
            screen.blit(combat_background_image, (0, 0)) 
            draw_health_bar(Kebin.hp, Kebin.max_hp, 100, 50, 200, 20, (0, 255, 0))
            draw_health_bar(mob.hp, mob.max_hp, screen_width - 250, 25, 200, 20, (0, 255, 0))
            draw_inventory(Kebin) 

            Kebin.rect.center = (200, screen_height // 2)
            mob.rect.center = (screen_width - 200, screen_height // 2)

            current_time = pygame.time.get_ticks()

            if player_turn:
                # Player's turn
                Kebin.set_action('idle')
                mob.set_action('idle')
                Kebin.update()
                mob.update()
                Kebin.draw()
                mob.draw()
                if current_time - combat_message_time < combat_message_duration:
                    draw_dialogue_box("Player's turn: Press A to attack, P to use potion")
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a]:
                        Kebin.attack(mob)
                        player_turn = False
                        combat_message_time = current_time
                    elif keys[pygame.K_p]:
                        Kebin.use_potion()
                        player_turn = False
                        combat_message_time = current_time
            else:
                # Mob's turn
                Kebin.set_action('idle')
                mob.set_action('idle')
                Kebin.update()
                mob.update()
                Kebin.draw()
                mob.draw()
                if current_time - combat_message_time < combat_message_duration:
                    draw_dialogue_box("Mob's turn")
                else:
                    mob.attack(Kebin)
                    player_turn = True
                    combat_message_time = current_time

            # Check for game over
            if Kebin.hp <= 0:
                in_combat = False
            elif mob.hp <= 0:
                in_combat = False
                combat_over = True
                show_skill_tree = True

        if show_skill_tree:
            screen.fill((0, 0, 0))  # Clear the screen
            draw_stats_skill_tree(Kebin, root_stats)
            draw_dialogue_box("Press 1 to upgrade Attack, 2 for Defense, 3 for Vitality")

        if show_skill_tree_upgrade:
            screen.fill((0, 0, 0))  # Clear the screen
            draw_abilities_skill_tree(root_abilities)
            draw_dialogue_box("Press 1 to upgrade Fireball, 2 for Ice Shard, 3 for Lightning Strike")

        if show_player_stats:
            screen.fill((0, 0, 0))  # Clear the screen
            draw_player_stats(Kebin)

    pygame.display.update()
    clock.tick(60)

pygame.quit()