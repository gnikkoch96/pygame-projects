import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Pygame Window")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(f"Key Pressed: {event.key}")
            
        if event.type == pygame.QUIT:
            running = False

    # background
    screen.fill(pygame.Color("#3b0929"))

    # adding text
    font = pygame.font.SysFont(None, 48)
    text = font.render("Me Learning...", True, pygame.Color("#ffffff"))
    screen.blit(text, (300, 250))

    # draw a rectangle                                  (x, y, width, height)
    pygame.draw.rect(screen, pygame.Color("#4287f5"), (100, 100, 200, 150))  


    pygame.display.flip()

pygame.quit()