import world
import pygame
import argparse
import sys
import colors
from pygame.locals import *
import time


pygame.display.set_caption('Life')

cell_size = 30


def run(screen: pygame.Surface, grid: world.Grid):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()

                mouse_rect_x = int(mouse_pos[0]/cell_size)
                mouse_rect_y = int(mouse_pos[1]/cell_size)

                print(mouse_rect_x, ", ", mouse_rect_y)
                grid.set_cell_type(
                    (mouse_rect_x, mouse_rect_y), world.cell.CellType.WALL)

            if event.type == pygame.KEYDOWN:

                mouse_pos = pygame.mouse.get_pos()

                mouse_rect_x = int(mouse_pos[0]/cell_size)
                mouse_rect_y = int(mouse_pos[1]/cell_size)

                print(mouse_rect_x, ", ", mouse_rect_y)

                if event.key == pygame.K_s:
                    grid.set_start_cell(
                        (mouse_rect_x, mouse_rect_y))

                if event.key == pygame.K_e:
                    grid.set_end_cell(
                        (mouse_rect_x, mouse_rect_y))

                if event.key == pygame.K_w:
                    grid.set_cell_type((mouse_rect_x, mouse_rect_y), world.cell.CellType.WALL)

        # grid.start_a_star()
        grid.interate_a_star()
        draw(screen, grid)
        # time.sleep(0.05)


def draw_grid_from_array(screen: pygame.Surface, grid: world.Grid):
    font = pygame.font.SysFont('Arial', 12, False, False)
    for y, row in enumerate(grid.get_cells()):
        for x, cell in enumerate(row):
            # color = white if cell == 0 else black
            # color = colors.white if cell.type == world.cell.CellType.ROAD else colors.black
            color = cell.get_cell_color_by_state()
            pygame.draw.rect(screen, color, (x * cell_size,
                             y * cell_size, cell_size - 2, cell_size-2))

            # screen.blit(font.render(
            #     f"{cell.f_score}", True, colors.red, color), (x*cell_size, y*cell_size))
            # pygame.draw.rect(screen, black, (x * cell_size, y *
            #                  cell_size, cell_size, cell_size), 1)  # grid lines
            if cell.equals(grid.start_cell):
                screen.blit(font.render(
                    f"START", True, colors.red, color), (x*cell_size, y*cell_size))

            if cell.equals(grid.end_cell):
                screen.blit(font.render(
                    f"END", True, colors.red, color), (x*cell_size, y*cell_size))


def draw(screen: pygame.Surface, grid: world.Grid):
    screen.fill(colors.black)  # You can use a different background color
    draw_grid_from_array(screen, grid)
    pygame.display.flip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid_width', type=int, default=30)
    parser.add_argument('--grid_height', type=int, default=25)
    args = parser.parse_args()

    pygame.init()

    global grid_width
    grid_width = args.grid_width

    global grid_height
    grid_height = args.grid_height

    screen = pygame.display.set_mode(
        (grid_width * cell_size, grid_height * cell_size))

    grid = world.Grid(grid_width, grid_height)

    grid.set_start_cell((20, 10))
    grid.set_end_cell((15, 20))
    grid.set_cell_type((1, 5), world.cell.CellType.WALL)
    grid.set_cell_type((1, 6), world.cell.CellType.WALL)
    grid.set_cell_type((1, 7), world.cell.CellType.WALL)
    grid.set_cell_type((1, 8), world.cell.CellType.WALL)
    grid.set_cell_type((1, 9), world.cell.CellType.WALL)
    grid.set_cell_type((1, 10), world.cell.CellType.WALL)
    grid.set_cell_type((1, 11), world.cell.CellType.WALL)
    grid.set_cell_type((1, 12), world.cell.CellType.WALL)
    grid.set_cell_type((1, 13), world.cell.CellType.WALL)
    grid.set_cell_type((1, 14), world.cell.CellType.WALL)
    grid.set_cell_type((1, 15), world.cell.CellType.WALL)

    # path = grid.start_a_star()
    print(grid.start_cell, "score: ", grid.start_cell.f_score)
    print(grid.end_cell)
    # grid.print(path)

    run(screen, grid)
