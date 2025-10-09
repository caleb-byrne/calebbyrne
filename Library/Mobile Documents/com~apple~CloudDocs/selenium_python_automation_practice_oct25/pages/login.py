from .base_page import BasePage


class LoginPage(BasePage):
    # Provide locators in the string format expected by seleniumpagefactory.
    locators = {
        "username": ("id", "user-name"),
        "password": ("id", "password"),
        "login_button": ("id", "login-button"),
    }

    def open(self, url: str):
        self.driver.get(url)

    def enter_username(self, username: str):
        self.username.set_text(username)

    def validate_username_entered_exists(self, expected_username: str) -> bool:
        username_field = self.username
        return username_field.get_attribute("value") == expected_username

    def enter_password(self, password: str):
        self.password.set_text(password)

    def validate_password_entered_exists(self, expected_password: str) -> bool:
        password_field = self.password
        return password_field.get_attribute("value") == expected_password

    def click_submit_login_button(self):
        self.login_button.click_button()

    def validate_submit_button_exists(self) -> bool:
        button = self.login_button
        return button.is_displayed()
