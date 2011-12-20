def pairlist_to_tree(pairlist):
    num_parents = {}  # element -> # of predecessors 
    children = {}  # element -> list of successors 
    for parent, child in pairlist: 
        # Make sure every element is a key in num_parents.
        if not num_parents.has_key( parent ): 
            num_parents[parent] = 0 
        if not num_parents.has_key( child ): 
            num_parents[child] = 0 

        # Since child has a parent, increment child's num_parents count.
        num_parents[child] += 1

        # ... and parent gains a child.
        children.setdefault(parent, []).append(child)
    return num_parents, children

def find_trees(pairlist):
    # Given a list of [(parent1, child1), (parent2, child2)...]
    # Return a dictionary of {rootOfTree1: iterator(tree1Node1, tree1Node2...), rootOfTree2:...}
    num_parents, children = pairlist_to_tree(pairlist)

    def find_tree_nodes(root, nodes = set()):
        if root not in nodes:
            nodes.add(root)
            yield root
            if root in children:
                for child in children[root]:
                    for node in find_tree_nodes(child, nodes):
                        yield node
    
    return dict((node, find_tree_nodes(node))
                for node in num_parents.keys()
                if num_parents[node] == 0)
