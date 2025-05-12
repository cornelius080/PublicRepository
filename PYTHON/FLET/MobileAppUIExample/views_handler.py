import flet as ft
from views.welcome import Welcome
from views.login import Login
from views.home import Home
from views.other import Other
from views.faq import Faq
from views.message_box import MessageBox
from views.movements import Movements

def nav_bar_on_change(page, e):
    if e.control.selected_index == 0:
        page.go(routes['home'])
    elif e.control.selected_index == 1:
        page.go(routes['other'])

def views_manager(page):
  # returns a dictionary of views with keys corresponding to their routes
  return {
    routes['welcome'] : Welcome(
        parent_page=page,
        route=routes['welcome'], 
        on_click=lambda _: page.go(routes['login'])
    ),
    routes['login'] : Login(
        parent_page=page,
        route=routes['login'], 
        on_click=lambda _: page.go(routes['home'])
    ),
    routes['home'] : Home(
        parent_page=page,
        route=routes['home'], 
        go_to_view_message_box=lambda _: page.go(routes['message_box']),
        go_to_view_faq=lambda _: page.go(routes['faq']),
        go_to_view_cards=lambda _: page.go(routes['cards']),
        go_to_view_other=lambda _: page.go(routes['other']),
        go_to_view_movements=lambda _: page.go(routes['movements']),
    ),
    routes['other'] : Other(
        parent_page=page,       
        exit_from_app=lambda _: page.window_destroy(),
        go_to_view_home=lambda _: page.go(routes['home']),
        go_to_view_cards=lambda _: page.go(routes['cards']),
        go_to_view_message_box=lambda _: page.go(routes['message_box']),
    ),
    routes['faq'] : Faq(
        parent_page=page,
        route=routes['faq'], 
        go_to_view_home=lambda _: page.go(routes['home']),
    ),
    routes['message_box'] : MessageBox(
        parent_page=page,
        route=routes['message_box'], 
        go_to_view_home=lambda _: page.go(routes['home']),
    ),
    routes['movements'] : Movements(
        parent_page=page,
        route=routes['movements'], 
        go_to_view_home=lambda _: page.go(routes['home']),
    ),
  }

routes = {
    'welcome': '/', 
    'login': '/login', 
    'home': '/home', 
    'cards': '/cards', 
    'other': '/other', 
    'faq': '/faq', 
    'message_box': '/message_box', 
    'movements': '/movements',
}