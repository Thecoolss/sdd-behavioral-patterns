import pytest
from encore.waitlist import Show, EmailWaitlistNotifier, SMSWaitlistNotifier


def test_release_seats_notifies_waitlist_when_show_was_sold_out():
    show = Show("Hamilton", available_seats=0)
    fan = EmailWaitlistNotifier("fan@example.com")
    show.join_waitlist(fan)

    show.release_seats(2)

    assert show.available_seats == 2
    assert len(fan.sent) == 1
    assert "Hamilton" in fan.sent[0]


def test_release_seats_does_not_notify_when_show_already_had_seats():
    show = Show("Hamilton", available_seats=5)
    fan = EmailWaitlistNotifier("fan@example.com")
    show.join_waitlist(fan)

    show.release_seats(2)

    assert fan.sent == []


def test_leave_waitlist_stops_future_notifications():
    show = Show("Hamilton", available_seats=0)
    fan = EmailWaitlistNotifier("fan@example.com")
    show.join_waitlist(fan)
    show.leave_waitlist(fan)

    show.release_seats(2)

    assert fan.sent == []


def test_multiple_observers_are_all_notified():
    show = Show("Hamilton", available_seats=0)
    email_fan = EmailWaitlistNotifier("fan@example.com")
    sms_fan = SMSWaitlistNotifier("+34600000000")
    show.join_waitlist(email_fan)
    show.join_waitlist(sms_fan)

    show.release_seats(1)

    assert len(email_fan.sent) == 1
    assert len(sms_fan.sent) == 1


def test_release_seats_rejects_non_positive_count():
    show = Show("Hamilton", available_seats=0)

    with pytest.raises(ValueError):
        show.release_seats(0)


def test_sell_seats_reduces_availability_without_notifying():
    show = Show("Hamilton", available_seats=3)
    fan = EmailWaitlistNotifier("fan@example.com")
    show.join_waitlist(fan)

    show.sell_seats(3)

    assert show.available_seats == 0
    assert fan.sent == []


def test_sell_seats_rejects_more_than_available():
    show = Show("Hamilton", available_seats=1)

    with pytest.raises(ValueError):
        show.sell_seats(2)
