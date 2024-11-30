import time
import board
import adafruit_bno055
import socket
import threading

# Initialize sensor
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

last_val = 0xFFFF

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


# Network settings
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5000       # Port for sending data

# Record the start time
start_time = time.time()

# Set the desired sleep time in milliseconds
frequency = 100  # in HZ
sleep_ms = 1000.0 / frequency

# Retry mechanism for binding the socket
retries = 5
while retries > 0:
    try:
        # Create a socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server started on {HOST}:{PORT}")
        break
    except socket.error as e:
        print(f"Error binding to port: {e}")
        retries -= 1
        if retries == 0:
            print("Max retries reached. Exiting.")
            exit(1)
        print(f"Retrying in 2 seconds...")
        time.sleep(2)

# Accept client connections
clients = []

def handle_client(conn, addr):
    print(f"Client connected: {addr}")
    clients.append(conn)
    try:
        while True:
            time.sleep(1)  # Keep connection alive
    except Exception as e:
        print(f"Client {addr} disconnected: {e}")
    finally:
        clients.remove(conn)
        conn.close()


# Start a thread to accept client connections
def accept_connections():
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


threading.Thread(target=accept_connections, daemon=True).start()

# Open the CSV file for writing
with open("data.csv", "w") as file:
    # Write the header row
    file.write("Elapsed Time (s),Gyro X,Gyro Y,Gyro Z,Accel X,Accel Y,Accel Z,Mag X,Mag Y,Mag Z\n")

    try:
        while True:
            # Calculate elapsed time in seconds
            elapsed_time = time.time() - start_time

            # Extract sensor readings
            gyro = sensor.gyro
            accel = sensor.acceleration
            magnetometer = sensor.magnetic

            # Skip iteration if any reading is None
            if gyro is None or accel is None or magnetometer is None:
                print("Skipping data point due to None value.")
                time.sleep(sleep_ms / 1000.0)
                continue

            # Unpack tuples into individual variables
            try:
                gyro_x, gyro_y, gyro_z = gyro
                accel_x, accel_y, accel_z = accel
                mag_x, mag_y, mag_z = magnetometer
            except TypeError:
                print("Sensor data format is incorrect. Skipping this data point.")
                continue

            # Format the data line
            try:
                data_line = (
                    f"{elapsed_time:.2f},"
                    f"{gyro_x:.2f},{gyro_y:.2f},{gyro_z:.2f},"
                    f"{accel_x:.2f},{accel_y:.2f},{accel_z:.2f},"
                    f"{mag_x:.2f},{mag_y:.2f},{mag_z:.2f}\n"
                )
            except ValueError as e:
                print(f"Error formatting data: {e}")
                continue

            # Print to the console
            #print(data_line.strip())

            # Write to the file
            #file.write(data_line)

            # Send data to all connected clients
            for client in clients:
                try:
                    client.sendall(data_line.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending to client: {e}")
                    clients.remove(client)

            # Sleep for the specified duration in milliseconds
            time.sleep(sleep_ms / 1000.0)

    except KeyboardInterrupt:
        # Handle graceful exit on Ctrl+C
        print("\nProgram interrupted. Closing file and exiting...")
    finally:
        # File will be closed automatically by the 'with' statement
        server_socket.close()
        print("Server shut down.")
