import pygame as pg
import sys

pg.init()
pg.mixer.init()

screen_width = 1100
screen_height = 800
screen = pg.display.set_mode((screen_width, screen_height))

clock = pg.time.Clock()
font = "fonts/main_font.ttf"
font_large = pg.font.Font(font, 48)
font_small = pg.font.Font(font, 24)

win_text = font_small.render("YOU ARE WIN!", True, (255, 255, 255))
win_rect = win_text.get_rect()
win_rect.midtop = (screen_width // 2, screen_height // 2)

retry_text = font_small.render("PRESS F TO RESTART", True, (0, 0, 0))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (screen_width // 2, screen_height // 2)

icon = pg.image.load("icon/icong.png")
pg.display.set_icon(icon)

bg_menu = pg.image.load("images/buttons/bg_menu.jpg")
bg_menu = pg.transform.scale(bg_menu, (screen_width, screen_height))

music_kit = [
    "music/StreetKnights.ogg",
    "music/The_Lonely_Keyboard_Princess.ogg",
    "music/What_Good_is_Honor.ogg",
]
current_sound = pg.mixer.Sound(music_kit[0])
current_sound.play()
current_sound.set_volume(0.05)

enemy_image = pg.image.load("images/Enemy_1/idle/right/1.png")
enemy_image = pg.transform.scale(enemy_image, (110, 140))

enemy_dead_image = pg.image.load("images/Enemy_1/Dead/5.png")
enemy_dead_image = pg.transform.scale(enemy_dead_image, (80, 80))

ghost_image = pg.image.load("images/Enemy_2/idle/right/0.png")
ghost_image = pg.transform.scale(ghost_image, (100, 80))

ghost_dead_image = pg.image.load("images/Enemy_2/dead/right/0.png")
ghost_dead_image = pg.transform.scale(ghost_dead_image, (80, 80))

player_image = pg.image.load("images/Player/Idle/Right/(right)adventurer-idle-2-00.png")
player_image = pg.transform.scale(player_image, (60, 95))

platform_image = pg.image.load("blocks/block_purple.png")
platform_image = pg.transform.scale(platform_image, (50, 50))

stone_image = pg.image.load("blocks/block_stone.png")
stone_image = pg.transform.scale(stone_image, (50, 50))


class Menu:
    def __init__(self, punkts=None):
        if punkts is None:
            # 120, 140 - координаты пункта меню по умолчанию
            # Punkt название пунка
            # цвет пункта
            # цвет выделенного пункта
            # номер пункта
            punkts = [120, 140, "Punkt", (250, 30, 30), (250, 250, 30), 1]
        self.punkts = punkts
        self.currently_level = 0

    def render(self, surf, font_small, num_punkt):
        for i in self.punkts:
            #проверка текущего номера пункта с номером переданного функцией
            if num_punkt == i[5]:
                # закрашивается цветом активного элемента
                surf.blit(font_small.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                surf.blit(font_small.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pg.font.Font("fonts/main_font.ttf", 50)
        punkt = 0
        flag_1 = True
        while done:
            screen.blit(bg_menu, (0, 0))

            mp = pg.mouse.get_pos()
            for i in self.punkts:
                # проверка нахождения курсора на пункте меню
                if (
                    mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50
                ):
                    # передаем пункт активного элемента
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pg.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        if flag_1:
                            self.currently_level = 1
                        else:
                            self.currently_level = 2
                        done = False
                # напротив выбранного уровня отображается идентификатор "selected"
                    if punkt == 1:
                        done = False
                        punkts.append(
                            (
                                screen_width // 2 + 200,
                                screen_height // 2 + 100,
                                "selected",
                                (249, 6, 27),
                                (249, 6, 27),
                                4,
                            )
                        )
                        if (
                            screen_width // 2 + 200,
                            screen_height // 2 + 200,
                            "selected",
                            (249, 6, 27),
                            (249, 6, 27),
                            4,
                        ) in punkts:
                            punkts.remove(
                                (
                                    screen_width // 2 + 200,
                                    screen_height // 2 + 200,
                                    "selected",
                                    (249, 6, 27),
                                    (249, 6, 27),
                                    4,
                                )
                            )
                        self.currently_level = 1
                        flag_1 = True
                        player.is_dead = True

                    if punkt == 2:
                        punkts.append(
                            (
                                screen_width // 2 + 200,
                                screen_height // 2 + 200,
                                "selected",
                                (249, 6, 27),
                                (249, 6, 27),
                                4,
                            )
                        )
                        if (
                            screen_width // 2 + 200,
                            screen_height // 2 + 100,
                            "selected",
                            (249, 6, 27),
                            (249, 6, 27),
                            4,
                        ) in punkts:

                            punkts.remove(
                                (
                                    screen_width // 2 + 200,
                                    screen_height // 2 + 100,
                                    "selected",
                                    (249, 6, 27),
                                    (249, 6, 27),
                                    4,
                                )
                            )
                        self.currently_level = 2
                        flag_1 = False
                        player.is_dead = True
                    elif punkt == 3:
                        sys.exit()
            pg.display.flip()


class Platform:
    def __init__(self, x, y, image):
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, self.rect)


platforms = []
platform_width = 50
platform_height = 50


class Entity:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 5
        self.is_out = False
        self.is_dead = False
        self.jump_speed = -11
        self.gravity = 0.45
        self.is_grounded = False

        self.go = False
        self.frame = 0
        self.frame_jump = 0
        self.left = False
        self.right = True
        self.up = False

        self.attack = False
        self.frame_attack = 0
        self.sword_width = 40
        self.sword_height = 90
        self.sword_offset_x = 28
        self.sword_offset_y = 35

        self.go_enemy = True
        self.frame_enemy = 0
        self.left_enemy = False
        self.right_enemy = True

    def handle_input(self):
        # Проверяем пересечение с платформами
        for platform in platforms:
            if (
                self.rect.colliderect(platform.rect)
                and self.rect.bottom <= platform.rect.bottom
            ):
                # Если игрок столкнулся с платформой и его нижняя граница меньше или равна нижней границе платформы,
                # значит он находится на платформе и может прыгать
                self.is_grounded = True
                self.up = False
                self.y_speed = 0
                self.rect.bottom = platform.rect.top

    def kill(self, dead_image):
        # Процесс убийства игрока
        self.image = dead_image
        self.is_dead = True
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed

        self.go_enemy = False

    def update(self):
        prev_x = self.rect.x
        prev_y = self.rect.y
        # Проверяем пересечение с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.rect.x = prev_x

        self.y_speed += self.gravity

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.rect.y = prev_y

        self.rect.y += self.y_speed

        if self.is_dead:
            if self.rect.top > screen_height:
                self.is_out = True
        else:
            self.handle_input()

            if self.rect.bottom > screen_height:
                self.is_grounded = True
                self.up = False
                self.y_speed = 0
                self.rect.bottom = screen_height

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self):
        super().__init__(player_image)
        self.respawn()

        self.score = 0

    def handle_input(self):
        super().handle_input()

        self.x_speed = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_b]:
            self.attack = True
            self.go = False

        if keys[pg.K_ESCAPE]:
            game.menu()
        if keys[pg.K_a]:
            self.x_speed = -self.speed

            self.go = True
            self.left = True
            self.right = False

        elif keys[pg.K_d]:
            self.x_speed = self.speed

            self.go = True
            self.left = False
            self.right = True

        if self.is_grounded and keys[pg.K_SPACE]:
            self.is_grounded = False
            self.jump()
            self.attack = False

    def respawn(self):
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (50, 700)

    def jump(self):
        self.y_speed = self.jump_speed
        self.up = True

    def update(self):
        super().update()

        self.rect.x += self.x_speed

        if self.right:
            file = "right"
            sword_rect = pg.Rect(
                self.rect.x + self.sword_offset_x,
                self.rect.y + self.sword_offset_y,
                self.sword_width,
                self.sword_height,
            )
        elif self.left:
            file = "left"
            sword_rect = pg.Rect(
                self.rect.x - self.sword_offset_x,
                self.rect.y - self.sword_offset_y,
                self.sword_width,
                self.sword_height,
            )
        if not self.up and not self.attack:
            if self.go:
                self.frame += 0.2
                if self.frame > 5:
                    self.frame -= 5
                run = [
                    "adventurer-run-00.png",
                    "adventurer-run-01.png",
                    "adventurer-run-02.png",
                    "adventurer-run-03.png",
                    "adventurer-run-04.png",
                    "adventurer-run-05.png",
                ]
                self.image = pg.image.load(
                    "images/Player/Run/" + file + "/" + run[int(self.frame)]
                )
                self.image = pg.transform.scale(self.image, (100, 100))

            else:
                idle = "images/Player/Idle/Right/(right)adventurer-idle-2-00.png"
                self.image = pg.image.load(idle)
                self.image = pg.transform.scale(self.image, (100, 100))

        elif not self.attack:
            self.frame_jump += 2
            if self.frame_jump > 2:
                self.frame_jump -= 2
            jump = [
                "adventurer-crnr-jmp-00.png",
                "adventurer-crnr-jmp-01.png",
                "adventurer-crnr-jmp-02.png",
            ]
            self.image = pg.image.load(
                "images/Player/Jump/" + file + "/" + jump[int(self.frame_jump)]
            )
            self.image = pg.transform.scale(self.image, (100, 100))

        else:
            if self.attack:
                for enemy in list(enemies):
                    if not enemy.is_dead and sword_rect.colliderect(enemy.rect):
                        enemy.kill(enemy_dead_image)
                        self.score += 1

                self.frame_attack += 0.15
                if self.frame_attack > 4:
                    self.attack = False
                    self.frame_attack = 0

                attack_player = [
                    "adventurer-attack2-00.png",
                    "adventurer-attack2-01.png",
                    "adventurer-attack2-02.png",
                    "adventurer-attack2-03.png",
                    "adventurer-attack2-04.png",
                ]
                self.image = pg.image.load(
                    "images/Player/Attack/"
                    + file
                    + "/"
                    + attack_player[int(self.frame_attack)]
                )
                self.image = pg.transform.scale(self.image, (100, 100))


class Enemy_1(Entity):
    def __init__(self):
        super().__init__(enemy_image)
        self.spawn()

    def spawn(self):

        self.distance = 0

        self.speed = 4
        self.x_speed = self.speed
        self.right_enemy = True
        self.left_enemy = False

    def update(self):
        super().update()

        if self.right_enemy:
            self.rect.x += self.x_speed
            self.distance += abs(self.x_speed)
            if self.distance >= self.max_distance:
                self.right_enemy = False
                self.left_enemy = True
                self.x_speed = -self.speed
                self.distance = 0
        elif self.left_enemy:
            self.rect.x += self.x_speed
            self.distance += abs(self.x_speed)
            if self.distance >= self.max_distance:
                self.right_enemy = True
                self.left_enemy = False
                self.x_speed = self.speed
                self.distance = 0

        if self.right_enemy:
            file_enemy = "right/"
        elif self.left_enemy:
            file_enemy = "left/"

        if self.go_enemy:
            self.frame_enemy += 0.5
            if self.frame_enemy > 4:
                self.frame_enemy -= 4

            run_enemy = ["1.png", "2.png", "3.png", "4.png", "5.png"]
            self.image = pg.image.load(
                "images/Enemy_1/Run/" + file_enemy + run_enemy[int(self.frame_enemy)]
            )
            self.image = pg.transform.scale(self.image, (170, 180))
        else:
            if self.frame_enemy > 8:
                return
            self.frame_enemy += 0.1

            dead_enemy = [
                "1.png",
                "2.png",
                "3.png",
                "4.png",
                "5.png",
                "6.png",
                "7.png",
                "8.png",
                "9.png",
            ]
            self.image = pg.image.load(
                "images/Enemy_1/Dead/" + dead_enemy[int(self.frame_enemy)]
            )
            self.image = pg.transform.scale(self.image, (170, 180))


class Enemy_2(Entity):
    def __init__(self):
        super().__init__(ghost_image)
        self.spawn()

    def spawn(self):

        self.distance = 0
        self.speed = 2
        self.x_speed = self.speed
        self.right_enemy = True
        self.left_enemy = False

    def update(self):
        super().update()

        if self.right_enemy:
            self.rect.x += self.x_speed
            self.distance += abs(self.x_speed)
            if self.distance >= self.max_distance:
                self.right_enemy = False
                self.left_enemy = True
                self.x_speed = -self.speed
                self.distance = 0
        elif self.left_enemy:
            self.rect.x += self.x_speed
            self.distance += abs(self.x_speed)
            if self.distance >= self.max_distance:
                self.right_enemy = True
                self.left_enemy = False
                self.x_speed = self.speed
                self.distance = 0

        if self.right_enemy:
            file_ghost = "right/"
        elif self.left_enemy:
            file_ghost = "left/"

        if self.go_enemy:
            self.frame_enemy += 0.12
            if self.frame_enemy > 5:
                self.frame_enemy -= 5

            run_ghost = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
            self.image = pg.image.load(
                "images/Enemy_2/idle/" + file_ghost + run_ghost[int(self.frame_enemy)]
            )

            self.image = pg.transform.smoothscale(self.image, (65, 70))
        else:
            if self.frame_enemy > 6:
                return
            self.frame_enemy += 0.05

            dead_ghost = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "7.png"]
            self.image = pg.image.load(
                "images/Enemy_2/dead/" + file_ghost + dead_ghost[int(self.frame_enemy)]
            )
            self.image = pg.transform.scale(self.image, (150, 150))


