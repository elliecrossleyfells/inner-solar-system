import pygame as pg
import math
pg.init() #initialize pygame submodules and verify they are working as expected.

#set-up size of window
WIDTH, HEIGHT = 800, 700
#set up window and create pygame surface referencing size of window 
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("The Solar System")

WIN_BG = pg.image.load("ss_bg.jpg")

#Planet colour variables 
BG = (19, 0, 26)#(31, 34, 72) # window background
YELLOW = (253, 180, 17) #sun
GREY = (214, 214, 214) #mercury
ORANGE = (255, 216, 90) #venus
BLUE = (116, 228, 255) #earth
RED = (241, 0, 21) #mars
WHITE = (230,230,230) #text
PALEBLUE = (166, 200, 255) #comets

FONT = pg.font.SysFont("centurygothic", 16)
def draw_text(text, x, y, color=WHITE, font_size=16):
    font = FONT
    rendered_text = font.render(text, True, color)
    WIN.blit(rendered_text, (x, y))

#Creating Planets class and specifying its attributes
class Planet:
    AU = 149.6e6 * 1000 #distance from the sun in metres 
    G = 6.67428e-11 #universal gravitational constant
    SCALE = 200 / AU #scaling pixels in window
    TIMESTEP = 3600 * 10 #10hr per frame
    ORBIT_TRAIL = 1 #increase this to get orbit trailing

    def __init__(self, x, y, radius, color, mass, img = None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.img = None
        self.rotation_angle = 0

        if img:
            raw_img = pg.image.load(img).convert_alpha()
            scaled_img = pg.transform.scale(raw_img, (2 * self.radius, 2 * self.radius))
            self.base_img = scaled_img  # Keep the original image for rotation
            self.img = pg.Surface((2 * self.radius, 2 * self.radius), pg.SRCALPHA)
            pg.draw.circle(self.img, (255, 255, 255, 255), (self.radius, self.radius), self.radius)
            self.img.blit(scaled_img, (0, 0), special_flags=pg.BLEND_RGBA_MIN)

        self.orbit = []
        self.sun = False #planet is not the sun
        self.d_sun = 0

        self.x_v = 0 #x and y velocities
        self.y_v = 0 
    
    def draw(self,WIN):
        x = self.x * self.SCALE + WIDTH/2 
        y = self.y * self.SCALE + HEIGHT/2
                
        if self.img:
            rotated_img = pg.transform.rotate(self.base_img, self.rotation_angle)
            self.rotation_angle = (self.rotation_angle + 1) % 360  # Increment rotation angle
            # Center the image on the planet's position
            image_rect = self.img.get_rect(center=(x, y))
            WIN.blit(rotated_img, image_rect)
        else:
            pg.draw.circle(WIN, self.color, (x, y), self.radius)

        #creating a list of points from orbits that are scaled
        if len(self.orbit) >2:
            updated_points = []
            for point in self.orbit:
                 x, y = point
                 x = x * self.SCALE + WIDTH/2
                 y = y * self. SCALE + HEIGHT/2
                 updated_points.append((x,y))

            #draw points as a line
            pg.draw.lines(WIN, self.color, False, updated_points, 2)

        # pg.draw.circle(WIN, self.color, (x, y), self.radius)

#calculating distance from the sun text markers
        if not self.sun:
            distance_text = FONT.render(f"{round(self.d_sun/1000, 1):,}km", 1, WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width()/2, y + distance_text.get_height()/2))

    #calculating the force of attraction
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        #calculating distance between "current" object and "other" object 
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2) #pythag 

        if other.sun:
            self.d_sun = distance 

        #gravitational force equation calculating magnitude of force 
        F = self.G * self.mass * other.mass / distance**2
        #calculating the angle between bodies
        theta = math.atan2(distance_y, distance_x)
        #Resolving x and y components of vector F 
        F_x = F * math.cos(theta)
        F_y = F * math.sin(theta)
        return F_x, F_y
    
    #Getting total forces exerted on the planet (that is not itself)
    def update_position(self, planets):
        total_Fx = total_Fy = 0
        for planet in planets: #preventing divison by zero error from calculating F of planet with itself 
            if self == planet:
                continue 

            #sum
            fx, fy = self.attraction(planet)
            total_Fx += fx
            total_Fy += fy

        #calculate planet acceleration --> a = F / m then * timestep 
        self.x_v += total_Fx / self.mass * self.TIMESTEP
        self.y_v += total_Fy / self.mass * self.TIMESTEP

        #increment x and y positions from velocity 
        self.x += self.x_v * self.TIMESTEP
        self.y += self.y_v * self.TIMESTEP
        self.orbit.append((self.x, self.y))

        if len(self.orbit) > self.ORBIT_TRAIL:
         self.orbit = self.orbit[-self.ORBIT_TRAIL:]

