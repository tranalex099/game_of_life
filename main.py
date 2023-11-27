#SET IMPORTS HERE
import pygame
import numpy as np

#SET VARIABLES HERE
COLOR_BG = (10, 10, 10)
COLOR_GRID = (60, 60, 60)
COLOR_DIE = (150, 150, 150)
COLOR_LIVE = (255, 255, 255)

CELL_SIZE = 10
CELLS_WIDE = 80
CELLS_TALL = 60
SCREEN_WIDTH = CELL_SIZE * CELLS_WIDE
SCREEN_HEIGHT = CELL_SIZE * CELLS_TALL

FPS = 24

def update(screen, cells, size, evolve=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        neighbors = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_LIVE

        if cells[row, col] == 1:
            if 2 <= neighbors <= 3:
                updated_cells[row, col] = 1
                if evolve:
                    color = COLOR_LIVE
            else:
                if evolve:
                    color = COLOR_DIE
        else:
            if neighbors == 3:
                updated_cells[row, col] = 1
                if evolve:
                    color = COLOR_LIVE
        
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1 , size - 1))
    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    cells = np.zeros((CELLS_TALL, CELLS_WIDE))
    screen.fill(COLOR_GRID)
    update(screen, cells, CELL_SIZE)

    pygame.display.flip()
    pygame.display.update()

    running = False

    clock = pygame.time.Clock()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, CELL_SIZE)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
                update(screen, cells, CELL_SIZE)
                pygame.display.update()

        if running:
            cells = update(screen, cells, CELL_SIZE, evolve=True)
            pygame.display.update()

        dt = clock.tick(FPS)

if __name__ == '__main__':
    main()