#!/usr/bin/env python3
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker

import card as c
from utils import *


def add_choose_color(results):
    for color in c.COLORS:
        results.append(
            InlineQueryResultArticle(
                id=color,
                title="Escolha cor",
                description=display_color(color),
                input_message_content=
                InputTextMessageContent(display_color(color))
            )
        )


def add_other_cards(playable, player, results, game):
    if not playable:
        playable = list()

    players = player_list(game)

    results.append(
        InlineQueryResultArticle(
            "hand",
            title="Cartas (selecione para estado do jogo):",
            description=', '.join([repr(card) for card in
                                   list_subtract(player.cards, playable)]),
            input_message_content=InputTextMessageContent(
                "Jogando agora: " + display_name(game.current_player.user) +
                "\n" +
                "Última carta: " + repr(game.last_card) + "\n" +
                "Jogadores: " + " -> ".join(players))
        )
    )


def player_list(game):
    players = list()
    for player in game.players:
        add_player(player, players)
    return players


def add_no_game(results):
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title="Você não está jogando!",
            input_message_content=
            InputTextMessageContent('Você não está jogando! Use /new ou /join.')
        )
    )


def add_not_started(results):
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title="O jogo ainda não começou",
            input_message_content=
            InputTextMessageContent('Comece o jogo com /start ou /startfouyer')
        )
    )


def add_draw(player, results):
    results.append(
        Sticker(
            "draw", sticker_file_id=c.STICKERS['option_draw'],
            input_message_content=
            InputTextMessageContent('Comprando %d carta(s)'
                                    % (player.game.draw_counter or 1))
        )
    )


def add_gameinfo(game, results):
    players = player_list(game)

    results.append(
        Sticker(
            "gameinfo",
            sticker_file_id=c.STICKERS['option_info'],
            input_message_content=InputTextMessageContent(
                "Jogando agora: " + display_name(game.current_player.user) +
                "\n" +
                "Última carta: " + repr(game.last_card) + "\n" +
                "Jogadores: " + " -> ".join(players))
        )
    )


def add_pass(results):
    results.append(
        Sticker(
            "pass", sticker_file_id=c.STICKERS['option_pass'],
            input_message_content=InputTextMessageContent('Pass')
        )
    )


def add_call_bluff(results):
    results.append(
        Sticker(
            "call_bluff",
            sticker_file_id=c.STICKERS['option_bluff'],
            input_message_content=
            InputTextMessageContent("É BLEFE SUA PUTA!")
        )
    )


def add_play_card(game, card, results, can_play):
    players = player_list(game)

    if can_play:
        results.append(
            Sticker(str(card), sticker_file_id=c.STICKERS[str(card)])
        )
    else:
        results.append(
            Sticker(str(uuid4()), sticker_file_id=c.STICKERS_GREY[str(card)],
                    input_message_content=InputTextMessageContent(
                        "Jogando agora: " + display_name(
                            game.current_player.user) +
                        "\n" +
                        "Última carta: " + repr(game.last_card) + "\n" +
                        "Jogadores: " + " -> ".join(players)))
        )


def add_player(itplayer, players):
    players.append(itplayer.user.first_name + " (%d cartas)"
                   % len(itplayer.cards))

