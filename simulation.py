import pygame
import math
import random
from datetime import datetime, timedelta

# custom mouse function :

def run_simulation(screen):

    x, y = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    custom_cursor = pygame.image.load("Assets/cursor.png")
    cursor_normal = pygame.image.load("Assets/cursor.png")
    cursor_click = pygame.image.load("Assets/cursor click.png")
    def cursor(x, y):
        screen.blit(custom_cursor, (x, y))

    # loading the Assets :

    simulation_dashboard = pygame.image.load("Assets/simulation dashboard.png").convert_alpha()
    space_background = pygame.image.load("Assets/space.png")
    main_menu = pygame.image.load("Assets/main menu button.png")
    main_menu_normal = pygame.image.load("Assets/main menu button2.png")
    main_menu_glow = pygame.image.load("Assets/main menu button2 glow.png")
    real_orbit = pygame.image.load("Assets/real orbit button.png")
    real_orbit_normal = pygame.image.load("Assets/real orbit button.png")
    real_orbit_glow = pygame.image.load("Assets/real orbit button glow.png")
    dashboard_planets = pygame.image.load("Assets/planet dashboard.png")
    spawning_dashboard = pygame.image.load("Assets/spawning dashboard.png")
    button_spawn = pygame.image.load("Assets/spawn button.png")
    button_spawn_normal = pygame.image.load("Assets/spawn button.png")
    button_spawn_glow = pygame.image.load("Assets/spawn button glow.png")
    newton_1 = pygame.image.load("Assets/newton1.png")
    newton_2 = pygame.image.load("Assets/newton2.png")
    newton_3 = pygame.image.load("Assets/newton3.png")
    newton_4 = pygame.image.load("Assets/newton4.png")
    newton_5 = pygame.image.load("Assets/newton5.png")
    feynman_1 = pygame.image.load("Assets/feynman1.png")
    feynman_2 = pygame.image.load("Assets/feynman2.png")
    feynman_3 = pygame.image.load("Assets/feynman3.png")
    feynman_4 = pygame.image.load("Assets/feynman4.png")
    feynman_5 = pygame.image.load("Assets/feynman5.png")
    einstein_1 = pygame.image.load("Assets/einstein1.png")
    einstein_2 = pygame.image.load("Assets/einstein2.png")
    einstein_3 = pygame.image.load("Assets/einstein3.png")
    einstein_4 = pygame.image.load("Assets/einstein4.png")
    einstein_5 = pygame.image.load("Assets/einstein5.png")

    # loading the sound effects :

    click = pygame.mixer.Sound("Music/click.wav")
    impact = pygame.mixer.Sound("Music/impact.wav")
    impact.set_volume(10)
    click.set_volume(0.3)

    # setting up the display settings :

    pygame.display.set_caption("Aether - simulation")
    clock = pygame.time.Clock()

    # variables:

    # quotes :

    quotes_list = [newton_1, newton_2, newton_3, newton_4, newton_5, feynman_1, feynman_2, feynman_3, feynman_4, feynman_5, einstein_1, einstein_2, einstein_3, einstein_4, einstein_5]
    quotes = random.choice(quotes_list)

    # effects :

    shock = []
    randomized = ""
    fade_timer = 0
    fade_duration = 40
    selected_planet = None
    clicked_planet = None
    placing_planet = False
    placement_pos = None
    placement_anim = 0
    placement_locked = False
    placement_blocked_timer = 0
    blocked = False
    # camera :

    camera_x = 0
    camera_y = 0
    center_x = 1205 / 2
    center_y = 1080 / 2
    zoom = 2.14e-9
    zoom_speed = 1.5
    target = zoom
    zoom_interp = 0.1
    max_dragging = 5e12
    dragging = False

    # physics :

    scale = 2.14e-9
    dt = 3600
    G = 6.674e-11
    steps = 10

    # input / ui and other :

    name_input = ""
    mass_input = ""
    type_input = ""
    type_index = 0
    typing_name = False
    typing_mass = False
    paused = False
    run = True
    the_time = 0
    start_date = datetime.today()
    
    # text :

    text_font = pygame.font.SysFont("Times New Roman", 35)
    text_font2 = pygame.font.SysFont("Times New Roman", 50)
    surface = pygame.Surface((1205, 1080), pygame.SRCALPHA)
    surface_text = pygame.Surface((1920, 1080), pygame.SRCALPHA)

    # planet types :

    planet_types = ["rocky", "gas giant", "ice giant", "black hole", "white hole", "star"]

    # random color for added palnets function :

    def random_color(r_range, g_range, b_range):
        return [random.randint(*r_range), random.randint(*g_range), random.randint(*b_range)]

    type_colors = {
        "rocky":      lambda: random_color((140, 200), (100, 160), (60, 120)),
        "gas giant":  lambda: random_color((180, 230), (130, 180), (60, 120)),
        "ice giant":  lambda: random_color((60, 120),  (180, 230), (200, 255)),
        "black hole": lambda: random_color((10, 30),   (10, 30),   (10, 30)),
        "white hole": lambda: random_color((220, 255), (220, 255), (230, 255)),
        "star":       lambda: random_color((220, 255), (180, 230), (30, 100)),
    }

    # setting the error animation timer to 0 :

    name_error_timer = 0
    mass_error_timer = 0
    type_error_timer = 0

    # planets :

    # basic planet information dictionarie :

    planets_basic = {
        "Sun": {
            "mass": 1.989e30,
            "radius": 35,
            "color": [255, 220, 50],
            "facts": [
                "Contains 99.86% of the solar system's mass.",
                "Energy comes from hydrogen fusion into helium.",
                "Core temperature reaches ~15 million degrees C.",
                "Light takes ~8 minutes to reach Earth.",
                "Gravity holds all planets in orbit.",
            ]
        },
        "Mercury": {
            "mass": 3.3e23,
            "radius": 4,
            "color": [180, 180, 180],
            "facts": [
                "A day on Mercury lasts 176 Earth days, longer than its year (88 days).",
                "It has almost no atmosphere, so temperatures swing from ~430 to -180 degrees C.",
                "Its surface is heavily cratered, similar to the Moon.",
                "Despite being closest to the Sun, it is not the hottest planet.",
                "Mercury is tidally influenced by the Sun in a 3:2 spin orbit resonance.",
            ]
        },
        "Venus": {
            "mass": 4.87e24,
            "radius": 7,
            "color": [225, 100, 40],
            "facts": [
                "Venus is the hottest planet (~465 degrees C) due to a runaway greenhouse effect.",
                "It rotates backwards (retrograde rotation).",
                "A day on Venus (243 Earth days) is longer than its year (225 days).",
                "Its atmosphere is ~96% CO2 with clouds of sulfuric acid.",
                "Surface pressure is about 92x Earth like being deep underwater.",
            ]
        },
        "Earth": {
            "mass": 5.97e24,
            "radius": 7,
            "color": [50, 100, 255],
            "facts": [
                "The only known planet with life.",
                "71% of its surface is covered by liquid water.",
                "It has a strong magnetic field that protects from solar radiation.",
                "Earth atmosphere is 78% nitrogen, 21% oxygen.",
                "It has one large Moon that stabilizes its axial tilt.",
            ]
        },
        "Mars": {
            "mass": 6.39e23,
            "radius": 5,
            "color": [200, 80, 40],
            "facts": [
                "Home to Olympus Mons, the largest volcano in the solar system.",
                "Has the largest canyon, Valles Marineris.",
                "Evidence suggests ancient liquid water once flowed on Mars.",
                "Its atmosphere is thin (~95% CO2), causing weak greenhouse warming.",
                "Mars has two small moons: Phobos and Deimos.",
            ]
        },
        "Jupiter": {
            "mass": 1.898e27,
            "radius": 14,
            "color": [200, 160, 100],
            "facts": [
                "The largest planet, more massive than all others combined.",
                "The Great Red Spot is a storm lasting over 300 years.",
                "It has strong gravity, influencing asteroid belts and orbits.",
                "Jupiter has 90+ moons, including Ganymede (largest moon).",
                "It emits more heat than it receives from the Sun.",
            ]
        },
        "Saturn": {
            "mass": 5.68e26,
            "radius": 12,
            "color": [210, 180, 100],
            "facts": [
                "Known for its spectacular ring system made of ice and rock.",
                "It is so low-density it could float in water (theoretically).",
                "Saturn has 140+ moons, including Titan.",
                "Titan has lakes of liquid methane.",
                "Strong winds can reach ~1800 km/h.",
            ]
        },
        "Uranus": {
            "mass": 8.68e25,
            "radius": 9,
            "color": [100, 210, 210],
            "facts": [
                "Rotates on its side (98 degree tilt), it basically rolls around the Sun.",
                "Has a faint ring system.",
                "Its blue color comes from methane absorbing red light.",
                "It is the coldest planet (~-224 degrees C).",
                "Seasons last about 21 Earth years each.",
            ]
        },
        "Neptune": {
            "mass": 1.024e26,
            "radius": 9,
            "color": [50, 50, 255],
            "facts": [
                "The farthest planet from the Sun.",
                "Has the strongest winds in the solar system (~2100 km/h).",
                "Discovered using mathematical prediction, not direct observation.",
                "Its moon Triton orbits backwards (captured object).",
                "Neptune radiates internal heat, similar to Jupiter.",
            ]
        },
    }

    # mass unit dectionarie :

    mass_units = {
        "ks": planets_basic["Sun"]["mass"],
        "km": planets_basic["Mercury"]["mass"],
        "kv": planets_basic["Venus"]["mass"],
        "ke": planets_basic["Earth"]["mass"],
        "ka": planets_basic["Mars"]["mass"],
        "kj": planets_basic["Jupiter"]["mass"],
        "kt": planets_basic["Saturn"]["mass"],
        "ku": planets_basic["Uranus"]["mass"],
        "kn": planets_basic["Neptune"]["mass"],
    }

    # position dictionarie :

    position = {
        "Mercury": {"a": 5.79e10,  "e": 0.2056},
        "Venus":   {"a": 1.082e11, "e": 0.0068},
        "Earth":   {"a": 1.496e11, "e": 0.0167},
        "Mars":    {"a": 2.279e11, "e": 0.0934},
        "Jupiter": {"a": 7.786e11, "e": 0.0489},
        "Saturn":  {"a": 1.432e12, "e": 0.0565},
        "Uranus":  {"a": 2.867e12, "e": 0.0457},
        "Neptune": {"a": 4.495e12, "e": 0.0113},
    }

    # calculating each planet initial velocity with vis visa equation :

    data = []
    total_momentum_y = 0
    mass_sun = planets_basic["Sun"]["mass"]
    for name, params in position.items():
        a = params["a"]
        e = params["e"]
        r_p = a * (1 - e)
        v_p = math.sqrt(G * mass_sun * (2 / r_p - 1 / a))
        data.append((name, [r_p, 0], [0, v_p]))
        total_momentum_y += planets_basic[name]["mass"] * v_p

    vy_sun = -total_momentum_y / mass_sun

    # planets dictionarie :

    planets = [
        {
            "name": "Sun",
            "mass": planets_basic["Sun"]["mass"],
            "position": [0, 0],
            "velocity": [0, vy_sun],
            "radius": 35,
            "color": [255, 232, 124],
            "ax": 0,
            "ay": 0,
        },
    ]

    # for each planet in the gathred data, add it to the dictionarie :

    for name, pos, vel in data:
        Planet = planets_basic[name]
        planets.append({
            "name": name,
            "mass": Planet["mass"],
            "position": pos,
            "velocity": vel,
            "radius": Planet["radius"],
            "color": Planet["color"],
            "ax": 0,
            "ay": 0,
        })

    # functions :

    # calculate the energu produced by the solar system :

    def energy(planets):
        K = 0
        U = 0
        for planet in planets:
            K += 0.5 * planet["mass"] * (planet["velocity"][0] ** 2 + planet["velocity"][1] ** 2)
        for pl, planet in enumerate(planets):
            for ot, other in enumerate(planets):
                if ot <= pl:
                    continue
                dx_r = other["position"][0] - planet["position"][0]
                dy_r = other["position"][1] - planet["position"][1]
                r_r = math.sqrt(dx_r ** 2 + dy_r ** 2)
                U += -G * planet["mass"] * other["mass"] / r_r
        return K + U

    initial_energy = energy(planets)

    # calculate the force from each planet :

    def calculate_forces(planet, planets):
        fx = 0
        fy = 0
        for other in planets:
            if other is planet:
                continue
            dx = other["position"][0] - planet["position"][0]
            dy = other["position"][1] - planet["position"][1]
            r = math.sqrt(dx ** 2 + dy ** 2)
            if r == 0:
                continue
            F = G * planet["mass"] * other["mass"] / r ** 2

            if planet.get("type") == "white hole" or other.get("type") == "white hole":
                repel_dist = 2e10 
                if r < repel_dist:
                    fx -= F * dx / r
                    fy -= F * dy / r
                else:
                    fx += F * dx / r
                    fy += F * dy / r
            else:
                fx += F * dx / r
                fy += F * dy / r
        return fx, fy

    # add a shadow relative to the sun for 3d looking planets :

    def draw_planet_3d(surface, color, cx, cy, radius, sun_screen_x, sun_screen_y, is_sun=False, has_star=True):
        radius = min(radius, 80)
        pygame.draw.circle(surface, color, (cx, cy), radius)
        if is_sun or radius < 2:
            return
        if has_star:
            dark_alpha = 160
            dx = sun_screen_x - cx
            dy = sun_screen_y - cy
            dist = math.sqrt(dx * dx + dy * dy) or 1
            offset = int(radius * 0.35)
            ox = int(-dx / dist * offset)
            oy = int(-dy / dist * offset)
        else:
            dark_alpha = 60
            ox, oy = 0, int(radius * 0.2)
        shadow_r = int(radius * 0.92)
        pad = abs(ox) + abs(oy) + 4
        size = (radius + pad) * 2
        shadow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center_in_surf = (size // 2 + ox, size // 2 + oy)
        pygame.draw.circle(shadow_surf, (0, 0, 0, dark_alpha), center_in_surf, shadow_r)
        surface.blit(shadow_surf, (cx - size // 2, cy - size // 2))

    # reset the whole simulation :    

    def reset():
        nonlocal camera_x, camera_y, zoom, target, dt, steps, the_time
        nonlocal start_date, selected_planet, randomized, paused
        nonlocal planets, initial_energy

        camera_x = 0
        camera_y = 0
        zoom = 2.14e-9
        target = zoom
        dt = 3600
        steps = 10
        the_time = 0
        start_date = datetime.today()
        selected_planet = None
        randomized = ""
        paused = False

        planets.clear()
        total_momentum_y = 0

        planets.append({
            "name": "Sun",
            "mass": planets_basic["Sun"]["mass"],
            "position": [0, 0],
            "velocity": [0, 0],
            "radius": 35,
            "color": [255, 232, 124],
            "ax": 0,
            "ay": 0,
        })

        for name, params in position.items():
            a = params["a"]
            e = params["e"]
            r_p = a * (1 - e)
            v_p = math.sqrt(G * mass_sun * (2 / r_p - 1 / a))
            total_momentum_y += planets_basic[name]["mass"] * v_p
            Planet = planets_basic[name]
            planets.append({
                "name": name,
                "mass": Planet["mass"],
                "position": [r_p, 0],
                "velocity": [0, v_p],
                "radius": Planet["radius"],
                "color": Planet["color"],
                "ax": 0,
                "ay": 0,
            })

        vy_sun = -total_momentum_y / mass_sun
        planets[0]["velocity"][1] = vy_sun

        for planet in planets:
            fx, fy = 0, 0
            for other in planets:
                if other is planet:
                    continue
                dx = other["position"][0] - planet["position"][0]
                dy = other["position"][1] - planet["position"][1]
                r = math.sqrt(dx ** 2 + dy ** 2)
                F = G * planet["mass"] * other["mass"] / r ** 2
                fx += F * dx / r
                fy += F * dy / r
            planet["ax"] = fx / planet["mass"]
            planet["ay"] = fy / planet["mass"]

        initial_energy = energy(planets)

    # check if the user input is valid or not :

    def parse_mass(text):
        text = text.strip().lower()
        for unit, multiplier in mass_units.items():
            if text.endswith(unit):
                number = text[:-len(unit)].strip()
                try:
                    val = float(number)
                    if val <= 0:
                        return None
                    return val * multiplier
                except ValueError:
                    return None
        try:
            val = float(text)
            if val <= 0:
                return None
            return val
        except ValueError:
            return None
        
    # set a realistic radius for added planets :

    def get_radius(mass, type_input):
        earth_mass = 5.97e24
        sun_mass   = 1.989e30

        if type_input == "black hole":
            r = int(8 + math.log10(max(1, mass / sun_mass)) * 3)
            return max(8, min(r, 25))
        if type_input == "white hole":
            r = int(8 + math.log10(max(1, mass / sun_mass)) * 3)
            return max(8, min(r, 22))
        if type_input == "gas giant":
            r = int(10 * (mass / (1.898e27)) ** (1/3))
            return max(10, min(r, 28))
        if type_input == "ice giant":
            r = int(9 * (mass / (8.68e25)) ** (1/3))
            return max(7, min(r, 20))
        if type_input == "rocky":
            r = int(7 * (mass / earth_mass) ** (1/3))
            return max(3, min(r, 14))
        if type_input == "star":
            r = int(35 * (mass / sun_mass) ** (1/3))
            return max(15, min(r, 60))

        return max(4, min(int((mass / earth_mass) ** (1/3) * 7), 20))

    # text rendering function :

    def text_render(text, font, color, x, y):
        image = font.render(text, True, color)
        surface_text.blit(image, (x, y))

    # set a spawning velocity for added planets :

    def get_spawn_velocity(placement_pos, type_input):
        if type_input == "black hole":
            return [0, 0]

        total_mass = sum(p["mass"] for p in planets)
        com_x = sum(p["mass"] * p["position"][0] for p in planets) / total_mass
        com_y = sum(p["mass"] * p["position"][1] for p in planets) / total_mass
        com_vx = sum(p["mass"] * p["velocity"][0] for p in planets) / total_mass
        com_vy = sum(p["mass"] * p["velocity"][1] for p in planets) / total_mass

        if type_input == "star":
            return [com_vx, com_vy]

        dx = placement_pos[0] - com_x
        dy = placement_pos[1] - com_y
        r = math.sqrt(dx * dx + dy * dy)
        if r == 0:
            return [com_vx, com_vy]

        v = math.sqrt(G * total_mass / r)
        vx = -dy / r * v + com_vx
        vy =  dx / r * v + com_vy
        return [vx, vy]

    # pre acceleration calculation :

    for planet in planets:
        fx, fy, ax, ay = 0, 0, 0, 0
        for other in planets:
            if other is planet:
                continue
            dx = other["position"][0] - planet["position"][0]
            dy = other["position"][1] - planet["position"][1]
            r = math.sqrt(dx ** 2 + dy ** 2)
            F = G * planet["mass"] * other["mass"] / r ** 2
            fx += F * dx / r
            fy += F * dy / r
        ax += fx / planet["mass"]
        ay += fy / planet["mass"]
        planet["ax"] += ax
        planet["ay"] += ay

    while run:

        sim_per_real_second = dt * steps * 60
        sim_years_per_real_second = sim_per_real_second / 31_536_000
        mouse = pygame.mouse.get_pos()
        mx, my = pygame.mouse.get_pos()
        hover_main_menu = 0 <= mouse[0] <= 277 and 0 <= mouse[1] <= 104
        hover_real_orbit = 294 <= mouse[0] <= 571 and 0 <= mouse[1] <= 121
        name_button = 1484 <= mouse[0] <= 1808 and 133 <= mouse[1] <= 186
        mass_button = 1462 <= mouse[0] <= 1812 and 204 <= mouse[1] <= 259
        type_button = 1472 <= mouse[0] <= 1818 and 525 <= mouse[1] <= 578
        hover_spawn_button = 1405 <= mouse[0] <= 1750 and 736 <= mouse[1] <= 850

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            # hover / click detection :

            if event.type == pygame.MOUSEBUTTONDOWN:
                if name_button:
                    if placing_planet and placement_locked:
                        typing_name = True
                        typing_mass = False
                if mass_button:
                    if placing_planet and placement_locked:
                        typing_mass = True
                        typing_name = False
                if type_button:
                    if placing_planet and placement_locked:
                        type_index = (type_index + 1) % len(planet_types)
                        type_input = planet_types[type_index]

                if hover_spawn_button:
                    if placing_planet and placement_locked:
                        valid = True

                        if not name_input.strip():
                            name_error_timer = 30
                            valid = False

                        mass_value = parse_mass(mass_input)
                        if mass_value is None:
                            mass_error_timer = 30
                            valid = False

                        if type_input not in planet_types:
                            type_error_timer = 30
                            valid = False

                        if valid:
                            radius = get_radius(mass_value, type_input)
                            vel = get_spawn_velocity(placement_pos, type_input)
                            planets.append({
                                "name": name_input.strip(),
                                "mass": mass_value,
                                "position": [placement_pos[0], placement_pos[1]],
                                "velocity": vel,
                                "radius": radius,
                                "color": type_colors[type_input](),
                                "type": type_input,
                                "ax": 0,
                                "ay": 0,
                            })
                            initial_energy = energy(planets)
                            name_input = ""
                            mass_input = ""
                            type_input = ""
                            type_index = 0
                            typing_name = False
                            typing_mass = False
                            placing_planet = False
                            placement_locked = False
                            placement_pos = None
                            selected_planet = None

                if hover_main_menu:
                    return "menu"
                if hover_real_orbit:
                    return "run_real_orbit"

                selected_planet = None
                randomized = ""
                for planet in planets:
                    screen_x = center_x + (planet["position"][0] + camera_x) * zoom
                    screen_y = center_y + (planet["position"][1] + camera_y) * zoom
                    radius = max(1, int(planet["radius"] * zoom / scale))
                    dist = math.sqrt((mx - screen_x) ** 2 + (my - screen_y) ** 2)
                    if dist < radius + 20:
                        clicked_planet = planet
                        if selected_planet == planet:
                            selected_planet = None
                            randomized = ""
                        else:
                            selected_planet = planet
                            if selected_planet["name"] in planets_basic:
                                facts = planets_basic[selected_planet["name"]]["facts"]
                                randomized = random.choice(facts)
                            else:
                                randomized = "a mysterious unknown body."

                dragging = True
                prevx = mx
                prevy = my
                click.play()

            if event.type == pygame.TEXTINPUT:
                if typing_name and placing_planet and placement_locked:
                    if len(name_input) < 14:
                        name_input += event.text
                if typing_mass and placing_planet and placement_locked:
                    allowed = set("0123456789.eE+-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
                    if event.text in allowed and len(mass_input) < 12:
                        mass_input += event.text

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    target *= zoom_speed
                if event.y < 0:
                    target /= zoom_speed
                zoom = max(5e-11, min(5e-9, zoom))
                target = max(5e-11, min(5e-9, target))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if typing_name:
                        name_input = name_input[:-1]
                    if typing_mass:
                        mass_input = mass_input[:-1]

                if not typing_name and not typing_mass:
                    if event.key == pygame.K_x:
                        if selected_planet is not None:
                            planets = [p for p in planets if p is not selected_planet]
                            selected_planet = None
                            initial_energy = energy(planets)

                                    

                    if event.key == pygame.K_d:
                        if not placing_planet:
                            placing_planet = True
                            placement_locked = False
                            placement_pos = None
                            placement_anim = 0
                        elif placing_planet and not placement_locked:
                            world_x = (mx - center_x) / zoom - camera_x
                            world_y = (my - center_y) / zoom - camera_y
                            too_close = False
                            for planet in planets:
                                dx = world_x - planet["position"][0]
                                dy = world_y - planet["position"][1]
                                dist_world = math.sqrt(dx ** 2 + dy ** 2)
                                min_dist = (planet["radius"] + 12) / scale
                                if dist_world < min_dist:
                                    too_close = True
                                    blocked = True
                                    break
                            if not too_close:
                                placement_pos = (world_x, world_y)
                                placement_locked = True
                            else:
                                placement_blocked_timer = 40
                        elif placing_planet and placement_locked:
                            placing_planet = False
                            placement_locked = False
                            placement_pos = None

                    if event.key == pygame.K_ESCAPE:
                        placing_planet = False
                        placement_locked = False
                        placement_pos = None
                    if event.key == pygame.K_c:
                        camera_x = 0
                        camera_y = 0
                    if event.key == pygame.K_r:
                        reset()
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    if event.key == pygame.K_UP:
                        return"custom"
                        dt *= 1.2
                    if event.key == pygame.K_DOWN:
                        dt //= 1.1
                    steps = max(10, min(200, int(dt / 3600) * 2))
                    dt = max(100, min(86400, dt))

        # simulation physics :

        if not paused:
            for _ in range(steps):
                for planet in planets:
                    fx, fy = calculate_forces(planet, planets)
                    ax = fx / planet["mass"]
                    ay = fy / planet["mass"]
                    planet["velocity"][0] += ax * dt / 2
                    planet["velocity"][1] += ay * dt / 2
                    planet["position"][0] += planet["velocity"][0] * dt
                    planet["position"][1] += planet["velocity"][1] * dt
                    fx, fy = calculate_forces(planet, planets)
                    ax = fx / planet["mass"]
                    ay = fy / planet["mass"]
                    planet["velocity"][0] += ax * dt / 2
                    planet["velocity"][1] += ay * dt / 2

                collisions = []
                for i in range(len(planets)):
                    for j in range(i + 1, len(planets)):
                        p1 = planets[i]
                        p2 = planets[j]
                        dx = p2["position"][0] - p1["position"][0]
                        dy = p2["position"][1] - p1["position"][1]
                        r_real = math.sqrt(dx * dx + dy * dy)

                        r1_phys = p1["radius"] * 1e8
                        r2_phys = p2["radius"] * 1e8

                        if r_real < (r1_phys + r2_phys):
                            collisions.append((i, j))
                to_remove = set()
                new_planets = []

                for i, j in collisions:
                    if i in to_remove or j in to_remove:
                        continue
                    p1 = planets[i]
                    p2 = planets[j]

                    bh = None
                    eaten = None
                    bh_idx = None
                    eaten_idx = None

                    if p1.get("type") == "black hole":
                        bh, bh_idx = p1, i
                        eaten, eaten_idx = p2, j
                    elif p2.get("type") == "black hole":
                        bh, bh_idx = p2, j
                        eaten, eaten_idx = p1, i

                    if bh is not None:
                        bh["mass"] += eaten["mass"]
                        bh["radius"] = get_radius(bh["mass"], "black hole")
                        to_remove.add(eaten_idx)
                        initial_energy = energy(planets)
                        impact.play()
                        shock.append({
                            'x': eaten["position"][0],
                            'y': eaten["position"][1],
                            'radius': 0,
                            'alpha': 255
                        })
                    else:
                        M_total = p1["mass"] + p2["mass"]
                        v_x_merged = (p1["mass"] * p1["velocity"][0] + p2["mass"] * p2["velocity"][0]) / M_total
                        v_y_merged = (p1["mass"] * p1["velocity"][1] + p2["mass"] * p2["velocity"][1]) / M_total
                        x_merged = (p1["mass"] * p1["position"][0] + p2["mass"] * p2["position"][0]) / M_total
                        y_merged = (p1["mass"] * p1["position"][1] + p2["mass"] * p2["position"][1]) / M_total
                        R_total = (p1["radius"] ** 3 + p2["radius"] ** 3) ** (1 / 3)
                        new_planets.append({
                            "name": "merged",
                            "mass": M_total,
                            "position": [x_merged, y_merged],
                            "velocity": [v_x_merged, v_y_merged],
                            "radius": R_total,
                            "color": p1["color"],
                            "ax": 0,
                            "ay": 0
                        })
                        to_remove.add(i)
                        to_remove.add(j)
                        impact.play()
                        shock.append({
                            'x': x_merged,
                            'y': y_merged,
                            'radius': 0,
                            'alpha': 255
                        })

                planets = [p for idx, p in enumerate(planets) if idx not in to_remove]
                planets.extend(new_planets)
                initial_energy = energy(planets)

        # button hover glowing :

        if hover_main_menu:
            main_menu = main_menu_glow
        else:
            main_menu = main_menu_normal
        if hover_real_orbit:
            real_orbit = real_orbit_glow
        else:
            real_orbit = real_orbit_normal
        if placing_planet and placement_locked:
            if hover_spawn_button:
                spawn_button = button_spawn_glow
            else:
                spawn_button = button_spawn_normal

        # camera dragging :

        if dragging:
            cx = mx - prevx
            cy = my - prevy
            camera_x += cx / zoom
            camera_y += cy / zoom
            camera_x = max(-max_dragging, min(max_dragging, camera_x))
            camera_y = max(-max_dragging, min(max_dragging, camera_y))
            prevx, prevy = mx, my

        # placement mode update :

        if placing_planet:
            placement_anim = (placement_anim + 3) % 360
        if placement_blocked_timer > 0:
            placement_blocked_timer -= 1
        if blocked:
            fade_text = "can't place here"
            fade_timer = fade_duration
            blocked = False

        # zoom lerp :

        zoom += (target - zoom) * zoom_interp

        # shockwaves :

        for sw in shock:
            sw['radius'] += 1
            sw['alpha'] -= 5
        shock = [sw for sw in shock if sw['alpha'] > 0]
        
        # time :

        if not paused:
            the_time += dt * steps
        current_date = start_date + timedelta(seconds=the_time)

        # error timers :

        if name_error_timer > 0:
            name_error_timer -= 1
        if mass_error_timer > 0:
            mass_error_timer -= 1
        if type_error_timer > 0:
            type_error_timer -= 1


        surface_text.fill((0, 0, 0, 0))

        # energy :

        energy_now = energy(planets)
        drift = (energy_now - initial_energy) / abs(initial_energy) * 100
        energy_text = energy(planets)

        # rendering :

        # text rendering :

        if selected_planet is None and not placement_locked:
            text_render(f"{current_date.strftime('%d/%m/%Y')}", text_font2, (0, 0, 0), 1450, 100)
            text_render(f"{sim_years_per_real_second:.2f} years", text_font, (0, 0, 0), 1510, 150)
            text_render(f"{energy_text:.2e}", text_font, (0, 0, 0), 1480, 277)
            text_render(f"{drift:.11f}%", text_font, (0, 0, 0), 1570, 325)

        if placing_planet and placement_locked:
            text_render(name_input, text_font, (0, 0, 0), 1490, 140)
            text_render(mass_input, text_font, (0, 0, 0), 1490, 210)
            text_render(type_input if type_input else "click to pick", text_font, (0, 0, 0), 1490, 530)

        # dashboard rendering :

        screen.blit(space_background, (0, 0))
        if selected_planet is None and not placement_locked:
            screen.blit(simulation_dashboard, (0, 0))
            screen.blit(quotes, (0, 0))
        if selected_planet is not None and not placement_locked:
            screen.blit(dashboard_planets, (0, 0))
        if placing_planet and placement_locked:
            screen.blit(spawning_dashboard, (0, 0))

        # spawning dashboarrendering :

        if placing_planet and placement_locked:
            if name_error_timer > 0:
                alpha = int((name_error_timer / 30) * 180)
                surface_error = pygame.Surface((324, 53), pygame.SRCALPHA)
                surface_error.fill((200, 0, 0, alpha))
                screen.blit(surface_error, (1484, 133))
            if mass_error_timer > 0:
                alpha = int((mass_error_timer / 30) * 180)
                surface_error = pygame.Surface((350, 55), pygame.SRCALPHA)
                surface_error.fill((200, 0, 0, alpha))
                screen.blit(surface_error, (1462, 204))
            if type_error_timer > 0:
                alpha = int((type_error_timer / 30) * 180)
                surface_error = pygame.Surface((346, 53), pygame.SRCALPHA)
                surface_error.fill((200, 0, 0, alpha))
                screen.blit(surface_error, (1472, 525))

        shock = [sw for sw in shock if sw['alpha'] > 0]
        surface.fill((0, 0, 0, 0))

        hovered_planet = None
        for planet in planets:
            screen_x = center_x + (planet["position"][0] + camera_x) * zoom
            screen_y = center_y + (planet["position"][1] + camera_y) * zoom
            radius = max(1, int(planet["radius"] * zoom / scale))
            dist = math.sqrt((mx - screen_x) ** 2 + (my - screen_y) ** 2)
            if dist < radius + 20:
                hovered_planet = planet

        star = None
        for planet in planets:
            if planet.get("type") == "star" or planet["name"] == "Sun":
                star = planet
                break
        if star:
            sun_sx = int(center_x + (star["position"][0] + camera_x) * zoom)
            sun_sy = int(center_y + (star["position"][1] + camera_y) * zoom)
            has_star = True
        else:
            sun_sx, sun_sy = int(center_x), int(center_y)
            has_star = False

        # planet drawing :

        for planet in planets:
            screen_x = center_x + (planet["position"][0] + camera_x) * zoom
            screen_y = center_y + (planet["position"][1] + camera_y) * zoom
            radius = max(1, int(planet["radius"] * zoom / scale))
            draw_planet_3d(surface, planet["color"], int(screen_x), int(screen_y),radius, sun_sx, sun_sy,is_sun=(planet.get("type") == "star" or planet["name"] == "Sun"),has_star=has_star)
            
        # selected planet info :

        if selected_planet is not None and not placement_locked:
            vel = math.sqrt(selected_planet["velocity"][0] ** 2 + selected_planet["velocity"][1] ** 2) / 1000
            au = math.sqrt(selected_planet["position"][0] ** 2 + selected_planet["position"][1] ** 2) / 1.496e11
            text_render(f"{selected_planet['name']}", text_font2, (0, 0, 0), 1490, 120)
            text_render(f"{vel:.2f} km/s", text_font, (0, 0, 0), 1530, 340)
            sun = next((p for p in planets if p["name"] == "Sun"), None)
            if selected_planet["name"] == "Sun":
                text_render("this is the sun", text_font, (0, 0, 0), 1460, 240)
            elif sun:
                text_render(f"{au:.2e} AU", text_font, (0, 0, 0), 1460, 240)
            else:
                text_render("the sun has vanished", text_font, (0, 0, 0), 1460, 240)
            text_render(f"{selected_planet['mass']:.2e} kg", text_font, (0, 0, 0), 1480, 415)
            text_render(f"{randomized}", text_font, (0, 0, 0), 1340, 520)

        # shockwave rendering :

        for sw in shock:
            sx = int(center_x + (sw['x'] + camera_x) * zoom)
            sy = int(center_y + (sw['y'] + camera_y) * zoom)
            r = int(sw['radius'])
            if r > 0:
                surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 255, 255, int(sw['alpha'])), (r, r), r, 2)
                screen.blit(surf, (sx - r, sy - r))

        # hover box :

        if hovered_planet:
            custom_cursor = cursor_click
            screen_x = int(center_x + (hovered_planet["position"][0] + camera_x) * zoom)
            screen_y = int(center_y + (hovered_planet["position"][1] + camera_y) * zoom)
            screen_radius = max(1, int(hovered_planet["radius"] * zoom / scale))
            box_size = min(screen_radius + 5, 60)
            pygame.draw.rect(surface, hovered_planet["color"],
                            (screen_x - box_size, screen_y - box_size, box_size * 2, box_size * 2), 2)
            text_render(hovered_planet["name"], text_font, hovered_planet["color"], screen_x + box_size + 5, screen_y - 20)
        else:
            custom_cursor = cursor_normal

        screen.blit(surface, (0, 0))

        # placement dot :

        if placing_planet:
            if placement_locked and placement_pos:
                dot_sx = int(center_x + (placement_pos[0] + camera_x) * zoom)
                dot_sy = int(center_y + (placement_pos[1] + camera_y) * zoom)
            else:
                dot_sx, dot_sy = mx, my
            pygame.draw.circle(screen, (100, 180, 255), (dot_sx, dot_sy), 6)

        # ui :

        screen.blit(main_menu, (0, 0))
        screen.blit(real_orbit, (0, 0))
        if placing_planet and placement_locked:
            screen.blit(spawn_button, (0, 0))
        screen.blit(surface_text, (0, 0))

        # fade text :
        
        if fade_timer > 0:
            alpha = int((fade_timer / fade_duration) * 255)
            fade_surf = text_font.render("can't place here", True, (225, 225, 225))
            fade_surf.set_alpha(alpha)
            screen.blit(fade_surf, (mx + 20, my - 20))
            fade_timer -= 1
        
        cursor(mx, my)
        clock.tick(60)
        pygame.display.flip()
