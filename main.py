import pygame
from Board import Board
from Button import Button
from Search import SearchAlgorithms
from State import State
import time

pygame.init()
pygame.display.init()
pygame.font.init()

w = 960
h = 960
screen = pygame.display.set_mode((w, h))
stageBg =  pygame.transform.scale(pygame.image.load("./Asset/Background/stageBG.png"), (w, h))
bg =  pygame.transform.scale(pygame.image.load("./Asset/Background/BG.png"), (w, h))

offset = 120
scaleBase = 120
font = pygame.font.Font("./Asset/PRESSSTART2P.TTF", 28)

# Game buttons
bPlay = pygame.transform.scale(pygame.image.load("./Asset/Button/Play.png"), (120, 120))
bDown = pygame.transform.scale(pygame.image.load("./Asset/Button/Down.png"), (84, 84))
bUp = pygame.transform.scale(pygame.image.load("./Asset/Button/Up.png"), (84, 84))
bReturn = pygame.transform.scale(pygame.image.load("./Asset/Button/Return.png"), (120, 120))
bChange = pygame.transform.scale(pygame.image.load("./Asset/Button/Change.png"), (120, 120))
bPause = pygame.transform.scale(pygame.image.load("./Asset/Button/Pause.png"), (120, 120))
bReset = pygame.transform.scale(pygame.image.load("./Asset/Button/Reset.png"), (120, 120))
bExit = pygame.transform.scale(pygame.image.load("./Asset/Button/Exit.png"), (120, 120))

def mainMenu():
    pygame.display.set_caption("Main Menu")
    screen.fill("black")
    clock = pygame.time.Clock()
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))

        mainText = font.render("Project 1. Search", True, "black")
        screen.blit(mainText, mainText.get_rect(center=(w / 2, 360 - 20)))
        subText = font.render("Rush Hour: Solve the Traffic Jam!", True, "black")
        screen.blit(subText, subText.get_rect(center=(w / 2, 360 + 20)))

        Play = Button(image=bPlay, pos=(w / 3, h / 2))
        Play.update(screen)
        Exit = Button(image=bExit, pos=(w * 2 / 3, h / 2))
        Exit.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Exit.checkForInput(mouse):
                    return False
                elif Play.checkForInput(mouse):
                    if not stageOptions(1, algo="BFS"):
                        return False
        pygame.display.update()
        clock.tick(60)

def stageOptions(level, algo):
    pygame.display.set_caption("Stage Options")
    screen.fill("black")
    algoList = ["BFS", "DFS", "UCS", "A*"]
    a = algoList.index(algo) if algo in algoList else 0
    clock = pygame.time.Clock()
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))

        lvl = font.render('LEVEL: ' + str(level), True, "black")
        lvlRect = lvl.get_rect(center=(w / 3 - 50, h / 2))
        screen.blit(lvl, lvlRect)
        UpLvl = Button(image=bUp, pos=(w / 3 - 50 + 52, h / 2 - 100))
        UpLvl.update(screen)
        DownLvl = Button(image=bDown, pos=(w / 3 - 50 - 52, h / 2 - 100))
        DownLvl.update(screen)

        algoText = font.render('Algorithm: ' + algoList[a % 4], True, "black")
        algoRect = algoText.get_rect(center=(w * 2 / 3 + 50, h / 2))
        screen.blit(algoText, algoRect)
        UpAlgo = Button(image=bUp, pos=(w * 2 / 3 + 50 + 52, h / 2 - 100))
        UpAlgo.update(screen)
        DownAlgo = Button(image=bDown, pos=(w * 2 / 3 + 50 - 52, h / 2 - 100))
        DownAlgo.update(screen)

        Play = Button(image=bPlay, pos=(w / 3, h * 2 / 3))
        Play.update(screen)
        Back = Button(image=bReturn, pos=(w * 2 / 3, h * 2 / 3))
        Back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back.checkForInput(mouse):
                    return True
                if Play.checkForInput(mouse):
                    if not play(level, algoList[a % 4]):
                        return False
                if UpLvl.checkForInput(mouse):
                    level = 1 if level == 10 else level + 1
                elif DownLvl.checkForInput(mouse):
                    level = 10 if level == 1 else level - 1
                elif UpAlgo.checkForInput(mouse):
                    a += 1
                elif DownAlgo.checkForInput(mouse):
                    a -= 1
        pygame.display.update()
        clock.tick(60)

