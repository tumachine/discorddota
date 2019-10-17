from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import asyncio


class Map:
    def __init__(self, dictionary: dict):
        self.game_time = dictionary['game_time']
        self.clock_time = dictionary['clock_time']
        self.daytime = dictionary['daytime']
        self.nightstalker_night = dictionary['nightstalker_night']
        self.game_state = dictionary['game_state']
        self.paused = dictionary['paused']
        self.win_team = dictionary['win_team']
        self.customgamename = dictionary['customgamename']
        # self.ward_purchase_cooldown = dictionary['ward_purchase_cooldown']

    def runes_warning(self, before_time=30):
        if (self.clock_time + before_time) % 300 == 0:
            return True
        return False


class Server(BaseHTTPRequestHandler):
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message: dict = json.loads(self.rfile.read(length))
        dmap = message.get('map')
        print(message)
        if dmap is not None:
            des_map = Map(dmap)
            if des_map.runes_warning():
                print("RUNES!")

        # game_time = message['map']['clock_time']
        # print(game_time)


async def run(server_class=HTTPServer, handler_class=Server, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    # httpd.serve_forever()
    while True:
        httpd.handle_request()
        await asyncio.sleep(0.5)


async def main():
    await run()
    print('a')

# async def a():
#     await print('a')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.run_until_complete(main())
