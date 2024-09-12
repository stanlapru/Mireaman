import pygame

class DialogBox:
    def __init__(self, screen, max_width=600):
        self.screen = screen
        self.dialog_active = False
        self.text_lines = []
        self.max_width = max_width  # Max width for the wrapped text area
        self.padding = 10  # Padding inside the dialog box
        self.dialog_rect = pygame.Rect(50, 500, max_width + self.padding * 2, 200)  # Dialog box area
        self.text_color = (255, 255, 255)
        self.npc_image = None
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.npc_name = ""
        self.dialog_data = None
        self.dialog_index = 0
        self.current_dialog = None

    def set_dialog_data(self, dialog_data):
        self.dialog_data = dialog_data
    
    def wrap_text(self, text):
        """Wraps the given text into lines that fit within the max_width."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = ''
        
        for word in words:
            if self.font.size(current_line + word)[0] > self.max_width:
                wrapped_lines.append(current_line)
                current_line = word + ' '
            else:
                current_line += word + ' '
        
        if current_line:
            wrapped_lines.append(current_line.strip())
        
        return wrapped_lines

    def load_dialog(self, dialog_id):
        """Loads dialog text, NPC name, and image based on dialog ID."""
        self.dialog_index = 0  # Reset the dialog to the first line
        dialog = self.dialog_data.get(dialog_id)
        print(dialog)
        if dialog:
            self.current_dialog = dialog['lines']  # Assume this is a list of dialog strings for multi-line conversations
            self.update_current_dialog()
            self.npc_name = dialog['npc_name']
            self.npc_image = pygame.image.load(dialog['npc_image']).convert_alpha()
            self.npc_image = pygame.transform.scale(self.npc_image, (64, 64))  # Scale the image to fit
            self.dialog_active = True

    def update_current_dialog(self):
        """Update the current dialog text with wrapping."""
        if self.current_dialog and self.dialog_index < len(self.current_dialog):
            self.text_lines = self.wrap_text(self.current_dialog[self.dialog_index])

    def advance(self):
        """Advance to the next part of the dialog."""
        if self.dialog_active:
            self.dialog_index += 1
            if self.dialog_index < len(self.current_dialog):
                self.update_current_dialog()
            else:
                self.dialog_active = False  # End of dialog

    def render(self):
        if self.dialog_active:
            # Draw the dialog box background
            pygame.draw.rect(self.screen, (0, 0, 0), self.dialog_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.dialog_rect, 2)

            # Draw the NPC image (to the left of the dialog)
            image_pos = (self.dialog_rect.x + self.padding, self.dialog_rect.y + self.padding)
            if self.npc_image:
                self.screen.blit(self.npc_image, image_pos)

            # Draw the NPC name
            name_pos = (image_pos[0] + 70, self.dialog_rect.y + self.padding)
            name_render = self.font.render(self.npc_name, True, self.text_color)
            self.screen.blit(name_render, name_pos)

            # Adjust text position to accommodate the NPC image and name
            text_x = name_pos[0]
            text_y = name_pos[1] + self.font.get_height() + 10  # Move text below the NPC name

            # Draw each wrapped line of text
            for line in self.text_lines:
                rendered_text = self.font.render(line, True, self.text_color)
                self.screen.blit(rendered_text, (text_x, text_y))
                text_y += self.font.get_height() + 5  # Adjust line spacing