def play(level, algo):
    pygame.display.set_caption("Play")
    screen.blit(stageBg, (0, 0))
    pygame.display.flip()

    board = Board()
    board.level = level - 1
    board.stagePrep()
    
    search = SearchAlgorithms(board)
    
    algo_map = {"BFS": search.bfs,
                "DFS": lambda: search.dfs(max_depth=50),
                "UCS": search.ucs,
                "A*": search.a_star}
    
    paused = False
    steps = 0
    path = None
    move_index = 0
    solution_found = False
    no_solution = False
    last_move_time = time.time()
    move_delay = 0.3

    Change = Button(bChange, (540, 60))
    Pause = Button(bPause, (660, 60))
    Reset = Button(bReset, (780, 60))
    Exit = Button(bExit, (900, 60))

    clock = pygame.time.Clock()
    running = True
    
    try:
        search_result = algo_map[algo]()
        if search_result and search_result[0]:
            path = search_result[0].moves
            solution_found = True
            print(f"Solution found in {len(path)} moves")
        else:
            no_solution = True
            print("No solution found")
    except Exception as e:
        print(f"Search error: {e}")
        no_solution = True

    while running:
        current_time = time.time()
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Change.checkForInput(mouse):
                    return stageOptions(level, algo)
                elif Pause.checkForInput(mouse):
                    paused = not paused
                elif Reset.checkForInput(mouse):
                    board.stagePrep()
                    steps = 0
                    move_index = 0
                    last_move_time = current_time
                elif Exit.checkForInput(mouse):
                    return True

        screen.blit(stageBg, (0, 0))

        for vid, vehicle in board.vehicles.items():
            pos = (offset + vehicle.pos[0] * scaleBase, 
                   offset + vehicle.pos[1] * scaleBase)
            screen.blit(vehicle.img, pos)

        Change.update(screen)
        Pause.update(screen)
        Reset.update(screen)
        Exit.update(screen)

        bLvl = font.render(f'LEVEL: {level}', True, "black")
        bSteps = font.render(f'STEPS: {steps}', True, "black")
        bAlgo = font.render(f'ALGO: {algo}', True, "black")
        screen.blit(bLvl, (w / 6 - bLvl.get_width()/2, 900))
        screen.blit(bSteps, (w / 2 - bSteps.get_width()/2, 900))
        screen.blit(bAlgo, (w * 5/6 - bAlgo.get_width()/2, 900))

        # Show searching messages
        if not solution_found and not no_solution:
            loading_text = font.render("Searching...", True, "black")
            screen.blit(loading_text, (w/2 - loading_text.get_width()/2, h/2))
        elif no_solution:
            error_text = font.render("No solution found!", True, "red")
            screen.blit(error_text, (w/2 - error_text.get_width()/2, h/2))
            paused = True

        # Execute solution moves
        if solution_found and path and not paused and move_index < len(path):
            if current_time - last_move_time >= move_delay:
                vehicle_id, direction = path[move_index]
                if vehicle_id in board.vehicles:
                    if board.move(vehicle_id, direction):
                        steps += 1
                        move_index += 1
                        last_move_time = current_time
                    else:
                        print(f"Invalid move: {vehicle_id}, {direction}")
                        no_solution = True
                else:
                    print(f"Vehicle {vehicle_id} not found")
                    no_solution = True

        # Check win condition
        if solution_found and path and move_index >= len(path):
            current_state = State(board.vehicles.copy())
            if board.is_goal(current_state):
                win_text = font.render("You Win!", True, "green")
                screen.blit(win_text, (w/2 - win_text.get_width()/2, h/2))
                pygame.display.flip()
                pygame.time.wait(3000)
                return True

        pygame.display.flip()
        clock.tick(60)
        
    return False

def main():
    if not mainMenu():
        pygame.quit()

if __name__ == "__main__":
    main()