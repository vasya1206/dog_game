import pygame as pg
import random

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
ICON_SIZE = 80
PADDING = 5

DOG_WIDTH = 310
DOG_HEIGHT = 500

DOG_Y = 100

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

FOOD_SIZE = 200
TOY_SIZE = 100

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130

FPS = 60

font = pg.font.Font(None, 40)
font_mini = pg.font.Font(None, 15)
font_maxi = pg.font.Font(None, 200)

def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text):
    return font.render(str(text), True, "black")




class Item:
    def __init__(self, name, price, file):
        self.name = name
        self.price = price
        self.file = file
        self.image = load_image(file, DOG_WIDTH // 1.7, DOG_HEIGHT // 1.7)
        self.is_using = False
        self.is_bought = False

        self.full_image = load_image(file, DOG_WIDTH, DOG_HEIGHT)




class ClothesMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Item("Синяя футболка", 10, "t-shirt.png"),
                      Item("Ботинки", 50, "boots.png"),
                      Item("Шляпа", 50, "hat.png")]

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперёд", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)

        self.previous_button = Button("Назад", MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                      width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                      func=self.to_previous)

        self.use_button = Button("Надеть", MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD - 50 - PADDING,
                                 width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                 func=self.use_item)

        self.buy_button = Button("Купить", SCREEN_WIDTH // 2 - int(BUTTON_WIDTH // 1.5) // 2,
                                 SCREEN_HEIGHT // 2 + 95,
                                 width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5),
                                 func=self.buy)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.use_text = text_render("Надето")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midright = (SCREEN_WIDTH - 150, 130)

        self.buy_text = text_render("Куплено")
        self.buy_text_rect = self.buy_text.get_rect()
        self.buy_text_rect.midright = (SCREEN_WIDTH - 140, 200)

    def update(self):
        self.next_button.update()
        self.previous_button.update()
        self.use_button.update()
        self.buy_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.previous_button.is_clicked(event)
        self.use_button.is_clicked(event)
        self.buy_button.is_clicked(event)

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def use_item(self):
        self.items[self.current_item].is_using = not self.items[self.current_item].is_using
        print(self.items[self.current_item].is_using)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))
        if self.items[self.current_item].is_using:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))
        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.use_button.draw(screen)
        self.buy_button.draw(screen)

        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.use_text, self.use_text_rect)
        screen.blit(self.buy_text, self.buy_text_rect)

class Food:
    def __init__(self, name, file, price,  satiety, medicine_power = 0):
        self.name = name
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)
        self.price = price
        self.satiety = satiety
        self.medicine_power = medicine_power

class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Food("Яблоко", "apple.png", 10, 5),
                      Food("Кость", "bone.png", 20, 5),
                      Food("Собачья еда", "dog food.png", 15, 5),
                      Food("Мясо", "meat.png", 30, 5),
                      Food("Лекарство", "medicine.png", 100, 0, 50)]

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперёд", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)

        self.previous_button = Button("Назад", MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                      width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                      func=self.to_previous)


        self.buy_button = Button("Съесть", SCREEN_WIDTH // 2 - int(BUTTON_WIDTH // 1.5) // 2,
                                 SCREEN_HEIGHT // 2 + 95,
                                 width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5),
                                 func=self.buy)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def update(self):
        self.next_button.update()
        self.previous_button.update()
        self.buy_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.previous_button.is_clicked(event)
        self.buy_button.is_clicked(event)

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100

            self.game.health += self.items[self.current_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100


    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)



        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.buy_button.draw(screen)

        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)


class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)


class MiniGame:
    def __init__(self, game):
        self.game = game
        self.game_background = load_image("game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def new_game(self):
        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def update(self):
        ...

    def draw(self, screen):
        screen.blit(self.game_background, (0, 0))

        #screen.blit(self.dog.image, self.dog.rect)

        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))

        self.toys.draw(screen)

