from core import admin, user


func_dic = {

    '1': admin.admin_view,
    '2': user.user_view,
}
def run():
    while True:
        print('''
        1.管理员功能
        2.用户功能
        q.退出
        ''')

        choice = input('请选择功能编号: ').strip()

        if choice == 'q':
            break

        if choice not in func_dic:
            continue

        func_dic.get(choice)()






