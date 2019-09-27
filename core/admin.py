from tcp_client import socket_client
from lib import common
import os
from conf import settings
user_info = {
    'cookies': None
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
                        'user_type': 'admin'}
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
            'user_type': 'admin'
        }
        # {'flag': False, 'msg': '用户不存在'}
        back_dic = common.send_msg_back_dic(send_dic, client)

        if back_dic.get('flag'):
            session = back_dic.get('session')
            user_info['cookies'] = session
            print(back_dic.get('msg'))
            break

        else:
            print(back_dic.get('msg'))

# 上传电影
def upload_movie(client):
    while True:
        # 1.打印电影列表
        movie_list = common.get_movie_list()
        for index, movie in enumerate(movie_list):
            print(index, movie)

        choice = input('请输入上传的电影编号:').strip()

        if not choice.isdigit():
            print('请输入数字!')
            continue

        choice = int(choice)

        if choice not in range(len(movie_list)):
            print("请选择正确编号!")
            continue

        # 用户选择电影
        movie_name = movie_list[choice]

        # 上传电影绝对路径
        movie_path = os.path.join(
            settings.UPLOAD_FILES, movie_name
        )

        # 2.去服务端校验电影是否存在
        file_md5 = common.get_movie_md5(movie_path)

        send_dic = {
            'type': 'check_movie',
            'session': user_info.get('cookies'),
            'file_md5': file_md5
        }

        back_dic = common.send_msg_back_dic(
            send_dic, client)

        if back_dic.get('flag'):
            # 电影可以上传
            print(back_dic.get('msg'))

            # 上传电影功能字典
            send_dic = {
                'type': 'upload_movie',
                'file_md5': file_md5,
                # 大小用来判断服务端需要接受文件的大小
                'file_size': os.path.getsize(movie_path),
                'movie_name': movie_name,
                'session': user_info.get('cookies')
            }

            is_free = input('上传电影是否免费: y/n').strip()

            if is_free == 'y':
                send_dic['is_free'] = 1

            else:
                send_dic['is_free'] = 0

            back_dic = common.send_msg_back_dic(
                send_dic, client, file=movie_path)

            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break

        else:
            print(back_dic.get('msg'))



    #
    #
    # send_dic = {'type': 'upload_movie','session': user_info.get('cookies')}
    # back_dic = common.send_msg_back_dic(send_dic, client)
    # print(back_dic)

# 删除电影
def delete_movie(client):
    while True:
        # 1.从服务端获取电影列表
        send_dic = {'type': 'get_movie_list',
                    'session': user_info.get('cookies')}

        # 发送获取电影请求
        back_dic = common.send_msg_back_dic(
            send_dic, client)

        if back_dic.get('flag'):
            back_movie_list = back_dic.get('back_movie_list')
            # 打印选择的电影
            for index, movie_list in enumerate(back_movie_list):
                print(index, movie_list)

            # 2.选择需要删除的电影
            choice = input('请输入需要删除的电影编号：').strip()

            if not choice.isdigit():
                continue

            choice = int(choice)

            if choice not in range(len(back_movie_list)):
                continue

            # 获取电影ID，传递给服务端，让服务端去mysql数据库修改当前电影对象的is_delete=1
            movie_id = back_movie_list[choice][2]

            send_dic = {
                'type': 'delete_movie', 'movie_id': movie_id,
                'session': user_info.get('cookies')
            }

            # 发送删除电影请求
            back_dic = common.send_msg_back_dic(send_dic, client)

            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
        else:
            print(back_dic.get('msg'))
            break

# 发布公告
def put_notice(client):
    title = input('请输入公告标题:').strip()
    content = input('请输入公告内容:').strip()

    send_dic = {
        'type': 'put_notice',
        'session': user_info.get('cookies'),
        'title': title,
        'content': content
    }
    back_dic = common.send_msg_back_dic(send_dic, client)

    print(back_dic.get('msg'))

func_dic = {
    '1': register,
    '2': login,
    '3': upload_movie,
    '4': delete_movie,
    '5': put_notice,
}

def admin_view():

    sk_client = socket_client.SocketClient()
    client = sk_client.get_client()

    while True:
        print('''
        	1.注册
            2.登录
            3.上传视频
            4.删除视频
            5.发布公告
            q.退出
        ''')

        choice = input('请选择功能编号:').strip()

        if choice == 'q':
            break

        if choice not in func_dic:
            continue

        func_dic.get(choice)(client)
