# -*- encoding: utf-8 -*-
import json
import pygame
import random

link = "Keywords\keywords_.json"
file = open(link)
data = json.load(file)

TIME_PLAY = 2 * 60
pygame.init()
pygame.mixer.init()
width = 800
height = 600
score_font = pygame.font.SysFont("comicsansms", 28)
keyword_font = pygame.font.SysFont("comicsansms", 28, bold = True)
timer_font = pygame.font.SysFont("comicsansms", 40)
title_font = pygame.font.SysFont("comicsansms", 40, bold = True)

pygame.display.set_caption("Keywords - Renamed team - Made by Jug")
surface = pygame.display.set_mode((width, height))
music = pygame.mixer.music.load("sound/30s_countdown.mp3")
introImage = pygame.image.load("sound/thachthuc.png").convert()
# introImage = pygame.transform.scale(introImage, (16, 16))
# pygame.display.set_icon(introImage)

event_list = []

""" --- button object ---"""
class Button:
    def __init__(self, x, y, width, height, value):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("comicsansms", 28)
        self.text = self.font.render(value, True, (0, 0, 0))
        self.background_color = (255, 255, 123)
        self.visible = False

    def draw(self, screen):
        """ This method will draw the button to the screen """
        # First fill the screen with the background color
        pygame.draw.rect(screen, self.background_color, self.rect)
        # Draw the edges of the button
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        # Get the width and height of the text surface
        _width = self.text.get_width()
        _height = self.text.get_height()
        # Calculate the posX and posY
        posX = self.rect.centerx - (_width / 2)
        posY = self.rect.centery - (_height / 2)
        # Draw the image into the screen
        screen.blit(self.text, [posX, posY])
        self.visible = True

    def isPressed(self):
        """ Return true if the mouse is on the button """
        pos = pygame.mouse.get_pos()
        if (self.visible) and (self.rect.collidepoint(pos)):
            self.visible = False
            return True
        else:
            return False
    pass

""" --- option box ---"""


class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
            self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1
    pass

