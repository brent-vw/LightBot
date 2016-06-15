from urllib import request
import json
from Notice import NoticeBoard
from Notice import Notice


class LightCafeParser:
    url = 'https://www.withhive.com/api/help/notice_list/1'
    game = 'Light: Fellowship of Loux'

    @staticmethod
    def get_notices():
        with request.urlopen(LightCafeParser.url) as response:
            raw = response.read().decode('UTF-8')
        data = json.loads(str(raw))
        notices = data['result']
        b = NoticeBoard.get_board()
        for notice in notices:
            if notice['GameName'] == LightCafeParser.game:
                item = Notice(id_notice=notice['NoticeId'], title=notice['Title'],
                              notice_type=notice['TypeString'], date=notice['ModifyTime_Ymd'])
                b.add(item)
        NoticeBoard.write_board(b)
