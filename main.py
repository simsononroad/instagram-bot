from instagrapi import Client
from login_data import *
from instabot import Bot
from rich.console import *

console = Console()
console.print("Menu", style="black bold")

send_ig_message_name = ""
try:
    my_bot = Bot()
    my_bot.login(username=username_ig, password=password_ig)
except:
    console.print("ERROR: Sikertelen bejelentkezés az instabot-ba", style="bold red")
    client = Client()
    client.login(username_ig, password_ig)
    console.print("SUCCESSFUL: Sikeres bejelentkezés az instagrapi-ba", style="bold green")

def Like_post(hashtag):
    medias = client.hashtag_medias_recent(hashtag, 20)
    total_liked_post = int()
    for i, media in enumerate(medias):
        client.media_like(media.id)
        print(f"Kedvelt posztok száma: {i+1} a hashtagnek {hashtag}")
        total_liked_post +=1
    print(f"Kedvelt posztok száma :{total_liked_post}")
    menu()
    return total_liked_post

def send_direct_message(instagram_name, message):
    send_to = client.user_id_from_username(username=instagram_name)
    client.direct_send(text=message, user_ids=[send_to])
    print(f"Üzenet: {message} elküldve {instagram_name}-nak/nek")
    menu()

def menu():
    global send_ig_message_name
    try:
        menu = int(console.input("[bold cyan]Postokat bekedvelni(1)[/bold cyan] || [bold cyan]Üzenet küldése(2)[/bold cyan] || [bold red]Kilépés(3)[/bold red]: "))
    except:
        console.print("ERROR: Számot írj be!", style="bold red")
        menu()
    print(menu)
    if menu == 1:
        ht = input("Kedveld be ezeket azt a post-ot amiben szerepel a hashtag\n>>> #")
        Like_post(ht)
    elif menu == 2:
        if send_ig_message_name == "":
            ig_name = input("Írd be a felhasználó nevét\n>>>")
            send_ig_message_name = ig_name
            message = input(f"Írd be az üzenetet @{ig_name}-nak/nek\n>>>")
            send_direct_message(ig_name, message)
        else:
            try:
                send_people = int(input(f"Küldés {send_ig_message_name}-nak/nek(1) || Küldés új embernek(2)"))
            except:
                console.print("ERROR: Számot írj be!", style="bold red")
                send_people = int(input(f"Küldés {send_ig_message_name}-nak/nek(1) || Küldés új embernek(2)"))
            if send_people == 1:
                message = input(f"Írd be az üzenetet @{send_ig_message_name}-nak/nek\n>>>")
                send_direct_message(send_ig_message_name, message)
            elif send_people == 2:
                send_ig_message_name = ""
                ig_name = input("Írd be a felhasználó nevét\n>>>")
                send_ig_message_name = ig_name
                message = input(f"Írd be az üzenetet @{ig_name}-nak/nek\n>>>")
                send_direct_message(ig_name, message)


if __name__ == "__main__":
    menu()