""" --- A game --- """
class Game:
    def __init__(self, score = 0, keyword_index = 0):
        self.correct_button = Button(150, 500, 150, 50, "Correct")
        self.next_button = Button(width - 150 - 150, 500, 150, 50, "Ignore")
        self.continue_button = Button(150, 500, 150, 50, "Continute")
        self.summary_button = Button(width - 150 - 150, 500, 150, 50, "Summary")
        self.score = score
        self.keyword_index = keyword_index
        self.inGame = 0
        self.clock = pygame.time.Clock()
        self.timer = TIME_PLAY
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.result_list = []
        self.ignore_list = []
        self.data_setting = Setting(0)


        self.order_list = OptionBox(
                320, 420, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30),
                ["Random", "Sorted", "Reversed"])


    def showButton(self):
        self.next_button.draw(surface)
        self.correct_button.draw(surface)

    def checkButton(self):
        if self.inGame == 1:
            if self.correct_button.isPressed():
                self.keyword_index += 1
                self.score += 1
                if self.keyword_index % 10 == 0:
                    self.endGame()
            elif self.next_button.isPressed():
                self.ignore_list.append(data[self.keyword_index]['Keyword'])
                self.keyword_index += 1
                if self.keyword_index % 10 == 0:
                    self.endGame()

        elif self.inGame == 2:
            if self.summary_button.isPressed():
                self.showSumary()
            elif self.continue_button.isPressed():
                self.resetGameState()
        elif self.inGame == 3:
            if self.again_button.isPressed():
                self.__init__()
                self.inGame = 0
        elif self.inGame == 0:
            if (self.play_button.isPressed()):
                self.inGame = 1
                self.data_setting.setting();
        pass

    def showKeyword(self, surface, idx):
        value = keyword_font.render(str(idx % 10 + 1) + ". " + str(data[idx]['Keyword']), True, (0, 0, 0));
        rect = value.get_rect()
        rect.center = (width // 2, 250)
        surface.blit(value, rect)

    def showClock(self, surface):
        if self.timer <= 0:
            self.endGame()
        else:
            surface.blit(timer_font.render(str(self.timer), True, (0,191,255)), (width - 100, 48))

    def endGame(self):
        self.inGame = 2
        self.result_list.append((self.score, self.timer))
        if (len(self.result_list) == 30):
            self.result_list.pop(0)
        for i in range((10 - self.keyword_index % 10) % 10):
            self.ignore_list.append(data[self.keyword_index + i]['Keyword'])
        self.timer = -1

    def resetGameState(self):
        self.score = 0
        self.keyword_index += 10 - self.keyword_index % 10;
        self.inGame = 1
        self.timer = TIME_PLAY
        self.ignore_list.clear()
        self.data_setting.setting(self.keyword_index, self.keyword_index + 10);

    def showSumary(self):
        self.inGame = 3
        surface.fill((255, 255, 255))
        value = keyword_font.render("Sumary", True, (0, 0, 0));
        rect = value.get_rect()
        rect.center = (width // 2, 50)
        surface.blit(value, rect)
        # for i in range(20): self.result_list.append((10, 10))
        for i in range(len(self.result_list)):
            value = score_font.render("[" + str(i + 1) + "] " + str(self.result_list[i][0]) + " - " + str(self.result_list[i][1]) + "s.", True, (255, 0, 0))
            surface.blit(value, (200 * (i // 10 + 0) + 10, 50 * (i % 10 + 2)))

        self.again_button = Button(600, 500, 150, 50, "Play again")
        self.again_button.draw(surface)


    def gameIntro(self):
        surface.fill((51, 204, 255))
        value = title_font.render("Keywords Guess Game", True, (255, 255, 255))
        rect = value.get_rect()
        rect.center = (width // 2, 200)
        surface.blit(value, rect)

        font = pygame.font.SysFont("comicsansms", 18, italic = True)
        value = font.render("Author: NĐTT - 19120036 - Renamed team (2021)", True, (255, 255, 255))
        surface.blit(value, [width - 440, height - 30])
        choice_index = self.order_list.update()

        if (choice_index == 1):
            self.data_setting.order = 1
        elif (choice_index == 2):
            self.data_setting.order = -1
        elif (choice_index == 0):
            self.data_setting.order = 0
        self.order_list.draw(surface)
        self.play_button = Button(width // 2 - 150 // 2, rect.center[1] + 150 - 10, 150, 50, "Play")
        self.play_button.draw(surface)

        # surface.blit(introImage, (width // 8, 450))
        pygame.display.flip()

    def gameOver(self):
        pygame.mixer.music.stop()
        self.inGame = 2
        surface.fill((0, 0, 0))
        value = keyword_font.render("Your score: " + str(self.score) + "/10", True, (255, 255, 255))
        rect = value.get_rect()
        rect.center = (width // 2, 30)
        surface.blit(value, rect)

        for idx in range(len(self.ignore_list)):

            value = score_font.render(str(idx + 1) + ". " + str(self.ignore_list[idx]), True, (255, 255, 255));
            surface.blit(value, [100, idx * 50 + 50])

        if (self.timer < -2):
            self.summary_button.draw(surface)
            self.continue_button.draw(surface)


    def gamePlay(self):
        if self.inGame == 1:
            surface.fill((255, 255, 255))
            self.showButton()
            self.showKeyword(surface, self.keyword_index)
            self.showClock(surface)
        elif self.inGame == 2:
            self.gameOver()
        elif self.inGame == 3:
            self.showSumary()
        else:
            self.gameIntro()


class Setting:
    def __init__(self, order = 0):
        # Random - Descreasing - Increasing
        #    0   -    -1       -    1
        self.order = order # random default
        global data
        for i in range(10):
            random.shuffle(data)

    def load_data(self, left, right):
        if (self.order == 1):
            data[left : right] = sorted(data[left : right], key = lambda x: len(x['Keyword']))
        elif (self.order == -1):
            data[left : right] = sorted(data[left : right], key = lambda x: len(x['Keyword']), reverse = True)

    def setting(self, left = 0, right = 10):
        self.load_data(left, right)

    pass

if __name__ == '__main__':
    game = Game(0, 0)
    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT:
                if game.inGame != 0:
                    game.timer -= 1
                if game.timer == 30:
                    pygame.mixer.music.play(-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.checkButton()
        # go game
        game.gamePlay()
        pygame.display.update()

file.close()
