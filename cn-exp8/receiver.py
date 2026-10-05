import socket
import random

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Receiver listening on port", PORT)
connection, address = server_socket.accept()
print("Connected to sender at", address)

expected_frame = 0
buffer = ""

while True:
    try:
        data = connection.recv(1024)
        if not data:
            break
        buffer += data.decode()

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()
            if not line:
                continue

            if line == "END":
                print("\nTransmission completed by sender.")
                break

            if line.startswith("FRAME:"):
                frame_number = int(line.split(":")[1])

                if frame_number == expected_frame:
                    print(f"Frame {frame_number} received correctly.")

                    # Simulate ACK loss (15% chance)
                    if random.random() < 0.15:
                        print(f"ACK {frame_number} lost in transit.")
                    else:
                        ack_msg = f"ACK:{frame_number}\n"
                        connection.send(ack_msg.encode())
                        print(f"ACK {frame_number} sent.")

                    expected_frame += 1
                else:
                    print(f"Frame {frame_number} out of order (expected {expected_frame}), discarded.")
                    # Resend ACK for last received frame
                    last_ack = expected_frame - 1
                    if last_ack >= 0:
                        ack_msg = f"ACK:{last_ack}\n"
                        connection.send(ack_msg.encode())
                        print(f"Resent ACK {last_ack}")

        if line == "END":
            break

    except ConnectionResetError:
        break

connection.close()
server_socket.close()
print("Connection closed.")