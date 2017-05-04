from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class ServerConnection(Protocol):
    def __init__(self, addr, connection):
        self.addr=addr
        self.connection=connection

    def connectionMade(self):
        print 'connection made'

    def dataReceived(self, data):
        print 'data: ', data

    def connectionLost(self, reasonForDisconnect):
        print 'connection lost-reason: ', reasonForDisconnect
        try:
            reactor.stop()
        except:
            pass

class ServerConnectionFactory(ClientFactory):
    def __init__(self, connection):
        self.connection=connection

    def buildProtocol(self, addr):
        return ServerConnection(addr, self.connection)

class Connections(object):
    def run(self):
        reactor.connectTCP("ash.campus.nd.edu", 40043, ServerConnectionFactory(self))
        reactor.run()

if __name__=='__main__':
    connection=Connections()
    connection.run()
