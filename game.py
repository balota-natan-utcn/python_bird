import pygame
import random
import sys

pygame.init()

#game constants
screen_width = 400
screen_height= 600
bird_size = 30
pipe_width = 60
pipe_gap = 150
gravity = 0.5
jump_strength = -8
pipe_speed = 3

#colors
white = (255, 255, 255)
green = (0, 128, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
blue = (135, 206, 235)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = screen_height // 2
        self.velocity = 0
        self.size = bird_size
    
    def jump(self):
        self.velocity = jump_strength

    def update(self):
        self.velocity += gravity
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, yellow, (int(self.x), int(self.y)), self.size)
        #simple eye
        pygame.draw.circle(screen, black, (int(self.x + 10), int(self.y - 5)), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(pipe_gap, screen_height - pipe_gap)
        self.passed = False

    def update(self):
        self.x -= pipe_speed

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, green, 
                        (self.x, 0, pipe_width, self.gap_y - pipe_gap // 2))
        # Bottom pipe
        pygame.draw.rect(screen, green, 
                        (self.x, self.gap_y + pipe_gap // 2, pipe_width, 
                         screen_height - (self.gap_y + pipe_gap // 2)))
        
        # Pipe caps
        pygame.draw.rect(screen, green, 
                        (self.x - 5, self.gap_y - pipe_gap // 2 - 20, 
                         pipe_width + 10, 20))
        pygame.draw.rect(screen, green, 
                        (self.x - 5, self.gap_y + pipe_gap // 2, 
                         pipe_width + 10, 20))
    
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, pipe_width, self.gap_y - pipe_gap // 2)
        bottom_rect = pygame.Rect(self.x, self.gap_y + pipe_gap // 2, pipe_width, 
                                 screen_height - (self.gap_y + pipe_gap // 2))
        return [top_rect, bottom_rect]
    
    def is_off_screen(self):
        return self.x + pipe_width < 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
    
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_timer = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.bird.jump()
        return True
    
    def update(self):
        if not self.game_over:
            # Update bird
            self.bird.update()
            
            # Check if bird hits ground or ceiling
            if self.bird.y > screen_height or self.bird.y < 0:
                self.game_over = True
            
            # Add new pipes
            self.pipe_timer += 1
            if self.pipe_timer > 90:  # Add pipe every 1.5 seconds at 60 FPS
                self.pipes.append(Pipe(screen_width))
                self.pipe_timer = 0
            
            # Update pipes
            for pipe in self.pipes[:]:
                pipe.update()
                
                # Check collision
                bird_rect = self.bird.get_rect()
                for pipe_rect in pipe.get_rects():
                    if bird_rect.colliderect(pipe_rect):
                        self.game_over = True
                
                # Check if pipe passed
                if not pipe.passed and pipe.x + pipe_width < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                
                # Remove off-screen pipes
                if pipe.is_off_screen():
                    self.pipes.remove(pipe)
    
    def draw(self):
        # Background
        self.screen.fill(blue)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, white)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, white)
            restart_text = self.font.render("Press SPACE to restart", True, white)
            
            game_over_rect = game_over_text.get_rect(center=(screen_width//2, screen_height//2))
            restart_rect = restart_text.get_rect(center=(screen_width//2, screen_height//2 + 40))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()