import pygame

DIALOG_BOX_HEIGHT = 150
DIALOG_BOX_PADDING = 20

class DialogBox:
    def __init__(self, screen, lines):
        self.screen = screen
        self.lines = lines  # List of strings to display
        self.current_line = 0
        self.current_char = 0
        self.finished = True
        self.started = False
        self.text_surface = None
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.max_width = 1280 - 2 * (DIALOG_BOX_PADDING + 20)  # Maximum width for text before wrapping
        self.next_line()
    
    def wrap_text(self, text):
        """Wrap text into lines that fit within the dialog box width."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            if self.font.size(test_line)[0] <= self.max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word

        wrapped_lines.append(current_line)
        return wrapped_lines

    def next_line(self):
        """Move to the next line or finish the dialog."""
        if self.current_line < len(self.lines):
            self.current_char = 0
            # Wrap the current line text to fit the dialog box width
            wrapped_lines = self.wrap_text(self.lines[self.current_line])
            self.current_line_text = wrapped_lines
            self.current_line += 1
        else:
            self.finished = True

    def update(self):
        """Update the text display (simulate typewriter effect)."""
        if not self.finished:
            if self.current_char < len(self.current_line_text):
                self.current_char += 1
                text_to_display = ' '.join(self.current_line_text[:self.current_char])
                self.text_surface = self.font.render(text_to_display, True, (255,255,255))

    def draw(self, surface):
        """Draw the dialog box and the current line of text."""
        # Draw dialog box background
        dialog_box_rect = pygame.Rect(DIALOG_BOX_PADDING, 720 - DIALOG_BOX_HEIGHT - DIALOG_BOX_PADDING,
                                      1280 - 2 * DIALOG_BOX_PADDING, DIALOG_BOX_HEIGHT)
        pygame.draw.rect(surface, (0,0,0), dialog_box_rect)

        # Draw the current text line
        if self.text_surface:
            y_offset = 720 - DIALOG_BOX_HEIGHT - DIALOG_BOX_PADDING + 20
            for line in self.current_line_text:
                line_surface = self.font.render(line, True, (255,255,255))
                surface.blit(line_surface, (DIALOG_BOX_PADDING + 20, y_offset))
                y_offset += self.font.get_linesize()

    def advance(self):
        """Advance to the next line of dialog."""
        if self.current_char == len(self.current_line_text):
            self.next_line()

    def display(self):
        # Update the dialog box
        self.update()

        # Draw the dialog box
        self.draw(self.screen)
        
        # Update the display
        pygame.display.flip()

        # Delay to control text speed
        pygame.time.delay(20)
