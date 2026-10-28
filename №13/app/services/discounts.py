"""Скидки, которые зависят от самого проживания."""
import config


def long_stay_percent(nights_count):
    if nights_count >= config.LONG_STAY_NIGHTS:
        return config.LONG_STAY_PERCENT
    return 0
