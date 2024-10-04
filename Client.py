import socket
import time
import json
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

packets = 0

def start():
    try:  
        with open('Client_settings.json', 'r', encoding='utf-8') as f:  
            text = json.load(f)

            total_packets = int(text["TotalPackets"])
            interval = int(text["TimeInterval"])
            address = text["gRPCServerAddr"]
            port = int(text["gRPCServerPort"])

            s.connect((address, port))

            print("Client connected to server: " + address + ":" + str(port))
                
    except FileNotFoundError:  
        print("Error: The file 'Client_settings.json' was not found.")  
    except json.JSONDecodeError as e:  
        print(f"JSON decode error: {e}")  
    except Exception as e:  
        print(f"An error occurred: {e}")

    while True:

        with open('Client_settings.json', 'r', encoding='utf-8') as f:
            thistime = time.perf_counter()
            
            text = json.load(f)

            number_packet = text["NumberPacket"]

            time_str = datetime.timezone(datetime.timedelta(hours=3))

            message = number_packet + ":" + str(datetime.datetime.now(time_str)) + ":" + str(time.perf_counter()-thistime)
            
            s.sendall(message .encode())
            data = s.recv(1024).decode()
            print(message + " Sended!")
            time.sleep(interval)

            global packets
            packets = packets + 1

            with open('Client_settings.json') as f:
                data = json.load(f)

                a = int(number_packet)
                b = a + 1
                c = str(b)
                    
                data['NumberPacket'] = c
                with open('Client_settings.json', 'w') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            if packets == total_packets:
                    print("Sended total packets")
                    break

start()
