debug = False

def current_parents(ancestors, target):
    parents = []
    for parent, child in ancestors:
        if child == target:
            parents.append(parent)
    if debug: print(f"current_parents for person {target}: {parents}")
    return parents

def recursive_parent_traversal(ancestors, start, distance):
    oldest_ancestor = (start, distance)
    if debug: print(f"recursive_parent_traversal, oldest_ancestor: {oldest_ancestor}")

    parents = current_parents(ancestors, start)

    for parent in parents:
        target = recursive_parent_traversal(ancestors, parent, distance + 1)
        if debug: print(f"parent: {parent}, target: {target}, further: {target[1] > distance}")
        if target[1] > oldest_ancestor[1]:
            oldest_ancestor = target

    return oldest_ancestor

def earliest_ancestor(ancestors, starting_node):
    # input is array of tuples
    # each tuple contains 2 positive integers
    # First integer is parent, 2nd is child
    # traverse from input child to parent until no more parents to find earliest ancestor
    # if no result, return -1

    if debug: print(f"earliest_ancestor, starting at {starting_node}")

    elder = recursive_parent_traversal(ancestors, starting_node, 0)
    if debug: print(f"elder: {elder}")

    if elder[0] == starting_node: return -1

    return elder[0]


if debug:
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    print(earliest_ancestor(test_ancestors, 1), 10)
    print(earliest_ancestor(test_ancestors, 2), -1)
    print(earliest_ancestor(test_ancestors, 3), 10)
    print(earliest_ancestor(test_ancestors, 4), -1)
    print(earliest_ancestor(test_ancestors, 5), 4)
    print(earliest_ancestor(test_ancestors, 6), 10)
    print(earliest_ancestor(test_ancestors, 7), 4)
    print(earliest_ancestor(test_ancestors, 8), 4)
    print(earliest_ancestor(test_ancestors, 9), 4)
    print(earliest_ancestor(test_ancestors, 10), -1)
    print(earliest_ancestor(test_ancestors, 11), -1)
