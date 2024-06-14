import wifi
import socketpool
import gc
import time
import ipaddress
import sys
import os
import json
import errno

from atoms.hid import AtomDucky, load_payload_from_file
from atoms.config_man import ConfigMan
from atoms.buttons import button, pixel
from atoms.colors import color

def button_pressed():
    return button.value

class WebHost:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.config = ConfigMan()
        self.start_web_server()
        pixel.fill(color("cyan"))
        self.run_web_loop()

    def start_web_server(self):
        try:
            self.pool = socketpool.SocketPool(wifi.radio)
            self.server_socket = self.pool.socket(self.pool.AF_INET, self.pool.SOCK_STREAM)
            """
                PROTIP: without this line the program will scream EADDRINUSE with every soft reboot.
            """
            self.server_socket.setsockopt(self.pool.SOL_SOCKET, self.pool.SO_REUSEADDR, 1)
            # ^^
            self.server_socket.bind((str(self.ip), self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(None)  # Use blocking mode
            print(f"Listening on http://{self.ip}:{self.port}")
        except OSError as e:
            """
                we used pool.SO_REUSEADDR, but just in case
            """
            pixel.fill(color("red"))
            if e.errno == errno.EADDRINUSE:
                print("Address already in use. Retrying...")
                self.server_socket.close()
                time.sleep(5)
                self.start_web_server()

    def read_file_in_chunks(self, path, chunk_size=1024):
        try:
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            print(str(e))
            yield None

    def get_content_type(self, path):
        if path.endswith(".html"):
            return "text/html"
        elif path.endswith(".css"):
            return "text/css"
        elif path.endswith(".svg"):
            return "image/svg+xml"
        elif path.endswith(".ico"):
            return "image/x-icon"
        else:
            return "application/octet-stream"

    def send_with_retry(self, client_socket, data):
        while data:
            try:
                sent = client_socket.send(data)
                data = data[sent:]
            except OSError as e:
                if e.errno == errno.EAGAIN:
                    continue
                else:
                    raise
                
    def handle_request(self, client_socket):
        try:
            buffer = bytearray(1024)
            received_bytes = client_socket.recv_into(buffer)
            request = buffer[:received_bytes].decode()
            print("Request:", request)

            request_line = request.splitlines()[0]
            method, file_path, _ = request_line.split(" ")
            if file_path == "/":
                file_path = "/index.html"

            endpoint_handlers = {
                "/modify_payload": self.handle_modify_payload,
                "/file_manager": self.handle_file_manager,
                "/single_payload": self.handle_single_payload,
                "/ret_templates": self.handle_ret_templates,
                "/edit_config": self.handle_edit_config,
                "/restart": self.handle_restart,
                "/inject": self.handle_inject,
            }

            handler = None
            for ep, h in endpoint_handlers.items():
                if file_path.startswith(ep):
                    handler = h
                    break

            if handler:
                handler(client_socket, request)
            else:
                content_type = self.get_content_type(file_path)
                headers = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode()
                self.send_with_retry(client_socket, headers)

                for chunk in self.read_file_in_chunks(file_path[1:]):
                    if chunk is None:
                        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                        self.send_with_retry(client_socket, response)
                        break
                    self.send_with_retry(client_socket, chunk)
            gc.collect()
        except OSError as e:
            print("OSError in handle_request", str(e))
        finally:
            client_socket.close()

    def unpack_body_and_headers(self, req_lines):
        headers = {}
        body = ""
        is_body = False

        for line in req_lines[1:]:
            if line == "":
                is_body = True
                continue
            if is_body:
                body += line + "\n"
            else:
                key, value = line.split(": ", 1)
                headers[key] = value

        return headers, body.strip()

    def handle_restart(self, client_socket, req=None):
        print("Restarting...")
        import supervisor
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nRestarting..."
        self.send_with_retry(client_socket, response)
        supervisor.reload()

    def handle_inject(self, client_socket, req=None):
        print("Injecting...")
        ducky = AtomDucky()
        payload = load_payload_from_file()
        gc.collect()
        if payload is not None:
            ducky.payloads_write(payload)
        gc.collect()
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nPayload Injected"
        self.send_with_retry(client_socket, response)

    def handle_file_manager(self, client_socket, request):
        request_lines = request.splitlines()
        method, url, _ = request_lines[0].split(" ")
        headers, body = self.unpack_body_and_headers(request_lines)
        
        print("Headers:", headers)
        print("Body:", body)
        if method == 'POST':
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOk, but why POST Method?"
        elif method == 'GET':
            files = os.listdir()
            response_body = json.dumps(files)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        self.send_with_retry(client_socket, response.encode())

    def handle_single_payload(self, client_socket, request):
        request_lines = request.splitlines()
        method, url, _ = request_lines[0].split(" ")
        headers, body = self.unpack_body_and_headers(request_lines)
    
        print("Headers:", headers)
        print("Body:", body)
        if method == 'POST':
            print("Injecting...")
            ducky = AtomDucky()
            payload = body
            gc.collect()
            if payload is not None:
                ducky.payloads_write(payload, skip_release=True)
            gc.collect()
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nSuccess!"
            self.send_with_retry(client_socket, response)     
    
    def handle_ret_templates(self, client_socket, request):
        request_lines = request.splitlines()
        method, url, _ = request_lines[0].split(" ")
        path, _, query = url.partition('?')
        params = dict(param.split('=') for param in query.split('&'))
        headers, body = self.unpack_body_and_headers(request_lines)

        print("Headers:", headers)
        print("Body:", body)
        if method == 'GET' and params.get('action') == 'read_list':
            content = json.dumps(os.listdir('/atoms/templates'))
            print(content)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{content}"
            self.send_with_retry(client_socket, response.encode())
        if method == 'GET' and params.get('action') == 'read':
            template_name = params.get('name')
            self.read_payload(client_socket, folder='atoms/templates', name=template_name)
        elif method == 'POST' and params.get('action') == 'write':
            data = body
            template_name = params.get('name')
            # Name of the file can be maximum 16 chars
            if template_name != '' and len(template_name) < 16:
                self.write_payload(client_socket, data, folder='atoms/templates', name=template_name)
     
    def handle_modify_payload(self, client_socket, request):
        request_lines = request.splitlines()
        method, url, _ = request_lines[0].split(" ")
        path, _, query = url.partition('?')
        params = dict(param.split('=') for param in query.split('&'))

        headers, body = self.unpack_body_and_headers(request_lines)

        print("Headers:", headers)
        print("Body:", body)
        if method == 'GET' and params.get('action') == 'read':
            self.read_payload(client_socket)
        elif method == 'POST' and params.get('action') == 'write':
            data = body
            self.write_payload(client_socket, data)

    def handle_edit_config(self, client_socket, request):
        try:
            request_lines = request.splitlines()
            method, url, _ = request_lines[0].split(" ")
            path, _, query = url.partition('?')
            headers, body = self.unpack_body_and_headers(request_lines)

            print("Headers:", headers)
            print("Body:", body)
            
            if method == 'POST':
                try:
                    config_updates = json.loads(body)
                    valid_fields = {"IP", "SSID", "PASSW", "AP", "MODE"}
                    if not all(field in valid_fields for field in config_updates.keys()):
                        response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid field in request body."
                    else:
                        self.config.edit_config(**config_updates)
                        response = "HTTP/1.1 200 OK\r\n\r\nConfig updated successfully."
                except ValueError:
                    response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON in request body."
                except Exception as e:
                    print(str(e))
                    response = f"HTTP/1.1 500 Internal Server Error\r\n\r\nError updating config: {str(e)}"
            else:
                response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid request method."
            
            self.send_with_retry(client_socket, response)
        except Exception as e:
            print(f"Exception in handle_edit_config: {e}")
            response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n{str(e)}"
            self.send_with_retry(client_socket, response)
 
    def read_payload(self, client_socket, folder="atoms", name="payload"):
        try:
            with open(f'/{folder}/{name}.txt', 'r') as f:
                content = f.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{content}"
        except Exception as e:
            print(str(e))
            response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError reading payload: {str(e)}"
        self.send_with_retry(client_socket, response.encode())
        
    def write_payload(self, client_socket, data, folder="atoms", name="payload"):
        try:
            with open(f'/{folder}/{name}.txt', 'w') as f:
                f.write(data)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nPayload written successfully"
        except Exception as e:
            print(str(e))
            response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError writing payload: {str(e)}"
        self.send_with_retry(client_socket, response.encode())

    def run_web_loop(self): 
            while True:
                client_socket, addr = self.server_socket.accept()
                print("Client connected from", addr)
                self.handle_request(client_socket)