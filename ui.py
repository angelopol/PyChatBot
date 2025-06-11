import flet as ft

class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message, current_user: str):
        super().__init__()
        is_user = message.user_name == current_user
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        self.controls = [
            # Si es usuario, avatar a la derecha, si no, a la izquierda
            ft.Container(
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                margin=ft.margin.only(left=8) if is_user else ft.margin.only(right=8),
                visible=not is_user or True,  # Siempre visible, pero puedes ocultar si quieres
            ) if not is_user else None,
            ft.Container(
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold", color=ft.colors.BLACK, size=12),
                        ft.Text(message.text, selectable=True, color=ft.colors.WHITE if is_user else ft.colors.WHITE),
                    ],
                    tight=True,
                    spacing=5,
                ),
                bgcolor=self.get_avatar_color(message.user_name) if is_user else self.get_avatar_color(message.user_name),
                border_radius=ft.border_radius.only(
                    top_left=15, top_right=15,
                    bottom_left=15 if is_user else 2,
                    bottom_right=2 if is_user else 15
                ),
                padding=10,
                margin=ft.margin.only(left=40 if is_user else 0, right=0 if is_user else 40, bottom=4, top=4),
                alignment=ft.alignment.center_right if is_user else ft.alignment.center_left,
            ),
            ft.Container(
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                margin=ft.margin.only(right=8),
            ) if is_user else None,
        ]
        self.controls = [c for c in self.controls if c is not None]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"  # or any default value you prefer

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def ui(page: ft.Page, title: str = "Flet Chat"):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = title

    def bot_response(user_message):
        # Aquí puedes poner la lógica de tu bot
        return f"Echo: {user_message}"

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    "You",
                    new_message.value,
                    message_type="chat_message",
                )
            )
            bot_msg = bot_response(new_message.value)
            page.pubsub.send_all(
                Message(
                    "Bot",
                    bot_msg,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        current_user = "You"
        if message.message_type == "chat_message":
            m = ChatMessage(message, current_user)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

def runUi(title: str = "Flet Chat"):
    ft.app(target=lambda page: ui(page, title))


if __name__ == "__main__":
    # Run the app
    runUi()