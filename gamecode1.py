from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.protocols.basic import LineReceiver
import sys, pygame

class ServerConnection(Protocol):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(1,30) #helps for drag feature
        self.size=800,800
        self.screen= pygame.display.set_mode(self.size)
        self.color= 0,0,0
        self.gs=None
        self.screen.fill(self.color)
        self.color = 255,0,0
        self.colorstring="red"
        reactor.callLater(.05, self.tick)
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.color = 0,255,0
                    self.colorstring="green"
                if event.key == pygame.K_b:
                    self.color = 0,0,255
                    self.colorstring="blue"
                if event.key == pygame.K_r:
                    self.color = 255, 0, 0
                    self.colorstring = "red"
                if event.key == pygame.K_p:
                    self.color = 254, 143, 194
                    self.colorstring="pink"
                if event.key == pygame.K_y:
                    self.color = 255, 255, 0
                    self.colorstring="yellow"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y,z = self.color
                x=str(x).encode("UTF-8")
                y=str(y).encode('UTF-8')
                z=str(z).encode('UTF-8')
                aa, bb = pygame.mouse.get_pos()
                aa=str(aa).encode('UTF-8')
                bb=str(bb).encode('UTF-8')
               # self.transport.write("draw circle: "+x+","+y+","+z+":"+aa+","+bb+"\r\n")
                string='draw circle: 255,0,0:400,400\r\n'
                string=str.encode(string)
                self.transport.write(string)

        pygame.display.flip()
        reactor.callLater(.05, self.tick)

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

    def lineReceived(self, line):
        print('line received')
        line.split(':')
        if line[0]=='draw circle':
            pygame.draw_circle(self.screen,tuple(line[1]),tuple(line[2]),5,2)

class ServerConnectionFactory(ClientFactory):
    def buildProtocol(self, addr):
        return ServerConnection()

if __name__ == "__main__":
    reactor.connectTCP("ash.campus.nd.edu", 40043, ServerConnectionFactory())
    reactor.run()



