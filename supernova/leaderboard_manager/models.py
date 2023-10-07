class User:
    def __init__(self, username):
        self.username = username
        self.posts = []
        self.total_score = 0

    def update_score(self):
        # This method will utilize functions from scoring.py
        # Its implementation will be filled later
        pass


class Post:
    def __init__(self, content_type, timestamp):
        self.content_type = content_type
        self.timestamp = timestamp
        self.reactions = []

    def add_reaction(self, reaction_type, reactor):
        self.reactions.append(Reaction(reaction_type, reactor))


class Reaction:
    def __init__(self, type, reactor):
        self.type = type
        self.reactor = reactor
