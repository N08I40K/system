import psutil
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import traceback
import json
vk_session = vk_api.VkApi(token='')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
moder = [548215920, 615887613]
def cpu():
    try:
        p = psutil.cpu_percent(interval=1, percpu=True)
        m = psutil.virtual_memory()
        d = psutil.disk_usage('/')

        total = int(m.total / (1*10**9))
        s = ''
        for i in range(len(p)):
            s = s + 'CPU[' + str(i) + ']: ' + str(p[i]) + '%\n'
        s = s + 'RAM: ' + str(m.percent) + '% от ' + str(total) + ' GB' + ' (' + str(round(m.used/1024/1024)) + ' MB)'
        s = s + '\nDisk: ' + str(d.percent) + '%'  +'(' + str(round(d.used/1024/1024)) + ' MB)'
        vk.messages.send(peer_id=event.peer_id, random_id=0, message = s)
    except Exception as er:
        print(er)
print('Бот запущен')                                                   
while True:
     try:
         for event in longpoll.listen():
             if event.type == VkEventType.MESSAGE_NEW and event.user_id in moder:
                     try:
                         if event.text.lower().startswith("/статавдс"):
                             cpu()    
                     except:
                         print(traceback.format_exc())
     except:
        print('Ошибка:')
        print(traceback.format_exc())
        print('-'*80)
