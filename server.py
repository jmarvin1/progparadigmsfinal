#Rachael Mullin and James Marvin
#Programming Paradigms Final Project
#server.py
#Due: May 10, 2017

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from itertools import count

clientsConnected=[]
numberOfClients=count(1)

class ClientConnection(Protocol):
    #def __init__(self, addr, connection):
     #   self.addr=addr
      #  self.connection=connection

    def connectionMade(self):
        self.clientID=numberOfClients.next()
        clientsConnected.append(self)
        print 'client ', self.clientID, ' has joined'
        for client in clientsConnected:
            client.transport.write("client %s has joined\n" % (self.clientID,))

    def dataReceived(self, data):
        print self.clientID, ' sent ', data.strip()
        for client in clientsConnected:
            client.transport.write("%s sent %s\n" % (self.clientID, data.rstrip()))
            if data.strip()=='quit':
                self.transport.loseConnection()

    def connectionLost(self, reason):
        clientsConnected.remove(self)
        print self.clientID, ' quit'

class ClientConnectionFactory(Factory):
    def __init__(self):
        #self.connection=connection
        self.myconn=ClientConnection()

    def buildProtocol(self, addr):
        #return ClientConnection(addr, self.connection)
        return self.myconn

#class for instantiating connection
class Connections(object):
    def run(self):
        reactor.listenTCP(40043, ClientConnectionFactory(self))
        reactor.run()

if __name__=='__main__':
    #connection=Connections()
    #connection.run()
    reactor.listenTCP(40043, ClientConnectionFactory())
    reactor.run()
