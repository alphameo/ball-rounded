def merge_set(acceptor: set, donor: set) -> set:
    for item in donor:
        acceptor.add(item)

    return donor
