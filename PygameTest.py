#Import the Necessary Packages
import pygame
import DrawTest

#Initialize Pygame - Sets up the modules and data structures for Pygame
pygame.init()

#Create the Display
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')

#Initialize the clock to be used in FPS calculations
clock = pygame.time.Clock()

#Set the Boolean for Termination
crashed = False

#Main Loop
while not crashed:
	#See if the user has specified termination condition
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True
		print(event)

	#Should a draw function be called, it will be through here
	DrawTest.drawTest(gameDisplay)

	#Update the Display and Tick the Clock
	pygame.display.update()
	clock.tick(60)

#Close the Program once we leave the loop
pygame.quit()
quit()
