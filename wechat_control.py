import itchat
import os
import time
import cv2
# 人脸识别库
# import face_recognition


# sendMsg = u"有事暂时不在，稍后回复"
# 发送给文件传输助手的开启提示消息
# 可自行修改
usageMsg = u"1.运行CMD命令：cmd xxx (xxx为命令)\n" \
           u"-输入 关机 关闭电脑\n"\
           u"-输入 待机 进入休眠模式\n" \
           u"-输入 chrome 打开chrome\n" \
           u"2.输入capture，获取当前用户"
# 发送给指定用户的提示消息
xwjMsg = u"-- 远程助手已部署 --\n"\
         u"--发送 capture 即可获取当前用户"


# 自动回复组件
@itchat.msg_register('Text')
def text_reply(msg):
    global flag
    message = msg['Text']
    # print(msg.fromUserName)
    # fromName = msg['FromUserName']
    # toName = msg['ToUserName']

    # 指定用户的的UserName，具体参考itchat库的文档
    if msg.fromUserName == '@a2c84de92a939c757ed032e981be9c88ca445bf2ef73f98d4360e3cf4ec954a3':
        # 接收到消息‘capture’，则打开摄像头获取当前用户照片
        if message == "capture":
            # 如电脑有两个摄像头，则0为后置摄像头，1为前置摄像头
            cap = cv2.VideoCapture(1)
            ret, img = cap.read()
            cv2.imwrite("weixinTemp.jpg", img)
            # 将获取的照片发送给指定用户
            xwj.send('@img@%s' % u'weixinTemp.jpg')
            # 人脸识别组件，不需要可注释掉
            # recognition(xwj)
        # 释放摄像头
        cv2.VideoCapture().release()

    # 文件助手命令逻辑
    # 如果发送消息给文件传输助手
    if msg.toUserName == 'filehelper':
        # 显示命令内容
        print(msg['Content'])
        if message == "capture":
            cap = cv2.VideoCapture(1)
            ret, img = cap.read()
            cv2.imwrite("weixinTemp.jpg", img)
            itchat.send('@img@%s' % u'weixinTemp.jpg', toUserName='filehelper')
            # recognition(xwj)
            # cap.release()
        cv2.VideoCapture().release()
        # cmd命令，可以实现远程操作电脑
        if message[0:3] == "cmd":
            os.system(message.strip(message[0:4]))
        # 预置的待机命令
        if message == '待机':
            os.system('rundll32.exe powrProf.dll SetSuspendState')
        # 预置的关机命令
        if message == '关机':
            os.system('shutdown -s -t 0')
        # cmd打开应用程序 可自行修改
        if message == 'chrome':
            os.system(r"C:\Users\13626\AppData\Local\Google\Chrome\Application\chrome.exe")


# 人脸识别组件模块，不需要可注释
"""
zwz_image = face_recognition.load_image_file("zwz.jpg")

zwz_encoding = face_recognition.face_encodings(zwz_image)[0]


# 人脸识别组件
def recognition(xwj):
    unknown_image = face_recognition.load_image_file("weixinTemp.jpg")
    try:
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([zwz_encoding], unknown_encoding)
        labels = ['Zhou Wenzhang']
        print('results:'+str(results))
        for i in range(0, len(results)):
            if results[i] == True:
                print('The person is:' + labels[i])
                xwj.send('The person is:' + labels[i])
            else:
                print('The person is Unknown')
                xwj.send('The person is Unknown')
    except:
        print("There is nobody here.")
        xwj.send("There is nobody here.")
        pass
"""


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=True)
    itchat.send(usageMsg, toUserName='filehelper')
    # 特定用户
    # 昵称自行修改nickName
    xwj = itchat.search_friends(nickName='用户昵称')[0]
    itchat.run()