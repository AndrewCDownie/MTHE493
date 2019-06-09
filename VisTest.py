import pygame


screen = pygame.display.set_mode((200,200))
i = 1
def update(i):
    print("Updating")
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(2,100,100),pygame.rect.Rect(0,0,i+10,i+10),1)
    pygame.display.update()


running = True
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((200,200))
i =0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    i +=1
    clock.tick(30)
    update(i)