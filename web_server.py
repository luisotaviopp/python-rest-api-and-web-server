from http.server import HTTPServer, BaseHTTPRequestHandler
import json 


class Serv(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/':
			self.path = '/index.html'
		try:
			# Aqui, ele abre o html que foi passado na rota
			# (ex: /home.html, /arquivo.html, pode adicionar quantas páginas quiser nessa pasta).
			file_to_open = open(self.path[1:]).read()
			self.send_response(200)
		except:
			file_to_open = "File not found"
			self.send_response(404)

		self.end_headers()
		self.wfile.write(bytes(file_to_open, 'utf-8'))


httpd = HTTPServer(('localhost', 8085), Serv)
httpd.serve_forever()
