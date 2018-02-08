import json

class ActorInfo:
    def __init__(self, name, id, html):
        self.name = name
        self.id = id
        self.titles = None
        self.html = html

    def set_titles(self, titles):
        self.titles = {title.id: title for title in titles}

    def add_titles(self, titles):
        if self.titles is None:
            self.titles = {}
        for title in titles:
            self.add_title(title)

    def add_title(self, title):
        if self.titles is None:
            self.titles = {}
        self.titles[title.id] = title

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class TitleInfo:
    def __init__(self, name, id, year):
        self.name = name
        self.id = id
        self.year = year
        self.actors = None
        self.html = None

    def set_actors(self, actors):
        self.actors = {actor.id: actor for actor in actors}

    def add_actors(self, actors):
        if self.actors is None:
            self.actors = {}

        for actor in actors:
            self.add_actor(actor)

    def add_actor(self, actor_info):
        if self.actors is None:
            self.actors = {}
        self.actors[actor_info.id] = actor_info

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ActorTitleActorRelationship:
    def __init__(self, from_actor, to_actor, via_title, depth):
        self.from_actor = from_actor
        self.to_actor = to_actor
        self.via_title = via_title
        self.depth = depth
        #self.degree = degree
        self.key = '({}) {}.{}.{}'.format(self.depth, self.from_actor.id, self.via_title.id, self.to_actor.id)
        #self.key2 = self.to_actor.id + "." + self.via_title.id + "." + self.from_actor.id


    def __str__(self):
        return '({}): {} ==> {} ==> {}'.format(self.depth, self.from_actor.name, self.via_title.name, self.to_actor.name)

