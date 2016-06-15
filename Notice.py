from datetime import datetime
import pickle
import os


class NoticeBoard:
    file_name = 'data/NoticeBoard'

    @staticmethod
    def last_modified():
        try:
            return os.path.getmtime(NoticeBoard.file_name)
        except FileNotFoundError:
            return 0

    @staticmethod
    def get_board():
        try:
            with open(NoticeBoard.file_name, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            notice_board = NoticeBoard()
            NoticeBoard.write_board(notice_board)
            return notice_board

    @staticmethod
    def write_board(notice_board):
        if notice_board.changed:
            with open(NoticeBoard.file_name, "wb") as file:
                pickle.dump(notice_board, file)

    def __init__(self):
        self.queue = []
        self.all_ids = []
        self.completed = []
        self.changed = False

    def add(self, notice):
        if notice.notice_id not in self.all_ids:
            self.queue.append(notice)
            self.all_ids.append(notice.notice_id)
            self.changed = True

    def get(self):
        try:
            item = self.queue[0]
        except IndexError:
            return None
        new_queue = []
        for i in range(len(self.queue) - 1):
            new_queue.append(self.queue[i + 1])
        self.queue = new_queue
        self.completed.append(item)
        self.changed = True
        return item


class Notice:
    def __init__(self, id_notice='None', title='None', notice_type='None', date='None'):
        self.url = 'https://www.withhive.com/help/notice_view/'+id_notice
        self.notice_id = id_notice
        self.title = title
        self.notice_type = notice_type
        self.date = datetime.strptime(date, '%Y.%m.%d')

    def __eq__(self, other):
        if type(other) == type(self):
            if self.notice_id == other.notice_id:
                return True
        return False

    def __str__(self):
        return '**['+self.notice_type+']** '+self.title+' '+self.url

    def __repr__(self):
        return '['+self.notice_type+'] '+self.title+' '+self.url
