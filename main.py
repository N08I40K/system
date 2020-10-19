import argparse
import time
import os
import random
import traceback
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api import VkApi
import platform
import psutil
class CPU_LOAD:
    __slots__ = (
                 'cpu_cores',
                 'cores_list',
                 'cores_full',
                 'num_cores'
                 )
class CPU_FREC:
    __slots__ = (
                 'cpu_full',
                 'frec_current'
                 )
class VIRT_MEM:
    __slots__ = (
                 'total',
                 'available',
                 'used'
                 )
class DISK_PART:
    __slots__ = (
                 'list',
                 'using_info',
                 'total',
                 'free',
                 'percent',
                 'mountpoint',
                 'fstype',
                 'used'
                 )
vk_session = vk_api.VkApi(token="code here")
long_poll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# vk_session = vk_api.VkApi(args.user, args.passw, app_id=2685278)
# vk_session.auth(token_only=True)
# long_poll = VkLongPoll(vk_session)
# vk = vk_session.get_api()

def send_msg(peer_id=None, domain=None, chat_id=None, text=None,
             sticker_id=None, user_id=None, forward_messages=None, attachments=None, payload=None, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        random_id=random.randint(-2147483648, 2147483647),
        peer_id=peer_id,
        domain=domain,
        chat_id=chat_id,
        message=text,
        sticker_id=sticker_id,
        attachment=attachments,
        forward_messages=forward_messages,
        payload=payload,
        keyboard=keyboard,
    )
