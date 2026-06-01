import pygame
import random
import math

# CONFIG CONSTANTS
WIDTH = 800
HEIGHT = 600
FPS = 60

# COLOR PALETTE
COLOR_BLACK = (10, 15, 10)
COLOR_DARK_GREEN = (0, 60, 0)
COLOR_RADAR_GREEN = (50, 255, 50)

class RadarEntity:
    """
    Represents a dynamic entity (ship/plane) on the radar screen.
    Handles its own position, velocity, and movement logic.
    """

    def __init__(self):
        self.x = random.uniform(50, WIDTH - 50)
        self.y = random.uniform(50, HEIGHT - 50)
        
        # Velocity vectors for movement
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(-0.5, 0.5)

    def update_position(self):
        """Moves the entity and handles boundary collisions."""
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Reverse direction if hitting the screen boundaries
        if self.x <= 0 or self.x >= WIDTH:
            self.velocity_x *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.velocity_y *= -1

def draw_radar_background(screen, sweep_angle):
    """Draws the static radar rings and the rotating sweep line."""
    screen.fill(COLOR_BLACK)
    center_point = (WIDTH // 2, HEIGHT // 2)
    
    # Draw radar rings
    for radius in range(50, 400, 50):
        pygame.draw.circle(screen, COLOR_DARK_GREEN, center_point, radius, 1)
        
    # Draw central crosshairs
    pygame.draw.line(screen, COLOR_DARK_GREEN, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
    pygame.draw.line(screen, COLOR_DARK_GREEN, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)

    # Draw the rotating line
    end_x = center_point[0] + 400 * math.cos(sweep_angle)
    end_y = center_point[1] + 400 * math.sin(sweep_angle)
    pygame.draw.line(screen, COLOR_RADAR_GREEN, center_point, (end_x, end_y), 2)

def start_radar_simulation():
    """
    Initializes the Pygame window and runs the main simulation loop.
    """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Radar Simulation - Visual Test")
    clock = pygame.time.Clock()

    # Initialize a list of random radar entities
    radar_entities = [RadarEntity() for _ in range(15)]
    sweep_angle = 0.0 

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        # UPDATE DOTS
        for entity in radar_entities:
            entity.update_position()
        sweep_angle += 0.02

        # RENDER GRAPHICS
        draw_radar_background(screen, sweep_angle)

        # Calculate and draw all pairs within a danger threshold
        from algorithms.closest_pair import get_pairs_within_distance
        DANGER_DISTANCE = 80.0
        dangerous_pairs = get_pairs_within_distance(radar_entities, DANGER_DISTANCE)
        
        dangerous_entities = set()
        for p1, p2 in dangerous_pairs:
            pygame.draw.line(screen, (255, 100, 50), (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), 2)
            dangerous_entities.add(p1)
            dangerous_entities.add(p2)

        # Render entities
        for entity in radar_entities:
            # Highlight the dangerous points
            color = (255, 50, 50) if entity in dangerous_entities else COLOR_RADAR_GREEN
            radius = 5 if entity in dangerous_entities else 3
            pygame.draw.circle(screen, color, (int(entity.x), int(entity.y)), radius)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()