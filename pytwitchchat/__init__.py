import socket
import getopt
import sys


class TwitchChatClient:
    def __init__(self, password, username, channel, handle_method=None):
        self.__SERVER = "irc.twitch.tv"
        self.__PORT = 6667
        self.__PASSWORD = password  # This needs to be an OAuth token
        self.__USERNAME = username  # This needs to be in lowercase
        self.__CHANNEL = channel  # This needs to be in lowercase
        self.__IRC = socket.socket()
        self.__HANDLE_METHOD = handle_method

    def __is_user_message(self, line):
        try:
            info = line.split(":", 2)[1]
        except:
            info = ""
        return True if "PRIVMSG" in info else False

    def __get_message(self, line):
        return line.split(":", 2)[2]

    def __get_user(self, line):
        info = line.split(":", 2)[1]
        user = info.split("!", 1)[0]
        return user

    def __is_mod(self, line):
        tags = line.split(":", 2)[0]
        return True if "user-type=mod" in tags else False

    def send_message(self, message):
        messageTemp = "PRIVMSG #" + self.__CHANNEL + " :" + message
        self.__IRC.send((messageTemp + "\n").encode())

    def connect(self):
        print("Connecting...")
        connecting = True
        self.__IRC.connect((self.__SERVER, self.__PORT))
        self.__IRC.send(
            ("PASS " + self.__PASSWORD + "\n" +
             "NICK " + self.__USERNAME + "\n" +
             "JOIN #" + self.__CHANNEL + "\n" +
             "CAP REQ :twitch.tv/tags" + "\n")
            .encode()
        )
        while connecting:
            readbuffer_join = self.__IRC.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                if ("End of /NAMES list" in line):
                    connecting = False
                    print("Connected!")

    def run(self):
        while True:
            try:
                readbuffer = self.__IRC.recv(1024).decode()
            except:
                readbuffer = ""
            for line in readbuffer.split("\r\n"):
                if self.__is_user_message(line):
                    message = self.__get_message(line)
                    user = self.__get_user(line)
                    is_mod = self.__is_mod(line)
                    if self.__HANDLE_METHOD:
                        self.__HANDLE_METHOD(message, user, is_mod)
                elif "PING" in line:
                    message = "PONG tmi.twitch.tv\r\n".encode()
                    self.__IRC.send(message)
