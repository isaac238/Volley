import pygame
import sys
from network import Network
from player import Player
white = (255, 255, 255)
black = (0, 0, 0)
grey = (111, 111, 111)


class App:

    def __init__(self):
        self._home = True
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self._muted = False

    def on_init(self):
        pygame.init()
        pygame.mixer.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Volley")
        self._running = True
        self._home = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def text_objects(self, text, font_file, font_size, colour):
        font = pygame.font.Font(font_file, font_size)
        text_surface = font.render(text, True, colour)
        return text_surface, text_surface.get_rect()

    def home_screen(self):
        home = self._home
        muted = self._muted
        if home:
            self._display_surf.fill(black)
            volley_surf, volley_rect = self.text_objects('Volley', 'Rightious.ttf', 100, white)
            credit_surf, credit_rect = self.text_objects('By isaac238', 'Rightious.ttf', 12, white)
            quit_surf, quit_rect = self.text_objects('Exit', 'Rightious.ttf', 32, black)
            start_surf, start_rect = self.text_objects('Start', 'Rightious.ttf', 32, black)
            volley_rect.center = ((self.weight/2), (self.height/4))
            credit_rect.center = ((self.weight/1.05), (self.height/1.03))
            quit_rect.center = ((self.weight/2), (self.height/2) + 50)
            start_rect.center = ((self.weight/2), (self.height/2))
            self._display_surf.blit(volley_surf, volley_rect)
            self._display_surf.blit(credit_surf, credit_rect)

            box1 = pygame.draw.rect(self._display_surf, white, ((self.weight/2) - 50, (self.height/2) - 20, 100, 40))
            self._display_surf.blit(start_surf, start_rect)
            box2 = pygame.draw.rect(self._display_surf, white, ((self.weight/2) - 50, (self.height/2) + 30, 100, 40))
            self._display_surf.blit(quit_surf, quit_rect)

            if not muted:
                mute_surf, mute_rect = self.text_objects('Music: On', 'Rightious.ttf', 32, white)
                mute_rect.center = ((self.weight/10), (self.height/1.05))
                self._display_surf.blit(mute_surf, mute_rect)
            else:
                mute_surf, mute_rect = self.text_objects('Music: Off', 'Rightious.ttf', 32, white)
                mute_rect.center = ((self.weight/10), (self.height/1.05))
                self._display_surf.blit(mute_surf, mute_rect)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if mute_rect.collidepoint(mouse_pos):
                if not muted:
                    mute_surf, mute_rect = self.text_objects('Music: On', 'Rightious.ttf', 32, grey)
                    mute_rect.center = ((self.weight / 10), (self.height / 1.05))
                    self._display_surf.blit(mute_surf, mute_rect)
                else:
                    mute_surf, mute_rect = self.text_objects('Music: Off', 'Rightious.ttf', 32, grey)
                    mute_rect.center = ((self.weight / 10), (self.height / 1.05))
                    self._display_surf.blit(mute_surf, mute_rect)
            if mute_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
                if not muted:
                    self._muted = True
                    pygame.mixer.music.pause()
                    pygame.time.wait(1)
                else:
                    self._muted = False
                    pygame.mixer.music.unpause()
                    pygame.time.wait(1)
            if box1.collidepoint(mouse_pos):
                box1 = pygame.draw.rect(self._display_surf, grey, ((self.weight/2) - 50, (self.height/2) - 20, 100, 40))
                self._display_surf.blit(start_surf, start_rect)

            if box1.collidepoint(mouse_pos) and mouse_pressed[0]:
                self._home = False

            if box2.collidepoint(mouse_pos):
                box2 = pygame.draw.rect(self._display_surf, grey, ((self.weight / 2) - 50, (self.height / 2) + 30, 100, 40))
                self._display_surf.blit(quit_surf, quit_rect)

            if box2.collidepoint(mouse_pos) and mouse_pressed[0]:
                self.on_cleanup()

            pygame.display.update()

    def play_screen(self, player, player2):
        self._display_surf.fill(black)
        divider_rect = pygame.draw.rect(self._display_surf, white, ((self.weight/2), (self.height/1000), 10, self.height))
        player.draw(self._display_surf)
        player2.draw(self._display_surf)
        pygame.display.update()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False
        n = Network()
        player = n.getPlayer()
        if self._home:
            pygame.mixer.music.load("amadeus-legendary.mp3")
            pygame.mixer.music.play(-1, 0.0)
        while self._running:
            player2 = n.send(player)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            if self._home:
                self.home_screen()
            else:
                player.move()
                pygame.mixer.music.stop()
                self.play_screen(player, player2)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
