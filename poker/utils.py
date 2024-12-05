from pypokerengine.api.game import setup_config, start_poker
import importlib.util


def load_bot(filepath):
    spec = importlib.util.spec_from_file_location("Bot", filepath)
    bot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot)
    return bot.Bot()


def play_match(bot1_path, bot2_path, bot1, bot2):
    """
    Simulates a match between two bots and updates their chips based on the outcome.
    """
    bot1_instance = load_bot(bot1_path)
    bot2_instance = load_bot(bot2_path)

    config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)
    config.register_player(name="bot1", algorithm=bot1_instance)
    config.register_player(name="bot2", algorithm=bot2_instance)

    result = start_poker(config, verbose=0)
    bot1_stack = result["players"][0]["stack"]
    bot2_stack = result["players"][1]["stack"]

    # Determine winner and chips exchanged
    chips_exchanged = abs(bot1_stack - bot2_stack)
    if bot1_stack > bot2_stack:
        bot1.chips += chips_exchanged
        bot2.chips -= chips_exchanged
        winner = bot1.name
    else:
        bot1.chips -= chips_exchanged
        bot2.chips += chips_exchanged
        winner = bot2.name

    bot1.save()
    bot2.save()

    return winner, chips_exchanged



