class Vertex(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<Vertex {}>'.format(self.name)