enemies = []

player = Player()

bg_x = 0

enemy_1_x = 55
enemy_1_y = 170

enemy_2_x = 860
enemy_2_y = 110

enemy_3_x = 280
enemy_3_y = 1000

ghost_1_x = 0
ghost_1_y = 0

ghost_2_x = 400
ghost_2_y = 100

ghost_3_x = 800
ghost_3_y = 100

ghost_4_x = 800
ghost_4_y = 500

ghost_5_x = 800
ghost_5_y = 1000

punkts = [
    (
        screen_width // 2,
        screen_height // 2,
        "resume",
        (250, 30, 250),
        (250, 250, 30),
        0,
    ),
    (
        screen_width // 2,
        screen_height // 2 + 100,
        "Level 1",
        (250, 30, 250),
        (250, 250, 30),
        1,
    ),
    (
        screen_width // 2,
        screen_height // 2 + 200,
        "Level 2",
        (250, 30, 250),
        (250, 250, 30),
        2,
    ),
    (
        screen_width // 2,
        screen_height // 2 + 300,
        "quit",
        (250, 30, 250),
        (250, 250, 30),
        3,
    ),
]

game = Menu(punkts)
game.menu()
if game.currently_level == 1:

    bg_image = pg.image.load("bg_images/Fading_Sky-Sunset.png")
    bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))
    bg_image_2 = pg.image.load("bg_images/Fading_Sky-Sunset_2.png")
    bg_image_2 = pg.transform.scale(bg_image_2, (screen_width, screen_height))

    enemies.clear()

    enemy_1 = Enemy_1()
    enemy_1.rect.x = enemy_1_x
    enemy_1.rect.y = enemy_1_y
    enemy_1.max_distance = 170
    enemies.append(enemy_1)

    enemy_2 = Enemy_1()
    enemy_2.rect.x = enemy_2_x
    enemy_2.rect.y = enemy_2_y
    enemy_2.max_distance = 140
    enemies.append(enemy_2)

    enemy_3 = Enemy_1()
    enemy_3.rect.x = enemy_3_x
    enemy_3.rect.y = enemy_3_y
    enemy_3.max_distance = 700
    enemies.append(enemy_3)
    platforms.clear()
    map_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 1:
                platform_x = x * platform_width
                platform_y = y * platform_height
                platform = Platform(platform_x, platform_y, platform_image)
                platforms.append(platform)
