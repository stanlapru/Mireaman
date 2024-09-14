import pygame

class DialogBox:
    def __init__(self, screen, max_width=800):
        self.screen = screen
        self.dialog_active = False
        self.text_lines = []
        self.max_width = max_width  # Max width for the wrapped text area
        self.padding = 10  # Padding inside the dialog box
        self.line_width = screen.get_width() - 200
        self.dialog_rect = pygame.Rect(50, 500, self.line_width + self.padding * 2, 200)  # Dialog box area
        self.text_color = (255, 255, 255)
        self.npc_image = None
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.npc_name = ""
        self.dialog_data = None
        self.dialog_index = 0
        self.current_dialog = None
        self.rect = pygame.Rect(0, screen.get_height() - 300, screen.get_width(), 300)
        
        self.cursor_images = [
            pygame.transform.scale(pygame.image.load('./resources/textures/cursor/dialog/cursor1.png').convert_alpha(), (48, 48)),
            pygame.transform.scale(pygame.image.load('./resources/textures/cursor/dialog/cursor2.png').convert_alpha(), (48, 48))
        ]
        self.cursor_image = self.cursor_images[0]  # Start with the first cursor image
        self.cursor_index = 0
        self.cursor_position = (self.rect.x + self.rect.width - 100, self.rect.y + self.rect.height - 100)  # Adjust position
        # Timer for switching the cursor every 500ms
        self.cursor_animation_timer = 0
        self.cursor_animation_interval = 500  # 500 milliseconds

    def set_dialog_data(self, dialog_data):
        self.dialog_data = dialog_data
    
    def wrap_text(self, text):
        """Wraps the given text into lines that fit within the max_width."""
        words = text.split(' ')  # Split the text into words
        wrapped_lines = []
        current_line = ''
        
        for word in words:
            if self.font.size(current_line + word)[0] > self.line_width:
                wrapped_lines.append(current_line)  # Add the current line if it exceeds max width
                current_line = word + ' '
            else:
                current_line += word + ' '
        
        if current_line:
            wrapped_lines.append(current_line.strip())  # Add the last line
        
        return wrapped_lines


    def load_dialog(self, dialog_id):
        """Loads dialog text, NPC name, and image based on dialog ID."""
        self.dialog_index = 0  # Reset the dialog to the first line

        # Split dialog_id to access nested dialog data
        parts = dialog_id.split('.')
        dialog = self.dialog_data.get(parts[0], {}).get(parts[1], None)

        if dialog:
            # Load the dialog lines, NPC name, and texture
            self.current_dialog = dialog['lines']  # List of dialog strings
            self.update_current_dialog()
            self.npc_name = dialog['npc_name']
            self.npc_image = pygame.image.load(dialog['npc_texture']).convert_alpha()
            self.npc_image = pygame.transform.scale(self.npc_image, (64, 64))  # Scale the image to fit
            self.dialog_active = True
        else:
            print(f"Dialog ID {dialog_id} not found.")


    def update_current_dialog(self):
        """Updates the currently displayed dialog text and handles wrapping."""
        if self.current_dialog and self.dialog_index < len(self.current_dialog):
            # Extract the text from the current dialog line (which is a dictionary)
            current_line = self.current_dialog[self.dialog_index]
            if isinstance(current_line, dict) and 'text' in current_line:
                wrapped_text = self.wrap_text(current_line['text'])  # Correctly access 'text' value
                self.displayed_text = wrapped_text  # Store the wrapped lines for rendering
            else:
                print(f"Error: Current dialog line is not properly formatted: {current_line}")
        else:
            print("Dialog has finished.")


    def advance(self):
        """Advance to the next line of the dialog."""
        if self.current_dialog:
            if self.dialog_index < len(self.current_dialog) - 1:
                # Move to the next line
                self.dialog_index += 1
                self.update_current_dialog()
            else:
                # End of dialog; reset dialog state
                self.dialog_active = False
                self.current_dialog = None
                self.displayed_text = []
                self.dialog_index = 0
        else:
            print("No dialog is currently active.")

    def update_cursor_animation(self):
        """Updates the cursor animation by cycling between the two cursor images."""
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_animation_timer > self.cursor_animation_interval:
            self.cursor_animation_timer = current_time
            self.cursor_index = (self.cursor_index + 1) % 2  # Switch between 0 and 1
            self.cursor_image = self.cursor_images[self.cursor_index]
    
    def render(self):
        """Render the dialog box, NPC image, name, and wrapped dialog text."""
        # Draw the dialog box background
        pygame.draw.rect(self.screen, (0, 0, 0, 0), self.rect)
        
        # Render the NPC image
        if self.npc_image:
            self.screen.blit(self.npc_image, (self.rect.x + 20, self.rect.y + 20))
        
        # Render the NPC name
        if self.npc_name:
            name_surface = self.font.render(self.npc_name, True, pygame.Color('yellow'))
            self.screen.blit(name_surface, (self.rect.x + 100, self.rect.y + 20))
        
        # Render the dialog text (wrapped lines)
        if self.displayed_text:
            y_offset = self.rect.y + 80  # Start below the NPC name
            for line in self.displayed_text:
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (self.rect.x + 100, y_offset))
                y_offset += text_surface.get_height() + 5  # Line spacing
                
        # Update and render the animated cursor
        self.update_cursor_animation()
        self.screen.blit(self.cursor_image, self.cursor_position)

