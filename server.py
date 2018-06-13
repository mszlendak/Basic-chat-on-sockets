from functools import reduce
import socket
import threading
import datetime

class CreateServer:
    clients = {}

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 8081))
        self.sock.listen(5)

    def get_clients(self):
        while True:
            (client_socket, adress) = self.sock.accept()

            client_socket.send('Udało ci się połączyć, Gratulacje! Podaj swój nick'.encode())

            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client):
        name = client.recv(400).decode('utf-8')
        welcome = 'Witaj {}! Jeżeli chcesz opuścic czat napisz !quit'.format(name)

        usr = {
            'client': client,
            'server': 'General'
        }

        self.clients[name] = usr

        client.send(welcome.encode())
        self.user_connected(name, self.clients[name]['server'])

        while True:
            try:
                wiadomosc = client.recv(800)
                if wiadomosc == '!quit'.encode():
                    client.send('Opuściłeś czat!'.encode())
                    if name in self.clients:
                        raise OSError
                elif wiadomosc.decode().startswith('!server'):
                    serv = wiadomosc.decode().split()[1]

                    self.clients[name]['server'] = serv
                    client.send('Zmieniłeś server na {}'.format(serv).encode())
                    self.user_connected_to_server(name, serv)

                elif wiadomosc.decode() == '!online':
                    client.send((reduce(lambda x, y: x + ', ' + y, list(self.clients.keys())).encode() if len(self.clients) > 1 else list(self.clients.keys())[0].encode()))

                else:
                    self.broadcast(wiadomosc, name, self.clients[name]['server'])
            except OSError:
                self.user_disconnected(name, self.clients[name]['server'])
                del self.clients[name]
                break

    def broadcast(self, message, name, server):
        for x in self.clients.values():
            if server == x['server']:
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                x['client'].send('[{}][{}] {}: {}'.format(date, x['server'], name, message.decode()).encode())

    def user_disconnected(self, name, server):
        for x in self.clients.values():
            if server == x['server']:
                x['client'].send('Użytkownik {} opuścił czat'.format(name).encode())

    def user_connected(self, name, server):
        for x in self.clients.values():
            if server == x['server']:
             x['client'].send('Użytkownik {} dołączył do czatu'.format(name).encode())

    def user_connected_to_server(self, name, server):
        for x in self.clients.values():
            if server == x['server']:
             x['client'].send('Użytkownik {} dołączył do servera'.format(name).encode())


server = CreateServer()

server.start()
server.get_clients()
