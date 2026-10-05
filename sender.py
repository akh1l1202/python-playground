import socket
import random
import time

HOST = "127.0.0.1"
PORT = 5000

total_frames = int(input("Enter total number of frames: "))
window_size = int(input("Enter window size (N): "))
timeout_value = float(input("Enter timeout value in seconds: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.settimeout(timeout_value)

print("Connected to receiver.")

# Display all frames ready to send
print("Frames ready for transmission:")
for i in range(total_frames):
    print(f"Frame {i}", end=" ")
print("\n")

base = 0
next_seq_num = 0
lost_frames = 0
retransmissions = 0
total_transmissions = 0
ack_buffer = ""
loss_count = {}

while base < total_frames:
    # Send all frames allowed by the window
    while next_seq_num < base + window_size and next_seq_num < total_frames:
        curr_window = f"[{base} to {min(base + window_size - 1, total_frames - 1)}]"

        # Simulate frame loss (20% chance, max twice per frame)
        history = loss_count.get(next_seq_num, 0)
        if (random.random() < 0.20) and (history < 2):
            loss_count[next_seq_num] = history + 1
            lost_frames += 1
            total_transmissions += 1
            print(f"Frame {next_seq_num} lost during transmission.")
            next_seq_num += 1
        else:
            msg = f"FRAME:{next_seq_num}\n"
            client_socket.send(msg.encode())
            total_transmissions += 1
            print(f"Frame {next_seq_num} sent. Current window: {curr_window}")
            next_seq_num += 1

        time.sleep(0.05)

    # Wait for acknowledgment
    try:
        data = client_socket.recv(1024)
        if not data:
            break

        ack_buffer += data.decode()

        while "\n" in ack_buffer:
            line, ack_buffer = ack_buffer.split("\n", 1)
            line = line.strip()
            if not line:
                continue

            if line.startswith("ACK:"):
                ack_num = int(line.split(":")[1])
                print(f"ACK {ack_num} received.")

                if ack_num >= base:
                    base = ack_num + 1
                    new_window = f"[{base} to {min(base + window_size - 1, total_frames - 1)}]"
                    print(f"Window moved forward. New window: {new_window}")
                else:
                    print(f"Duplicate ACK {ack_num} ignored.")

    except socket.timeout:
        print(f"Timeout for Frame {base}. Retransmitting window from Frame {base} to {next_seq_num - 1}")
        retransmissions += (next_seq_num - base)
        next_seq_num = base

client_socket.send(b"END\n")
client_socket.close()

print("\nFinal Statistics:")
print("Total frames:", total_frames)
print("Window size:", window_size)
print("Successfully sent:", total_frames)
print("Lost frames:", lost_frames)
print("Retransmissions:", retransmissions)
print("Total transmissions:", total_transmissions)
print("\nTransmission finished.")