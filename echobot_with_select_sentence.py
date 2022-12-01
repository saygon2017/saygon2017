import requests

root_url = "https://api.telegram.org/bot"

token = "5605346711:AAHmkZgSZLVJKs7uldd3pKnnKtaFCg6lCHc"

good_codes = (200, 201, 202, 203, 204)

users = []

sentences = [
    {"text": "When my time comes \n Forget the wrong that I’ve done.",
     "level": 1},
    {"text": "In a hole in the ground there lived a hobbit.",
     "level": 2},
    {
        "text": "The sky the port was the color of television, tuned to a dead channel.",
        "level": 1},
    {"text": "I love the smell of napalm in the morning.",
     "level": 1},
    {
        "text": "The man in black fled across the desert, and the gunslinger followed.",
        "level": 1},
    {"text": "The Consul watched as Kassad raised the death wand.",
     "level": 1},
    {"text": "If you want to make enemies, try to change something.",
     "level": 2},
    {
        "text": "We're not gonna take it. \n Oh no, we ain't gonna take it \nWe're not gonna take it anymore",
        "level": 1},
    {
        "text": "I learned very early the difference between knowing the name of something and knowing something.",
        "level": 2}
]


# check bot active
def get_update(token: str):
    url = f"{root_url}{token}/getUpdates"
    result = requests.get(url)
    if result.status_code in good_codes:
        # print("all is ok")
        # print(result.json())
        return result.json()
    else:
        print(f"request failed with error {result.status_code}")


def format_update(update: dict):
    user_id = update["result"][-1]["message"]["from"]["id"]
    chat_id = update["result"][-1]["message"]["chat"]["id"]
    text = update["result"][-1]["message"]["text"]
    # print(update)
    message_id = update["result"][-1]["update_id"]

    return {"user_id": user_id, "chat_id": chat_id, "text": text, "message_id": message_id}


def send_msg(token: str, chat_id: int, msg: object):
    url = f"{root_url}{token}/sendMessage"
    result = requests.post(url, data={"chat_id": chat_id, "text": msg})
    if result.status_code in good_codes:
        print("message sent ok")
    else:
        print(f"request failed with error {result.status_code}")


def check_word(sentences: list, word: str, usrlvl: int, chat_id: int):
    found_msg = False
    for sentence in sentences:
        if sentence["level"] == usrlvl and word in sentence["text"]:
            send_msg(token, chat_id,
                     msg=sentence["text"])
            found_msg = True

    if not found_msg:
        send_msg(token, chat_id,
             msg=f"Sorry, no sentence with {word} found")


def validate_user(users, update, usr_level):
    user_exist = False
    for user in users:
        if user["user_id"] == update["user_id"]:
            user_exist = True
    if not user_exist:
        user = {"user_id": update["user_id"], "chat_id": update["chat_id"],
                "usr_lvl": usr_level}
        users.append(user)
        print(users)
        print("user is added")


def main():
    last_message_id = 0
    update = format_update(get_update(token))
    chat_id = update["chat_id"]
    while True:
        update = format_update(get_update(token))
        # check if start word
        if update["text"] == "/start" and last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            send_msg(token, chat_id, msg="Enter your English level (1 - Beginner, 2 - Intermediate, 3 - Advanced)")

        if format_update(get_update(token))["text"] in ("1", "2", "3") and last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            usr_level = int(update["text"])
            validate_user(users, update, usr_level)

            send_msg(token, chat_id, msg="Enter the keyword")

        if last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            for user in users:
                if user["user_id"] == update["user_id"]:
                    usr_level = user["usr_lvl"]
                    check_word(sentences, update["text"], usr_level, chat_id)


main()







