#ToDo: add validation for sapce character

import pygame
import sys
from pygame.locals import *

pygame.init()

def setup_display(strWord):
	fontSize=1
	screen_resolution = pygame.display.Info()
	screen = pygame.display.set_mode((screen_resolution.current_w, screen_resolution.current_h))
	font = pygame.font.Font(None, fontSize)
	pygame.display.set_caption('LargeType')
	arrToReturn={
		'screen': screen,
		'font': font,
		'word': strWord,
		'resolution': screen_resolution
	}
	return arrToReturn

def setup_background(screen):
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))
	return background

def render_text(stuff):
	text = stuff['font'].render(stuff['word'], 1, (255, 255, 255))
	fontSize = 1
	#streching the text as far as it can 
	while text.get_width()<stuff['resolution'].current_w-80 and text.get_height()<stuff['resolution'].current_h:
		fontSize+=5
		stuff['font'] = pygame.font.Font(None, fontSize)
		text = stuff['font'].render(stuff['word'], 1, (255, 255, 255))
	print fontSize
	stuff['text'] = text
	return stuff

def paint(stuff):
	textPosition= stuff['text'].get_rect()
	textPosition.centerx = stuff['background'].get_rect().centerx
	textPosition.centery = stuff['background'].get_rect().centery 
	stuff['background'].blit(stuff['text'], textPosition)

	stuff['screen'].blit(stuff['background'], (0,0))
	pygame.display.flip()
	return stuff

def main(argv):
	if(len(sys.argv) != 2):
		sys.exit('Usage: largeType.py <string>')

	word=str(sys.argv[1])

	#getting display size and setting up font
	stuff = setup_display(word)

	#setting up background 
	stuff['background']=setup_background(stuff['screen'])

	stuff = render_text(stuff)
	stuff = paint(stuff)
	

	#this below is for spliting into two parts if expression is larger than screen_w
	#firstpart, secondpart = string[:len(string)/2], string[len(string)/2:]

#	if fontSize<60:	
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
					return
			if event.type == QUIT:
				return

		stuff['screen'].blit(stuff['background'], (0, 0))
		pygame.display.flip()

if __name__ == "__main__":
	main(sys.argv[1:])