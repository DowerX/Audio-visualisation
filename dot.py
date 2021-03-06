import pygame as pygame
from pygame import gfxdraw
import pyaudio
import struct
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#SETTINGS
size = (1024, 256)
chunk = 1024
stepsize = 1
filter_255 = False
filter_2 = True
max_fps = 30
width_of_col = 1
scale = 1
skip_under = 0

#Init
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("AV")
done = False
clock = pygame.time.Clock()


p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    output=True,
    as_loopback=True,
    input_device_index=1, #0 laptop , 3 fejes
    frames_per_buffer=chunk
)


while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    temp = stream.read(chunk)
    data = struct.unpack(f"{str(2*chunk)}B", temp)

    screen.fill(BLACK)

    x = 0
    for i in range(len(data)//stepsize):
        if i%2 == 0 and filter_2:
            #x += 1
            continue

        if x > size[0]:
            continue

        if data[i*stepsize] >= 255 and filter_255:
            continue
        
        if data[i*stepsize] < skip_under:
            continue

        if data[i*stepsize] > 127:
            gfxdraw.pixel(screen, x, size[1]-data[i*stepsize]*scale+127*scale, WHITE)
        else:
            gfxdraw.pixel(screen, x, -data[i*stepsize]*scale+127, WHITE)
        x += 1

    pygame.display.flip()

    #print(x)
    pygame.display.set_caption(f"AV {int(clock.get_fps())+1}fps")
    clock.tick(max_fps)

pygame.quit()