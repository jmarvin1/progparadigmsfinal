#Rachael Mullin and James Marvin
#Programming Paradigms Final Project
#server.py
#Due: May 10, 2017

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from itertools import count

#Player ports on ash
p1PORT=40043
p2PORT=41043

#Player 1 Client Connection Class
class P1Connection(Protocol):
    def __init__(self, addr, connection):
        self.addr=addr
        self.connection=connection
        self.connection.p1connection=self

    def connectionMade(self):
        self.connection.p1connected=True
        print 'p1 connected'

    def dataReceived(self, data):
        print 'data: ', data
        self.connection.sendUpdate(data)

    def connectionLost(self, reason):
        print 'p1 connection lost'

#Player 1 Client Connection Class Factory
class P1ConnectionFactory(Factory):
    def __init__(self, connection):
        self.connection=connection

    def buildProtocol(self, addr):
        return P1Connection(addr, self.connection)

#Player 2 Client Connection Class
class P2Connection(Protocol):
    def __init__(self, addr, connection):
        self.addr=addr
        self.connection=connection
        self.connection.p2connection=self

    def connectionMade(self):
        self.connection.p2connected=True
        print 'p2 connected'

    def dataReceived(self, data):
        print 'data: ', data
        self.connection.sendUpdate(data)

    def connectionLost(self, reason):
        print 'p2 connection lost'

#Player 2 Client Connection Class Factory
class P2ConnectionFactory(Factory):
    def __init__(self, connection):
        self.connection=connection

    def buildProtocol(self, addr):
        return P2Connection(addr, self.connection)

#class for instantiating connection
class Connections(object):
    def __init__(self):
        reactor.listenTCP(p1PORT, P1ConnectionFactory(self))
        reactor.listenTCP(p2PORT, P2ConnectionFactory(self))
        self.p1connection=None
        self.p2connection=None
        self.p1connected=False
        self.p2connected=False

    #used to update the screens of both players when one player causes an event
    def sendUpdate(self, updateString):
        try:
            self.p1connection.transport.write(updateString)
        except:
            pass

        try:
            self.p2connection.transport.write(updateString)
        except:
            pass

if __name__=='__main__':
    connection=Connections()
    reactor.run()
