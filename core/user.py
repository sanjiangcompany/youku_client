from tcp_client.socket_client import SocketClient
from lib import common
from conf import settings
import time
import os
user_info = {
    'cookies': None,
    'is_vip': None
}

def register(client):
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('请确认密码:').strip()
        if password == re_password:
            send_dic = {'username': username,
                        'password': password,
                        'type': 'register',
                        'user_type': 'user'}
            # {'flag': False, 'msg': '用户已存在!'}
            # {'flag': True, 'msg': '注册成功'}
            back_dic = common.send_msg_back_dic(send_dic, client)

            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break

            else:
                print(back_dic.get('msg'))

def login(client):
    while True:
        username = input('请输入用户名: ').strip()
        password = input('请输入密码:').strip()

        send_dic = {
            'type': 'login',  # 判断对应的接口
            'username': username,
            'password': password,
            'user_type': 'user'
        }
        # {'flag': False, 'msg': '用户不存在'}
        back_dic = common.send_msg_back_dic(send_dic, client)

        if back_dic.get('flag'):
            session = back_dic.get('session')
            user_info['cookies'] = session
            user_info['is_vip'] = back_dic.get('is_vip')
            print(back_dic.get('msg'))

            # 打印最新公告
            if back_dic.get('new_notice'):
                print(back_dic.get('new_notice'))

            break

        else:
            print(back_dic.get('msg'))

# 购买会员功能
def buy_vip(client):
    if user_info.get('is_vip'):
        print('已经是会员了!')
        return

    is_vip = input('购买会员（y or n）？').strip()
    if is_vip == 'y':
        send_dic = {
            'type': 'buy_vip',
            'session': user_info.get('cookies')
        }

        back_dic = common.send_msg_back_dic(
            send_dic, client)

        if back_dic.get('flag'):
            print(back_dic.get('msg'))



    else:
        print('*穷*，快去打工赚钱!')

# 查看所有电影
def check_all_movie(client):
    send_dic = {
        'type': 'get_movie_list',
        'session': user_info.get('cookies')
    }

    back_dic = common.send_msg_back_dic(
        send_dic, client)
    if back_dic.get('flag'):
        print(back_dic.get('back_movie_list'))
    else:
        print(back_dic.get('msg'))

# 下载免费电影
def download_free_movie(client):
    while True:
        # 1.获取服务端所有免费电影
        send_dic = {
            'type': 'get_movie_list',
            'session': user_info.get('cookies'),
            'movie_type': 'free'
        }
        back_dic = common.send_msg_back_dic(send_dic, client)
        if back_dic.get('flag'):
            # 2.选择下载的免费电影，并提交给服务端
            movie_list = back_dic.get('back_movie_list')

            for index, movie in enumerate(movie_list):
                print(index, movie)

            choice = input('请输入下载电影编号:').strip()

            if not choice.isdigit():
                continue

            choice = int(choice)

            if choice not in range(len(movie_list)):
                continue

            movie_name, movie_type, movie_id = movie_list[choice]

            send_dic = {'type': 'download_movie',
                        'session': user_info.get('cookies'),
                        'movie_id': movie_id,
                        'movie_name': movie_name,
                        'movie_type': movie_type}

            back_dic = common.send_msg_back_dic(send_dic, client)

            if back_dic.get('flag'):
                # 3.开始下载电影
                movie_path = os.path.join(settings.DOWNLOAD_FILES, movie_name)
                movie_size = back_dic.get('movie_size')

                # 准备下载电影: 判断是否是VIP，若不是则等待广告播放
                wait_time = back_dic.get('wait_time')

                if wait_time:
                    print('惠州某工厂上线啦....')
                    time.sleep(wait_time)

                recv_data = 0
                with open(movie_path, 'wb') as f:
                    while recv_data < movie_size:
                        data = client.recv(1024)
                        f.write(data)
                        recv_data += len(data)
                    f.flush()

                print('免费电影下载成功!')
                break

        else:
            print(back_dic.get('msg'))
            break


# 下载收费电影
def download_pay_movie(client):
    while True:

        if user_info.get('is_vip'):
            is_pay = input('VIP打骨折，收费5$一部(y or n):').strip()
        else:
            is_pay = input('普通用户，收费50$一部(y or n):').strip()

        if not is_pay == 'y':
            print('Gun去充钱!')
            break

        # 1.获取服务端所有免费电影
        send_dic = {
            'type': 'get_movie_list',
            'session': user_info.get('cookies'),
            'movie_type': 'pay'
        }
        back_dic = common.send_msg_back_dic(send_dic, client)
        if back_dic.get('flag'):
            # 2.选择下载的免费电影，并提交给服务端
            movie_list = back_dic.get('back_movie_list')

            for index, movie in enumerate(movie_list):
                print(index, movie)

            choice = input('请输入下载电影编号:').strip()

            if not choice.isdigit():
                continue

            choice = int(choice)

            if choice not in range(len(movie_list)):
                continue

            movie_name, movie_type, movie_id = movie_list[choice]

            send_dic = {'type': 'download_movie',
                        'session': user_info.get('cookies'),
                        'movie_id': movie_id,
                        'movie_name': movie_name,
                        'movie_type': movie_type}

            back_dic = common.send_msg_back_dic(send_dic, client)

            if back_dic.get('flag'):
                # 3.开始下载电影
                movie_path = os.path.join(settings.DOWNLOAD_FILES, movie_name)
                movie_size = back_dic.get('movie_size')

                # 准备下载电影: 判断是否是VIP，若不是则等待广告播放
                wait_time = back_dic.get('wait_time')

                if wait_time:
                    time.sleep(wait_time)

                recv_data = 0
                with open(movie_path, 'wb') as f:
                    while recv_data < movie_size:
                        data = client.recv(1024)
                        f.write(data)
                        recv_data += len(data)
                    f.flush()

                print('收费电影下载成功!')
                break

        else:
            print(back_dic.get('msg'))
            break

# 查看下载记录功能
def check_download_record(client):
    send_dic = {'type': 'check_download_record',
                'session': user_info.get('cookies')}

    back_dic = common.send_msg_back_dic(send_dic, client)

    if back_dic.get('flag'):
        # 返回电影下载记录
        print(back_dic.get('record_list'))

    else:
        print(back_dic.get('msg'))

# 查看所有公告
def check_all_notice(client):
    send_dic = {'type': 'check_all_notice',
                'session': user_info.get('cookies')}
    back_dic = common.send_msg_back_dic(send_dic, client)
    if back_dic.get('flag'):
        print(back_dic.get('back_notice_list'))
    else:
        print(back_dic.get('msg'))

func_dic = {
    '1': register,
    '2': login,
    '3': buy_vip,
    '4': check_all_movie,
    '5': download_free_movie,
    '6': download_pay_movie,
    '7': check_download_record,
    '8': check_all_notice,
}

def user_view():
    sk_client = SocketClient()
    client = sk_client.get_client()
    while True:
        print('''
        1.注册
        2.登录
        3.充会员
        4.查看视频
        5.下载免费视频
        6.下载会员视频
        7.查看观影记录
        8.查看所有公告
        ''')

        choice = input('请选择功能编号:').strip()

        if choice == 'q':
            break

        if choice not in func_dic:
            continue

        func_dic.get(choice)(client)
