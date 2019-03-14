from visulization import *
from RRT import *
from Obstacle import *
from FMT import *
from state import state


if __name__ == "__main__":
    obs = []
    obs = [
        obstacle([(10, 10), (10, 20), (40, 20), (40, 10)]),
        obstacle([(10, 25), (10, 35), (40, 35), (40, 25)]),
        obstacle([(10, 40), (10, 50), (40, 50), (40, 40)]),
        obstacle([(10, 55), (10, 65), (40, 65), (40, 55)]),
        obstacle([(10, 70), (10, 80), (40, 80), (40, 70)]),

        obstacle([(60, 10), (60, 20), (90, 20), (90, 10)]),
        obstacle([(60, 25), (60, 35), (90, 35), (90, 25)]),
        obstacle([(60, 40), (60, 50), (90, 50), (90, 40)]),
        obstacle([(60, 55), (60, 65), (90, 65), (90, 55)]),
        obstacle([(60, 70), (60, 80), (90, 80), (90, 70)]),

        obstacle([(100, 10), (100, 40), (110, 40), (110, 10)]),
        obstacle([(120, 10), (120, 40), (130, 40), (130, 10)]),
        obstacle([(140, 10), (140, 40), (150, 40), (150, 10)]),

    ]

    size = (150,100)
    root = Node(0,0)
    target = (110,50)
    acc = 5
    state = state(size,5,acc,root,target,obs,name_ = "SUPER SIM")
    
    #vis = visualization(size,root,target_ = target,scale_= 4,accuracy_=acc,obstacles_ = obs)
    state.addPath(FMT(state,1500))
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                newRoot= Node(state.vis.path[0].x, state.vis.path[0].y)
                newTarget = state.getScaledPoint(event.pos)
                state.setNewRoot(newRoot)
                state.setNewTarget(newTarget)
                state.vis.nodes = []
                newPath = FMT(state,1500)
                state.addPath(newPath)
        state.vis.update()