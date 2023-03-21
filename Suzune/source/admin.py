from pyrogram import Client, filters
from pyrogram.types import Message
from Suzune import suzune as app

# define a filter to check if the user is an admin in the chat
def is_admin(chat_id, user_id):
    chat_member = app.get_chat_member(chat_id, user_id)
    return chat_member.status in ("creator", "administrator")

# define a command handler for /ban
@app.on_message(filters.command("ban", prefixes="/") & filters.private)
def ban_user(client, message):
    # check if the user is an admin in the chat
    if not is_admin(message.chat.id, message.from_user.id):
        return

    # get the user ID or username from the command or replied message
    user_id = None
    if len(message.command) > 1:
        user_id = message.command[1]
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

    if user_id is None:
        # no user ID or username specified
        return

    # check if the user ID is a number (i.e., it's a user ID)
    if user_id.isdigit():
        user_id = int(user_id)
    else:
        # it's not a user ID, so it must be a username
        user = client.get_users(user_id)
        user_id = user.id

    # ban the user
    client.kick_chat_member(message.chat.id, user_id)

    # send a message to the chat to announce that the user has been banned
    ban_reason = "Violating the community guidelines."
    client.send_message(
        message.chat.id, 
        f"The user {user_id} has been banned from the chat")
