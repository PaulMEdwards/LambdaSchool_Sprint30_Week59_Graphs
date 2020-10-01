debug = False
trace = False

import random
from util import Stack, Queue  # These may come in handy

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
            if trace: print(f"self.friendships[user_id={user_id}].add(friend_id={friend_id})")
            self.friendships[user_id].add(friend_id)
            if trace: print(f"self.friendships[friend_id={friend_id}].add(user_id={user_id})")
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
            if trace: print(f"call add_user({i})")
            self.add_user(i)

        if trace: print(f"users: {self.users}")

        total_friendships = num_users * avg_friendships
        if debug: print(f"total_friendships = {total_friendships}")

        combinations = []
        for x in range(num_users):
            for y in range(num_users):
                if x != y:
                    combinations.append((x, y))

        if trace: print(f"combinations ({len(combinations)}):\n{combinations}")

        random.shuffle(combinations)
        if trace: print(f"combinations shuffled:\n{combinations}")

        combinations = combinations[:total_friendships]
        if trace: print(f"final {len(combinations)} combinations:\n{combinations}")

        friendships_made = 0
        for c in combinations:
            user_id = c[0]
            friend_id = c[1]
            if friend_id > user_id:
                if trace: print(f"call add_friendship(user_id={user_id}, friend_id={friend_id})")
                self.add_friendship(user_id, friend_id)
                friendships_made += 2
            if friendships_made >= total_friendships: break

        if debug: print(f"friendships: {self.friendships}")


    def user_network(self, network, user):
        if trace: print(f"user_network for user: {user}\n\t{network}")
        connections = []
        for connection in network[user]:
            if trace: print(f"connection: {connection}")
            connections.append(connection)
        if debug: print(f"connections for user {user}: {connections}")
        return connections

    def bfs(self, starting_user, destination_user):
        """
        Return a list containing the shortest path from
        starting_user to destination_user in
        breath-first order.
        """
        q = Queue()
        visited = set()

        q.enqueue(starting_user)

        while q.size() > 0:
            if trace: print(f"Queue:\t\t{q}")
            current_path = q.dequeue()
            if trace: print(f"current_path\t{current_path}")
            if isinstance(current_path, list):
                current_user = current_path[-1]
            elif isinstance(current_path, int):
                current_user = current_path

            if trace: print(f"current_user\t{current_user}\tdestination_user\t{destination_user}")
            if current_user == destination_user:
                if debug: print(f"current_path:\t{current_path}")
                if isinstance(current_path, list):
                    return current_path
                else:
                    return [current_path]

            if current_user not in visited:
                visited.add(current_user)

                user_network = self.user_network(self.friendships, current_user)
                if trace: print(f"user_network\t{user_network}")

                for user in user_network:
                    if isinstance(current_path, list):
                        path_copy = current_path + [user]
                    elif isinstance(current_path, int):
                        path_copy = []
                        path_copy.append(current_path)
                        path_copy.append(user)
                    if trace: print(f"path_copy\t{path_copy}")
                    q.enqueue(path_copy)

        if debug: print(f"q: {q}")
        if q.size() == 1:
            return [q]
        if q.size() > 1:
            return q
        else:
            return None


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        if debug: print(f"get_all_social_paths({user_id})")

        visited = {}  # Note that this is a dictionary, not a set

        for f in self.friendships:
            if trace: print(f"f: {f}")
            v = self.bfs(user_id, f)
            if v: visited[f] = v

        if debug: print(f"visited: {visited}")
        return visited


def calculate_network_percentage(network, connections, num_users):
    count = 0

    for user in network.users:
        if user in connections.keys():
            count += 1

    percentage = (count / num_users) * 100
    if debug: print(f"percentage: {percentage}%")
    return percentage


def calculate_average_degrees_of_separation(network, connections):
    # length of users path to another user is the degree of separation
    friend_count = 0
    degrees = 0

    for user in connections:
        # add to friend count
        friend_count += 1
        if debug: print(f"friend_count = {friend_count}")
        # add degree of separation
        degrees += len(connections[user]) - 1
        if debug: print(f"degrees = {degrees}")

    # divide total degrees of separation by the number of user connections
    average = degrees / friend_count
    if debug: print(f"average = {average}")
    return average


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print("Friendships:", sg.friendships)
    connections = sg.get_all_social_paths(0)
    print("Connections:", connections)

    # To answer README question 2
    sg = SocialGraph()
    total_users = 1000
    average_friends = 5
    sg.populate_graph(total_users, average_friends)
    r = random.randint(0, 999)
    connections = sg.get_all_social_paths(r)
    np = calculate_network_percentage(sg, connections, total_users)
    ads = calculate_average_degrees_of_separation(sg, connections)

    print(f"Network Percentage of user # {r} out of {total_users} users: {round(np, 1)}%")
    print(f"Average degree of separation in user # {r}'s network: {round(ads, 2)}")
