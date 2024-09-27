import time
import psutil  # For fetching CPU load
from sense_hat import SenseHat
import math

# Define global variables
SCREEN_RES_WIDTH = 8
SCREEN_RES_HEIGHT = 8
OFF_PIXEL = [0, 0, 0]
BAR_COLOR = [128, 128, 128]
TIP_COLOR = [255, 255, 0] # Yellow
ANIMATE_TIP_COLOR = [255, 0, 0] # Red
display_buffer = [OFF_PIXEL for _ in range(SCREEN_RES_WIDTH * SCREEN_RES_HEIGHT)]
queue = []

# Initialize SenseHat instance
sense = SenseHat()
sense.low_light = True

# Function to map CPU load to screen height (0 to SCREEN_RES_HEIGHT)
def map_cpu_to_height(cpu_load):
    if cpu_load == 0:
        return 0
    return math.ceil(cpu_load / (100.0 / SCREEN_RES_HEIGHT))

# Function to draw a line on the display buffer
def draw_line(x1, y1, x2, y2, color):
    if x1 == x2:  # Vertical line
        for y in range(y1, y2 + 1):
            sense.set_pixel(x1, y, color[0], color[1], color[2])
    elif y1 == y2:  # Horizontal line
        for x in range(x1, x2 + 1):
            sense.set_pixel(x, y1, color[0], color[1], color[2])

def draw_line_buf(x1, y1, x2, y2, color):
    global display_buffer

    if x1 == x2:  # Vertical line
        for y in range(y1, y2 + 1):
            index = y * SCREEN_RES_WIDTH + x1
            if 0 <= index < SCREEN_RES_WIDTH * SCREEN_RES_HEIGHT:
                display_buffer[index] = color
    elif y1 == y2:  # Horizontal line
        for x in range(x1, x2 + 1):
            index = y1 * SCREEN_RES_WIDTH + x
            if 0 <= index < SCREEN_RES_WIDTH * SCREEN_RES_HEIGHT:
                display_buffer[index] = color
    sense.set_pixels(display_buffer)

def reset_display():
    global display_buffer

    sense.clear()
    display_buffer = ([OFF_PIXEL for _ in range(SCREEN_RES_WIDTH * SCREEN_RES_HEIGHT)])

# Function to update the display buffer based on the queue
def update_display(queue, animating=False):
    reset_display()
    for x in range(len(queue)):
        height = queue[x]
        if height > 1:
            # Draw bar
            draw_line_buf(x, SCREEN_RES_HEIGHT - height + 1, x, SCREEN_RES_HEIGHT - 1, BAR_COLOR)
            # Draw tip
            draw_line_buf(x, SCREEN_RES_HEIGHT - height, x, SCREEN_RES_HEIGHT - height, ANIMATE_TIP_COLOR if animating and x == len(queue) - 1 else TIP_COLOR)
        elif height > 0: # height = 1
            # Draw tip
            draw_line_buf(x, SCREEN_RES_HEIGHT - height, x, SCREEN_RES_HEIGHT - 1, TIP_COLOR)

def animate_display(queue):
    # Get the last element of the queue and store its value
    last_value = queue[-1]
     # Animate only if last value is greater than 1
    if last_value > 1:
        # Create a temporary queue for the animation
        temp_queue = queue[:-1] + [0]  # Start with the last element as 0

        for i in range(1, last_value):
            # Update the last element in the temp queue to gradually increase
            temp_queue[-1] = i
            update_display(temp_queue, True)
            time.sleep(0.1)

        temp_queue[-1] = last_value
        update_display(temp_queue)
    else:
        update_display(queue)

def map_load_queue(queue):
     # Map the CPU load values in the queue to screen height values (0 to SCREEN_RES_HEIGHT)
    mapped_queue = []

    # Left pad with 0 if the queue has fewer than SCREEN_RES_WIDTH elements
    padding_size = SCREEN_RES_WIDTH - len(queue)
    mapped_queue = [0] * padding_size

    # Map the CPU load values from 0-100 to 0-8
    for load in queue:
        mapped_queue.append(map_cpu_to_height(load))

    return mapped_queue

# Main run loop
def main():
    global queue
    try:
        while True:
            # Fetch CPU load and add it to the queue
            cpu_load = psutil.cpu_percent(interval=1)

            # Push new CPU load into the queue, keeping the queue size to SCREEN_RES_WIDTH
            queue.append(cpu_load)
            if len(queue) > SCREEN_RES_WIDTH:
                queue.pop(0)

            # Update the display
            mapped_queue = map_load_queue(queue)
            animate_display(mapped_queue)

            # Delay for 10 seconds
            time.sleep(10)
    except KeyboardInterrupt:
        print("Process interrupted by user.")
        sense.low_light = False
        sense.clear()

if __name__ == "__main__":
    main()
