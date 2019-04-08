from urllib import request
import re


'''
这个脚本可以得到虎牙直播，二次元区的实时直播热榜
我的第一个爬虫脚本，能跑就行，要求不高
'''


class Spider():
    # 站点的url
    url = 'http://www.huya.com/g/2633'

    # 数据的获取，获取房间名room、主播anchor、观看人数number，存入room_info_list二维数组中
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        html = str(r.read(), encoding='utf-8')
        root_content = re.findall('<li class="game-live-item" gid="[\s\S]*?">([\s\S]*?)</li>',html)
        root_content_str = str(root_content)
        room = re.findall('<a [\s\S]*? class="title new-clickstat" [\s\S]*?>([\s\S]*?)</a>',root_content_str)
        anchor = re.findall('<i class="nick" [\s\S]*?>([\s\S]*?)</i>',root_content_str)
        number = re.findall('<span class="num"><i class="num-icon"></i><i class="js-num">([\s\S]*?)</i></span>',root_content_str)
        room_info_list = []
        for i in range(0, len(root_content)):
            room_info_list.append((room[i], anchor[i], number[i]))
        return room_info_list

    # 排名前处理，将str转换为float，将带万字的数据转换为float
    def __pre_rank(self, room_info):
        number = room_info[2]
        if '万' in str(room_info[2]):
            number = re.sub('万', '', room_info[2], 0)
            number = float(number) * 10000
        else:
            number = float(number)
        return number

    # 按热度进行排名
    def __rank(self, room_info_list):
        room_info_list = sorted(room_info_list, key=lambda room_info: self.__pre_rank(room_info), reverse=True)
        return room_info_list

    # 打印排名和总人气
    def __show(self, room_info_list):
        number_sum = 0
        for i in range(0, len(room_info_list)):
            print('rank' + str(i + 1) + ': ' + room_info_list[i][0] + ' ' + room_info_list[i][1] + ' ' + room_info_list[i][2])
            temp = self.__pre_rank(room_info_list[i])
            number_sum += temp
        print('总人气：' + str(number_sum))

    # 主方法，从这个方法开始
    def go(self):
        room_info_list = self.__fetch_content()
        room_info_list = self.__rank(room_info_list)
        self.__show(room_info_list)


spider = Spider()
spider.go()
