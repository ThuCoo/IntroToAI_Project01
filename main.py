from Board import *

pygame.init()

board = Board()
board.stagePrep()

print(board.vehicles)

bgMusic = pygame.mixer.Sound("./Asset/A CYBER'S WORLD.mp3")
bgMusic.set_volume(0.5)

w = 960
h = 960
offset = 120
screen = pygame.display.set_mode((w, h)) # 960x960 screen
stageBg = pygame.image.load("./Asset/stageBG.png")
stageBg = pygame.transform.scale(stageBg, (w, h))

# GUI later
# pygame.display.set_caption("Project 01 : Rush Hour Game")
# font = pygame.font.SysFont(None, 32)

flag = True
while True :
    for event in pygame.event.get() :
        steps = 0

        if event.type == QUIT : flag = False

        # play here

    #print board : changes later
    screen.blit(stageBg, (0,0))
    for v in board.vehicles :
        cur = board.vehicles[v]
        screen.blit(cur.img, (offset + cur.pos[0] * scaleBase, offset + cur.pos[1] * scaleBase))
    pygame.display.update()