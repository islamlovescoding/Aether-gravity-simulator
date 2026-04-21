import pygame
from Menu import run_menu
from simulationmenu import run_simulation_menu
from simulation import run_simulation
from reaorbit import real_orbit

pygame.init()
pygame.mixer.init()
icon = pygame.image.load("Assets/Aether icon.png")
pygame.display.set_icon(icon)
pygame.key.start_text_input()
pygame.mixer.set_num_channels(60)
screen = pygame.display.set_mode((1920, 1080))


state = "menu"
while True:
    if state == "menu":
        state = run_menu(screen)
    elif state == "simulation":
        state = run_simulation_menu(screen)
    elif state == "engine":
        state = run_simulation(screen)
    elif state == "run_real_orbit":
        state = real_orbit(screen)
    elif state == "quit":
        break

pygame.quit()