import pytest
from encore.pricing import StandardPricing, EarlyBirdPricing, GroupPricing


def test_standard_pricing_leaves_subtotal_unchanged():
    assert StandardPricing().price(100.0, 3) == 100.0


def test_early_bird_pricing_applies_percentage_discount():
    strategy = EarlyBirdPricing(20)

    assert strategy.price(100.0, 2) == 80.0


@pytest.mark.parametrize("percent", [-1, 101])
def test_early_bird_pricing_rejects_invalid_percent(percent):
    with pytest.raises(ValueError):
        EarlyBirdPricing(percent)


def test_early_bird_pricing_never_goes_negative():
    strategy = EarlyBirdPricing(100)

    assert strategy.price(50.0, 1) == 0.0


def test_group_pricing_below_threshold_is_unchanged():
    strategy = GroupPricing(threshold=5, per_ticket_off=2.0)

    assert strategy.price(100.0, 4) == 100.0


def test_group_pricing_at_or_above_threshold_discounts_per_ticket():
    strategy = GroupPricing(threshold=5, per_ticket_off=2.0)

    assert strategy.price(100.0, 5) == 90.0


def test_group_pricing_never_goes_negative():
    strategy = GroupPricing(threshold=2, per_ticket_off=100.0)

    assert strategy.price(10.0, 2) == 0.0
