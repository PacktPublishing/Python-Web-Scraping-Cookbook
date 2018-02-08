import imdb.strategies
import imdb.models
import imdb

class ImdbRelationshipCrawler:
    def __init__(self,
                 start_actor_name, max_depth, max_titles_per_actor, max_actors_per_title, max_total_actors,
                 max_total_titles, max_actors_per_depth, max_titles_per_depth):
        self.start_actor_name = start_actor_name
        self.max_depth = max_depth
        self.max_titles_per_actor = max_titles_per_actor
        self.max_actors_per_title = max_actors_per_title
        self.max_total_actors = max_total_actors
        self.max_total_titles = max_total_titles
        self.max_actors_per_depth = max_actors_per_depth
        self.max_titles_per_depth = max_titles_per_depth
        self.actors = {}
        self.titles = {}
        self.relationships = {}
        self.start_actor = None

    def crawl(self):
        self.start_actor = imdb.strategies.get_actor_info_from_actor_name(self.start_actor_name)
        actors_at_current_depth = {}
        actors_at_current_depth[self.start_actor.id] = self.start_actor

        print("Starting with: %s" % self.start_actor.name)

        current_depth = 0

        found_titles = {}

        actors_to_process = {}
        actors_to_process[self.start_actor.id] = self.start_actor

        actors_at_next_depth = {}
        titles_at_current_depth = {}
        titles_to_process_from_current_actor = {}

        while current_depth <= self.max_depth and len(actors_at_current_depth):
            current_actor_id, current_actor = actors_at_current_depth.popitem()
            print("checking out: {}".format(current_actor.name))

            self.actors[current_actor_id] = current_actor

            if current_actor.html is None:
                current_actor.html = imdb.strategies.get_actor_page_html(current_actor_id)
            if current_actor.titles is None:
                titles_for_current_actor = { a.id:a for a in imdb.strategies.extract_acted_in_titles_from_actor_page_html(current_actor.html)}
            else:
                titles_for_current_actor = current_actor.titles

            titles_to_process_from_current_actor.clear()

            while len(titles_for_current_actor) > 0 and len(found_titles) + len(self.titles) < self.max_total_titles:
                current_title_id, current_title = titles_for_current_actor.popitem()

                print("Examining title: {}".format(current_title.name))

                if current_title_id in found_titles or current_title_id in self.titles:
                    print("Skipping title as already processed")
                    continue

                if len(titles_to_process_from_current_actor) >= self.max_titles_per_actor:
                    print('Breaking as reached max titles per actor')
                    break

                if len(titles_at_current_depth) >= self.max_titles_per_depth:
                    print('Breaking as reached max titles per depth')
                    break

                print("Using title: {}".format(current_title.name))

                found_titles[current_title_id] = current_title
                titles_at_current_depth[current_title_id] = current_title
                titles_to_process_from_current_actor[current_title_id] = current_title

            # process found titles for this actor for related actors
            while (len(titles_to_process_from_current_actor) > 0):
                current_title_id, current_title = titles_to_process_from_current_actor.popitem()

                print("Processing title for actors ({}): {}".format(current_actor.name, current_title.name))

                if current_title.html is None:
                    current_title.html = imdb.strategies.get_title_page_html(current_title_id)
                actors_in_current_title = imdb.strategies.get_actors_for_title(current_title)

                actors_found_in_title = {}
                while (len(actors_in_current_title) > 0):
                    related_actor = actors_in_current_title.pop(0)
                    print('Examining actor in title ({}): {}'.format(current_title.name, related_actor.name))

                    if (related_actor.id in self.actors):
                        print('Actor already processed, continuing: {}'.format(related_actor.name))
                        continue

                    if len(actors_found_in_title) >= self.max_actors_per_title:
                        print("breaking on # of actors per title exceeded")
                        break

                    if len(self.actors) + len(actors_found_in_title) + 1 >= self.max_total_actors:
                        print("Found total # of actors, breaking")
                        break

                    if len(actors_at_next_depth) >= self.max_actors_per_depth:
                        print("Found max actors at 'next' depth: {}".format(current_depth))
                        break

                    print("{} ==> {}".format(current_title.name, related_actor.name))
                    actors_found_in_title[related_actor.id] = related_actor
                    actors_at_next_depth[related_actor.id] = related_actor

                    relationship = imdb.models.ActorTitleActorRelationship(current_actor, related_actor, current_title, current_depth)
                    print("Adding relationship: {}".format(relationship))
                    self.relationships[relationship.key] = relationship

                    # record these in our actors and titles result set
                    self.actors[related_actor.id] = related_actor
                    self.titles[current_title.id] = current_title

            # if no more actors at the current depth, and we go another depth level,
            if len(actors_at_current_depth) == 0 and current_depth + 1 < self.max_depth:
                # then lets process actors at the next depth
                for actor in actors_at_next_depth.values():
                    actors_at_current_depth[actor.id] = actor

                actors_at_next_depth.clear()
                titles_at_current_depth.clear()

                current_depth += 1

        print("done crawl")

    def distinct_actors_in_relationships(self):
        actors = {}
        for relationship in self.relationships.values():
            if relationship.from_actor.id not in actors:
                actors[relationship.from_actor.id] = relationship.from_actor
            if relationship.to_actor.id not in actors:
                actors[relationship.to_actor.id] = relationship.to_actor
        return actors


    def distinct_titles_in_relationships(self):
        titles = {}
        for relationship in self.relationships.values():
            if relationship.via_title.id not in titles:
                titles[relationship.via_title.id] = relationship.via_title
        return titles


    def get_titles_for_actor(self, actor):
        # if we don't have titles for this actor yet, then get them
        if actor.html is None:
            actor.html = imdb.strategies.get_actor_page_html(actor.id)

        titles = imdb.strategies.extract_acted_in_titles_from_actor_page_html(actor.html)

        filtered_titles = []
        index = 0
        while index < len(titles) and index < self.max_titles_per_actor and \
                        (len(self.titles) + index) < self.max_total_titles:
            filtered_titles.append(titles[index])
            index += 1

        actor.set_titles(filtered_titles)
