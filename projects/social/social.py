debug = True

import random

class User:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            if debug: print(f"self.friendships[user_id={user_id}].add(friend_id={friend_id})")
            self.friendships[user_id].add(friend_id)
            if debug: print(f"self.friendships[friend_id={friend_id}].add(user_id={user_id})")
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = -1
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(num_users):
            if debug: print(f"call add_user({i})")
            self.add_user(i)

        if debug: print(f"users: {self.users}")

        # Create friendships
        #   You could create a list with all possible friendship combinations,
        #       [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
        #   shuffle the list,
        #   then grab the first N elements from the list.

        total_friendships = num_users * avg_friendships
        if debug: print(f"total_friendships = {total_friendships}")

        combinations = []
        for x in range(num_users):
            for y in range(num_users):
                if x != y:
                    combinations.append((x, y))

        if debug: print(f"combinations ({len(combinations)}):\n{combinations}")

        random.shuffle(combinations)
        if debug: print(f"combinations shuffled:\n{combinations}")

        for z in range(total_friendships):
            user_id = combinations[z][0]
            friend_id = combinations[z][1]
            if friend_id > user_id:
                if debug: print(f"call add_friendship(user_id={user_id}, friend_id={friend_id})")
                self.add_friendship(user_id, friend_id)

        if debug: print(f"friendships: {self.friendships}")

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # TODO !!!! IMPLEMENT ME
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
