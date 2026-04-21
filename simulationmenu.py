import pygame

# custom mouse function :

def run_simulation_menu(screen):
    x, y = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    custom_cursor = pygame.image.load("Assets/cursor.png")
    cursor_normal = pygame.image.load("Assets/cursor.png")
    cursor_click = pygame.image.load("Assets/cursor click.png")
    def cursor(x, y):
        screen.blit(custom_cursor, (x, y))

    # loading the Assets :

    dashboard = pygame.image.load("Assets/Aether menu.png").convert_alpha()
    button_main_menu = pygame.image.load("Assets/main menu button.png")
    button_main_menu_defult = pygame.image.load("Assets/main menu button.png")
    button_main_menu_glow = pygame.image.load("Assets/main menu button glow.png")
    button_start = pygame.image.load("Assets/start button.png")
    button_start_defult = pygame.image.load("Assets/start button.png")
    button_start_glow = pygame.image.load("Assets/start button glow.png")
    space_background = pygame.image.load("Assets/space.png")

    # loading the sound effects :

    click = pygame.mixer.Sound("Music/click.wav")
    click.set_volume(0.1)

    # setting up the display settings :

    pygame.display.set_caption("Aether - simulation")
    clock = pygame.time.Clock()

    while True:

        mouse = pygame.mouse.get_pos()
        mx,my = pygame.mouse.get_pos()
        button_start_hover = 766 <= mouse[0] <= 1190 and 683 <= mouse[1] <= 825
        button_main_menu_hover = 767 <= mouse[0] <= 1191 and 846 <= mouse[1] <= 991

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                click.play()
                # checking if player click on a button using cordinates :
                if button_main_menu_hover:
                    # main menu button clicked
                    return "menu"
                elif button_start_hover:
                    # start button clicked
                    return "engine"

        # checking if mouse hovred on top of a button without clicking for glow effect : 

        if button_start_hover:
            start_btn = button_start_glow
            main_btn = button_main_menu_defult
            custom_cursor = cursor_click
        elif button_main_menu_hover:
            main_btn = button_main_menu_glow
            start_btn = button_start_defult
            custom_cursor = cursor_click
        else:
            main_btn = button_main_menu_defult
            start_btn = button_start_defult
            custom_cursor = cursor_normal
        
        # rendering the Assets :

        screen.blit(space_background, (0, 0))
        screen.blit(dashboard, (0, 0))
        screen.blit(start_btn, (-600, 0))
        screen.blit(main_btn, (-600, 0))

        cursor(mx, my)
        clock.tick(60)
        pygame.display.update()
    