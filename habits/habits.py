from rxconfig import config
import reflex as rx


class State(rx.State):
    choices: dict[str, bool] = {
        k: False
        for k in ["Habit A", "Habit B", "Habit C"]
    }
    _check_limit = len(choices)

    def check_choice(self, value, index):
        self.choices[index] = value

    @rx.var
    def choice_limit(self):
        return (
            sum(self.choices.values()) >= self._check_limit
        )

    @rx.var
    def checked_choices(self):
        choices = [l for l, v in self.choices.items() if v]
        return " / ".join(choices) if choices else "None"


def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.responsive_grid(
            rx.heading(
                "Welcome to the habit tracker!"),
            rx.vstack(
                render_checkboxes(
                    State.choices,
                    State.choice_limit,
                    State.check_choice,
                )),
            height="100vh",
        )
    )


def render_checkboxes(values, limit, handler):
    return rx.vstack(
        rx.checkbox_group(
            rx.foreach(
                values,
                lambda choice: rx.checkbox(
                    choice[0],
                    is_checked=choice[1],
                    is_disabled=~choice[1] & limit,
                    on_change=lambda val: handler(
                        val, choice[0]
                    ),
                ),
            )
        )
    )


def about():
    return rx.text("About Page")


app = rx.App()
app.add_page(index, route="/")
app.add_page(about, route="/about")
app.compile()
