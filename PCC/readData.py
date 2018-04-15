import csv
from pymongo import MongoClient


conn = MongoClient('127.0.0.1', 27017)  # 连接MongoDB
db = conn.pcc                           # 连接数据库
user_set = db.user                      # 选择集合
like_set = db.like                      # 选择集合
friends_set = db.friends                # 选择集合

# 删除所有数据
# user_set.remove()
# like_set.remove()
# friends_set.remove()


# 获取数据
# user_list = []
# like_list = []
# friends_list = []
# user_file = csv.reader(open(r'C:\Users\Asus\Desktop\py\py3\architecture\test\user.csv'))
# like_file = csv.reader(open(r'C:\Users\Asus\Desktop\py\py3\architecture\test\like.csv'))
# friends_file = csv.reader(open(r'C:\Users\Asus\Desktop\py\py3\architecture\test\friends.csv'))
#
# for i, j in user_file:
#     ret = {'uid': i, 'name': j}
#     user_list.append(ret)
#
# for i, *j in like_file:
#     ret = {'oid':i, 'uids':list(set(j))}
#     like_list.append(ret)
#
# for i, j in friends_file:
#     ret = {'uid':i, 'friend_id':j}
#     friends_list.append(ret)
#
# # 插入数据
# user_set.insert(user_list)
# like_set.insert(like_list)
# friends_set.insert(friends_list)


# 查询数据
# user_name = user_set.find_one({'uid':'6000100010'})
# print(user_name)