import arcade
import json
import random

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Johnny Bravo Joke Machine"

# Johnny Bravo "sprite" dimensions (placeholder)
JB_WIDTH = 150
JB_HEIGHT = 300
JB_COLOR_IDLE = arcade.color.BLUEBERRY
JB_COLOR_TALKING = arcade.color.BLUE_SAPPHIRE

# Joke display settings
JOKE_TEXT_COLOR = arcade.color.WHITE
JOKE_FONT_SIZE = 20
PUNCHLINE_FONT_SIZE = 24
JOKE_DISPLAY_TIME = 3.0  # seconds

class JohnnyBravoGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        self.johnny_bravo = None
        self.jokes = []
        self.current_joke_index = -1
        self.display_punchline = False
        self.joke_timer = 0.0
        self.is_talking = False

    def setup(self):
        """ Set up the game here. Call this to restart the game. """
        # Placeholder for Johnny Bravo
        self.johnny_bravo = arcade.SpriteSolidColor(JB_WIDTH, JB_HEIGHT, JB_COLOR_IDLE)
        self.johnny_bravo.center_x = SCREEN_WIDTH // 2
        self.johnny_bravo.center_y = SCREEN_HEIGHT // 2

        # Load jokes
        try:
            with open("JohnnyBravo_jokes.json", "r") as f:
                self.jokes = json.load(f)
        except FileNotFoundError:
            print("Error: JohnnyBravo_jokes.json not found.")
            self.jokes = [{"joke": "Hey there, mama!", "punchline": "Wanna see my moves?"}]
        
        self.new_joke()

    def new_joke(self):
        """ Selects a new random joke and resets display. """
        if self.jokes:
            self.current_joke_index = random.randrange(len(self.jokes))
            self.display_punchline = False
            self.joke_timer = 0.0
            self.is_talking = True
            self.johnny_bravo.color = JB_COLOR_TALKING
        else:
            self.current_joke_index = -1
            self.display_punchline = False
            self.joke_timer = 0.0
            self.is_talking = False
            self.johnny_bravo.color = JB_COLOR_IDLE

    def on_draw(self):
        """ Render the screen. """
        self.clear()

        # Draw Johnny Bravo
        if self.johnny_bravo:
            self.johnny_bravo.draw()

        # Draw joke text
        if self.current_joke_index != -1 and self.jokes:
            joke_data = self.jokes[self.current_joke_index]
            joke_text = joke_data["joke"]
            punchline_text = joke_data["punchline"]

            # Display joke
            arcade.draw_text(
                joke_text,
                SCREEN_WIDTH // 2,
                self.johnny_bravo.center_y + JB_HEIGHT // 2 + 50,
                JOKE_TEXT_COLOR,
                font_size=JOKE_FONT_SIZE,
                anchor_x="center",
                anchor_y="center",
            )

            # Display punchline after a delay
            if self.display_punchline:
                arcade.draw_text(
                    punchline_text,
                    SCREEN_WIDTH // 2,
                    self.johnny_bravo.center_y + JB_HEIGHT // 2 + 10,
                    JOKE_TEXT_COLOR,
                    font_size=PUNCHLINE_FONT_SIZE,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )

            # Instruction text
            arcade.draw_text(
                "Click to hear another joke!",
                SCREEN_WIDTH // 2,
                50,
                arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                anchor_y="center",
            )


    def on_update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if self.is_talking:
            self.joke_timer += delta_time
            if not self.display_punchline and self.joke_timer >= JOKE_DISPLAY_TIME:
                self.display_punchline = True
                self.joke_timer = 0.0 # Reset timer for punchline display
            elif self.display_punchline and self.joke_timer >= JOKE_DISPLAY_TIME:
                self.is_talking = False
                self.johnny_bravo.color = JB_COLOR_IDLE


    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        self.new_joke()


def main():
    """ Main function """
    game = JohnnyBravoGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
