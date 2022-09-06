from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from . import views
import time

ap = 0
cp = 0
ve = 0
i = 0

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        #start = time.time()
        text_data_json = json.loads(text_data)
        num = text_data_json['num']
        global ap
        global cp
        global ve
        if num == 1:
            views.movVel()
            #while True:
            cPos, aPos, vel = views.re_status()
                #if cp != 0 and cp == cPos:
                 #   break
                #cp = cPos #바뀌기전의 cmd_pos의 위치를 기억하기 위해
            stalist = [cPos, aPos, vel]
            #print(stalist)
            await self.send(text_data=json.dumps(
                stalist
            ))
            #print('complete')
                #time.sleep(10)
        else:
            views.movEstop()
            cPos, aPos, vel = views.re_status()
            stalist = [cPos, aPos, vel]
            await self.send(text_data=json.dumps(
                stalist
            ))
        #end = time.time()
        #print(end-start)

    '''
    def submit(self, text_data):
        #views.store_status(text_data)
        print('send')
        async_to_sync(self.send)(
            text_data=json.dumps({
            'message': text_data
            })
        )
        print('complete')
    '''


class hello(WebsocketConsumer):
    def hello2(self, text_data):
        print('here')
        self.send(text_data=json.dumps({
            'message': text_data
        }))
        print('hi')
