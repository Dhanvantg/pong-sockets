import socket
from _thread import *
import sys

screen_width = 1280
screen_height = 750

bx = screen_width/2 - 15
by = screen_height/2 - 15
bsx = 7
bsy = 7
lscore = 0
rscore = 0
p1 = screen_height/2-70
p2 = screen_height/2-70
players = {}

server = "192.168.0.118"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, server ready")

def threaded_client(conn, player, addr):
    global p1, ps1, p2, ps2, bx, by, bsx, bsy, rscore, lscore, players
    conn.sendall(str.encode('Connection successful'))
    while True:
        reply = ""
        data = conn.recv(2048).decode("utf-8")

        if not data:
            print("Disconnected")
            break
        else:
            #print("Received:", data)

            if data == "newcon":
                if len(players) == 0:
                    players[addr] = 1
                    reply += '1'
                elif len(players) == 1:
                    players[addr] = 2
                    reply += '2'
                else:
                    print('huh')
                    break
                print(players)
            elif data == "waiting":
                if len(players) == 2:
                    reply = 'waitover'
                    conn.sendall(str.encode(reply))
                    conl.sendall(str.encode(reply))

            if len(players) == 2 and data != "newcon":
                if data == "waiting":
                    continue
                if players[addr] == 1:
                    p1 = eval(data)[0]
                    ps1 = eval(data)[1]
                    reply += str(p2)
                elif players[addr] == 2:
                    p2 = eval(data)[0]
                    ps2 = eval(data)[1]
                    reply += str(p1)
                else:
                    print('wut')
                    break

                if by <=0 or by+30 >=screen_height:
                    bsy *= -1
                if bx <=0:
                    bsx *= -1
                    rscore +=1
                if bx+30 >=screen_width:
                    bsx *=-1
                    lscore +=1

                if bx <= 70 and bx >= 20 and by >= p1 and by <= p1 + 140:
                    bsx *= -1
                elif bx >= screen_width - 100 and bx <= screen_width - 50 and by >= p2 and by <= p2 + 140:
                    bsx *= -1
                bx += bsx
                by += bsy
                
                reply += ', ' + str(bx) + ', ' + str(by) + ', ' + str(lscore) + ', ' + str(rscore)
            if reply != "":
                #print("Sending:", reply)
                pass
            else:
                continue

        conn.sendall(str.encode(reply))


    print("Lost Connection")
    print("Connection Closed")

curPlayer = 0

while True:
    conn, addr = s.accept()
    print("connected to:", addr)
    if curPlayer == 0:
        conl = conn

    start_new_thread(threaded_client, (conn, curPlayer, addr[1]))
    curPlayer += 1