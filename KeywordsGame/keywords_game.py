# -*- encoding: utf-8 -*-

''' ----------- Keyword game for Thach Thuc Academic Contest ----------- 
    Author: tienthanh214
    Team: Renamed
    FIT@HCMUS
'''

import json
import pygame
import random
import os
import sys

# read keywords from json
link = os.path.join("Keywords", "keywords_.json")
file = open(link)
data = json.load(file)
file.close()

# define constant here
TIME_PLAY = 2 * 60
NUM_KEYWORDs = 10

# init pygame state
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
# introImage = pygame.image.load("sound/thachthuc.png").convert()
# introImage = pygame.transform.scale(introImage, (16, 16))
# pygame.display.set_icon(introImage)

event_list = []

""" --- button object ---"""
class Button:
    def __init__(self, x, y, width, height, value, color = (242, 250, 90)):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("comicsansms", 28)
        self.text = self.font.render(value, True, (0, 0, 0))
        self.background_color = color
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

""" --- option box --- """

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
                surf.blit(msg, msg.get_rect(center = rect.center))
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

""" --- game --- """
class Game:
    def __init__(self, score = 0, keyword_index = 0):
        self.correct_button = Button(150, 500, 150, 50, "Correct")
        self.next_button = Button(width - 150 - 150, 500, 150, 50, "Ignore")
        self.continue_button = Button(150, 500, 150, 50, "Continue")
        self.summary_button = Button(width - 150 - 150, 500, 150, 50, "Summary")
        self.stop_button = Button((width - 150) // 2 + 25, 500, 100, 50, "Stop", (251, 224, 196))

        self.score = score
        self.keyword_index = keyword_index
        self.inGame = 0  # 1: in game, 2: end round, 3: summary, 0: intro
        # self.clock = pygame.time.Clock()
        self.timer = TIME_PLAY
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        # self.max_keywords = NUM_KEYWORDs

        self.result_list = []
        self.ignore_list = []
        self.data_setting = Setting(0)

        self.order_list = OptionBox(width // 10 * 2, 420, 160, 40, (150, 150, 150), (100, 200, 255), score_font, ["Random", "Sorted", "Reversed"])
        self.mode_list = OptionBox(width // 10 * 6, 420, 160, 40, (150, 150, 150), (100, 200, 255), score_font, ["Official", "Endless"])
        self.is_endless_mode = False

        self.hasUpdated = False

    def updateCounter(self, keyword_index):
        if "Count" not in data[keyword_index]:
            data[keyword_index]['Count'] = 0
        data[keyword_index]['Count'] += 1
        self.hasUpdated = True

    # handle click event on button
    def checkButton(self):
        if self.inGame == 1:
            if self.correct_button.isPressed():
                # count to prevent over-fit
                self.updateCounter(self.keyword_index)
                self.keyword_index += 1
                self.score += 1
                if self.keyword_index % NUM_KEYWORDs == 0 and self.is_endless_mode == False:
                    self.endGame()
            elif self.next_button.isPressed():
                if self.is_endless_mode == False:
                    self.ignore_list.append(data[self.keyword_index]['Keyword'])
                self.keyword_index += 1
                if self.keyword_index % NUM_KEYWORDs == 0 and self.is_endless_mode == False:
                    self.endGame()
            elif self.stop_button.isPressed():
                self.is_endless_mode = self.timer;
                self.endGame()

        elif self.inGame == 2:
            if self.summary_button.isPressed():
                self.showSummary()
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

    def showButton(self):
        self.next_button.draw(surface)
        self.correct_button.draw(surface)
        if self.is_endless_mode:
            self.stop_button.draw(surface)

    def showKeyword(self, surface, idx):
        show_str = str(data[idx]['Keyword']).split()
        # rendering every 5 word on a line avoid text-overflow 
        split_word_len = 5
        for i in range(0, len(show_str), split_word_len):
            cur_str = ' '.join(show_str[i : i + split_word_len])
            if i == 0:
                idx = idx + 1 if self.is_endless_mode else idx % NUM_KEYWORDs + 1
                value = keyword_font.render(str(idx) + ". " + cur_str, True, (0, 0, 0));
            else:
                value = keyword_font.render(cur_str, True, (0, 0, 0))
            rect = value.get_rect()
            rect.center = (width // 2, 250 + keyword_font.get_linesize() * (i // split_word_len))
            surface.blit(value, rect)
    
    def showClock(self, surface):
        if self.timer <= 0 and self.is_endless_mode == False:
            self.endGame()
        else:
            surface.blit(timer_font.render(str(self.timer), True, (0,191,255)), (width - 100, 48))

    ''' ----------- Game state ----------- '''

    def endGame(self):
        self.inGame = 2
        self.result_list.append((self.score, self.timer))
        if self.is_endless_mode == False:
            for i in range((NUM_KEYWORDs - self.keyword_index % NUM_KEYWORDs) % NUM_KEYWORDs):
                self.ignore_list.append(data[self.keyword_index + i]['Keyword'])
        self.timer = -1

    def resetGameState(self):
        self.score = 0
        self.keyword_index += NUM_KEYWORDs - self.keyword_index % NUM_KEYWORDs;
        self.inGame = 1
        self.timer = TIME_PLAY if not self.is_endless_mode else 0
        self.ignore_list.clear()
        # setup new set of keywords
        if self.is_endless_mode == False:
            if self.keyword_index + NUM_KEYWORDs > len(data):
                self.keyword_index = 0
                self.data_setting.prepare_data()

            self.data_setting.setting(self.keyword_index, self.keyword_index + NUM_KEYWORDs);
        else:
            self.keyword_index = 0
            self.data_setting.prepare_data()
    # --- setup summary stage show all round ----

    def showSummary(self):
        self.inGame = 3
        surface.fill((255, 255, 255))
        value = keyword_font.render("Summary", True, (0, 0, 0));
        rect = value.get_rect()
        rect.center = (width // 2, 50)
        surface.blit(value, rect)
        # for i in range(20): self.result_list.append((10, 10))
        for i in range(len(self.result_list)):
            value = score_font.render("[" + str(i + 1) + "] " + str(self.result_list[i][0]) + " - " + str(self.result_list[i][1]) + "s.", True, (255, 0, 0))
            surface.blit(value, (200 * (i // 10 + 0) + 10, 50 * (i % 10 + 2)))

        self.again_button = Button(600, 500, 150, 50, "Play again")
        self.again_button.draw(surface)

        if self.hasUpdated:
            self.hasUpdated = False            
            with open(link, 'w') as file:
                file.write(json.dumps(data, indent = 4))
                file.close()

    # ----- set up intro stage ----
    
    def setupOrderChoice(self):
        order_choice_index = self.order_list.update()
        if (order_choice_index == 1):
            self.data_setting.order = 1
        elif (order_choice_index == 2):
            self.data_setting.order = -1
        elif (order_choice_index == 0):
            self.data_setting.order = 0
        self.order_list.draw(surface)

    def setupModeChoice(self):
        mode_choice_index = self.mode_list.update()
        if (mode_choice_index == 1):
            self.timer = 0
            self.is_endless_mode = True
        elif (mode_choice_index == 2):
            self.is_endless_mode = False
        elif (mode_choice_index == 0):
            self.timer = TIME_PLAY
            self.is_endless_mode = False
        self.mode_list.draw(surface)

    def gameIntro(self):
        surface.fill((51, 204, 255))
        value = title_font.render("Keywords Guess Game", True, (255, 255, 255))
        rect = value.get_rect()
        rect.center = (width // 2, 200)
        surface.blit(value, rect)

        font = pygame.font.SysFont("comicsansms", 18, italic = True)
        value = font.render("Author: NĐTT - 19120036 - Renamed team (2021)", True, (255, 255, 255))
        surface.blit(value, [width - 440, height - 30])

        self.setupOrderChoice()
        self.setupModeChoice()    

        # setup button
        self.play_button = Button(width // 2 - 150 // 2, rect.center[1] + 150 - 10, 150, 50, "Play")
        self.play_button.draw(surface)

        # surface.blit(introImage, (width // 8, 450))
        # pygame.display.flip()

    # --- game over state - show score of round ---

    def gameOver(self):
        pygame.mixer.music.stop()
        self.inGame = 2
        surface.fill((86, 187, 241))

        if self.is_endless_mode == False: # time limit mode
            value = keyword_font.render("Your score: " + str(self.score) + "/" + str(NUM_KEYWORDs), True, (255, 255, 255))
            rect = value.get_rect()
            rect.center = (width // 2, 30)
            surface.blit(value, rect)
            for idx in range(len(self.ignore_list)):
                value = score_font.render(str(idx + 1) + ". " + str(self.ignore_list[idx]), True, (255, 255, 255));
                surface.blit(value, [100, idx * 50 + 50])
        else:
            value = keyword_font.render("Played time: " + str(self.is_endless_mode) + "s - " + "Score: " + str(self.score) + "/" + str(self.keyword_index), True, (255, 255, 255))
            rect = value.get_rect()
            rect.center = (width // 2, 30)
            surface.blit(value, rect)

        if (self.timer < -2 or self.is_endless_mode):
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
            self.showSummary()
        else:
            self.gameIntro()

''' ---- keyword order and set of keyword in round ---- '''
class Setting:
    def __init__(self, order = 0):
        # Random - Descreasing - Increasing
        #    0   -    -1       -    1
        self.order = order # random default
        self.prepare_data()

    def prepare_data(self):
        global data
        data = sorted(data, key = lambda x: ((0 if 'Count' not in x else x['Count']) + 1) * random.random())

    def load_data(self, left, right):
        if (self.order == 1):
            data[left : right] = sorted(data[left : right], key = lambda x: len(x['Keyword']))
        elif (self.order == -1):
            data[left : right] = sorted(data[left : right], key = lambda x: len(x['Keyword']), reverse = True)

    def setting(self, left = 0, right = NUM_KEYWORDs):
        self.load_data(left, right)

    pass

if __name__ == '__main__':
    game = Game(0, 0)
    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if game.inGame != 0:
                    if game.is_endless_mode: # endless mode
                        game.timer += 1
                    else:
                        game.timer -= 1
                if game.timer == 30 and not game.is_endless_mode:
                    pygame.mixer.music.play(-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.checkButton()
        # go game
        game.gamePlay()
        pygame.display.update()