elif game.currently_level == 2:

    bg_image = pg.image.load("bg_images/Wispy_Sky-Night_1.png")
    bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))
    bg_image_2 = pg.image.load("bg_images/Wispy_Sky-Night_2.png")
    bg_image_2 = pg.transform.scale(bg_image_2, (screen_width, screen_height))

    enemies.clear()

    ghost_1 = Enemy_2()
    ghost_1.rect.x = ghost_1_x
    ghost_1.rect.y = ghost_1_y
    ghost_1.max_distance = 150
    enemies.append(ghost_1)

    ghost_2 = Enemy_2()
    ghost_2.rect.x = ghost_2_x
    ghost_2.rect.y = ghost_2_y
    ghost_2.max_distance = 50
    enemies.append(ghost_2)

    ghost_3 = Enemy_2()
    ghost_3.rect.x = ghost_3_x
    ghost_3.rect.y = ghost_3_y
    ghost_3.max_distance = 270
    enemies.append(ghost_3)

    ghost_4 = Enemy_2()
    ghost_4.rect.x = ghost_4_x
    ghost_4.rect.y = ghost_4_y
    ghost_4.max_distance = 270
    enemies.append(ghost_4)

    ghost_5 = Enemy_2()
    ghost_5.rect.x = ghost_5_x
    ghost_5.rect.y = ghost_5_y
    ghost_5.max_distance = 260
    enemies.append(ghost_5)

    platforms.clear()
    map_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 1:
                platform_x = x * platform_width
                platform_y = y * platform_height
                platform = Platform(platform_x, platform_y, stone_image)
                platforms.append(platform)

