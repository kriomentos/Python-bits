'''Handle loading and initalization of game seesions'''
from __future__ import annotations

import copy
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
import input_handlers
from procgen import generate_dungeon

background_image = tcod.image.load("menu_background.png")[:, :, :3]

def new_game() -> Engine:
    '''return a brand new game session as Engine instance'''
    map_width = 80
    map_height = 44

    init_open = 0.5

    max_monsters = 5
    max_items = 3

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player = player)

    engine.game_map = generate_dungeon(
        map_width = map_width,
        map_height = map_height,
        initial_open = init_open,
        max_monsters = max_monsters,
        max_items = max_items,
        engine = engine,
    )

    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome choomer, to yet another dungeon!", color.welcome_text
    )

    return engine

class MainMenu(input_handlers.BaseEventHandler):
    '''handle main menu rendering and input'''

    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "SCUFFED ROUGELIKE",
            fg = color.menu_title,
            alignment = tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height -2,
            "By Kreeo",
            fg = color.menu_title,
            alignment = tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Contiune last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg = color.menu_text,
                # bg = color.black,
                alignment = tcod.CENTER,
                bg_blend = tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            pass
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None