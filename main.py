import sys, pathlib
from pygame.math import Vector2

from snake import Snake
from apple import Apple
from button import Button
from slider import Slider

from important_constants import *

def get_font(font_size):
    return pygame.font.Font('fonts/menu_font.ttf', font_size)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Apple()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        if self.snake.is_moving():
            self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        if not self.snake.is_moving():
            self.draw_move_to_start_message()

    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            self.snake.play_eating_sound()
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.position:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.add_score_to_file(self.snake.get_score())

        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)

        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(self.snake.get_score())
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        score_y = int(CELL_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def run(self):
        self.main_menu()

    def main_menu(self):
        while True:
            screen.fill("#a6d13b")

            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(75).render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(400, 100))

            play_button = Button(image=pygame.image.load("resources/Play Rect.png"), pos=(400, 250),
                                 text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=pygame.image.load("resources/Options Rect.png"), pos=(400, 400),
                                    text_input="OPTIONS", font=get_font(50), base_color="#d7fcd4",
                                    hovering_color="White")
            highest_scores = Button(image=pygame.image.load("resources/Score Rect.png"), pos=(400, 550),
                                        text_input="SCORES", font=get_font(50), base_color="#d7fcd4",
                                        hovering_color="White")
            quit_button = Button(image=pygame.image.load("resources/Quit Rect.png"), pos=(400, 700),
                                 text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

            screen.blit(menu_text, menu_rect)

            for button in [play_button, options_button, highest_scores, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        self.play()
                    if options_button.checkForInput(menu_mouse_pos):
                        self.options()
                    if highest_scores.checkForInput(menu_mouse_pos):
                        self.scores()
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def play(self):
        options = self.load_options()
        eating_sound.set_volume(float(options[0]) / 10)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == SCREEN_UPDATE:
                    main_game.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)

                    if event.key == pygame.K_ESCAPE:
                        self.snake.stop()
                        self.main_menu()

            screen.fill((175, 215, 70))
            main_game.draw_elements()
            pygame.display.update()
            clock.tick(60)

    def options(self):
        options = self.load_options()

        sound_scale = Slider((500, 360), width=200, height=30, min_value=0, max_value=10, value=int(options[0]),
                             color="red", hovering_color="orange3")

        while True:
            options_mouse_pos = pygame.mouse.get_pos()

            screen.fill("#a6d13b")

            options_text = get_font(30).render("Options", True, "Black")
            options_rect = options_text.get_rect(center=(400, 260))
            screen.blit(options_text, options_rect)

            sound_options_text = get_font(30).render("Sound", True, "Black")
            sound_options_rect = sound_options_text.get_rect(center=(250, 360))
            screen.blit(sound_options_text, sound_options_rect)

            sound_scale.check_for_hover(options_mouse_pos)
            sound_scale.draw()

            options_back = Button(image=None, pos=(400, 560),
                                  text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Green")

            options_back.changeColor(options_mouse_pos)
            options_back.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_options(sound_scale.value)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if options_back.checkForInput(options_mouse_pos):
                        self.save_options(sound_scale.value)
                        self.main_menu()

                    sound_scale.check_for_click(options_mouse_pos)

                    sound_scale.check_for_unclick(options_mouse_pos)

                if event.type == pygame.KEYDOWN:
                    sound_scale.check_for_arrow_keys(event.key)

            pygame.display.update()

    def save_options(self, sound_value):
        with open("options.txt", "w") as file:
            file.write(str(sound_value))

    def load_options(self):
        options = []
        options_file = pathlib.Path("options.txt")
        if options_file.exists():
            with open("options.txt", "r") as file:
                for line in file:
                    options.append(line.strip())
        else:
            options.append("5")
            self.save_options(5)

        return options

    def get_scores(self):
        scores = []
        score_file = pathlib.Path("scores.txt")
        if score_file.exists():
            with open("scores.txt", "r") as file:
                for line in file:
                    scores.append(line.strip())
        else:
            score_file.touch()

        return [score for score in scores if score != "" and score != " " and score != "\n" and score != "0"]

    def scores(self):
        scores = self.get_scores()

        while True:
            scores_mouse_pos = pygame.mouse.get_pos()

            screen.fill("#a6d13b")

            if len(scores) <= 0:
                scores_text = get_font(30).render("There are no scores", True, "Black")
                scores_rect = scores_text.get_rect(center=(400, 260))
                screen.blit(scores_text, scores_rect)
            else:
                scores_text = get_font(35).render("Current highest scores", True, "Black")
                scores_rect = scores_text.get_rect(center=(400, 50))
                screen.blit(scores_text, scores_rect)

                for i, score in enumerate(scores):
                    score_text = get_font(30).render(f"{score}", True, "Black")
                    score_rect = score_text.get_rect(center=(400, 150 + (i * 40)))
                    apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))

                    screen.blit(apple, apple_rect)
                    screen.blit(score_text, score_rect)

            scores_back = Button(image=None, pos=(400, 650),
                                  text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")

            scores_back.changeColor(scores_mouse_pos)
            scores_back.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if scores_back.checkForInput(scores_mouse_pos):
                        self.main_menu()

            pygame.display.update()

    def add_score_to_file(self, score):
        scores = self.get_scores()

        scores = [int(score) for score in scores]

        scores.append(score)
        scores.sort(reverse=True)

        if len(scores) > 10:
            scores = scores[:10]

        with open("scores.txt", "w") as file:
            for score in scores:
                file.write(f"{score}\n")

    def draw_move_to_start_message(self):
        message = get_font(30).render("Press any key to start!", True, "Black")
        message_rect = message.get_rect(center=(400, 350))

        screen.blit(message, message_rect)


main_game = Game()
main_game.run()
