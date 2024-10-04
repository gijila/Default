import socket
import json
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
def go():
    conn, addr = s.accept()
    print(f'Connected {addr}')
    
    while True:
        try:
            data = conn.recv(1024).decode()

            msg = data.split(":")

            try:

                global connection
                global cursor
                
                connection = psycopg2.connect(user="postgres",
                                  password="test",
                                  host="0.0.0.0",
                                  port="5432",
                                  database="grpc_db")

            
                cursor = connection.cursor()  

                create_table_query = '''
                    create table if not exists grpc_data (  
                    NUMBER TEXT,  
                    DATA TEXT,
                    TIMING TEXT
                );  
                '''

                msg1 = msg[0]
                msg2 = msg[1]
                msg3 = msg[3]

                insert_query = "INSERT INTO grpc_data (NUMBER, DATA, TIMING) VALUES (%s, %s, %s);"  
                
                cursor.execute(create_table_query)
                cursor.execute(insert_query, (msg1, msg2, msg3))
                
                connection.commit()    

            except (Exception, Error) as error:
                print("Error PostgreSQL", error)

            reply = " "
            print("Accepted packet! Number: " + msg1 + " Data: " + msg2 + " Timing: " + msg3)
            conn.sendall(reply.encode())
        except:
            go()
            break

def start():
    try:  
        with open('Server_settings.json', 'r', encoding='utf-8') as f:  
            text = json.load(f)

            port = int(text["gRPCServerPort"])

            s.bind(('0.0.0.0', port))
            s.listen(100)

            print("Server start on port " + str(port))

            go()
    except FileNotFoundError:  
        print("Error: The file 'Client_settings.json' was not found.")  
    except json.JSONDecodeError as e:  
        print(f"JSON decode error: {e}")  
    except Exception as e:  
        print(f"An error occurred: {e}")


start()