running = True

while running:
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image_2, (bg_x + screen_width, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYUP:
            player.go = False
            if player.is_out and game.currently_level == 1:

                bg_image = pg.image.load("bg_images/Fading_Sky-Sunset.png")
                bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))
                bg_image_2 = pg.image.load("bg_images/Fading_Sky-Sunset_2.png")
                bg_image_2 = pg.transform.scale(
                    bg_image_2, (screen_width, screen_height)
                )

                player.score = 0
                player.respawn()
                enemies.clear()

                enemy_1 = Enemy_1()
                enemy_1.rect.x = enemy_1_x
                enemy_1.rect.y = enemy_1_y
                enemy_1.max_distance = 170
                enemies.append(enemy_1)

                enemy_2 = Enemy_1()
                enemy_2.rect.x = enemy_2_x
                enemy_2.rect.y = enemy_2_y
                enemy_2.max_distance = 140
                enemies.append(enemy_2)

                enemy_3 = Enemy_1()
                enemy_3.rect.x = enemy_3_x
                enemy_3.rect.y = enemy_3_y
                enemy_3.max_distance = 700
                enemies.append(enemy_3)

                platforms.clear()
                map_data = [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ]
                for y, row in enumerate(map_data):
                    for x, cell in enumerate(row):
                        if cell == 1:
                            platform_x = x * platform_width
                            platform_y = y * platform_height
                            platform = Platform(platform_x, platform_y, platform_image)
                            platforms.append(platform)

            elif player.is_out and game.currently_level == 2:
                bg_image = pg.image.load("bg_images/Wispy_Sky-Night_1.png")
                bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))
                bg_image_2 = pg.image.load("bg_images/Wispy_Sky-Night_2.png")
                bg_image_2 = pg.transform.scale(
                    bg_image_2, (screen_width, screen_height)
                )

                player.score = 0
                player.respawn()
                enemies.clear()

                ghost_1 = Enemy_2()
                ghost_1.rect.x = ghost_1_x
                ghost_1.rect.y = ghost_1_y
                ghost_1.max_distance = 150
                enemies.append(ghost_1)

                ghost_2 = Enemy_2()
                ghost_2.rect.x = ghost_2_x
                ghost_2.rect.y = ghost_2_y
                ghost_2.max_distance = 220
                enemies.append(ghost_2)

                ghost_3 = Enemy_2()
                ghost_3.rect.x = ghost_3_x
                ghost_3.rect.y = ghost_3_y
                ghost_3.max_distance = 270
                enemies.append(ghost_3)

                ghost_4 = Enemy_2()
                ghost_4.rect.x = ghost_4_x
                ghost_4.rect.y = ghost_4_y
                ghost_4.max_distance = 270
                enemies.append(ghost_4)

                ghost_5 = Enemy_2()
                ghost_5.rect.x = ghost_5_x
                ghost_5.rect.y = ghost_5_y
                ghost_5.max_distance = 260
                enemies.append(ghost_5)

                platforms.clear()
                map_data = [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ]
                for y, row in enumerate(map_data):
                    for x, cell in enumerate(row):
                        if cell == 1:
                            platform_x = x * platform_width
                            platform_y = y * platform_height
                            platform = Platform(platform_x, platform_y, stone_image)
                            platforms.append(platform)

    bg_x -= 0.3
    if bg_x == -screen_width:
        bg_x = 0

    score_text = font_large.render(str(player.score), True, (255, 255, 255))
    score_rect = score_text.get_rect()

    if player.score == 5 and game.currently_level == 2:
        screen.blit(win_text, win_rect)
    elif player.score == 3 and game.currently_level == 1:
        screen.blit(win_text, win_rect)
    if player.is_out:
        score_rect.midbottom = (screen_width // 2, screen_height // 2)
        screen.blit(retry_text, retry_rect)
    else:
        player.update()
        player.draw(screen)

        for enemy in list(enemies):
            if enemy.is_out:
                enemies.remove(enemy)
            else:
                enemy.update()
                enemy.draw(screen)

            if (
                not player.is_dead
                and not enemy.is_dead
                and player.rect.colliderect(enemy.rect)
            ):
                if player.rect.bottom - player.y_speed < enemy.rect.top:
                    enemy.kill(enemy_dead_image)

                    player.jump()
                    player.score += 1
                else:
                    player.kill(player_image)

        score_rect.midtop = (screen_width // 2, 5)

        for platform in platforms:
            platform.draw(screen)

    screen.blit(score_text, score_rect)
    pg.display.flip()
    clock.tick(60)
quit()
