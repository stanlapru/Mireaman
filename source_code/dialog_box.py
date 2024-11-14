import pygame, json

class DialogBox:
    def __init__(self, screen, data, game, max_width=800):
        self.screen = screen
        self.data = data
        self.game = game
        self.dialog_active = False
        self.text_lines = []
        self.max_width = max_width  
        self.padding = 10  
        self.line_width = screen.get_width() - 200
        self.dialog_rect = pygame.Rect(50, 500, self.line_width + self.padding * 2, 200)  
        self.text_color = (255, 255, 255)
        self.npc_image = None
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.npc_name = ""
        self.dialog_data = None
        self.dialog_index = 0
        self.current_dialog = None
        self.rect = pygame.Rect(0, screen.get_height() - 300, screen.get_width(), 300)
        self.task = 'ict1'
        
        self.cursor_images = [
            pygame.transform.scale(pygame.image.load('./resources/textures/cursor/dialog/cursor1.png').convert_alpha(), (48, 48)),
            pygame.transform.scale(pygame.image.load('./resources/textures/cursor/dialog/cursor2.png').convert_alpha(), (48, 48))
        ]
        self.cursor_image = self.cursor_images[0] 
        self.cursor_index = 0
        self.cursor_position = (self.rect.x + self.rect.width - 100, self.rect.y + self.rect.height - 100)  
        self.cursor_animation_timer = 0
        self.cursor_animation_interval = 500
        
        self.choice_buttons = {
            'yes': pygame.image.load('resources/textures/cursor/dialog/tick.png').convert_alpha(),
            'no': pygame.image.load('resources/textures/cursor/dialog/cross.png').convert_alpha()
        }
        self.choice_selected = None
        self.choice_action = None
        self.choice_texts = None
        self.choice_rects = {
            'yes': self.choice_buttons['yes'].get_rect(topleft=(800, 500)),  
            'no': self.choice_buttons['no'].get_rect(topleft=(900, 500))
        }
        self.show_choices = False

    def set_dialog_data(self, dialog_data):
        self.dialog_data = dialog_data
    
    def wrap_text(self, text):
        words = text.split(' ')  
        wrapped_lines = []
        current_line = ''
        
        for word in words:
            if self.font.size(current_line + word)[0] > self.line_width:
                wrapped_lines.append(current_line)  
                current_line = word + ' '
            else:
                current_line += word + ' '
        
        if current_line:
            wrapped_lines.append(current_line.strip())  
        
        return wrapped_lines


    def load_dialog(self, npc_id, dialog_section):
        self.npc_id = npc_id
        self.dialog_index = 0 
        dialog = self.dialog_data.get(npc_id, {}).get(dialog_section)

        if dialog:
            self.current_dialog_root = dialog
            self.current_dialog = dialog['lines']
            self.update_current_dialog()
            self.npc_name = dialog['npc_name']
            self.npc_image = pygame.image.load(dialog['npc_texture']).convert_alpha()
            self.npc_image = pygame.transform.scale_by(self.npc_image, 1)  
            self.dialog_active = True 
        else:
            print(f"Dialog section '{dialog_section}' for NPC '{npc_id}' not found.")

    def update_current_dialog(self):
        # if self.current_dialog and self.dialog_index < len(self.current_dialog):
        #     # Extract the text from the current dialog line (which is a dictionary)
        #     current_line = self.current_dialog[self.dialog_index]
        #     if isinstance(current_line, dict) and 'text' in current_line:
        #         wrapped_text = self.wrap_text(current_line['text'])  # Correctly access 'text' value
        #         self.displayed_text = wrapped_text  # Store the wrapped lines for rendering
        #     else:
        #         print(f"Error: Current dialog line is not properly formatted: {current_line}")
        # else:
        #     print("Dialog has finished.")
        if self.current_dialog:
            if self.dialog_index < len(self.current_dialog):
                current_line = self.current_dialog[self.dialog_index]
                if isinstance(current_line, dict) and 'text' in current_line:
                    wrapped_text = self.wrap_text(current_line['text']) 
                    self.displayed_text = wrapped_text 
                else:
                    print(f"Error: Current dialog line is not properly formatted: {current_line}")
                    
            else:
                self.dialog_index = 1000
                
            print(self.dialog_index)
            if self.dialog_index == 1000:
                print(self.current_dialog, self.current_dialog_root)
                
                if 'next' in self.current_dialog_root:
                    next_section = self.current_dialog_root['next']
                    self.load_dialog(self.npc_id, next_section)  
                else:
                    # No more dialog; end conversation
                    self.dialog_active = False
                    self.current_dialog = None
                    self.current_dialog_root = None
                    print("End of dialog.")
        else:
            print("No active dialog to update.")


    def advance(self):
        if self.current_dialog:
            if self.dialog_index < len(self.current_dialog) :
                # Move to the next line
                self.dialog_index += 1
                self.update_current_dialog()
            else:
                # End of dialog
                self.dialog_active = False
                self.current_dialog = None
                self.displayed_text = []
                self.dialog_index = 0
        else:
            print("No dialog is currently active.")

    def update_cursor_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_animation_timer > self.cursor_animation_interval:
            self.cursor_animation_timer = current_time
            self.cursor_index = (self.cursor_index + 1) % 2  
            self.cursor_image = self.cursor_images[self.cursor_index]
            
    def mark_dialog_as_seen(self, npc_id):


        # if npc_id not in self.data['npc_interactions']:
        #     self.data['npc_interactions'][npc_id] = {'dialog_seen': False}
        if npc_id not in self.data['npc_interactions']:
            self.data['npc_interactions'][npc_id] = {'dialog_seen': False}

        self.data['npc_interactions'][npc_id]['dialog_seen'] = True


    
        self.save_game_data()

    def save_game_data(self):
        with open('./data/savedata.json', 'w') as file:
            json.dump(self.data, file, indent=4)
            
    # def show_choices_dialog(self, choices):
    #     """Display the yes/no choices."""
    #     self.show_choices = True
    #     self.choice_texts = choices
        
    # def handle_mouse_click(self, pos):
    #     """Handle mouse click on choice buttons."""
    #     if self.show_choices:
    #         if self.choice_rects['yes'].collidepoint(pos):
    #             self.choice_selected = 'yes'
    #             self.execute_choice_action(self.choice_texts['yes'])
    #         elif self.choice_rects['no'].collidepoint(pos):
    #             self.choice_selected = 'no'
    #             self.execute_choice_action(self.choice_texts['no'])

    # def execute_choice_action(self, choice_data):
    #     """Execute the action associated with the chosen option."""
    #     self.show_choices = False  # Hide the choices after selection
    #     if choice_data['action'] == 'load_new_screen':
    #         # Call your function to load a new screen
    #         self.game.switch_screen(self.task)
    #     elif choice_data['action'] == 'repeat_question':
    #         # If 'no' is selected, repeat the question
    #         self.dialog_index -= 1  # Go back to the same question in the dialog
    #     # Show the NPC's response after the choice
    #     self.current_dialog = [choice_data['response']]
        
    def load_new_screen(self):
        """Placeholder for the screen loading logic."""
        print("Loading a new screen...")

    
    def render(self):
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
                
        if self.show_choices:
                # Render choice buttons (yes/no)
                self.screen.blit(self.choice_buttons['yes'], self.choice_rects['yes'])
                self.screen.blit(self.choice_buttons['no'], self.choice_rects['no'])
                
        # Update and render the animated cursor
        self.update_cursor_animation()
        self.screen.blit(self.cursor_image, self.cursor_position)

