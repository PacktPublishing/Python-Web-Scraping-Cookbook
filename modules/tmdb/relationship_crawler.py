import tmdb.strategies
import tmdb.models
import tmdb

class RelationshipCrawler:
    def __init__(self,
                 start_actor_name, max_depth, max_titles_per_actor, max_actors_per_title,
                 max_total_actors, max_total_titles, max_actors_per_depth, max_titles_per_depth):
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
        self.start_actor = tmdb.strategies.get_actor_info_from_actor_name(self.start_actor_name)
        self.actors = {}
        self.titles = {}

        print("Starting with: %s" % self.start_actor.name)

        current_depth = 0

        actors_identified_at_next_depth = {}

        actors_to_process_at_current_depth = {}
        actors_to_process_at_current_depth[self.start_actor.id] = self.start_actor
        titles_processed_at_current_depth = {}

        while current_depth < self.max_depth:
            if len(self.titles) >= self.max_total_titles: break
            if len(self.actors) >= self.max_total_actors: break

            if len(actors_to_process_at_current_depth) == 0:
                actors_to_process_at_current_depth = actors_identified_at_next_depth
                titles_processed_at_current_depth.clear()
                current_depth += 1
                continue

            current_actor_id, current_actor = actors_to_process_at_current_depth.popitem()
            print("Examining: %s" % current_actor.name)

            self.actors[current_actor_id] = current_actor

            if current_actor.html is None:
                current_actor.html = tmdb.strategies.get_actor_page_html(current_actor_id)
            if current_actor.titles is None:
                current_actor.titles = {
                    a.id: a for a in tmdb.strategies.extract_acted_in_titles_from_actor_page_html(current_actor.html)
                }

            new_titles = [title for title in current_actor.titles.values() if title.id not in self.titles]

            title_trim = min(len(new_titles),
                             self.max_titles_per_actor,
                             self.max_titles_per_depth - len(titles_processed_at_current_depth),
                             self.max_total_titles - len(self.titles))

            titles_to_process_from_current_actor = new_titles[:title_trim]

            actors_identified_at_next_depth = {}

            # now loop through all these titles, identifying more actors
            while len(titles_to_process_from_current_actor) > 0:
                current_title = titles_to_process_from_current_actor.pop(0)

                print("Using title: %s" % current_title.name)
                titles_processed_at_current_depth[current_title.id] = current_title

                print("Getting actors from title: %s" % current_title.name)

                if current_title.html is None:
                    print("Loading content for title: %s" % current_title.id)
                    current_title.html = tmdb.strategies.get_cast_page_html(current_title.id)

                actors_in_current_title = tmdb.strategies.get_actors_for_title(current_title)
                new_actors = [actor for actor in actors_in_current_title if actor.id not in self.actors]

                actor_trim = min(len(new_actors),
                                 self.max_actors_per_title,
                                 self.max_total_actors - len(self.actors) - len(actors_identified_at_next_depth),
                                 self.max_actors_per_depth - len(actors_identified_at_next_depth))

                if actor_trim > 0:
                    self.titles[current_title.id] = current_title

                    actors_to_use = new_actors[:actor_trim]

                    relationships = [tmdb.models.ActorTitleActorRelationship(current_actor,
                                                                             related_actor,
                                                                             current_title,
                                                                             current_depth)
                                     for related_actor in actors_to_use]
                    for relationship in relationships:
                        print("Adding relationship: %s" % relationship)
                        self.relationships[relationship.key] = relationship
                        self.actors[relationship.to_actor.id] = relationship.to_actor
                        actors_identified_at_next_depth[relationship.to_actor.id] = relationship.to_actor

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
            actor.html = tmdb.strategies.get_actor_page_html(actor.id)

        titles = tmdb.strategies.extract_acted_in_titles_from_actor_page_html(actor.html)

        filtered_titles = []
        index = 0
        while index < len(titles) and index < self.max_titles_per_actor and \
                        (len(self.titles) + index) < self.max_total_titles:
            filtered_titles.append(titles[index])
            index += 1

        actor.set_titles(filtered_titles)
