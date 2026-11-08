from quiz_game.quiz import QuizGame

def main():
    game = QuizGame()
    game.load_data()
    game.run()

if __name__ == "__main__":
    main()