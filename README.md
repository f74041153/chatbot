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
