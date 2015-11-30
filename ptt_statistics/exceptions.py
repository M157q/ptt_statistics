class NoBoardError(Exception):
    def __init__(self, board_name):
        self.board_name = board_name

    def __str__(self):
        return "Board '{}' not found in db.".format(self.board_name)
