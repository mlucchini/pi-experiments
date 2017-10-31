class LogUserOnFaceRecognizedHandler:
    def __init__(self):
        pass

    @staticmethod
    def handle(user, location, frame):
        print('User recognized:')
        print('   %s with id %s' % (user['name'], user['id']))
