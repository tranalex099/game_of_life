import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DEAD = (170, 170, 170)
COLOR_ALIVE = (255, 255, 255)

CELL_SIZE =10
CELL_WIDTH = 80
CELL_HEIGHT = 60
SCREEN_WIDTH = CELL_SIZE * 80
SCREEN_HEIGHT = CELL_SIZE * 60

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DEAD
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE
        
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1 , size - 1))
    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    cells = np.zeros((CELL_HEIGHT, CELL_WIDTH))
    screen.fill(COLOR_GRID)
    update(screen, cells, CELL_SIZE)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, CELL_SIZE)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
                update(screen, cells, CELL_SIZE)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, CELL_SIZE, with_progress=True)
            pygame.display.update()

if __name__ == '__main__':
    main()