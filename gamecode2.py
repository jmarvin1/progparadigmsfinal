#James Marvin (jmarvin1) Rachael Mullin (rmullin)
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.protocols.basic import LineReceiver
import sys, pygame
import os
import time
#create connection 
class ServerConnection(Protocol):
    def __init__(self):
        pygame.init() #starts up pygame
        pygame.key.set_repeat(1,30) #helps for drag feature
        self.size=800,800
        self.screen= pygame.display.set_mode(self.size)
        self.dragging=False
        self.color= 0,0,0
        #fill the screen with black
        self.screen.fill(self.color)
        self.color = 255,0,0
        self.colorstring="red"
        #create the key
        self.font=pygame.font.Font(None, 24)
        self.key=self.font.render("R-red G-green B-blue Y-yellow P-pink", 1, (255,255,255))
        self.screen.blit(self.key, (30,10))
        #load the first image
        self.image=pygame.image.load('images/smiley-face-clip-art-dr-odd-uWlQ3w-clipart.jpg')
        self.rect=self.image.get_rect()
        self.rect.x=300
        self.rect.y=50
        self.screen.blit(self.image, self.rect)
        #initialize time variables
        self.firstImageTime=30
        self.timer=self.firstImageTime
        self.secondImageTime=60
        self.thirdImageTime=90
        self.start_ticks=pygame.time.get_ticks()
        self.gameOver=self.font.render("Game over! Thanks for playing!", 1, (255,255,255))
        self.countdownRect=pygame.draw.rect(self.screen, (0,0,0), (700,10,100,100), 0)
        self.seconds=0
        self.secondsPassed=self.timer
        self.getTicks=0
        reactor.callLater(.05, self.tick)
    def tick(self): #function checking game conditions
        self.secondsPassed=int((self.getTicks+pygame.time.get_ticks()-self.start_ticks)/1000)
        self.seconds=self.timer-self.secondsPassed
        #display time on screen
        self.countdownRect=pygame.draw.rect(self.screen, (0,0,0), (700,10,100,100), 0)
        self.secondsLabel=self.font.render(str(self.seconds), 1, (255,255,255))
        self.screen.blit(self.secondsLabel,(715,15))
        if self.seconds<0:
            if self.timer==self.firstImageTime:
                self.screen.fill((0,0,0))
                self.screen.blit(self.key, (30,10))
                self.image=pygame.image.load('images/ndlogo.png')
                self.screen.blit(self.image,self.rect)
                self.timer=self.secondImageTime
                self.seconds=0
                self.start_ticks=self.start_ticks+30000
            elif self.timer==self.secondImageTime:
                self.screen.fill((0,0,0))
                self.screen.blit(self.key, (30,10))
                self.image=pygame.image.load('images/160px-Mona_Lisa.PNG')
                self.screen.blit(self.image,self.rect)
                self.timer=self.thirdImageTime
                self.seconds=0
                self.start_ticks=self.start_ticks+60000
            else:
                self.screen.fill((0,0,0))
                self.screen.blit(self.gameOver,(400,400))
        #handle events
        for event in pygame.event.get(): #key event
            if event.type == pygame.QUIT:
                reactor.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.color = 0,255,0
                if event.key == pygame.K_b:
                    self.color = 0,0,255
                if event.key == pygame.K_r:
                    self.color = 255, 0, 0
                if event.key == pygame.K_p:
                    self.color = 254, 143, 194
                if event.key == pygame.K_y:
                    self.color = 255, 255, 0
                if event.key == pygame.K_d:
                    x,y,z = self.color
                    aa, bb = pygame.mouse.get_pos()
                    string='draw circle:'+str(x)+','+str(y)+','+str(z)+':'+str(aa)+','+str(bb)+'\r\n'
                    string =str.encode(string)
                    self.transport.write(string)
            if event.type == pygame.MOUSEBUTTONDOWN: #mouse button event
                x,y,z = self.color
                aa, bb = pygame.mouse.get_pos()
                string='draw circle:'+str(x)+','+str(y)+','+str(z)+':'+str(aa)+','+str(bb)+'\r\n'
                string=str.encode(string)
                self.transport.write(string)

        pygame.display.flip()
        reactor.callLater(.05, self.tick)
    #indicate to the server that player 2 has joined the game
    def connectionMade(self):
        print( 'connection made 2')
        string='connection made 2'+'\r\n'
        string=str.encode(string)
        self.transport.write(string)

    #report connection losses and the reason for the loss
    def connectionLost(self, reasonForDisconnect):
        print('connection lost-reason: ', reasonForDisconnect)
        try:
            reactor.stop()
        except:
            pass

    #handle data recieved from the server
    def dataReceived(self, line):
        try: #drawing a point
            print('line received')
            lineList=line.decode().split(':')
            print (lineList[0])
            print (lineList[1])
            print (lineList[2][0])
            if lineList[0]=='draw circle':
                lineListX=lineList[2].split(',')[0]
                lineListY=lineList[2].split(',')[1]
                lineListY=lineListY.split('\\')[0]
                newList=(int(lineListX), int(lineListY))
                print (newList)
                a=lineList[1].split(',')[0]
                b=lineList[1].split(',')[1]
                c=lineList[1].split(',')[2]
                colorList=(int(a), int(b), int(c))
                print (colorList)
            pygame.draw.circle(self.screen,colorList,newList,5,0)
        except:
            try: #get time from player 1
                line=line.decode()
                self.getTicks=int(line)
                print ('self.getTicks:', self.getTicks)
            except:
                pass


class ServerConnectionFactory(ClientFactory):
    def buildProtocol(self, addr):
        return ServerConnection()



if __name__ == "__main__":
    reactor.connectTCP("ash.campus.nd.edu", 41043, ServerConnectionFactory())
    reactor.run()

