import sys
import pandas
from io import BytesIO
import cairosvg
import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN ='461048831:AAFeDa2_qFiUO7nUvOf-7tDdrLjK148RW4w'
WEBHOOK_URL ='https://9d85bc06.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=['idle','onwork','NewTaipei','ExhibitInNewTaipei','MorningExhibitInNewTaipei','AfternoonExhibitInNewTaipei','EveningExhibitInNewTaipei'
                                        ,'DanceInNewTaipei','MorningDanceInNewTaipei','AfternoonDanceInNewTaipei','EveningDanceInNewTaipei'
                                        ,'DramaInNewTaipei','MorningDramaInNewTaipei','AfternoonDramaInNewTaipei','EveningDramaInNewTaipei'
                                        ,'MusicInNewTaipei','MorningMusicInNewTaipei','AfternoonMusicInNewTaipei','EveningMusicInNewTaipei'
                                        ,'MovieInNewTaipei','MorningMovieInNewTaipei','AfternoonMovieInNewTaipei','EveningMovieInNewTaipei'
                               ,'Taipei','ExhibitInTaipei','MorningExhibitInTaipei','AfternoonExhibitInTaipei','EveningExhibitInTaipei'
                                        ,'DanceInTaipei','MorningDanceInTaipei','AfternoonDanceInTaipei','EveningDanceInTaipei'
                                        ,'DramaInTaipei','MorningDramaInTaipei','AfternoonDramaInTaipei','EveningDramaInTaipei'
                                        ,'MusicInTaipei','MorningMusicInTaipei','AfternoonMusicInTaipei','EveningMusicInTaipei'
                                        ,'MovieInTaipei','MorningMovieInTaipei','AfternoonMovieInTaipei','EveningMovieInTaipei'
         		                          ,'KH','ExhibitInKH','MorningExhibitInKH','AfternoonExhibitInKH','EveningExhibitInKH'
                                        ,'DanceInKH','MorningDanceInKH','AfternoonDanceInKH','EveningDanceInKH'
                                        ,'DramaInKH','MorningDramaInKH','AfternoonDramaInKH','EveningDramaInKH'
                                        ,'MusicInKH','MorningMusicInKH','AfternoonMusicInKH','EveningMusicInKH'
                                        ,'MovieInKH','MorningMovieInKH','AfternoonMovieInKH','EveningMovieInKH'],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'idle',
            'dest': 'onwork',
            'conditions': 'is_going_to_onwork'
        },
        {
            'trigger': 'advance',
            'source': 'onwork',
            'dest': 'NewTaipei',
            'conditions': 'is_going_to_NewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'NewTaipei',
            'dest': 'ExhibitInNewTaipei',
            'conditions': 'is_going_to_ExhibitInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInNewTaipei',
            'dest': 'MorningExhibitInNewTaipei',
            'conditions': 'is_going_to_MorningExhibitInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInNewTaipei',
            'dest': 'AfternoonExhibitInNewTaipei',
            'conditions': 'is_going_to_AfternoonExhibitInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInNewTaipei',
            'dest': 'EveningExhibitInNewTaipei',
            'conditions': 'is_going_to_EveningExhibitInNewTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningExhibitInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonExhibitInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningExhibitInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'NewTaipei',
            'dest': 'DanceInNewTaipei',
            'conditions': 'is_going_to_DanceInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInNewTaipei',
            'dest': 'MorningDanceInNewTaipei',
            'conditions': 'is_going_to_MorningDanceInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInNewTaipei',
            'dest': 'AfternoonDanceInNewTaipei',
            'conditions': 'is_going_to_AfternoonDanceInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInNewTaipei',
            'dest': 'EveningDanceInNewTaipei',
            'conditions': 'is_going_to_EveningDanceInNewTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningDanceInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonDanceInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningDanceInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'NewTaipei',
            'dest': 'DramaInNewTaipei',
            'conditions': 'is_going_to_DramaInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInNewTaipei',
            'dest': 'MorningDramaInNewTaipei',
            'conditions': 'is_going_to_MorningDramaInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInNewTaipei',
            'dest': 'AfternoonDramaInNewTaipei',
            'conditions': 'is_going_to_AfternoonDramaInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInNewTaipei',
            'dest': 'EveningDramaInNewTaipei',
            'conditions': 'is_going_to_EveningDramaInNewTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningDramaInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonDramaInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningDramaInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'NewTaipei',
            'dest': 'MusicInNewTaipei',
            'conditions': 'is_going_to_MusicInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInNewTaipei',
            'dest': 'MorningMusicInNewTaipei',
            'conditions': 'is_going_to_MorningMusicInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInNewTaipei',
            'dest': 'AfternoonMusicInNewTaipei',
            'conditions': 'is_going_to_AfternoonMusicInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInNewTaipei',
            'dest': 'EveningMusicInNewTaipei',
            'conditions': 'is_going_to_EveningMusicInNewTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningMusicInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonMusicInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningMusicInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'NewTaipei',
            'dest': 'MovieInNewTaipei',
            'conditions': 'is_going_to_MovieInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInNewTaipei',
            'dest': 'MorningMovieInNewTaipei',
            'conditions': 'is_going_to_MorningMovieInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInNewTaipei',
            'dest': 'AfternoonMovieInNewTaipei',
            'conditions': 'is_going_to_AfternoonMovieInNewTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInNewTaipei',
            'dest': 'EveningMovieInNewTaipei',
            'conditions': 'is_going_to_EveningMovieInNewTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningMovieInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonMovieInNewTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningMovieInNewTaipei',
            'dest': 'idle'
        }		,{
            'trigger': 'advance',
            'source': 'onwork',
            'dest': 'Taipei',
            'conditions': 'is_going_to_Taipei'
        },
        {
            'trigger': 'advance',
            'source': 'Taipei',
            'dest': 'ExhibitInTaipei',
            'conditions': 'is_going_to_ExhibitInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInTaipei',
            'dest': 'MorningExhibitInTaipei',
            'conditions': 'is_going_to_MorningExhibitInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInTaipei',
            'dest': 'AfternoonExhibitInTaipei',
            'conditions': 'is_going_to_AfternoonExhibitInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInTaipei',
            'dest': 'EveningExhibitInTaipei',
            'conditions': 'is_going_to_EveningExhibitInTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningExhibitInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonExhibitInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningExhibitInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'Taipei',
            'dest': 'DanceInTaipei',
            'conditions': 'is_going_to_DanceInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInTaipei',
            'dest': 'MorningDanceInTaipei',
            'conditions': 'is_going_to_MorningDanceInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInTaipei',
            'dest': 'AfternoonDanceInTaipei',
            'conditions': 'is_going_to_AfternoonDanceInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInTaipei',
            'dest': 'EveningDanceInTaipei',
            'conditions': 'is_going_to_EveningDanceInTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningDanceInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonDanceInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningDanceInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'Taipei',
            'dest': 'DramaInTaipei',
            'conditions': 'is_going_to_DramaInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInTaipei',
            'dest': 'MorningDramaInTaipei',
            'conditions': 'is_going_to_MorningDramaInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInTaipei',
            'dest': 'AfternoonDramaInTaipei',
            'conditions': 'is_going_to_AfternoonDramaInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInTaipei',
            'dest': 'EveningDramaInTaipei',
            'conditions': 'is_going_to_EveningDramaInTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningDramaInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonDramaInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningDramaInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'Taipei',
            'dest': 'MusicInTaipei',
            'conditions': 'is_going_to_MusicInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInTaipei',
            'dest': 'MorningMusicInTaipei',
            'conditions': 'is_going_to_MorningMusicInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInTaipei',
            'dest': 'AfternoonMusicInTaipei',
            'conditions': 'is_going_to_AfternoonMusicInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInTaipei',
            'dest': 'EveningMusicInTaipei',
            'conditions': 'is_going_to_EveningMusicInTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningMusicInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonMusicInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningMusicInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'Taipei',
            'dest': 'MovieInTaipei',
            'conditions': 'is_going_to_MovieInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInTaipei',
            'dest': 'MorningMovieInTaipei',
            'conditions': 'is_going_to_MorningMovieInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInTaipei',
            'dest': 'AfternoonMovieInTaipei',
            'conditions': 'is_going_to_AfternoonMovieInTaipei'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInTaipei',
            'dest': 'EveningMovieInTaipei',
            'conditions': 'is_going_to_EveningMovieInTaipei'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningMovieInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonMovieInTaipei',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningMovieInTaipei',
            'dest': 'idle'
        }		,{
            'trigger': 'advance',
            'source': 'onwork',
            'dest': 'KH',
            'conditions': 'is_going_to_KH'
        },
        {
            'trigger': 'advance',
            'source': 'KH',
            'dest': 'ExhibitInKH',
            'conditions': 'is_going_to_ExhibitInKH'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInKH',
            'dest': 'MorningExhibitInKH',
            'conditions': 'is_going_to_MorningExhibitInKH'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInKH',
            'dest': 'AfternoonExhibitInKH',
            'conditions': 'is_going_to_AfternoonExhibitInKH'
        },
        {
            'trigger': 'advance',
            'source': 'ExhibitInKH',
            'dest': 'EveningExhibitInKH',
            'conditions': 'is_going_to_EveningExhibitInKH'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningExhibitInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonExhibitInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningExhibitInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'KH',
            'dest': 'DanceInKH',
            'conditions': 'is_going_to_DanceInKH'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInKH',
            'dest': 'MorningDanceInKH',
            'conditions': 'is_going_to_MorningDanceInKH'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInKH',
            'dest': 'AfternoonDanceInKH',
            'conditions': 'is_going_to_AfternoonDanceInKH'
        },
        {
            'trigger': 'advance',
            'source': 'DanceInKH',
            'dest': 'EveningDanceInKH',
            'conditions': 'is_going_to_EveningDanceInKH'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningDanceInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonDanceInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningDanceInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'KH',
            'dest': 'DramaInKH',
            'conditions': 'is_going_to_DramaInKH'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInKH',
            'dest': 'MorningDramaInKH',
            'conditions': 'is_going_to_MorningDramaInKH'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInKH',
            'dest': 'AfternoonDramaInKH',
            'conditions': 'is_going_to_AfternoonDramaInKH'
        },
        {
            'trigger': 'advance',
            'source': 'DramaInKH',
            'dest': 'EveningDramaInKH',
            'conditions': 'is_going_to_EveningDramaInKH'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningDramaInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonDramaInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningDramaInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'KH',
            'dest': 'MusicInKH',
            'conditions': 'is_going_to_MusicInKH'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInKH',
            'dest': 'MorningMusicInKH',
            'conditions': 'is_going_to_MorningMusicInKH'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInKH',
            'dest': 'AfternoonMusicInKH',
            'conditions': 'is_going_to_AfternoonMusicInKH'
        },
        {
            'trigger': 'advance',
            'source': 'MusicInKH',
            'dest': 'EveningMusicInKH',
            'conditions': 'is_going_to_EveningMusicInKH'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningMusicInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonMusicInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningMusicInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'advance',
            'source': 'KH',
            'dest': 'MovieInKH',
            'conditions': 'is_going_to_MovieInKH'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInKH',
            'dest': 'MorningMovieInKH',
            'conditions': 'is_going_to_MorningMovieInKH'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInKH',
            'dest': 'AfternoonMovieInKH',
            'conditions': 'is_going_to_AfternoonMovieInKH'
        },
        {
            'trigger': 'advance',
            'source': 'MovieInKH',
            'dest': 'EveningMovieInKH',
            'conditions': 'is_going_to_EveningMovieInKH'
        },
        {
            'trigger': 'go_back',
            'source': 'MorningMovieInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'AfternoonMovieInKH',
            'dest': 'idle'
        },
        {
            'trigger': 'go_back',
            'source': 'EveningMovieInKH',
            'dest': 'idle'
        }
    ],
    initial='idle',
    auto_transitions=False,
    show_conditions=True,
    show_auto_transitions=True
)
machine.get_bot(bot)
#cairosvg.svg2png(url='show-fsm.svg',write_to='output.png')

def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    try:   
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        machine.advance(update)
        return 'ok'
    except:
        print("webhook_handler error")
        return 'error'


#@app.route('/show-fsm', methods=['GET'])
def show_fsm():
	machine.graph.draw('result.pdf', prog='dot', format='pdf')
 
if __name__ == "__main__":
    _set_webhook()
    show_fsm()
    app.run()
