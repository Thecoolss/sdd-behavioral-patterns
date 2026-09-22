from encore.pricing import EarlyBirdPricing
from encore.cart import (
    Cart,
    AddTicketCommand,
    RemoveTicketCommand,
    SetPricingStrategyCommand,
    CartInvoker,
)


def test_add_ticket_command_adds_to_cart():
    cart = Cart()

    AddTicketCommand(cart, "GA", 2, 50.0).execute()

    assert cart.items()["GA"] == (2, 50.0)


def test_add_ticket_command_undo_removes_added_tickets():
    cart = Cart()
    command = AddTicketCommand(cart, "GA", 2, 50.0)
    command.execute()

    command.undo()

    assert "GA" not in cart.items()


def test_remove_ticket_command_removes_up_to_available_quantity():
    cart = Cart()
    cart.add_item("GA", 3, 50.0)

    RemoveTicketCommand(cart, "GA", 10).execute()

    assert "GA" not in cart.items()


def test_remove_ticket_command_undo_restores_exact_removed_quantity():
    cart = Cart()
    cart.add_item("GA", 3, 50.0)
    command = RemoveTicketCommand(cart, "GA", 2)
    command.execute()

    assert cart.items()["GA"] == (1, 50.0)

    command.undo()

    assert cart.items()["GA"] == (3, 50.0)


def test_set_pricing_strategy_command_swaps_strategy():
    cart = Cart()
    cart.add_item("GA", 2, 50.0)
    command = SetPricingStrategyCommand(cart, EarlyBirdPricing(10))

    command.execute()

    assert cart.total() == 90.0


def test_set_pricing_strategy_command_undo_restores_previous_strategy():
    cart = Cart()
    cart.add_item("GA", 2, 50.0)
    command = SetPricingStrategyCommand(cart, EarlyBirdPricing(10))
    command.execute()

    command.undo()

    assert cart.total() == 100.0


def test_invoker_runs_commands_and_updates_cart():
    cart = Cart()
    invoker = CartInvoker()

    invoker.run(AddTicketCommand(cart, "GA", 2, 50.0))

    assert cart.items()["GA"] == (2, 50.0)


def test_invoker_undo_reverts_last_command():
    cart = Cart()
    invoker = CartInvoker()
    invoker.run(AddTicketCommand(cart, "GA", 2, 50.0))
    invoker.run(AddTicketCommand(cart, "VIP", 1, 120.0))

    undone = invoker.undo(1)

    assert undone == 1
    assert "VIP" not in cart.items()
    assert cart.items()["GA"] == (2, 50.0)


def test_invoker_undo_returns_fewer_than_requested_when_history_runs_out():
    cart = Cart()
    invoker = CartInvoker()
    invoker.run(AddTicketCommand(cart, "GA", 2, 50.0))

    undone = invoker.undo(5)

    assert undone == 1


def test_invoker_redo_reapplies_undone_command():
    cart = Cart()
    invoker = CartInvoker()
    invoker.run(AddTicketCommand(cart, "GA", 2, 50.0))
    invoker.undo(1)

    redone = invoker.redo(1)

    assert redone == 1
    assert cart.items()["GA"] == (2, 50.0)


def test_invoker_running_new_command_clears_redo_stack():
    cart = Cart()
    invoker = CartInvoker()
    invoker.run(AddTicketCommand(cart, "GA", 2, 50.0))
    invoker.undo(1)

    invoker.run(AddTicketCommand(cart, "VIP", 1, 120.0))

    assert invoker.redo(1) == 0
