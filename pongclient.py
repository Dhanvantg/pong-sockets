import pygame, sys, math
import socket
pygame.init()
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.118"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

n = Network()
def ball_phy():
      
    global lscore, rscore

    if ball.top <=0 or ball.bottom >=screen_height:
        clack_sfx.play()
        
    if ball.left <=0:
        clack_sfx.play()
        
    if ball.right >=screen_width:
        clack_sfx.play()

    if pygame.Rect.colliderect(ball, player):
        clack_sfx.play()
    #if ball.colliderect(player)
    if pygame.Rect.colliderect(ball, opponent):
        clack_sfx.play()

clock = pygame.time.Clock()

screen_width = 1280
screen_height = 750

screen = pygame.display.set_mode ((screen_width, screen_height))
pygame.display.set_caption('Pong')
surface = pygame.Surface((screen_width,screen_height))
surface.set_colorkey((0, 0, 0))

ltransparency = pygame.Surface((screen_width/2,screen_height))
ltransparency.fill((255,178,86))

rtransparency = pygame.Surface((screen_width/2,screen_height))
rtransparency.fill((255,178,86))

ball = pygame.Rect((screen_width/2 - 15), (screen_height/2-15), 30,30)
player = pygame.Rect(screen_width-70, screen_height/2-70,20,140)
opponent = pygame.Rect(50, screen_height/2-70,20,140)

lscore = 0
rscore = 0

white = (211,81,0)
bg_color = (248,161,69)
black = (21, 21, 21)
lblack = (15, 15, 15)
mid = (240, 121, 0)
ghost_line = (0,0,0)

#SOUND
clack_sfx = pygame.mixer.Sound("C:/Users/dhanv/Downloads/Clack.wav")

#TEXT
font = pygame.font.Font("freesansbold.ttf", 64)

ballsp_x = 7
ballsp_y = 7
player_speed = 0
opp_speed = 0

ballcent = (screen_width/2,screen_height/2)

frames = 0
l=[]
print('hm')
pdat = n.send("newcon")
print(pdat)
if pdat == '1':
    player = pygame.Rect(50, screen_height/2-70,20,140)
    opponent = pygame.Rect(screen_width-70, screen_height/2-70,20,140)
    wdat = n.send('waiting')
    print(wdat)
elif pdat == '2':
    player = pygame.Rect(screen_width-70, screen_height/2-70,20,140)
    opponent = pygame.Rect(50, screen_height/2-70,20,140)
    wdat = n.send('waiting')
while True:
    frames+=1
    reply = eval(n.send(str(player.y) + ", " + str(player_speed)))
    # reply = [opponent.y, ball.x, ball.y, lscore, rscore]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:#and player.y <=screen_height:
                player_speed = 7
            if event.key == pygame.K_w: #and player.y >=0:
                player_speed = -7
            if pdat == 1 and ball.x > screen_width/2:
                player_speed = 0
            elif pdat == 2 and ball.x <= screen_width/2:
                player_speed = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:#and player.y <=screen_height:
                player_speed = 0
            if event.key == pygame.K_w: #and player.y >=0:
                player_speed = 0
        
               
                
    

    #a= pygame.time.get_ticks()
    #print(math.cos((a)*0.0006))
    #player.y += math.floor(1000*math.sin((a)*0.001))/200
    #print(player.y)
    
    ball_phy()
    player.y += player_speed 
    opponent.y = reply[0]
    ball.x = reply[1]
    ball.y = reply[2]
    lscore = reply[3]
    rscore = reply[4]


    if player.top<=0:
        player.top = 0

    if player.bottom>=screen_height:
        player.bottom = screen_height

    screen.fill(bg_color)
    if ball.x<= screen_width/2:
        screen.blit(ltransparency, (0,0))
    if ball.x> screen_width/2:
        screen.blit(rtransparency, (screen_width/2,0))
    l.append(ball.center)
    if len(l) >= 60:
        l.pop(0)
        linecent59 = l[1]
        linecent60 = l[0]
        pygame.draw.aaline(surface, bg_color, (linecent60),(linecent59))
        
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, opponent)
    pygame.draw.ellipse(screen, black, ball)

    pygame.draw.aaline(surface, lblack, (ballcent),(ball.center))

    pygame.draw.aaline(screen, mid, (screen_width/2,0),(screen_width/2, screen_height))
    
    ltext = font.render(str(lscore), True, black)
    screen.blit(ltext, (screen_width/4, 100))
    rtext = font.render(str(rscore), True, black)
    screen.blit(rtext, (screen_width*0.75, 100))

    


    
    screen.blit(surface, (0,0))
    ballcent = ball.center

    pygame.display.flip()
    
    clock.tick(60)


