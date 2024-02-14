from tkinter import *
import requests
class UpbitApp:
    def __init__(self, app):
        self.app = app
        self.app.title("Upbit Market Info")
        self.market_list = Listbox(app, width=50, height=20)
        self.market_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.market_list.bind("<<ListboxSelect>>", self.select_market)
        self.detail_text = Text(app, width=50, height=20)
        self.detail_text.pack(side=RIGHT, fill=BOTH, expand=True)
        self.load_market()
    def load_market(self):
        url = "http://api.upbit.com/v1/market/all"
        res = requests.get(url)
        if res.status_code == 200:
            obj = res.json()
            for v in obj:
                self.market_list.insert(END, v['market'])
    def select_market(self, event):
        selection = event.widget.curselection()
        if selection:
            idx = selection[0]
            market_code = event.widget.get(idx)
            detail_url = ("https://api.upbit.com/v1/ticker?markets="
                          + market_code)
            res = requests.get(detail_url)
            if res.status_code == 200:
                details = res.json()[0]
                # 이전 내용 삭제
                self.detail_text.delete(1.0, END)
                # 선택 상세내용 출력
                for key, val in details.items():
                    self.detail_text.insert(END, f"{key}:{val}\n")


if __name__ == '__main__':
    app = Tk()
    my_app = UpbitApp(app)
    app.mainloop()
