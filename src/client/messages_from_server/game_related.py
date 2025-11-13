from common.messages_from_server.game_events import GameEventType


def game_state_received(game_state: str, ui_manager):
    ui_manager.game_state_received(game_state)

def game_events_received(game_events, ui_manager):
    for event in game_events:
        execute_game_event(event, ui_manager)

def execute_game_event(event, ui_manager):
    event_type = GameEventType[event["event_type"]]
    match event_type:
        case GameEventType.MOVE_UNIT:
            ui_manager.move_unit_event(event["unit_id"], event["new_grid_position"])

def turn_ended(dummy, ui_manager):
    ui_manager.turn_ended()