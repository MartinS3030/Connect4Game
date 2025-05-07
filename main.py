from trainer import self_play_training
from player import play_against_ai


def main():
    print("Connect 4")
    print("1. Train AI by self-play")
    print("2. Play against trained AI")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        episodes = int(input("Enter number of training episodes: "))
        self_play_training(episodes)
        play_against_ai()
    else:
        play_against_ai()


if __name__ == "__main__":
    main()