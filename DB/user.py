from DB.models import User


class ManageUser:
    def __init__(self, user: User):
        self.user = user
        self.discord_id = user.discord_id

    @property
    def steam_id(self):
        return int(self.user.steam_id)

    @property
    def last_match(self):
        return int(self.user.last_match)

    @classmethod
    def load(cls, discord_id):
        query = User.select().where(User.discord_id == discord_id)
        if query.exists():
            return cls(query.get())
        else:
            return None

    def __str__(self):
        return f'{self.user.discord_id} {self.user.steam_id} {self.user.last_match}'

    def update(self, steam_id, match_id):
        self.user.update({
            User.steam_id: steam_id,
            User.last_match: match_id
        }).execute()
        return f"Successfully updated user {self.discord_id}"

    @staticmethod
    def insert(discord_id, steam_id, match_id):
        User.insert({
            User.discord_id: discord_id,
            User.steam_id: steam_id,
            User.last_match: match_id
        }).execute()
        return f"Successfully registered a user"

    def update_last_match(self, match_id):
        if self.user.last_match != match_id:
            self.user.update({
                User.last_match: match_id
            }).execute()
            return True
        return False







# print(command_connect('tumen', 86228570))
# print(command_lastmatch('tumen'))
# command_lastmatchranks('tumen')

# c.execute("select * from users where discord_id = ? and steam_id = ?", ('tusmen', '76561198046494298'))
# print(c.fetchone())


# hist = api.get_last_match(76561198046494298)
# player = api.get_player(76561198046494298)

# print(hist['match_id'])
# print(player['personaname'])

# fetchone() returns one row
# fetchone() is None, if there is no row returned

# add player
# discord_id is always going to be correct
# if exists, continue
# otherwise display message and exit

# !connect STEAM_ID
# check if STEAM_ID exists
# if exists
# display message 'succesfully connected account'
# update database
# with discord_id, steam_id, lastmatch
# if doesn't exist
# display message, 'incorrect steam_id

# check every two minutes for whether last match for a user is updated or not
# if updated
# display message 'match info'
# update sql lastmatch for that steam_id
# else
# do nothing


# print(hist['matches'][99]['match_id'])

# API_KEY = '7CB8779F71A78DDE9712E590674E9333'