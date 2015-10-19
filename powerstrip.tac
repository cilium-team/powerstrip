import os
from twisted.application import service, internet
#from twisted.protocols.policies import TrafficLoggingFactory
from urlparse import urlparse

from powerstrip.powerstrip import ServerProtocolFactory

application = service.Application("Powerstrip")

KUBE_SERVER = os.environ.get('KUBE_SERVER')
if KUBE_SERVER is None:
    # Default to assuming we've got a Kubernetes socket bind-mounted into a
    # container we're running in.
    KUBE_SERVER = "tcp://localhost:8080"
if "://" not in KUBE_SERVER:
    KUBE_SERVER = "tcp://" + KUBE_SERVER
if KUBE_SERVER.startswith("tcp://"):
    parsed = urlparse(KUBE_SERVER)
    kubeAPI = ServerProtocolFactory(kubeAddr=parsed.hostname,
        kubePort=parsed.port)
elif KUBE_SERVER.startswith("unix://"):
    socketPath = KUBE_SERVER[len("unix://"):]
    kubeAPI = ServerProtocolFactory(kubeSocket=socketPath)
#logged = TrafficLoggingFactory(kubeAPI, "api-")
kubeServer = internet.TCPServer(8080, kubeAPI, interface='0.0.0.0')
kubeServer.setServiceParent(application)

print r'export KUBE_SERVER=http://localhost:8080'