class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text_font=font, func=None):
        self.func = func

        self.idle_image = load_image("button.png", width, height)
        self.pressed_image = load_image("button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_font = text_font
        self.text = self.text_font.render(str(text), True, "black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.is_pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        

        self.happiness = 100
        self.satiety = 100
        self.health = 100

        self.money = 10

        self.coins_per_second = 1
        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}

        self.items_on = []

        self.mode = "Main"

        # Загрузка фона
        self.background = load_image("background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        # Загрузка иконок
        self.happiness_image = load_image("happiness.png", ICON_SIZE, ICON_SIZE)
        self.satiety_image = load_image("satiety.png", ICON_SIZE, ICON_SIZE)
        self.health_image = load_image("health.png", ICON_SIZE, ICON_SIZE)

        self.money_image = load_image("money.png", ICON_SIZE, ICON_SIZE)

        # Загрузка изображений для собаки
        self.body = load_image("dog.png", DOG_WIDTH, DOG_HEIGHT)

        # Создание кнопок
        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.eat_button = Button("Еда", button_x, PADDING + ICON_SIZE, func = self.food_menu_on)
        self.clothes_button = Button("Одежда", button_x, PADDING * 2 + ICON_SIZE + BUTTON_HEIGHT,
                                     func=self.clothes_menu_on)
        self.play_button = Button("Игры", button_x, PADDING * 3 + ICON_SIZE + BUTTON_HEIGHT * 2,
                                  func=self.game_on)

        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0,
                                     width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                     text_font=font_mini, func=self.increase_money)

        self.buttons = [self.eat_button, self.clothes_button, self.play_button, self.upgrade_button]

        # Создание события для кликера
        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.DECREASE=pg.USEREVENT + 2
        pg.time.set_timer(self.DECREASE, 3600)


        self.clothes_menu = ClothesMenu(self)
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)

        self.run()

    def clothes_menu_on(self):
        self.mode = "Clothes menu"

    def food_menu_on(self):
        self.mode = "Food menu"

    def game_on(self):
        self.mode = "Mini game"
        self.mini_game.new_game()


    def increase_money(self):
        for cost, check in self.costs_of_upgrade.items():
            if not check and self.money >= cost:
                self.coins_per_second += 1
                self.money -= cost
                self.costs_of_upgrade[cost] = True
                break

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            if event.type == self.DECREASE:
                chance = random.randint(1,10)
                if chance <= 5:
                    self.satiety -= 1
                elif 5 < chance <= 9:
                    self.happiness -= 1
                else:
                    self.health -= 1


            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += self.coins_per_second

            for button in self.buttons:
                button.is_clicked(event)

            if self.mode != "Main":
                self.clothes_menu.is_clicked(event)
                self.food_menu.is_clicked(event)

    def update(self):
        if self.mode == "Clothes menu":
            self.clothes_menu.update()
        elif self.mode == "Food menu":
            self.food_menu.update()
        elif self.mode == "Mini game":
            self.mini_game.update()
        else:
            for button in self.buttons:
                button.update()


    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.satiety_image, (PADDING, PADDING * 2 + ICON_SIZE))
        self.screen.blit(self.health_image, (PADDING, PADDING * 3 + ICON_SIZE * 2))

        # Упростить размещение предметов относительно других
        self.screen.blit(text_render(self.happiness), (PADDING * 2 + ICON_SIZE, PADDING * 6))
        self.screen.blit(text_render(self.satiety), (PADDING * 2 + ICON_SIZE, PADDING * 7 + ICON_SIZE))
        self.screen.blit(text_render(self.health), (PADDING * 2 + ICON_SIZE, PADDING * 8 + ICON_SIZE * 2))

        self.screen.blit(self.money_image, (SCREEN_WIDTH - PADDING - ICON_SIZE, PADDING))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - PADDING - ICON_SIZE - 40, PADDING * 6))

        # Отрисовка кнопок
        for button in self.buttons:
            button.draw(self.screen)

        # Отрисовка собаки
        self.screen.blit(self.body, (SCREEN_WIDTH // 2 - DOG_WIDTH // 2, DOG_Y))

        for item in self.clothes_menu.items:
            if item.is_using:
                self.screen.blit(item.full_image, (277, DOG_Y + 27))

        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)

        if self.mode == "Food menu":
            self.food_menu.draw(self.screen)

        if self.mode == "Mini game":
            self.mini_game.draw(self.screen)




        pg.display.flip()

if __name__ == "__main__":
    Game()
