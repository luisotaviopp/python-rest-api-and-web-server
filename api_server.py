from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import cgi

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    def do_HEAD(self):
        self._set_headers()


    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode('utf-8')) # Retorna um Hello World
    

    def do_POST(self):

        # Retorna um 400 se o arquivo não for do tipo json
        ctype, pdict = cgi.parse_header(self.headers.get("content-type"))        
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # Lê a mensagem e cria um dicionário.
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # Adiciona um campo "ok" no json de retorno, pra confirmar que funcionou.
        message['status'] = 'ok'
        
        # Retorna o json modificado.
        self._set_headers()
        self.wfile.write(bytes(json.dumps(message), 'utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8555):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()
    

if __name__ == "__main__":
    from sys import argv
    
    # Se o arquivo for aberto com uma porta, usa a porta especificada. 
    # Exemplo: Se abrir com o comando 'python3 arquivo.py 4555', abrirá na porta 4555
    # Se não especificar a porta ('python3 arquivo.py'), abrirá na porta especificada no 'def run'

    if len(argv) == 2:          
        run(port=int(argv[1]))
    else:
        run()