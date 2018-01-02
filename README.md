# chatbot
## How to run?(linux環境下) ##
1. cmdline 執行 ./ngrok http 5000
2. 複製https網址
3. 修改art.py內的WEBHOOK_URL，和其他需要網址的部分
4. 儲存修改
5. 執行 python3 art.py 
## How to interact? ##
1. bot的初始狀態為idle
2. user輸入字串來換醒bot
3. bot狀態由idle轉換到onwork
4. bot會問
