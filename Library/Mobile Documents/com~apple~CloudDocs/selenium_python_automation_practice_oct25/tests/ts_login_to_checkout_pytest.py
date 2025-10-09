import os


def tc_login_to_checkout(pages):
    """tc_lginaddprdctchckout_1 — login, add product to cart, complete checkout purchase"""
    url = os.getenv("APP_URL", "https://www.saucedemo.com/")
    user_name = "standard_user"
    password = "secret_sauce"

    login_page = pages.login()

    login_page.open(url)
    assert login_page.validate_submit_button_exists()
    login_page.enter_username(user_name)
    assert login_page.validate_username_entered_exists(user_name)
    login_page.enter_password(password)
    assert login_page.validate_password_entered_exists(password)
    login_page.click_submit_login_button()
