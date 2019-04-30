import pygame as pygame
import pyaudio
import struct
import time
import wave

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#SETTINGS
size = (512, 256)
chunk = 1024
stepsize = 1
filter_255 = True
filter_2 = True
max_fps = 60
width_of_col = 1
scale = 1
skip_under = 0
file_path = "./File0161.wav"


#Init
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("AV")
done = False
clock = pygame.time.Clock()

wf = wave.open(file_path, "rb")

p = pyaudio.PyAudio()
stream = p.open(
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(),
    output=True,
    input=True
)


while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    temp = wf.readframes(chunk)

    if len(temp) < 4096:
        done = True
        break

    data = struct.unpack(f"{str(4*chunk)}B", temp)
    stream.write(temp)

    screen.fill(BLACK)

    pygame.draw.line(screen, WHITE, (0, size[1]//2), (size[0], size[1]//2), 1)

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
            pygame.draw.line(screen, WHITE, (x, size[1]//2), (x, size[1]-data[i*stepsize]*scale+127*scale), width_of_col)
        else:
            pygame.draw.line(screen, WHITE, (x, size[1]//2), (x, -data[i*stepsize]*scale+127), width_of_col)
        x += 1

    pygame.display.flip()

    #print(x)
    pygame.display.set_caption(f"AV {int(clock.get_fps())+1}fps")
    clock.tick(max_fps)

pygame.quit()