def main():
    F_all = ""
    cmd_prefix = "!"
    try:
        for event in long_poll.listen():
            try:
                if (event.type == VkEventType.MESSAGE_NEW):
                    message_global = None
                    message_command = None
                    message_args = None
                    message_id = None
                    user_id = None
                    peer_id = None
                    chat_id = None
                    message_length = None
                    try:
                        
                        #само сообщение
                        message_global = event.text
                        
                        #его длинна
                        message_length = len(message_global)
                        
                        #если длинна сообщения меньше 1 символа то
                        if message_length < 1:
                            
                            #сообщение = знаку 0
                            message_global = "0"
                        
                        #если сообщение начинается с префикса (по умолчанию: "!") то
                        if (message_global[0] == cmd_prefix):
                            
                            #команда = текст после префикса до первого пробела
                            message_command = message_global.split(' ')[0][len(cmd_prefix):]
                            
                            #аргументы текст после первого пробела до конца переменной
                            message_args = message_global[len(message_global.split(' ')[0])+1:]
                        else:
                            
                            #если нет то аргументов и комманды нету
                            message_command = None
                            message_args = None
                    except:
                        #при ошибке
                        message_global = "undefined."
                        message_length = 10
                        message_command = None
                        message_args = None
                        traceback.print_exc()
                    
                    #ID отправителя
                    peer_id = event.peer_id
                    
                    #то же самое только - 2000000000
                    chat_id = peer_id-2000000000
                    
                    #id пользователя в вк
                    user_id = event.user_id
                    
                    message_id = event.message_id
                    if (message_command == "таймер"):
                        end_msg = message_args
                        vk.messages.edit(peer_id=peer_id, message_id=message_id, message='5')
                        time.sleep(1)
                        vk.messages.edit(peer_id=peer_id, message_id=message_id, message='4')
                        time.sleep(1)
                        vk.messages.edit(peer_id=peer_id, message_id=message_id, message='3')
                        time.sleep(1)
                        vk.messages.edit(peer_id=peer_id, message_id=message_id, message='2')
                        time.sleep(1)
                        vk.messages.edit(peer_id=peer_id, message_id=message_id, message='1')
                        time.sleep(1)
                        vk.messages.edit(peer_id=peer_id, message_id=message_id, message=str(end_msg))
                    if (message_command == "system"):
                        sys_name, pc_name, release_os, version_os, bit, processor = platform.uname()
                        version_global = sys_name+" "+release_os+" "+bit
                        processor_level = psutil.cpu_percent()

                        CPU_LOAD.cpu_cores = psutil.cpu_percent(interval=0.5, percpu=True)
                        CPU_LOAD.cores_list = ""
                        CPU_LOAD.cores_full = 0
                        CPU_LOAD.num_cores = 0
                        for i in CPU_LOAD.cpu_cores:
                            CPU_LOAD.cores_list += "\nCore №"+str(CPU_LOAD.num_cores)+": "+str(i)+"%"
                            CPU_LOAD.cores_full += int(i)
                            CPU_LOAD.num_cores += 1
                        CPU_LOAD.cpu_full = int(CPU_LOAD.cores_full)/int(CPU_LOAD.num_cores)
                        CPU_LOAD.cores_list = CPU_LOAD.cores_list[-1*len(CPU_LOAD.cores_list)+1:]
                        CPU_FREC.cpu_full = list(psutil.cpu_freq(percpu=False))
                        CPU_FREC.frec_current, unused, unused = CPU_FREC.cpu_full

                        VIRT_MEM.total = str(round(psutil.virtual_memory().total / (1024.0**2)))
                        VIRT_MEM.available = str(round(psutil.virtual_memory().available / (1024.0**2)))
                        VIRT_MEM.used = str(round(psutil.virtual_memory().used / (1024.0**2)))

                        num_disk =  0
                        DISK_PART.list = ''
                        for i in psutil.disk_partitions():
                            DISK_PART.mountpoint = str(i.mountpoint)
                            DISK_PART.fstype = str(i.fstype) 
                            DISK_PART.using_info = psutil.disk_usage(DISK_PART.mountpoint)
                            DISK_PART.total = str(round(DISK_PART.using_info.total / (1024.0**2)))
                            DISK_PART.used = str(round(DISK_PART.using_info.used / (1024.0**2)))
                            DISK_PART.free = str(round(DISK_PART.using_info.free / (1024.0**2)))
                            DISK_PART.percent = str(DISK_PART.using_info.percent)
                            DISK_PART.list += (
                                  'Диск '+str(num_disk)+':\n'+
                                  'Метка: '+DISK_PART.mountpoint+'\n'+
                                  'Файловая система: '+DISK_PART.fstype+'.\n'+
                                  'Всего: '+DISK_PART.total+'MB.\n'+
                                  'Использовано: '+DISK_PART.percent+'%. '+DISK_PART.used+' MB.\n'+
                                  'Свободно: '+DISK_PART.free+' MB.\n'
                                  )
                            num_disk += 1

                        full_full_full = (
                                            "Система: "+str(version_global)+"\n\n"+

                                            "Процессор: "+"\n"+
                                            "Загруженность процессора: "+str(CPU_LOAD.cpu_full)+"%"+"\n"+
                                            "Частота процессора: "+str(CPU_FREC.frec_current)[:len(str(CPU_FREC.frec_current))-2]+" Mhz."+"\n\n"+

                                            "Ядра процессора: "+"\n"+
                                            "Загруженность ядер:\n"+CPU_LOAD.cores_list+"\n"+
                                            "Ядра процессора: "+str(psutil.cpu_count())+"\n"+
                                            "Использующиеся ядра процессора: "+str(len(psutil.Process().cpu_affinity()))+"\n\n"+

                                            "Оперативная память: "+"\n"+
                                            "Всего: "+VIRT_MEM.total+" MB"+"\n"+
                                            "Доступно\Свободно: "+VIRT_MEM.available+" MB"+"\n"+
                                            "Занято: "+VIRT_MEM.used+" MB"+"\n\n"+

                                            DISK_PART.list
                                          )
                        send_msg(peer_id=peer_id, text=full_full_full)


            except Exception as vk_error:
                print("Ошибка: " + str(vk_error))
                traceback.print_exc()
                continue

    except Exception as vk_error:
        print("Ошибка: " + str(vk_error))
        print("Reloading...")
        time.sleep(10)
        print("Reloaded!")
        main()
        

# сбор инфы и вывод конфига перед запуском
if __name__ == "__main__":
    n = 0
    textt = "By N08I40K :)"
    for i in range(len(textt)):
        os.system("cls")
        time.sleep(0.1)
        print(textt[:n+1])
        n += 1
    main()
