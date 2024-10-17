import pygame
import time

# Initialize Pygame
pygame.init()

# Set the width and height of the screen [width, height]
screen_size = 800  # Adjusted for the two elevators
screen = pygame.display.set_mode((screen_size, screen_size))

# Load images
# Replace 'ele.png', 'man.png', 'floor.png', 'door_open.png', and 'door_closed.png' with your own images
elevator_img_open = pygame.image.load('elevator_1.jpeg')
elevator_img_closed = pygame.image.load('elevator_2.jpeg')
person_img = pygame.image.load('man.png')
floor_img = pygame.image.load('floor.png')

# Function to draw the elevator animation
def animate_elevator(people_on_each_floor, num_floors, target_floor, target_floor_second, door_status_first, door_status_second):
    global screen_size, elevator_img_open, elevator_img_closed, person_img, floor_img
    # Adjust image sizes to fit the screen
    floor_height = screen_size // min(num_floors, 10)
    elevator_img_open = pygame.transform.scale(elevator_img_open, (floor_height, floor_height))
    elevator_img_closed = pygame.transform.scale(elevator_img_closed, (floor_height, floor_height))
    person_img = pygame.transform.scale(person_img, (floor_height // 3, floor_height // 3))
    floor_img = pygame.transform.scale(floor_img, (screen_size, floor_height))
    clock = pygame.time.Clock()
    running = True
    elevator_width = elevator_img_open.get_width()
    elevator_height = elevator_img_open.get_height()
    person_width = person_img.get_width()
    person_height = person_img.get_height()
    elevator_y = screen_size - floor_height  # Set the first elevator to the first floor
    target_offset = floor_height // 2  # Set the offset for the elevator stop position
    target_y = screen_size - ((target_floor - 1) * floor_height) - floor_height + target_offset  # Calculate the target position with the offset
    second_elevator_y = screen_size - floor_height  # Set the second elevator to the first floor
    target_y_second = screen_size - ((target_floor_second - 1) * floor_height) - floor_height + target_offset  # Calculate the target position for the second elevator with the offset
    font = pygame.font.Font(None, 36)  # Font for the labels
    current_scroll = 0
    max_scroll = max(0, (num_floors - 10) * floor_height)  # Maximum amount of scroll
    while elevator_y > target_y or second_elevator_y > target_y_second:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        # Draw floors and labels
        font = pygame.font.Font(None, 36)  # Set the font and size
        for i in range(num_floors):
            floor_surface = floor_img.copy()  # Create a copy of the floor image
            text = font.render(str(i + 1), True, (0, 0, 0))  # Render the floor number with black color
            text_rect = text.get_rect(center=(floor_height // 2, floor_height // 2))  # Set the position of the text
            floor_surface.blit(text, text_rect)  # Blit the text onto the floor surface
            screen.blit(floor_surface, (0, screen_size - (i - current_scroll + 1) * floor_height))
        # Draw people on each floor
        center_x = screen_size // 2
        center_y = screen_size // 2
        max_people_on_floor = max(people_on_each_floor[:num_floors])
        x_pos_start = center_x - (max_people_on_floor * (person_width + 5)) // 2
        for floor, people in enumerate(people_on_each_floor[:num_floors]):
            y_pos = screen_size - (floor - current_scroll) * floor_height - person_height
            x_pos = x_pos_start
            for _ in range(people):
                screen.blit(person_img, (x_pos, y_pos))
                x_pos += person_width + 5
        # Draw elevator cell background
        pygame.draw.rect(screen, (0, 0, 0), (screen_size - floor_height, 0, floor_height, screen_size))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, floor_height, screen_size))
        # Draw first elevator
        if door_status_first:
            screen.blit(elevator_img_open, (screen_size - elevator_width, elevator_y - elevator_height // 2 - current_scroll * floor_height))
        else:
            screen.blit(elevator_img_closed, (screen_size - elevator_width, elevator_y - elevator_height // 2 - current_scroll * floor_height))
        # Draw second elevator
        if door_status_second:
            screen.blit(elevator_img_open, (0, second_elevator_y - elevator_height // 2 - current_scroll * floor_height))
        else:
            screen.blit(elevator_img_closed, (0, second_elevator_y - elevator_height // 2 - current_scroll * floor_height))
        pygame.display.flip()
        clock.tick(60)
        if elevator_y > target_y:
            elevator_y -= 0.8  # Move the first elevator upwards faster
        if second_elevator_y > target_y_second:
            second_elevator_y -= 0.8  # Move the second elevator upwards faster
        if elevator_y <= target_y and second_elevator_y <= target_y_second:
            break
        time.sleep(0.006)  # Adjust the speed
        if elevator_y <= target_y and second_elevator_y <= target_y_second:
            break
    time.sleep(2)

def call_animation_periodically(people_on_each_floor, num_floors, target_floor, target_floor_second, door_status_first, door_status_second):
    while True:
        animate_elevator(people_on_each_floor, num_floors, target_floor, target_floor_second, door_status_first, door_status_second)
        time.sleep(1)  # Wait for 1 second before calling the function again

# Example usage:
people_on_each_floor = [3, 2, 1, 0, 4, 2, 1, 3, 0, 9]  # Example data for 16 floors
num_floors = len(people_on_each_floor)
target_floor = 10
target_floor_second = 3
door_status_first = True  # Example boolean for the first elevator door status
door_status_second = False  # Example boolean for the second elevator door status
call_animation_periodically(people_on_each_floor, num_floors, target_floor, target_floor_second, door_status_first, door_status_second)
