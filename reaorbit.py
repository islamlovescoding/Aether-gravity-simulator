import pygame
import math
import random
import time
import requests
import re
from datetime import datetime, timedelta

def real_orbit(screen):

    # custom cursor :

    x, y = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    customcursor = pygame.image.load("Assets/cursor.png")
    cursor_normal = pygame.image.load("Assets/cursor.png")
    cursor_click = pygame.image.load("Assets/cursor click.png")
    def cursor(x, y):
        screen.blit(customcursor, (x, y))

    # nasa horizons api fetch function :

    def get_planet_state(command_id, date):
        url = "https://ssd.jpl.nasa.gov/api/horizons.api"
        start = datetime.strptime(date, "%Y-%m-%d")
        stop = (start + timedelta(days=1)).strftime("%Y-%m-%d")
        params = {
            "format": "text",
            "COMMAND": command_id,
            "OBJ_DATA": "NO",
            "MAKE_EPHEM": "YES",
            "EPHEM_TYPE": "VECTORS",
            "CENTER": "500@0",
            "START_TIME": date,
            "STOP_TIME": stop,
            "STEP_SIZE": "1d",
            "OUT_UNITS": "KM-S",
            "VEC_TABLE": "2",
            "CSV_FORMAT": "NO"
        }
        response = requests.get(url, params=params)
        text = response.text
        if "$$SOE" not in text:
            raise Exception("No ephemeris data returned:\n" + text[:300])
        block = text.split("$$SOE")[1].split("$$EOE")[0].splitlines()
        pos_line = None
        vel_line = None
        for i, line in enumerate(block):
            if "X =" in line:
                pos_line = line
                vel_line = block[i + 1]
                break
        if pos_line is None:
            raise ValueError("Position line not found")
        def extract(line, key):
            return float(line.split(key)[1].split()[0])
        x = extract(pos_line, "X =") * 1000
        y = extract(pos_line, "Y =") * 1000
        vx = extract(vel_line, "VX=") * 1000
        vy = extract(vel_line, "VY=") * 1000
        return [x, y], [vx, vy]

    # loading the assets :

    dashboard = pygame.image.load("Assets/simulation dashboard.png").convert_alpha()
    space_real = pygame.image.load("Assets/space.png")
    main_menu = pygame.image.load("Assets/main menu button2.png")
    main_menu_normal = pygame.image.load("Assets/main menu button2.png")
    main_menu_glow = pygame.image.load("Assets/main menu button2 glow.png")
    dashboard_planets = pygame.image.load("Assets/planet dashboard.png")
    time_machine = pygame.image.load("Assets/time machine.png")
    newton_1 = pygame.image.load("Assets/newton1.png")
    newton_2 = pygame.image.load("Assets/newton2.png")
    newton_3 = pygame.image.load("Assets/newton3.png")
    newton_4 = pygame.image.load("Assets/newton4.png")
    newton_5 = pygame.image.load("Assets/newton5.png")
    feynmen_1 = pygame.image.load("Assets/feynman1.png")
    feynmen_2 = pygame.image.load("Assets/feynman2.png")
    feynmen_3 = pygame.image.load("Assets/feynman3.png")
    feynmen_4 = pygame.image.load("Assets/feynman4.png")
    feynmen_5 = pygame.image.load("Assets/feynman5.png")
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

    # display settings :

    pygame.display.set_caption("Aether - real orbit")
    clock = pygame.time.Clock()

    # variables :

    # quotes :

    quotes_list = [newton_1, newton_2, newton_3, newton_4, newton_5, feynmen_1, feynmen_2, feynmen_3, feynmen_4, feynmen_5, einstein_1, einstein_2, einstein_3, einstein_4, einstein_5]
    quotes = random.choice(quotes_list)

    # effects :

    shock = []
    randomized = ""
    selected_planet = None
    clicked_planet = None
    show_error = False
    error_timer = 0

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
    dt = 1
    G = 6.674e-11
    steps = 1

    # input / ui and other :

    typing_g = False
    input_string = ""
    paused = False
    run = True
    the_time = 0
    start_date = datetime.today()
    last_nasa_refresh = time.time()
    nasa_refresh_interval = 300

    # text :

    text_font = pygame.font.SysFont("Times New Roman", 35)
    text_font2 = pygame.font.SysFont("Times New Roman", 50)
    surface = pygame.Surface((1205, 1080), pygame.SRCALPHA)
    surface_text = pygame.Surface((1920, 1080), pygame.SRCALPHA)

    # planets basic information :

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

    # nasa planet ids :

    planet_ids = {
        "Sun": "10",
        "Mercury": "199",
        "Venus": "299",
        "Earth": "399",
        "Mars": "499",
        "Jupiter": "599",
        "Saturn": "699",
        "Uranus": "799",
        "Neptune": "899"
    }

    # fetch real positions from nasa :

    date = datetime.today().strftime("%Y-%m-%d")
    planets = []
    for name, pid in planet_ids.items():
        pos, vel = get_planet_state(pid, date)
        planets.append({
            "name": name,
            "position": pos,
            "velocity": vel,
            "mass": planets_basic[name]["mass"],
            "radius": planets_basic[name]["radius"],
            "color": planets_basic[name]["color"],
            "ax": 0,
            "ay": 0,
        })

    # functions :

    # energy calculation :

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

    # force calculation :

    def calculate_forces(planet, planets):
        fx = 0
        fy = 0
        for other in planets:
            if other is planet:
                continue
            dx = other["position"][0] - planet["position"][0]
            dy = other["position"][1] - planet["position"][1]
            r = math.sqrt(dx ** 2 + dy ** 2)
            F = G * planet["mass"] * other["mass"] / r ** 2
            fx += F * dx / r
            fy += F * dy / r
        return fx, fy

    # 3d planet shadow rendering :

    def draw_planet_3d(surface, color, cx, cy, radius, sun_screen_x, sun_screen_y, is_sun=False):
        pygame.draw.circle(surface, color, (cx, cy), radius)
        if is_sun or radius < 2:
            return
        dx = sun_screen_x - cx
        dy = sun_screen_y - cy
        dist = math.sqrt(dx * dx + dy * dy) or 1
        offset = int(radius * 0.35)
        ox = int(-dx / dist * offset)
        oy = int(-dy / dist * offset)
        shadow_r = int(radius * 0.92)
        pad = abs(ox) + abs(oy) + 4
        size = (radius + pad) * 2
        shadow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center_in_surf = (size // 2 + ox, size // 2 + oy)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 160), center_in_surf, shadow_r)
        surface.blit(shadow_surf, (cx - size // 2, cy - size // 2))

    # date input validation :

    def parse_date(text):
        text = text.strip()
        match = re.fullmatch(r"(\d{4})[-/ ](\d{2})[-/ ](\d{1,2})", text)
        if not match:
            return None
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if not (1600 <= year <= 2200):
            return None
        if not (1 <= month <= 12):
            return None
        if not (1 <= day <= 31):
            return None
        return datetime(year, month, day)

    # text rendering :

    def text_texting(text, font, color, x, y):
        image = font.render(text, True, color)
        surface_text.blit(image, (x, y))

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
        typing = 810 <= mouse[0] <= 1166 and 108 <= mouse[1] <= 186

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                typing_g = True if typing else False
                if hover_main_menu:
                    return "menu"
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
                            facts = planets_basic[selected_planet["name"]]["facts"]
                            randomized = random.choice(facts)
                dragging = True
                prevx = mx
                prevy = my
                click.play()

            if event.type == pygame.TEXTINPUT:
                if typing_g:
                    if event.text.isdigit() or event.text == "/":
                        test_string = input_string + event.text
                        test_surface = text_font.render(test_string + "|", True, (255, 255, 255))
                        if test_surface.get_width() < 180:
                            input_string = test_string

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
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_c:
                    camera_x = 0
                    camera_y = 0
                if event.key == pygame.K_BACKSPACE:
                    if typing_g:
                        input_string = input_string[:-1]
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if typing:
                        result = parse_date(input_string)
                        if result is None:
                            input_string = ""
                            show_error = True
                            error_timer = 180
                        else:
                            start_date = result
                            the_time = 0
                            input_string = ""
                            refresh_date = result.strftime("%Y-%m-%d")
                            for i, (name, pid) in enumerate(planet_ids.items()):
                                try:
                                    pos, vel = get_planet_state(pid, refresh_date)
                                    planets[i]["position"] = pos
                                    planets[i]["velocity"] = vel
                                except Exception:
                                    pass
                            initial_energy = energy(planets)
                            last_nasa_refresh = time.time()
                if event.key == pygame.K_UP:
                    dt *= 1.2
                if event.key == pygame.K_DOWN:
                    dt //= 1.1
                steps = max(1, min(200, int(dt / 3600) * 2))
                dt = max(1, min(86400, dt))

        # nasa refresh every 5 minutes :

        now = time.time()
        if now - last_nasa_refresh >= nasa_refresh_interval:
            current_date = start_date + timedelta(seconds=the_time)
            refresh_date = current_date.strftime("%Y-%m-%d")
            for i, (name, pid) in enumerate(planet_ids.items()):
                try:
                    pos, vel = get_planet_state(pid, refresh_date)
                    planets[i]["position"] = pos
                    planets[i]["velocity"] = vel
                except Exception:
                    pass
            last_nasa_refresh = now

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
                        M_total = p1["mass"] + p2["mass"]
                        dx = p2["position"][0] - p1["position"][0]
                        dy = p2["position"][1] - p1["position"][1]
                        r_real = math.sqrt(dx * dx + dy * dy)
                        r1_real = p1["radius"] / scale
                        r2_real = p2["radius"] / scale
                        x_5 = (p1["mass"] * p1["position"][0] + p2["mass"] * p2["position"][0]) / M_total
                        y_5 = (p1["mass"] * p1["position"][1] + p2["mass"] * p2["position"][1]) / M_total
                        if r_real < (r1_real + r2_real):
                            impact.play()
                            shock.append({'x': x_5, 'y': y_5, 'radius': 0, 'alpha': 255})
                            collisions.append((i, j))

                to_remove = set()
                new_planets = []
                for i, j in collisions:
                    if i in to_remove or j in to_remove:
                        continue
                    p1 = planets[i]
                    p2 = planets[j]
                    M_total = p1["mass"] + p2["mass"]
                    v_x1 = (p1["mass"] * p1["velocity"][0] + p2["mass"] * p2["velocity"][0]) / M_total
                    v_y1 = (p1["mass"] * p1["velocity"][1] + p2["mass"] * p2["velocity"][1]) / M_total
                    x5 = (p1["mass"] * p1["position"][0] + p2["mass"] * p2["position"][0]) / M_total
                    y5 = (p1["mass"] * p1["position"][1] + p2["mass"] * p2["position"][1]) / M_total
                    R_total = (p1["radius"] ** 3 + p2["radius"] ** 3) ** (1 / 3)
                    new_planets.append({
                        "name": "merged",
                        "mass": M_total,
                        "position": [x5, y5],
                        "velocity": [v_x1, v_y1],
                        "radius": R_total,
                        "color": p1["color"],
                        "ax": 0,
                        "ay": 0
                    })
                    to_remove.add(i)
                    to_remove.add(j)
                planets = [p for idx, p in enumerate(planets) if idx not in to_remove]
                planets.extend(new_planets)

        # button hover :

        if hover_main_menu:
            main_menu = main_menu_glow
        else:
            main_menu = main_menu_normal

        # camera dragging :

        if dragging:
            cx = mx - prevx
            cy = my - prevy
            camera_x += cx / zoom
            camera_y += cy / zoom
            camera_x = max(-max_dragging, min(max_dragging, camera_x))
            camera_y = max(-max_dragging, min(max_dragging, camera_y))
            prevx, prevy = mx, my

        # zoom lerp :

        zoom += (target - zoom) * zoom_interp

        # shockwaves :

        for sw in shock:
            sw['radius'] += 1
            sw['alpha'] -= 5
        shock = [sw for sw in shock if sw['alpha'] > 0]

        if not paused:
            the_time += dt * steps
        current_date = start_date + timedelta(seconds=the_time)

        # energy :

        energy_now = energy(planets)
        drift = (energy_now - initial_energy) / abs(initial_energy) * 100
        energy_text = energy(planets)

        surface_text.fill((0, 0, 0, 0))

        # text rendering :

        if selected_planet is None:
            text_texting(f"{current_date.strftime('%d/%m/%Y')}", text_font2, (0, 0, 0), 1450, 100)
            text_texting(f"{sim_years_per_real_second:.2f} years", text_font, (0, 0, 0), 1510, 150)
            text_texting(f"{energy_text:.2e}", text_font, (0, 0, 0), 1480, 277)
            text_texting(f"{drift:.11f}%", text_font, (0, 0, 0), 1570, 325)
        text_texting(input_string, text_font2, (0, 0, 0), 870, 120)

        # rendering :

        screen.blit(space_real, (0, 0))
        if selected_planet is None:
            screen.blit(dashboard, (0, 0))
            screen.blit(quotes, (0, 0))
            screen.blit(time_machine, (0, 0))
        else:
            screen.blit(dashboard_planets, (0, 0))

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

        sun = planets[0]
        sun_sx = int(center_x + (sun["position"][0] + camera_x) * zoom)
        sun_sy = int(center_y + (sun["position"][1] + camera_y) * zoom)

        for planet in planets:
            screen_x = center_x + (planet["position"][0] + camera_x) * zoom
            screen_y = center_y + (planet["position"][1] + camera_y) * zoom
            radius = max(1, int(planet["radius"] * zoom / scale))
            draw_planet_3d(surface, planet["color"], int(screen_x), int(screen_y),
                           radius, sun_sx, sun_sy, is_sun=(planet["name"] == "Sun"))

        if selected_planet is not None:
            vel = math.sqrt(selected_planet["velocity"][0] ** 2 + selected_planet["velocity"][1] ** 2) / 1000
            au = math.sqrt(selected_planet["position"][0] ** 2 + selected_planet["position"][1] ** 2) / 1.496e11
            text_texting(f"{selected_planet['name']}", text_font2, (0, 0, 0), 1490, 120)
            text_texting(f"{vel:.2f} km/s", text_font, (0, 0, 0), 1530, 340)
            if selected_planet["name"] != "Sun":
                text_texting(f"{au:.2e} AU", text_font, (0, 0, 0), 1460, 240)
            else:
                text_texting("this is the sun", text_font, (0, 0, 0), 1460, 240)
            text_texting(f"{selected_planet['mass']:.2e} kg", text_font, (0, 0, 0), 1480, 415)
            text_texting(f"{randomized}", text_font, (0, 0, 0), 1340, 520)

        for sw in shock:
            sx = int(center_x + (sw['x'] + camera_x) * zoom)
            sy = int(center_y + (sw['y'] + camera_y) * zoom)
            r = int(sw['radius'])
            if r > 0:
                surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 255, 255, int(sw['alpha'])), (r, r), r, 2)
                screen.blit(surf, (sx - r, sy - r))

        if hovered_planet:
            customcursor = cursor_click
            screen_x = int(center_x + (hovered_planet["position"][0] + camera_x) * zoom)
            screen_y = int(center_y + (hovered_planet["position"][1] + camera_y) * zoom)
            radius = max(1, int(hovered_planet["radius"] * zoom / scale))
            box_size = radius + 5
            pygame.draw.rect(surface, hovered_planet["color"],
                             (screen_x - box_size, screen_y - box_size, box_size * 2, box_size * 2), 2)
            text_texting(hovered_planet["name"], text_font, hovered_planet["color"], screen_x + 30, screen_y - box_size - 30)
        else:
            customcursor = cursor_normal

        # error animation :

        if show_error:
            alpha = int((error_timer / 180) * 220)
            error_surf = pygame.Surface((360, 80), pygame.SRCALPHA)
            error_surf.fill((200, 0, 0, alpha))
            screen.blit(error_surf, (810, 110))
            error_timer -= 25
            if error_timer >= 100:
                error_text = text_font.render("wrong format", True, (255, int(80 * error_timer / 180), int(80 * error_timer / 180)))
                error_surf.blit(error_text, (10, 110 // 2 - error_text.get_height() // 2))
                screen.blit(error_surf, (810, 110))
            if error_timer <= 0:
                show_error = False

        screen.blit(surface, (0, 0))
        screen.blit(main_menu, (0, 0))
        screen.blit(surface_text, (0, 0))
        cursor(mx, my)
        clock.tick(60)
        pygame.display.flip()