from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sys

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class calculadora:
    def suma(self,x,y):
        return x+y
    def resta(self,x,y):
        return x-y
    def multiplicacion(self,x,y):
        return x*y
    def division(self,x,y):
        return x/y


try:
    server= SimpleXMLRPCServer(('localhost',8000),requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_instance(calculadora())
    print("Escuchando en la direccion localhost:8000")
    # Run the server's main loop
    server.serve_forever()
except Exception as e:
    print(str(e))
except KeyboardInterrupt:
    print("\nKeyboard interrupt recibida, saliendo.")
    sys.exit(0)
