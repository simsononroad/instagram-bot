from instagrapi import Client
from login_data import *
from instabot import Bot
from rich.console import *
import sqlite3
import webbrowser

con = sqlite3.connect("data.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE emberek(name)")

except:
    pass


instagram_url = "https://instagram.com"


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
    print(send_to)
    client.direct_send(text=message, user_ids=[send_to])
    print(f"Üzenet: {message} elküldve {instagram_name}-nak/nek")
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    ins = cur.execute(f"insert into emberek (name) values ('{instagram_name}')")
    while True:
        try:
            q = int(input("Profil megnyitása böngészőben(1) || tovább a menübe(2)\n>>>"))
        except:
            console.print("Számot írj be!")
            q = int(input("Profil megnyitása böngészőben(1) || tovább a menübe(2)\n>>>"))
        if q == 1:
            webbrowser.open(f"https://instagram.com/{instagram_name}/")
            menu()
            break
        elif q == 2:
            menu()
            break
        
    
    con.commit()
    menu()
    

def open_ig():
    webbrowser.open(instagram_url)
    menu()


def menu():
    global send_ig_message_name
    try:
        menu = int(console.input("[bold cyan]Postokat bekedvelni(1)[/bold cyan] || [bold cyan]Üzenet küldése(2)[/bold cyan] || [bold cyan]Megnyitás böngészőben(3)[/bold cyan] || [bold red]Kilépés(4)[/bold red]: "))
    except:
        console.print("ERROR: Számot írj be!", style="bold red")
        menu()
    if menu == 1:
        ht = input("Kedveld be ezeket azt a post-ot amiben szerepel a hashtag\n>>> #")
        Like_post(ht)
    elif menu == 2:
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        ins = cur.execute(f"select name FROM emberek")
        emberek = cur.fetchall()
        console.print("Eddig ezekkel az emberekkel beszéltél:", style="bold black on white")
        for i in emberek:
            i = i[0]
            console.print(f"-    {i}", style="bold black on white")
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
    elif menu == 3:
        open_ig()        
    else:
        pass

if __name__ == "__main__":
    menu()