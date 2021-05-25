import socket
import time


class TwitchChatClient:
    def __init__(self, password, username, channel, port, handle_method=None):
        self.__SERVER = "irc.twitch.tv"
        self.__PORT = port
        self.__PASSWORD = password  # This needs to be an OAuth token
        self.__USERNAME = username  # This needs to be in lowercase
        self.__CHANNEL = channel  # This needs to be in lowercase
        self.__IRC = socket.socket()
        self.__HANDLE_METHOD = handle_method
        self.is_hosting = False
        self.no_ads = False

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

    def __is_sub(self, line):
        badges = line
        badges = badges.split(";", -1)[1]
        if "subscriber" in badges or "founder" in badges:
            print("is sub")
            return True
        else:
            return False

    def __is_vip(selfself, line):
        badges = line
        badges = badges.split(";", -1)[1]
        print(str(badges))
        if "vip" in badges:
            return True
        else:
            return False

    def __is_mod(self, line):
        badges = line
        badges = badges.split(";", -1)[1]
        if "broadcaster" in badges:
            return True
        if "mod" in badges:
            return True
        else:
            return False

    def send_message(self, message):
        messageTemp = "PRIVMSG #" + self.__CHANNEL + " :" + message
        self.__IRC.send((messageTemp + "\n").encode())

    def send_whisper(self, user, message):
        messageTemp = "PRIVMSG #" + self.__CHANNEL + " :.w " + user + " " + message
        self.__IRC.send((messageTemp + "\n").encode())

    def host_channel(self, target):
        messageTemp = "PRIVMSG #" + self.__CHANNEL + " :.host " + str(target)
        self.__IRC.send((messageTemp + "\n").encode())
        self.is_hosting = True

    def raid_channel(self, target):
        messageTemp = "PRIVMSG #" + self.__CHANNEL + " :.raid " + str(target)
        self.__IRC.send((messageTemp + "\n").encode())
        self.is_hosting = True

    def disable_ads(self):
        self.no_ads = True

    def enable_ads(self):
        self.no_ads = False

    def stop_host_channel(self):
        messageTemp = "PRIVMSG #" + self.__CHANNEL + " :.unhost"
        self.__IRC.send((messageTemp + "\n").encode())
        self.is_hosting = False

    def stop_raid_channel(self):
        messageTemp = "PRIVMSG #" + self.__CHANNEL + " :.unraid"
        self.__IRC.send((messageTemp + "\n").encode())
        self.is_hosting = False

    def run_commercial(self, length):
        if self.no_ads is False:
            print("Trying to run an ad")
            messageTemp = "PRIVMSG #" + self.__CHANNEL + " :!commercial " + str(length) + " silent"
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
                    print("\nConnected!\n" + str(time.time()) + "\n")

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
                    is_sub = self.__is_sub(line)
                    is_vip = self.__is_vip(line)
                    if self.__HANDLE_METHOD:
                        self.__HANDLE_METHOD(message, user, is_mod, is_sub, is_vip)
                elif "PING" in line:
                    message = "PONG tmi.twitch.tv\r\n".encode()
                    self.__IRC.send(message)
