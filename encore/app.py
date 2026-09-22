
from .pricing import EarlyBirdPricing
from .cart import Cart, AddTicketCommand, RemoveTicketCommand, SetPricingStrategyCommand, CartInvoker
from .waitlist import Show, EmailWaitlistNotifier, SMSWaitlistNotifier


def main():
    cart = Cart()
    invoker = CartInvoker()

    invoker.run(AddTicketCommand(cart, "GA", 3, 45.0))
    invoker.run(AddTicketCommand(cart, "VIP", 1, 120.0))
    print("Subtotal:", cart.subtotal())

    invoker.run(SetPricingStrategyCommand(cart, EarlyBirdPricing(15)))
    print("Total with early-bird pricing:", cart.total())

    invoker.undo(1)  # back to standard pricing
    print("Total after undoing the pricing change:", cart.total())

    invoker.run(RemoveTicketCommand(cart, "GA", 2))
    print("Remaining GA tickets:", cart.items().get("GA"))

    invoker.undo(1)  # restore the removed GA tickets
    print("GA tickets after undo:", cart.items().get("GA"))

    show = Show("Hamilton - Closing Night", available_seats=0)
    fan_email = EmailWaitlistNotifier("fan@example.com")
    fan_sms = SMSWaitlistNotifier("+34600000000")
    show.join_waitlist(fan_email)
    show.join_waitlist(fan_sms)

    show.release_seats(2)  # sold out -> available, both fans notified
    for message in fan_email.sent:
        print(message)
    for message in fan_sms.sent:
        print(message)


if __name__ == "__main__":
    main()
