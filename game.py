# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started=False
count=0
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.is_thrusters=0
        self.forward=[0,0]
        
    def draw(self,canvas):
        if self.is_thrusters==2 or self.is_thrusters==0:
            canvas.draw_image(self.image, self.image_center,self.image_size,self.pos,self.image_size,self.angle)
            ship_thrust_sound.rewind()
        else:
            canvas.draw_image(self.image,[self.image_center[0]+90,self.image_center[1]],self.image_size,self.pos,self.image_size,self.angle)
            ship_thrust_sound.play()
    def update(self):
        self.angle+=self.angle_vel
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1] 
        self.pos[0]%=800
        self.pos[1]%=600
        self.forward=angle_to_vector(self.angle)
        if self.is_thrusters==1:
            self.vel[0]+=self.forward[0]*0.05
            self.vel[1]+=self.forward[1]*0.05
        elif self.is_thrusters==2:
            self.vel[0]*=(1-0.01)
            self.vel[1]*=(1-0.01)
            
        
    def rotate_left(self):
        self.angle_vel=-0.08
    
    def rotate_right(self):
        self.angle_vel=0.08
        
    def shoot(self):
        global missiles
        vel=[0,0]
        pos=[math.cos(self.angle)*45+self.pos[0],math.sin(self.angle)*45+self.pos[1]]
        vel[0]=self.vel[0]+self.forward[0]*7
        vel[1]=self.vel[1]+self.forward[1]*7
        angle_vel=0
        angle=self.angle
        a_missile=Sprite(pos,vel,angle,angle_vel,missile_image,missile_info,missile_sound)
        missiles.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.sound=sound
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image,self.image_center, self.image_size,self.pos,self.image_size,self.angle)
     
        
    def update(self):
        self.angle+=self.angle_vel
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1] 
        self.pos[0]%=800
        self.pos[1]%=600
        self.age+=1
        if self.age>=self.lifespan:
            return True
        else:
            return False
        
    def collide(self,s):
        if (dist(self.pos,s.pos))<=(self.radius+s.radius):
            return True
        else:
            return False
            
        
        


def draw(canvas):
    global time,rock_group,started,count,lives,score,missiles,my_ship,explosion_group
 
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Score = "+str(score),[100,100],35,"white")
    canvas.draw_text("Lives = "+str(lives),[600,100],35,"white")
 
    if not started:
        canvas.draw_image(splash_image,splash_info.get_center(),splash_info.get_size(),[WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    else: 
    # draw ship and sprites
        my_ship.draw(canvas)
        for i in rock_group:
                i.draw(canvas)
        for i in missiles:        
                i.draw(canvas)
    # update ship and sprites
        my_ship.update()
        for i in rock_group:
            i.update()
        for i in missiles:        
            a=i.update()
            if a:
                sprite_age(i)
        
        if group_collide(my_ship):
            lives-=1
        if lives==0:
            start_new_game()
 
        c=group_group_collide()
        score+=c
        count-=c
        
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group,count
    pos=[random.randrange(0,800),random.randrange(0,600)]
    vel=[random.randrange(-1,1),random.randrange(-1,1)]
    angle=random.randrange(-3,3)
    angle_vel=0.05
    if count<12:
        a_rock=Sprite(pos,vel,angle,angle_vel,asteroid_image, asteroid_info)
        if dist(a_rock.pos,my_ship.pos)>100:
            rock_group.add(a_rock)
            count+=1
        
def key_handler_down(key):
    if key==simplegui.KEY_MAP["left"]:
        my_ship.rotate_left()
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.rotate_right()
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.is_thrusters=1
    elif key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        

def key_handler_up(key):
    if key==simplegui.KEY_MAP["left"] or key==simplegui.KEY_MAP["right"]:
        my_ship.angle_vel=0 
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.is_thrusters=2

def mouse_handler(pos):
    global started
    p=splash_info.get_size()
    if pos[0]<=(WIDTH/2)+(p[0]/2) and pos[0]>=((WIDTH/2)-p[0]/2) and pos[1]<=HEIGHT/2+(p[1]/2) and pos[1]>=HEIGHT/2-(p[1]/2):
        started=True 
        soundtrack.play()   
            
            
def group_collide(sprite):
    global rock_group,explosion_group
    removed=set(rock_group)
    p=False
    for i in removed:
        a=i.collide(sprite)
        if a:
            rock_group.remove(i)
            p=True
    
    return p       

def sprite_age(i):
    missiles.remove(i)
        
def group_group_collide():
    global missiles,rock_group
    r=set(rock_group)
    m=set(missiles)
    count=0
    for i in r:
        for j in m:
            indicator=i.collide(j)
            if indicator:
                missiles.remove(j)
                rock_group.remove(i)
                count+=1
    return count 

def start_new_game():
        global started,rock_group,missiles,score,my_ship,lives,count
        started=False
        rock_group=set([])
        missiles=set([])
        score=0
        count=0
        lives=3
        soundtrack.pause()
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_handler_down)
frame.set_keyup_handler(key_handler_up)
frame.set_mouseclick_handler(mouse_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
start_new_game()
