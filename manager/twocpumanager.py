from .attendmanager import AttendManager
import urllib
import datetime
import random


class TwoCPUManager(AttendManager):
    def __init__(self, username, password, login_url, attend_url, comment):
        super().__init__(username=username, password=password, login_url=login_url,
                         attend_url=attend_url, comment=comment)

    def login(self, encoding='utf-8'):
        try:
            headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'url': 'http://www.2cpu.co.kr', 'mb_id': self.username, 'mb_password': self.password}

            response = self.send_request(url=self.login_url, headers=headers, data=data, encoding=encoding)
            self.make_cookie(response.info().items())
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
            return False
        else:
            return True

    def check_attend(self, encoding='utf-8'):
        try:
            s_date = datetime.date.today().isoformat()
            current_id = ''
            at_type = str(random.randrange(1, 4))
            at_memo = self.comment

            # check attendadnce
            headers = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded',
                       'Cookie': self.cookie}
            data = {'s_date': s_date, 'currentId': current_id, 'at_type': at_type, 'at_memo': at_memo}
            response = self.send_request(url=self.attend_url, headers=headers, data=data, encoding=encoding)
            content = response.read().decode(encoding)

            if content.find('포인트 획득') < 0:
                return False

        except (urllib.error.URLError, urllib.error.HTTPError, IndexError, ValueError):
            return False
        else:
            return True
