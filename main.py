import pygame
import sys
import math


DISPLAY_DISTANCE = False
###

start_pos = (9,9) # code 68
end_pos = (0,0) # code 69

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# grid[start_pos[1]][start_pos[0]] = 68
# grid[end_pos[1]][end_pos[0]] = 69

ff_grid = []

###

pygame.init()


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GRID_SIZE = 60

WHITE = (255,255,255)
GREY = (200,200,200)
RED = (255,20,20)
ORANGE = (255,200,0)
PINK = (255, 174, 200)
LINE_STROKE_SIZE = 1



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Template")


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    mouse_pos = pygame.mouse.get_pos()
    start_pos = (mouse_pos[0]//GRID_SIZE, mouse_pos[1]//GRID_SIZE)


    screen.fill((0,0,0))
    for i in range(SCREEN_WIDTH//GRID_SIZE):
        pygame.draw.line(screen, WHITE, (GRID_SIZE*(i+1), 0), (GRID_SIZE*(i+1), SCREEN_HEIGHT), LINE_STROKE_SIZE)

        for j in range(SCREEN_HEIGHT//GRID_SIZE):
            pygame.draw.line(screen, WHITE, (0, GRID_SIZE*(j+1)), (SCREEN_WIDTH, GRID_SIZE*(j+1)), LINE_STROKE_SIZE)
            
            
            # draw objects               

            if grid[j][i] == 1:
                pygame.draw.rect(screen, GREY, (i*GRID_SIZE,j*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[j][i] == 68:
                pygame.draw.rect(screen, ORANGE, (i*GRID_SIZE,j*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[j][i] == 69:
                pygame.draw.rect(screen, RED, (i*GRID_SIZE,j*GRID_SIZE, GRID_SIZE, GRID_SIZE))

            elif grid[j][i] == 99:
                # pygame.draw.rect(screen, PINK, (i*GRID_SIZE,j*GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pass
            
            if ff_grid != []:
                node = ff_grid[j][i]
                center=  (i*GRID_SIZE + GRID_SIZE//2,j*GRID_SIZE+ GRID_SIZE//2)
                
                if DISPLAY_DISTANCE:
                    font = pygame.font.Font(None, 15)
                    text = font.render(str(node.dist), True, WHITE)
                    text_rect = text.get_rect()
                    text_rect.center = center
                    screen.blit(text, text_rect)

                pygame.draw.line(screen, PINK, center, (center[0] + node.vector[0]*20, center[1] + node.vector[1]*20), 2)

    # FLOW FIELD

    class Node:
        def __init__(self, pos, dist):
            self.pos = pos
            self.dist = dist
            self.vector = (0,0)

    ff_grid = []

    for i in range(len(grid)):
        ff_grid.append([])
        for j in range(len(grid[i])):
            ff_grid[i].append(Node((j,i), float('inf')))


    ff_grid[start_pos[1]][start_pos[0]].dist = 0


    
    def get_neighbors(cur_node, give_dist=False):
        cp = cur_node.pos
        xs = []
        for i in range(cp[1]-1, cp[1]+2):
            for j in range(cp[0]-1, cp[0]+2):
                if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[i]):
                    if give_dist:
                        d = 1
                        if (i == cp[1]-1 and j == cp[0]-1) or (i == cp[1]+1 and j == cp[0]+1) or (i == cp[1]-1 and j == cp[0]+1) or (i == cp[1]+1 and j == cp[0]-1):
                            d = math.sqrt(2)
                        xs.append({'node': ff_grid[i][j], 'a': d})
                    else:
                        xs.append(ff_grid[i][j])

        return xs


    
    
    
    def helper(visted_nodes, open_list):
        
        while True:
            if len(open_list) < 1:
            #print('DONE')
                return
            cur_node = open_list[0]

            neighbors = get_neighbors(cur_node, give_dist=True)

            # remove cur_opened node and add the neighbors
            open_list = open_list[1:]
            for neighbor in neighbors:
                if grid[neighbor['node'].pos[1]][neighbor['node'].pos[0]] != 1:
                    if not neighbor['node'] in visted_nodes:
                        neighbor['node'].dist = cur_node.dist + neighbor['a']
                        open_list.append(neighbor['node'])
                        visted_nodes.append(neighbor['node'])
                    else: # visited before
                        # dist nonsense ...
                        if neighbor['node'].dist > cur_node.dist + neighbor['a']:
                            neighbor['node'].dist = cur_node.dist + neighbor['a']



    def kernel_vec(node):
        neighbors = get_neighbors(node)

        #nv = [Node((n.pos[0]-node.pos[0], n.pos[1]-node.pos[1]), n.dist) for n in neighbors]
        nv = []
        for n in neighbors:
            nn = Node((n.pos[0]-node.pos[0], n.pos[1]-node.pos[1]), n.dist)
            nv.append(nn)


        # calculate vector
        vector = (0,0)
        small_node = None
        for n in nv:
            if n.dist == 0:
                vector = n.pos
                break
            else:

                if small_node == None or (n.dist < small_node.dist and n.dist != float('inf')):
                    small_node = n
                    vector = n.pos

        node.vector = vector



    def kernel_conv():
        for i in range(len(ff_grid)):
            for j in range(len(ff_grid[i])):
                kernel_vec(ff_grid[i][j])


    visted_nodes = [ff_grid[start_pos[1]][start_pos[0]]]
    open_list = [ff_grid[start_pos[1]][start_pos[0]]]
    helper(visted_nodes, open_list)
    kernel_conv()


    pygame.display.flip()




pygame.quit()
sys.exit()



