from transitions.extensions import GraphMachine
import requests
from bs4 import BeautifulSoup
import pandas
import datetime
import telegram
#from IPython.display import Image,display,display_png

class TocMachine(GraphMachine):
    city={'NewTaipei':'B01','Taipei':'A63','KH':'A64'}
    kind={'Dance':'B3','Drama':'B2','Movie':'B8','Music':['B0','B1','B4'],'Exhibit':['A0','A1','A2']} 
    time={'Morning':'12','Afternoon':'18','Evening':'24'}
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
    def get_bot(self,bot_in):
        self.bot=bot_in
        print(self.bot.get_me())
     
   # def show_graph(self,**kwargs):
   #     self.get_graph(**kwargs).draw('state.pdf',prog='dot')
   #     display(Image('state.pdf'))
    
        
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
            
    #-------------------onwork--------------------------
    def is_going_to_onwork(self, update):
        text = update.message.text
        return text.lower() == 'hi'
    def on_enter_onwork(self, update):
        update.message.reply_text("welcome , where do you want to go?")
    def on_exit_onwork(self, update):
        print('Leaving onwork')
        
    #-------------------------------------------------------------------------------NewTaipei-----------------------------------------------------------------------------
    def is_going_to_NewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'newtaipei'
    def on_enter_NewTaipei(self, update):
        update.message.reply_text("in NewTaipei , what kind of art would you like to join?")
    def on_exit_NewTaipei(self, update):
        print('Leaving NewTaipei')
    
    #----------------------------------------------------exhibit in NewTaipei------------------------------------------------
    def is_going_to_ExhibitInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'exhibit'
    def on_enter_ExhibitInNewTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_ExhibitInNewTaipei(self, update):
        print('Leaving ExhibitInNewTaipei')
        
    #join exhibit in NewTaipei on morning
    def is_going_to_MorningExhibitInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningExhibitInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Exhibit'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningExhibitInNewTaipei(self, update):
        print('Leaving MorningExhibitInNewTaipei')
        
    
    #join exhibit in NewTaipei on afternoon
    def is_going_to_AfternoonExhibitInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonExhibitInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Exhibit'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonExhibitInNewTaipei(self, update):
        print('Leaving AfternoonExhibitInNewTaipei')
        
    #join exhibit in NewTaipei on Evening
    def is_going_to_EveningExhibitInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningExhibitInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Exhibit'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningExhibitInNewTaipei(self, update):
        print('Leaving EveningExhibitInNewTaipei')
   
    #----------------------------------------------------dance in NewTaipei--------------------------------------------------------------
    def is_going_to_DanceInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'dance'
    def on_enter_DanceInNewTaipei(self, update):
        update.message.reply_text("when would you like")
    def on_exit_DanceInNewTaipei(self, update):
        print('Leaving DanceInNewTaipei')
        
    #join DanceInNewTaipei on morning
    def is_going_to_MorningDanceInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningDanceInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Dance'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningDanceInNewTaipei(self, update):
        print('Leaving MorningDanceInNewTaipei')
        
    #join DanceInNewTaipei on afternoon
    def is_going_to_AfternoonDanceInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonDanceInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Dance'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonDanceInNewTaipei(self, update):
        print('Leaving AfternoonDanceInNewTaipei')

        
    #join DanceInNewTaipei on Evening
    def is_going_to_EveningDanceInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningDanceInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Dance'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningDanceInNewTaipei(self, update):
        print('Leaving EveningDanceInNewTaipei')
      
    #------------------------------------------------Drama in NewTaipei---------------------------------------------------------------
    def is_going_to_DramaInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'drama'
    def on_enter_DramaInNewTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_DramaInNewTaipei(self, update):
        print('Leaving DramaInNewTaipei')
        
    #join DramaInNewTaipei on morning
    def is_going_to_MorningDramaInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningDramaInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Drama'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningDramaInNewTaipei(self, update):
        print('Leaving MorningDramaInNewTaipei')
      
        
    #join DramainNewTaipei on afternoon
    def is_going_to_AfternoonDramaInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonDramaInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Drama'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonDramaInNewTaipei(self, update):
        print('Leaving AfternoonDramaInNewTaipei')
        
    #join DramaInNewTaipei on Evening
    def is_going_to_EveningDramaInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningDramaInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Drama'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningDramaInNewTaipei(self, update):
        print('Leaving EveningDramaInNewTaipei')
    
    #-----------------------------------------------Music in NewTaipei------------------------------------------------------
    def is_going_to_MusicInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'music'
    def on_enter_MusicInNewTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_MusicInNewTaipei(self, update):
        print('Leaving MusicInNewTaipei')
        
    #join MusicInNewTaipei on morning
    def is_going_to_MorningMusicInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningMusicInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Music'],self.time['Morning'])
    def on_exit_MorningMusicInNewTaipei(self, update):
        print('Leaving MorningMusicInNewTaipei')
  
        
    #join MusicInNewTaipei on afternoon
    def is_going_to_AfternoonMusicInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonMusicInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Music'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonMusicInNewTaipei(self, update):
        print('Leaving AfternoonMusicInNewTaipei')
        
    #join MusicInNewTaipei on Evening
    def is_going_to_EveningMusicInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningMusicInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Music'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningMusicInNewTaipei(self, update):
        print('Leaving EveningMusicInNewTaipei')
       
    #----------------------------------------------Movie in NewTaipei--------------------------------------------------------
    def is_going_to_MovieInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'movie'
    def on_enter_MovieInNewTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_MovieInNewTaipei(self, update):
        print('Leaving MovieInNewTaipei')
        
    #join MovieInNewTaipei on morning
    def is_going_to_MorningMovieInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningMovieInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Movie'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningMovieInNewTaipei(self, update):
        print('Leaving MorningMovieInNewTaipei')
     
        
    #join MovieInNewTaipei on afternoon
    def is_going_to_AfternoonMovieInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonMovieInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Movie'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonMovieInNewTaipei(self, update):
        print('Leaving AfternoonMovieInNewTaipei')
 
        
    #join MovieInNewTaipei on Evening
    def is_going_to_EveningMovieInNewTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningMovieInNewTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['NewTaipei'],self.kind['Movie'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningMovieInNewTaipei(self, update):
        print('Leaving EveningMovieinNewTaipei')
    
    
    #-------------------------------------------------------------------------------Taipei-----------------------------------------------------------------------------
    def is_going_to_Taipei(self, update):
        text = update.message.text
        return text.lower() == 'taipei'
    def on_enter_Taipei(self, update):
        update.message.reply_text("in Taipei , what kind of art would you like to join?")
    def on_exit_Taipei(self, update):
        print('Leaving Taipei')
    
    #----------------------------------------------------exhibit in Taipei------------------------------------------------
    def is_going_to_ExhibitInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'exhibit'
    def on_enter_ExhibitInTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_ExhibitInTaipei(self, update):
        print('Leaving ExhibitInTaipei')
        
    #join exhibit in Taipei on morning
    def is_going_to_MorningExhibitInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningExhibitInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Exhibit'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningExhibitInTaipei(self, update):
        print('Leaving MorningExhibitInTaipei')
     
    
    #join exhibit in Taipei on afternoon
    def is_going_to_AfternoonExhibitInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonExhibitInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Exhibit'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonExhibitInTaipei(self, update):
        print('Leaving AfternoonExhibitInTaipei')
      
        
    #join exhibit in Taipei on Evening
    def is_going_to_EveningExhibitInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningExhibitInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Exhibit'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningExhibitInTaipei(self, update):
        print('Leaving EveningExhibitInTaipei')
      
    #----------------------------------------------------dance in Taipei--------------------------------------------------------------
    def is_going_to_DanceInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'dance'
    def on_enter_DanceInTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_DanceInTaipei(self, update):
        print('Leaving DanceInTaipei')
        
    #join DanceInTaipei on morning
    def is_going_to_MorningDanceInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningDanceInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Dance'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningDanceInTaipei(self, update):
        print('Leaving MorningDanceInTaipei')
      
        
    #join DanceInTaipei on afternoon
    def is_going_to_AfternoonDanceInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonDanceInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Dance'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonDanceInTaipei(self, update):
        print('Leaving AfternoonDanceInTaipei')
    
        
    #join DanceInTaipei on Evening
    def is_going_to_EveningDanceInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningDanceInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Dance'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningDanceInTaipei(self, update):
        print('Leaving EveningDanceInTaipei')
      
    #------------------------------------------------Drama in Taipei---------------------------------------------------------------
    def is_going_to_DramaInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'drama'
    def on_enter_DramaInTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_DramaInTaipei(self, update):
        print('Leaving DramaInTaipei')
        
    #join DramaInTaipei on morning
    def is_going_to_MorningDramaInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningDramaInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Drama'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningDramaInTaipei(self, update):
        print('Leaving MorningDramaInTaipei')
      
        
    #join DramainTaipei on afternoon
    def is_going_to_AfternoonDramaInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonDramaInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Drama'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonDramaInTaipei(self, update):
        print('Leaving AfternoonDramaInTaipei')
    
        
    #join DramaInTaipei on Evening
    def is_going_to_EveningDramaInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningDramaInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Drama'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningDramaInTaipei(self, update):
        print('Leaving EveningDramaInTaipei')
    
    
    #-----------------------------------------------Music in Taipei------------------------------------------------------
    def is_going_to_MusicInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'music'
    def on_enter_MusicInTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_MusicInTaipei(self, update):
        print('Leaving MusicInTaipei')
        
    #join MusicInTaipei on morning
    def is_going_to_MorningMusicInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningMusicInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Music'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningMusicInTaipei(self, update):
        print('Leaving MorningMusicInTaipei')
        
    #join MusicInTaipei on afternoon
    def is_going_to_AfternoonMusicInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonMusicInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Music'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonMusicInTaipei(self, update):
        print('Leaving AfternoonMusicInTaipei')
    
        
    #join MusicInTaipei on Evening
    def is_going_to_EveningMusicInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningMusicInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Music'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningMusicInTaipei(self, update):
        print('Leaving EveningMusicInTaipei')
      
    #----------------------------------------------Movie in Taipei--------------------------------------------------------
    def is_going_to_MovieInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'movie'
    def on_enter_MovieInTaipei(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_MovieInTaipei(self, update):
        print('Leaving MovieInTaipei')
        
    #join MovieInTaipei on morning
    def is_going_to_MorningMovieInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningMovieInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Movie'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningMovieInTaipei(self, update):
        print('Leaving MorningMovieInTaipei')
    
        
    #join MovieInTaipei on afternoon
    def is_going_to_AfternoonMovieInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonMovieInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Movie'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonMovieInTaipei(self, update):
        print('Leaving AfternoonMovieInTaipei')
        
        
    #join MovieInTaipei on Evening
    def is_going_to_EveningMovieInTaipei(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningMovieInTaipei(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['Taipei'],self.kind['Movie'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningMovieInTaipei(self, update):
        print('Leaving EveningMovienTaipei')
    
    
    #-------------------------------------------------------------------------------KH-----------------------------------------------------------------------------
    def is_going_to_KH(self, update):
        text = update.message.text
        return text.lower() == 'kh'
    def on_enter_KH(self, update):
        update.message.reply_text("in Kaousiung , what kind of art would you like to join?")
    def on_exit_KH(self, update):
        print('Leaving KH')
    
    #----------------------------------------------------exhibit in KH------------------------------------------------
    def is_going_to_ExhibitInKH(self, update):
        text = update.message.text
        return text.lower() == 'exhibit'
    def on_enter_ExhibitInKH(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_ExhibitInKH(self, update):
        print('Leaving ExhibitInKH')
        
    #join exhibit in KH on morning
    def is_going_to_MorningExhibitInKH(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningExhibitInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Exhibit'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningExhibitInKH(self, update):
        print('Leaving MorningExhibitInKH')
       
    
    #join exhibit in KH on afternoon
    def is_going_to_AfternoonExhibitInKH(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonExhibitInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Exhibit'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonExhibitInKH(self, update):
        print('Leaving AfternoonExhibitInKH')
     
        
    #join exhibit inKH on Evening
    def is_going_to_EveningExhibitInKH(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningExhibitInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Exhibit'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningExhibitInKH(self, update):
        print('Leaving EveningExhibitInKH')
       
    #----------------------------------------------------dance in KH--------------------------------------------------------------
    def is_going_to_DanceInKH(self, update):
        text = update.message.text
        return text.lower() == 'dance'
    def on_enter_DanceInKH(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_DanceInKH(self, update):
        print('Leaving DanceInKH')
        
    #join DanceInKH on morning
    def is_going_to_MorningDanceInKH(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningDanceInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Dance'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningDanceInKH(self, update):
        print('Leaving MorningDanceInKH')
        
    #join DanceInKH on afternoon
    def is_going_to_AfternoonDanceInKH(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonDanceInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Dance'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonDanceInKH(self, update):
        print('Leaving AfternoonDanceInKH')

        
    #join DanceInKH on Evening
    def is_going_to_EveningDanceInKH(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningDanceInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Dance'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningDanceInKH(self, update):
        print('Leaving EveningDanceInKH')
    
    #------------------------------------------------Drama in KH---------------------------------------------------------------
    def is_going_to_DramaInKH(self, update):
        text = update.message.text
        return text.lower() == 'drama'
    def on_enter_DramaInKH(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_DramaInKH(self, update):
        print('Leaving DramaInKH')
        
    #join DramaInKH on morning
    def is_going_to_MorningDramaInKH(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningDramaInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Drama'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningDramaInKH(self, update):
        print('Leaving MorningDramaInKH')
     
        
    #join DramainKH on afternoon
    def is_going_to_AfternoonDramaInKH(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonDramaInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Drama'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonDramaInKH(self, update):
        print('Leaving AfternoonDramaInKH')
    
        
    #join DramaInKH on Evening
    def is_going_to_EveningDramaInKH(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningDramaInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Drama'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningDramaInKH(self, update):
        print('Leaving EveningDramaInKH')
        self.go_back(update)
    
    #-----------------------------------------------Music in KH------------------------------------------------------
    def is_going_to_MusicInKH(self, update):
        text = update.message.text
        return text.lower() == 'music'
    def on_enter_MusicInKH(self, update):
        update.message.reply_text("when would you like?")
    def on_exit_MusicInKH(self, update):
        print('Leaving MusicInKH')
        
    #join MusicInKH on morning
    def is_going_to_MorningMusicInKH(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningMusicInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Music'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningMusicInKH(self, update):
        print('Leaving MorningMusicInKH')
     
        
    #join MusicInKH on afternoon
    def is_going_to_AfternoonMusicInKH(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonMusicInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Music'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonMusicInKH(self, update):
        print('Leaving AfternoonDramaInKH')

        
    #join MusicInKH on Evening
    def is_going_to_EveningMusicInKH(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningMusicInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Music'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningMusicInKH(self, update):
        print('Leaving EveningMusicInKH')
      
    #----------------------------------------------Movie in KH--------------------------------------------------------
    def is_going_to_MovieInKH(self, update):
        text = update.message.text
        return text.lower() == 'movie'
    def on_enter_MovieInKH(self, update):
        update.message.reply_text("when would you like ?")
        self.go_back(update)
    def on_exit_MovieInKH(self, update):
        print('Leaving DramaInKH')
        
    #join MovieInKH on morning
    def is_going_to_MorningMovieInKH(self, update):
        text = update.message.text
        return text.lower() == 'morning'
    def on_enter_MorningMovieInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Movie'],self.time['Morning'])
        self.go_back(update)
    def on_exit_MorningMovieInKH(self, update):
        print('Leaving MorningDanceInKH')
      
        
    #join MovieInKH on afternoon
    def is_going_to_AfternoonMovieInKH(self, update):
        text = update.message.text
        return text.lower() == 'afternoon'
    def on_enter_AfternoonMovieInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Movie'],self.time['Afternoon'])
        self.go_back(update)
    def on_exit_AfternoonMovieInKH(self, update):
        print('Leaving AfternoonMovieInKH')
  
        
    #join MovieInKH on Evening
    def is_going_to_EveningMovieInKH(self, update):
        text = update.message.text
        return text.lower() == 'evening'
    def on_enter_EveningMovieInKH(self, update):
        update.message.reply_text("please wait for a while")
        self.crawl(update,self.city['KH'],self.kind['Movie'],self.time['Evening'])
        self.go_back(update)
    def on_exit_EveningMovieInKH(self, update):
        print('Leaving EveningMovienKH')
 
    
    
    
    
        
    