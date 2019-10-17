import re
import time


class ServerLog:
    def __init__(self, line):
        str_time = line[:21]
        self.time = time.strptime(str_time, "%m/%d/%Y - %H:%M:%S")
        self.server = None
        self.players_lobby = None
        self.players_party = None
        self.mode = None

        server_id = re.search(r'A:1:(\d*:\d*)', line)
        party = re.search(r'Party \d* (\d:\[U:1:\d*\] ?)*', line)
        lobby = re.search(r'Lobby \d* \w* (\d:\[U:1:\d*\] ?)*', line)
        if party:
            self.players_party = [player[7:-1] for player in party.group(0).split(' ')[2:]]
        if lobby:
            sep_lobby = lobby.group(0).split(' ')
            self.players_lobby = [player[7:-1] for player in sep_lobby[3:]]
            self.mode = sep_lobby[2]
        if server_id:
            self.server = server_id.group(1)

    def is_match(self):
        if self.players_lobby is not None:
            if self.server and len(self.players_lobby) == 10 and self.mode:
                return True
        return False

    def __str__(self):
        return f'Time: {self.time.tm_year}/{self.time.tm_mon}/{self.time.tm_mday} - {self.time.tm_hour}:' \
            f'{self.time.tm_min}:{self.time.tm_sec}\nServer: {self.server}\nMode: {self.mode}\n' \
            f'Players Match: {self.players_lobby}\nPlayers Party: {self.players_party}'


def test_server_log(server_log_file):
    with open(server_log_file, 'r') as f:
        for line in f:
            print(f'{ServerLog(line)}\n')

# test_server_log(server_log_path)