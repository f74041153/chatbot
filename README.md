# chatbot
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

