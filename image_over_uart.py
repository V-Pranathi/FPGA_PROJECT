import imageio as iio   
import numpy as np

import serial, time

from data_uart import data
from mapping import lookup

COMPORT = 'COM4'


MODE = "camera"

# Don't change these
BAUD_RATE = 1843200
RES_X = 320
RES_Y = 240

# This can be varied to see the effect of the number of bits per pixel
BITS_PER_PIXEL = 4
# Creating a mask to select the requisite number of bits
mask = np.uint8(int('1'*BITS_PER_PIXEL+'0'*(8-BITS_PER_PIXEL), 2))

# Open and get access to the camera at specified resolution and FPS
if MODE == "camera":
    camera = iio.get_reader("<video0>", size=(RES_X, RES_Y))

# Open the serial port at specified baud rate
ComPort = serial.Serial(COMPORT)
ComPort.baudrate = BAUD_RATE
ComPort.bytesize = 8    # Number of data bits = 8
ComPort.parity   = 'N'  # No parity
ComPort.stopbits = 1    # Number of Stop bits = 1

if MODE == "camera":
    n_frames = 1

captured = np.zeros((RES_X, RES_Y, 3), dtype=np.uint8)
buffer = np.zeros((RES_X, RES_Y, 3), dtype=np.uint8)
packed = np.zeros(RES_X * RES_Y, dtype=np.uint16)


print(f"Starting at {RES_X}x{RES_Y} for {n_frames} frames")

# Iterate for a certain number of frames, set above
for frame_counter in range(n_frames):
    if MODE == "camera":
        # Get the frame from the camera, and reshape
        captured = np.asarray(camera.get_next_data())

        captured = np.rot90(captured, 1, axes=(0, 1))
        captured = captured.reshape(RES_X, RES_Y, 3)

        buffer = np.bitwise_and(captured, mask)


    # This array will be sent over UART
    for index, pixel in enumerate(buffer.astype(np.uint16).reshape(-1, 3)[:, :]):
        R, G, B = pixel
        
        R = format(R, "08b")
        G = format(G, "08b")
        B = format(B, "08b")
        packed[index] = int(f"0{R[0:4]}{G[0:2]}00{G[2:4]}{B[0:4]}0", 2)

    byte_stream = packed.astype(np.uint16).tobytes()
    print(byte_stream)

    start = time.perf_counter()
    ComPort.write(byte_stream)

    print(f"Frame {frame_counter+1} sent in {round(time.perf_counter() - start, 2)}s")

if MODE == "camera":
    camera.close()

ComPort.close()
print("Done streaming")


