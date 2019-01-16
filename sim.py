from visulization import *
from RRT import *
from Obstacle import *
from FMT import *
from state import state


if __name__ == "__main__":
    obs = []
    obs = [
        obstacle([(20,20),(20,40),(80,40),(80,20)]),
        obstacle([(20,20+30),(20,40+30),(80,40+30),(80,20+30)]),
        obstacle([(90,30),(90,80),(100,80),(100,30)])
    ]

    size = (150,150)
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