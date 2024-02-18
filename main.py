import pygame
import sys





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

grid[start_pos[1]][start_pos[0]] = 68
grid[end_pos[1]][end_pos[0]] = 69

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
                font = pygame.font.Font(None, 15)
                text = font.render(str(ff_grid[j][i].dist), True, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (i*GRID_SIZE + GRID_SIZE//2,j*GRID_SIZE+ GRID_SIZE//2)
                screen.blit(text, text_rect)


    # FLOW FIELD
    # https://www.youtube.com/watch?v=ZJZu3zLMYAc

    class Node:
        def __init__(self, pos, dist):
            self.pos = pos
            self.dist = dist

    ff_grid = []

    for i in range(len(grid)):
        ff_grid.append([])
        for j in range(len(grid[i])):
            ff_grid[i].append(Node((j,i), float('inf')))


    ff_grid[start_pos[1]][start_pos[0]].dist = 0

    def get_neighbors(cur_node):
        # get neighbors
        c_node = cur_node.pos
        neighbors = []
        if c_node[0]-1 >= 0:
            node = ff_grid[c_node[0]-1][c_node[1]]
            neighbors.append(node)
        if c_node[0]+1 < len(ff_grid[c_node[1]]):
            node = ff_grid[c_node[0]+1][c_node[1]]
            neighbors.append(node)
        if c_node[1]-1 >= 0:
            node = ff_grid[c_node[0]][c_node[1]-1]
            neighbors.append(node)
        if c_node[1]+1 < len(grid):
            node = ff_grid[c_node[0]][c_node[1]+1]
            neighbors.append(node)
        return neighbors
    
    def helper(visted_nodes, open_list):

        # TODO check if end is reached
        if len(open_list) < 1:
            print('DONE')
            return
        cur_node = open_list[0]

        neighbors = get_neighbors(cur_node)

        # remove cur_opened node and add the neighbors
        # TODO check if it is a wall before adding it to open list
        open_list = open_list[1:]
        for neighbor in neighbors:
            if grid[neighbor.pos[1]][neighbor.pos[0]] != 1:
                if not neighbor in visted_nodes:
                    neighbor.dist = cur_node.dist + 1
                    #ff_grid[neighbor.pos[1]][neighbor.pos[0]] = neighbor
                    open_list.append(neighbor)
                    visted_nodes.append(neighbor)
                else: # visited before
                    # dist nonsense ...
                    if neighbor.dist > cur_node.dist + 1:
                        neighbor.dist = cur_node.dist + 1

        
        #print('new open list: ', open_list)


        helper(visted_nodes, open_list)


    visted_nodes = [ff_grid[start_pos[1]][start_pos[0]]]
    open_list = [ff_grid[start_pos[1]][start_pos[0]]]
    helper(visted_nodes, open_list)
    



    pygame.display.flip()




pygame.quit()
sys.exit()



