import pygame
import random

class ICTone:
    def __init__(self,screen):
        self.screen = screen
        self.background = pygame.image.load('./resources/textures/task-backgrounds/ict-1.png')
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.score = 0
        self.current_decimal = random.randint(0,255)
        self.binary_boxes = 8 * [0]
        self.selected = None
        self.message = ""
        self.message_color = (0,255,0)
        self.crt_surface = pygame.Surface((1280, 720))
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/минута-на-размышление.mp3")
        pygame.mixer.music.play(-1)
    
    def decimal_to_binary(self,decimal, length):
        return format(decimal, f'0{length}b')

    def draw_text(self, text, position, color=(0,255,0)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_binary_boxes(self,binary_list, position):
        global selected_box
        for i, bit in enumerate(binary_list):
            box_x = position[0] + i * (36 + 10)
            box_y = position[1]
            color = (255,0,0) if i == self.selected else (0,255,0)
            self.draw_text(str(bit), (box_x, box_y), color)

    def reset_game(self):
        self.current_decimal = random.randint(0, 255)
        self.binary_boxes = [0] * 8
        
        self.selected_box = None

    def check_answer(self):
        user_binary_str = ''.join(map(str, self.binary_boxes))
        correct_binary_str = self.decimal_to_binary(self.current_decimal, 8)
        
        print(user_binary_str, correct_binary_str)

        if user_binary_str == correct_binary_str:
            self.score += 1
            self.message = "Верно!"
            self.message_color = (0,255,0)
        else:
            if self.score > 0:
                self.score -= 1
            self.message = "Неправильно!"
            self.message_color = (255,0,0)
            #self.highlight_error()
        
        pygame.display.flip()
        self.reset_game()

    def apply_crt_effect(surface):
        # Apply scanlines
        for y in range(0, 720, 4):
            pygame.draw.line(surface, (0, 0, 0), (0, y), (1280, y), 1)
        
        # Apply curvature (simple pin-cushion distortion)
        new_surface = pygame.transform.scale(surface, (1280 + 20, 720 + 20))
        new_surface = pygame.transform.smoothscale(new_surface, (1280, 720))

        # Apply noise
        noise = pygame.Surface((1280, 720))
        noise.lock()
        for x in range(1280):
            for y in range(720):
                color = random.randint(0, 30)
                noise.set_at((x, y), (color, color, color))
        noise.unlock()
        surface.blit(noise, (0, 0), special_flags=pygame.BLEND_ADD)

    def draw(self):
        self.screen.fill((0,0,0))

        self.draw_text(f"Переведите данное число в двоичную систему счисления.", (50, 150))  
        self.draw_text(f"Нажмите цифру, чтобы помять её на 0 или 1.", (50, 200))        
        
        # Draw the current decimal number
        self.draw_text(f"Число: {self.current_decimal}", (50, 100))
        
        # Draw the binary boxes
        self.draw_text("0b", (350, 350))
        self.draw_binary_boxes(self.binary_boxes, (400, 350))
        
        # Draw the check button
        pygame.draw.rect(self.crt_surface, (0,255,0), (325, 450, 150, 50))
        self.draw_text("Проверить", (360, 460))

        # Draw the score and message
        self.draw_text(f"Счёт: {self.score}", (50, 50))
        self.draw_text(self.message, (325, 350), self.message_color)
    
