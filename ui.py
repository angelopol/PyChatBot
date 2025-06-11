import flet as ft

class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message, current_user: str, page: ft.Page = None):
        super().__init__()
        is_user = message.user_name == current_user
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        self.controls = [
            ft.Container(
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.Colors.BLACK,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                margin=ft.margin.only(left=8) if is_user else ft.margin.only(right=8),
                visible=not is_user or True,
            ) if not is_user else None,
            ft.Row(
                [
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text(
                                    message.user_name,
                                    weight="bold",
                                    color=ft.Colors.BLACK,
                                    size=16
                                ),
                                ft.Text(
                                    message.text,
                                    selectable=True,
                                    color=ft.Colors.BLACK,
                                    no_wrap=False,
                                    max_lines=None,
                                    size=16
                                ),
                            ],
                            tight=True,
                            spacing=5,
                        ),
                        bgcolor=self.get_avatar_color(message.user_name),
                        border_radius=ft.border_radius.only(
                            top_left=15, top_right=15,
                            bottom_left=15 if is_user else 2,
                            bottom_right=2 if is_user else 15
                        ),
                        padding=10,
                        margin=ft.margin.only(left=40 if is_user else 0, right=0 if is_user else 40, bottom=4, top=4),
                        alignment=ft.alignment.center_right if is_user else ft.alignment.center_left,
                        expand=False,
                        width=(min(400, 0.8 * page.width) if hasattr(page, "width") else 400) if not is_user else None
                    )
                ],
                alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
            ),
            ft.Container(
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.Colors.BLACK,
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
            return "Unknown"

    def get_avatar_color(self, user_name: str):
        Colors_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return Colors_lookup[hash(user_name) % len(Colors_lookup)]

class Ui:
    def __init__(self, title: str = "Flet Chat", offlineResponse=None, onlineResponse=None):
        self.title = title
        self.offlineResponse = offlineResponse
        self.onlineResponse = onlineResponse

    def __call__(self, page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.title = self.title
        self.responseFunction = self.offlineResponse if self.offlineResponse else self.onlineResponse

        self.switch_mode = ft.Switch(label="IA", value=False)

        def update_response_function(e):
            if self.switch_mode.value:
                if self.onlineResponse:
                    self.responseFunction = self.onlineResponse
            else:
                if self.offlineResponse:
                    self.responseFunction = self.offlineResponse
            page.update()

        self.switch_mode.on_change = update_response_function

        def bot_response(user_message):
            if not self.responseFunction:
                return "No hay una función de respuesta configurada."
            return self.responseFunction[0](user_message, self.responseFunction[1])

        def send_message_click(e):
            if self.new_message.value != "":
                page.pubsub.send_all(
                    Message(
                        "You",
                        self.new_message.value,
                        message_type="chat_message",
                    )
                )
                bot_msg = bot_response(self.new_message.value)
                page.pubsub.send_all(
                    Message(
                        self.onlineResponse[1].get("businessName", "Bot") if self.onlineResponse else "Bot",
                        bot_msg,
                        message_type="chat_message",
                    )
                )
                self.new_message.value = ""
                self.new_message.focus()
                page.update()

        def on_message(message: Message):
            current_user = "You"
            if message.message_type == "chat_message":
                m = ChatMessage(message, current_user, page)
            elif message.message_type == "login_message":
                m = ft.Text(message.text, italic=True, color=ft.Colors.BLACK45, size=12)
            self.chat.controls.append(m)
            page.update()

        page.pubsub.subscribe(on_message)

        self.chat = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

        self.new_message = ft.TextField(
            hint_text="Escribe un mensaje...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=send_message_click,
        )

        page.add(
            ft.Container(
                content=self.chat,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    self.new_message,
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=send_message_click,
                    ),
                    self.switch_mode
                ]
            ),
        )

def runUi(title: str = "Flet Chat", offlineResponse=None, onlineResponse=None):
    ft.app(target=Ui(title, offlineResponse, onlineResponse))

if __name__ == "__main__":
    runUi()