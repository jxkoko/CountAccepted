import requests
import time
from bs4 import BeautifulSoup as bs4

class User:
    archive = 'https://atcoder.jp/contests/archive?lang=ja&page='
    def __init__(self,user):
        self.user = user
    
    def get_soup(self,url):
        res = requests.get(url)
        return bs4(res.content,'lxml')
    
    def count_accepted(self):
        ac = 0
        roop = 0
        page = 1
        while roop <= 20:
            roop = roop + 1
            soup = self.get_soup(User.archive + str(page))
            page = page + 1
            contests = []
            try:
                contests = soup.find(
                    class_="table table-default table-striped table-hover table-condensed table-bordered small"
                ).tbody('tr')
            except AttributeError:
                pass
            
            cnt = 0
            for contest in contests:
                if cnt == 10:
                    break
                submission_page = 'https://atcoder.jp'
                submission_page += contest('td')[1].a.get('href')
                submission_page +=  f'/submissions?f.Task=&f.Language=&f.Status=AC&f.User={self.user}'
                print(submission_page)
                soup = self.get_soup(submission_page)
                table = soup.find(
                    class_="table table-bordered table-striped small th-center"
                )

                try:
                    submissions = table.tbody('tr')
                except AttributeError:
                    pass
                else:
                    problems = set()
                    for submission in submissions:
                        problems.add(submission('td')[1].a.get('href'))

                ac = ac + len(problems)
                cnt = cnt + 1
                time.sleep(1)
            
        return ac

def main():
    name = input('ユーザー名を入力して下さい : ')
    user = User(name)
    t1 = time.time()
    ac = user.count_accepted()
    t2 = time.time()
    dt = t2 - t1
    print(f'実行時間：{dt}')
    print(f'AC数 : {ac}')

main()