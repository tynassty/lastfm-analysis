from matplotlib import pyplot as plt
import datetime as dt
import time_graph
from lastfm_reader import read_scrobbles


def main_loop():
    scrobbles = read_scrobbles('scrobbles-tynassty.csv')
    scrobbles = sorted(scrobbles)

    while True:
        display_menu()
        choice = input("Enter the number of your choice: ")

        if choice == "0":
            print("Goooooodbye!")
            break
        elif choice == "1":
            run_time_graph(scrobbles)
        elif choice == "2":
            run_artist_graph(scrobbles)
        else:
            print("Invalid choice.")


def display_menu():
    print("\nWhat function would you like to execute?")
    print("0. Quit")
    print("1. Moving sum graph")
    print("2. Artist graph")


def run_time_graph(scrobbles):
    width = float(input("Moving average day length should be: "))
    k = int(input("How many artists? "))
    time_graph.graph_from_scrobbles(scrobbles, plot_func=plt.step, mvg_avg_period=dt.timedelta(days=width), k=k)


def run_artist_graph(scrobbles):
    artist = input("Enter artist name: ")
    time_graph.graph_from_scrobbles(scrobbles, mvg_avg_period=dt.timedelta(days=100000), k=0, addtl_artists=[artist])


if __name__ == "__main__":
    main_loop()
