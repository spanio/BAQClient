import serial


class BAQClient:
    def __init__(self, port):
        self.serial_port = port
        self.baud_rate = 9600
        self.timeout = 1  # seconds
        self.chans_in = 32
        self.channel_names = [f"Channel {i+1}" for i in range(self.chans_in)]
        self.serial_connection = None

    def open_connection(self):
        try:
            self.serial_connection = serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)
            time.sleep(.25)  # Wait for connection to establish
        except serial.SerialException as e:
            raise Exception(f"Error opening serial connection: {e}")

    def close_connection(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()

    def send_command(self, command):
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("Serial connection is not open")

        self.serial_connection.write(f"{command}\n".encode())
        response = self.serial_connection.readline().decode().strip()
        return response

    def read_samples(self, channel_number):
        if channel_number < 1 or channel_number > self.chans_in:
            raise ValueError("Channel number out of range")
        
        response = self.send_command(f"MEASure:CHANnel: {channel_number}")
        if not response.startswith(f"Channel {channel_number}:"):
            raise Exception(f"Unexpected response from device: {response}")
        
        # Extract and return the measurement value
        return int(response.split(': ')[-1])

    def get_channel_names(self):
        return self.channel_names
    def set_channel_name(self, position, name):
        if position < 0 or position >= self.chans_in:
            raise ValueError(f"Invalid position value. Must be between 0 and {self.chans_in-1}.")
        self.channel_names[position] = name
    def start(self):
        self.open_connection()
    def stop(self):
        pass
    def close(self):
        self.close_connection()
