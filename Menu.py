import pygame
import random

# custom mouse function :

def run_menu(screen):
    x, y = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    custom_cursor = pygame.image.load("Assets/cursor.png")
    cursor_defult = pygame.image.load("Assets/cursor.png")
    cursor_click = pygame.image.load("Assets/cursor click.png")
    def cursor(x, y):
        screen.blit(custom_cursor, (x, y))

    # loading music :

    track_1 = pygame.mixer.Sound("Music/background.flac")
    track_2 = pygame.mixer.Sound("Music/synth.wav")
    track_1.set_volume(0.1)
    track_2.set_volume(0.4)
    pygame.mixer.stop()
    track_1.play(-1)
    track_2.play(-1)
  
    # loading the sound effects :

    click = pygame.mixer.Sound("Music/click.wav")
    click.set_volume(0.1)
    Aetherslow = pygame.mixer.Sound("Music/Aether(male).wav")
    Aetherslow.set_volume(1.0)
    Aethersuperfast = pygame.mixer.Sound("Music/Aethersuperfast(male).wav")
    Aethersuperfast.set_volume(1.0)
    Aethersuperslow = pygame.mixer.Sound("Music/Aethersuperslow(male)h.wav")
    Aethersuperslow.set_volume(1.0)
    Aethernormal = pygame.mixer.Sound("Music/Aethernormal.wav")
    Aethernormal.set_volume(1.0)
    Aethernormal = pygame.mixer.Sound("Music/Aethernormal.wav")
    Aethernormal.set_volume(1.0)
    Aetherslows = pygame.mixer.Sound("Music/Aetherslow(male).wav")
    Aetherslow.set_volume(1.0)
    Aetherfast = pygame.mixer.Sound("Music/Aetherfast.wav")
    Aetherfast.set_volume(1.0)

    sounds = [Aetherslow, Aethersuperfast, Aethersuperslow, Aethernormal, Aetherslows, Aetherfast]

    # loading the Assets : 

    space_background = pygame.image.load("Assets/space background.png")
    main_screen = pygame.image.load("Assets/main menu.png")
    button_simulate_defult = pygame.image.load("Assets/simulate button.png")
    button_simulate_glow = pygame.image.load("Assets/simulate button glow.png")
    button_quit_defult = pygame.image.load("Assets/quit button.png")
    button_quit_glow = pygame.image.load("Assets/quit button glow.png")

    # setting display settings :

    pygame.display.set_caption("Aether - menu")
    clock = pygame.time.Clock()
    # variables

    while True:

        mouse = pygame.mouse.get_pos()
        mx,my = pygame.mouse.get_pos()
        hover_simulate = 613 <= mouse[0] <= 1246 and 505 <= mouse[1] <= 721
        hover_quit = 613 <= mouse[0] <= 1246 and 805 <= mouse[1] <= 1021

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                click.play()
                # checking if player click on a button using cordinates :

                # clicked on the game name
                if 559 <= mouse[0] <= 1484 and 200 <= mouse[1] <= 377:
                    random.choice(sounds).play()
                # simulate button clicked
                if 613 <= mouse[0] <= 1246 and 505 <= mouse[1] <= 721:
                    return "simulation"
                # quit button clicked
                if 613 <= mouse[0] <= 1246 and 805 <= mouse[1] <= 1021:
                    return "quit"
        
        # checking if mouse hovred on top of a button without clicking for glow effect : 

        if hover_simulate:
            btn_simulate = button_simulate_glow
            btn_quit = button_quit_defult
            custom_cursor = cursor_click
        elif hover_quit:
            btn_quit = button_quit_glow
            btn_simulate = button_simulate_defult
            custom_cursor = cursor_click
        else:
            btn_simulate = button_simulate_defult
            btn_quit = button_quit_defult
            custom_cursor = cursor_defult
            

        # rendering the Assets :

        screen.blit(space_background, (0, 0))
        screen.blit(main_screen, (0, 0))
        screen.blit(btn_simulate, (500, 200))
        screen.blit(btn_quit, (500, 500))

        cursor(mx,my)
        clock.tick(60)
        pygame.display.update()