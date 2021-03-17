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

""" --- button object --"""
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
        load_data()


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
            pass
        else:
            self.inGame = 1

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
        self.timer = -1

    def resetGameState(self):
        self.score = 0
        self.keyword_index += 10 - self.keyword_index % 10;
        self.inGame = 1
        self.timer = TIME_PLAY
        self.ignore_list.clear()

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

        # again_button = Button(500, 450, 150, 50, "Play again")
        # again_button.draw(surface)

    def gameIntro(self):
        surface.fill((51, 204, 255))
        value = title_font.render("Keywords Guess Game", True, (255, 255, 255))
        rect = value.get_rect()
        rect.center = (width // 2, 200)
        surface.blit(value, rect)

        font = pygame.font.SysFont("comicsansms", 18, italic = True)
        value = font.render("Author: NĐTT - 19120036 - Renamed team (2021)", True, (255, 255, 255))
        surface.blit(value, [width - 440, height - 30])

        play_button = Button(width // 2 - 150 // 2, rect.center[1] + 150, 150, 50, "Play")
        play_button.draw(surface)

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

def load_data():
    for i in range(5):
        random.shuffle(data)

if __name__ == '__main__':
    game = Game(0, 0)
    while True:
        for event in pygame.event.get():
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
