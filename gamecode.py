from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import sys, pygame
import math

class gameSpace(object):
    def __init__(self, connection):
        self.connection=connection
        print (self.connection)
        self.size = width, height = 800, 800
        self.color = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(self.color)
        #self.ship = ship(self)
        #self.earth = earth(self)
        #self.blaster= blaster(self)
        self.clock = pygame.time.Clock()
        self.color=255, 0, 0

    def run(self):
#        self.color= 255,0,0
    #    while 1:
     #       self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #self.ship.move(event)
                if event.key == pygame.K_g:
                    self.color= 0,255,0
                    self.connection.transport.write('green\n')
                if event.key == pygame.K_b:
                    self.color = 0,0,255
                if event.key == pygame.K_r:
                    self.color = 255,0,0
                if event.key == pygame.K_p:
                    self.color = 254, 143, 194
                if event.key == pygame.K_y:
                    self.color = 255, 255, 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(pygame.mouse.get_pos())
                #print("mouse pressed")	
                pygame.draw.circle(self.screen,self.color, pygame.mouse.get_pos(), 5, 2)	

            #self.ship.tick()
            #self.earth.tick(self)
            #self.blaster.tick(self)
            #self.screen.fill(self.color)
            #self.screen.blit(self.ship.image, self.ship.rect)
            #self.screen.blit(self.earth.image, self.earth.rect)
            #if self.blaster.render == 1: self.screen.blit(self.blaster.image, self.blaster.rect)

        pygame.display.flip()
            #reactor.callLater(0.1, self.clock.tick)

class colorIndex(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class ServerConnection(Protocol):
    def connectionMade(self):
        print( 'connection made')

    def dataReceived(self, data):
        print( 'data: ', data)

    def connectionLost(self, reasonForDisconnect):
        print('connection lost-reason: ', reasonForDisconnect)
        try:
            reactor.stop()
        except:
            pass

class ServerConnectionFactory(ClientFactory):
    def __init__(self):
        self.myconn=ServerConnection()
        #self.connection=connection

    def buildProtocol(self, addr):
        #return ServerConnection(addr, self.connection)
        return self.myconn

class Connections(object):
    def run(self):
        reactor.connectTCP("ash.campus.nd.edu", 40043, ServerConnectionFactory())
        reactor.run()

if __name__ == "__main__":
    connection=ServerConnectionFactory()
    conn=ServerConnection()
    reactor.connectTCP("ash.campus.nd.edu", 40043, connection)
    #reactor.run()
    gs = gameSpace(conn)
    lc=LoopingCall(gs.run)
    lc.start(0.1)
#    reactor.run()
    #s=ship(gs)
    #gs.run()
    #s = ship(gs)
    #connection=Connections()
    #connection.run()
    #reactor.connectTCP("ash.campus.nd.edu", 40043, ServerConnectionFactory())
    reactor.run()



