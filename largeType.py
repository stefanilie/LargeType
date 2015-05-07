import pygame
import sys
from pygame.locals import *
import math


class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message


class LargeType(object):
    def __init__(self, word):
        pygame.init()
        self.font_size = 1
        self.resolution = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.resolution.current_w, self.resolution.current_h))
        self.font = pygame.font.Font(None, self.font_size)
        pygame.display.set_caption('LargeType')

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.word = word

    def render_text_small(self):
        text = self.font.render(self.word, 1, (255, 255, 255))
        self.font_size = 1
        #streching the text as far as it can 
        while text.get_width() < self.resolution.current_w-80 and text.get_height() < self.resolution.current_h:
            self.font_size += 5
            self.font = pygame.font.Font(None, self.font_size)
            text = self.font.render(self.word, 1, (255, 255, 255))
        
        self.text = text

    def paint(self):
        textPosition= self.text.get_rect()
        textPosition.centerx = self.background.get_rect().centerx
        textPosition.centery = self.background.get_rect().centery
        self.background.blit(self.text, textPosition)

        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

    def render_text(self, justification=1):
        text = self.font.render(self.word, 1, (255, 255, 255))
        fontSize = 2
        # calculate font size proportionaly by width and height of the screen
        text_width = text.get_width()
        screen_width = self.resolution.current_w

        if text_width <= 100:
            self.font_size = pygame.font.Font(None, fontSize)
            while self.font.size(self.word)[0] <= self.resolution.current_w - 20:
                fontSize += 1
                self.font = pygame.font.Font(None, fontSize)

        else:
            fontSize = (self.resolution.current_w / text_width * 5) * fontSize + 5
            screen_width -= (3.0 / 100) * self.resolution.current_w
            
        self.font = pygame.font.Font(None, fontSize)
        text = self.font.render(self.word, 1, (255, 255, 255))
        self.text = text

        final_lines = []
        requested_lines = self.word.splitlines()

        font = pygame.font.Font(None, fontSize)

        for requested_line in requested_lines:
            if self.font.size(requested_line)[0] > screen_width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= screen_width:
                        raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.    
                    if self.font.size(test_line)[0] < screen_width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        rect = Rect(0, 0, screen_width, self.resolution.current_h)

        surface = pygame.Surface(rect.size)

        accumulated_height = 0
        text_color = (255, 255, 255)
        for line in final_lines:
            if accumulated_height + self.font.size(line)[1] >= rect.height:
                raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
            if line != "":
                tempsurface = self.font.render(line, 1, (255, 255, 255))
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException, "Invalid justification argument: " + str(justification)
            accumulated_height += font.size(line)[1]

        return surface




if __name__ == '__main__':
    if(len(sys.argv) != 2):
        sys.exit('Usage: largeType.py <string>')

    word=str(sys.argv[1])
    typer = LargeType(word)

    if len(word) < 10:
        typer.render_text_small()
        typer.paint()
        typer.screen.blit(typer.background, (0, 0))
        pygame.display.flip()
    else:
        renderd_text = typer.render_text()
        my_rect = Rect(0, 0, typer.resolution.current_w, typer.resolution.current_h)
        x = my_rect.width
        y = my_rect.height
        if len(word) < 30:
            x = int(math.ceil(1./100 * x))
        else:
            x = int(math.ceil(3./100 * x))

        y = int(math.ceil(20./100 * y))
        if renderd_text:
           typer.screen.blit(renderd_text, (x, y))

        pygame.display.update()


    while not pygame.event.wait().type in (QUIT, KEYDOWN):
        pass