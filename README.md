# chatbot
## 狀態圖 ##
![Alt text]state_diagram.jpg
## How to run?(linux環境下) ##
1. cmdline 執行 ./ngrok http 5000
2. 複製https網址
3. 修改art.py內的WEBHOOK_URL，和其他需要網址的部分
4. 儲存修改
5. 執行 python3 art.py 
## How to interact? ##
1. 以"hi"字串喚醒bot
2. 回答目標地，"newtaipei"/"taipei"/"kh"輸入字串擇一
3. 回答活動類型，"exhibit"/"music"/"drama"/"dance"/"movie"輸入字串擇一
4. 回答時段，"morning"/"afternoon"/"evening"輸入字串擇一
5. bot會根據user輸入的地點類型時段，回傳當日符合要求的活動
6. user可收到所要資料和詳細資訊的連結
## 功能說明 ##
* 為user到文化部全國藝文活動資訊網抓取所要資料
* 並回傳符合資料和詳細資訊連結
## 程式說明 ##
* 在fsm.py內的爬蟲程式

        def crawl(self,update,city,kind,time):
            chat_id=update.message.chat_id
            i=datetime.datetime.now()
            date_start=str(i.year)+'/'+str(i.month)+'/'+str(i.day)
            date_end=date_start
            page=1;
            try:
                msg=''
                page=1;
                while(1):
                    url='http://event.moc.gov.tw/sp.asp'
                    headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0','Connection':'keep-alive'}
                    params={'xdurl':'ccEvent2016/eventSearchList.asp','ctNode':'676','mp':'1','action':'query','stitle':'','ev_place':'','ev_start_m':'','ev_start':date_start,'ev_end_m':'','ev_end':date_end,'ev_city':city,'ev_format':'all','ev_char1':kind,'Search':'查詢','currentPage':page}
                    response=requests.get(url=url,params=params,headers=headers)

                    response.encoding='utf-8'
                    html=response.text

                    soup = BeautifulSoup(html,'html.parser')
                    for idx,tr in enumerate(soup.find_all('tr')):
                        if idx!=0:
                            tds=tr.find_all('td')
                            time_list=tds[1].contents[0].split()
                            start_time=int((time_list[1].split(":"))[0])
                            end_time=int((time_list[4].split(":"))[0])
                            if start_time<int(time) and end_time>int(time):
                                if tr.find('a'):
                                    href=tr.find('a')['href']
                                    url="http://event.moc.gov.tw/"+str(href)
                                    details="[details]("+url+")"
                                    msg=msg+tr.find('a').string.strip()+details+"\n"
                    if len(soup.select('.next'))>0:
                        page=page+1
                    else:
                        break
                if msg=='':
                    print("nothing")
                    update.message.reply_text("sorry , no match for you!")
                else:
                    print(msg)
                    self.bot.send_message(chat_id=chat_id,text=msg,parse_mode=telegram.ParseMode.MARKDOWN)
                update.message.reply_text("see you next time!")
            except:
                print("error")
