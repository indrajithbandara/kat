def find(predicate, collection):
    for item in collection:
        if predicate(collection):
            return item
    return None


def find_all(predicate, collection):
    for item in collection:
        if predicate(collection):
            yield item