class Comet:
    def __init__(self, x, y, radius, color, mass, period, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.period = period
        self.name = name
        
        self.orbit = []
        self.trail_length = 50  # Length of comet tail
        self.x_v = 0
        self.y_v = 0
        self.sun = False
        self.d_sun = 0
        
    def draw(self, WIN):
        x = self.x * Planet.SCALE + WIDTH/2
        y = self.y * Planet.SCALE + HEIGHT/2
        
        #Draw comet head
        pg.draw.circle(WIN, self.color, (x, y), self.radius)
        
        #Draw comet tail with fading effect
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit[-self.trail_length:]:
                x, y = point
                x = x * Planet.SCALE + WIDTH/2
                y = y * Planet.SCALE + HEIGHT/2
                updated_points.append((x, y))
            
            if len(updated_points) > 2:
                pg.draw.lines(WIN, self.color, False, updated_points, 2)
        
        #Draw distance text
        name_text = FONT.render(self.name, 1, WHITE)
        WIN.blit(name_text, (x - name_text.get_width()/2, y + self.radius + 5))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if other.sun:
            self.d_sun = distance
            
        F = Planet.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        F_x = F * math.cos(theta)
        F_y = F * math.sin(theta)
        return F_x, F_y
    
    def update_position(self, planets):
        total_Fx = total_Fy = 0
        for planet in planets:
            if self == planet:
                continue
                
            fx, fy = self.attraction(planet)
            total_Fx += fx
            total_Fy += fy
            
        self.x_v += total_Fx / self.mass * Planet.TIMESTEP
        self.y_v += total_Fy / self.mass * Planet.TIMESTEP
        
        self.x += self.x_v * Planet.TIMESTEP
        self.y += self.y_v * Planet.TIMESTEP
        self.orbit.append((self.x, self.y))
        
        if len(self.orbit) > self.trail_length:
            self.orbit = self.orbit[-self.trail_length:]

def main():
    run = True

    #ensuring framerate does not exceed a certain value
    clock = pg.time.Clock()
    # WIN.fill(BG)
    WIN.blit(WIN_BG, (0, 0))
    pg.display.update()

    #Create Planets in order of x, y, radius, color, mass as specified in Planet class
    #specifying inital y velocity y_v allows for orbit around sun
    sun = Planet(0, 0, 30, YELLOW, 1.98892*10**30, img = "SUN_IMG.jpg") 
    sun.sun = True
    
    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, 3.30*10**23, img = "merc_img.png")
    mercury.y_v = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 12, GREY, 6.39*10**23, img = "venus_img.png")
    venus.y_v = -35.02 * 1000

    earth = Planet(1 * Planet.AU, 0, 16, GREY, 5.9742*10**24, img = "earth_img.png")
    earth.y_v = -29.783 * 1000 

    mars = Planet(1.524 * Planet.AU, 0, 12, GREY, 6.39*10**23, img = "mars_img.png")
    mars.y_v = -24.077 * 1000

    #Comets - not real maths for aesthetic only!!
    halley = Comet(-0.45 * Planet.AU, 0, 1, PALEBLUE, 2.2*10**14, 75, "Halley")
    halley.y_v = -54 * 1000

    halebopp = Comet(-1.4 * Planet.AU, 0, 3, PALEBLUE, 1.3*10**19, 30, "Hale-Bopp")
    halebopp.y_v = -24 * 1000

    planets = [sun, mercury, venus, earth, mars, halley, halebopp]

    simulation_time = 0


    while run:
        clock.tick(60)
        WIN.blit(WIN_BG, (0, 0))
        #loop that runs while window is open - maintains animation looping until user closes window
        for event in pg.event.get(): 
             if event.type == pg.QUIT:  #specifying closing window event
                run = False 
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        # Increment simulation time
        simulation_time += Planet.TIMESTEP

        # Convert simulation time to readable format
        # 1 day = 86400 seconds
        # 1 year = 365.25 * 86400 seconds
        years = simulation_time // (365.25 * 86400)
        days = (simulation_time % (365.25 * 86400)) // 86400
        hours = (simulation_time % 86400) // 3600
        minutes = (simulation_time % 3600) // 60
        seconds = simulation_time % 60

        # Display formatted time
        time_text = f"Simulation Time: {int(years)}y {int(days)}d"
        draw_text(time_text, 10, 50)  # Display below the title text

        draw_text("Inner Solar System Simulation", 10, 10)
        draw_text("By Ellie Crossley-Fells", 10, 30)
        
        pg.display.update()
            
    pg.quit()


main()





