from climate import model, adapter


def channels():
    return [c.name.lower() for c in adapter.Channel]