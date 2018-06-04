import sys
import numpy as np
import skfuzzy as fuzz


def approximate_time_remaining_until_walk(hours_passed_after_pee, crying_intensity):
    last_time_peed_raw = int(hours_passed_after_pee)
    crying_intensity_raw = int(crying_intensity)

    if last_time_peed_raw < 0:
        raise ValueError('Last time peed must be greater than 0')

    if crying_intensity_raw < 0 or crying_intensity_raw > 10:
        raise ValueError('Crying intensity must be greater than 0 and less than or equals than 10')

    if last_time_peed_raw > 10:
        exit('now')

    last_time_peed_range = np.arange(0, 11, 0.1)
    crying_intensity_range = np.arange(0, 11, 0.1)

    last_time_peed_now_function = fuzz.zmf(last_time_peed_range, 0, 1.5)
    last_time_peed_couple_of_hours_function = fuzz.gaussmf(last_time_peed_range, 0.75, 2.9)
    last_time_peed_many_hours_function = fuzz.smf(last_time_peed_range, 2.8, 4.5)

    crying_intensity_none_function = fuzz.zmf(crying_intensity_range, 0, 1.5)
    crying_intensity_slight_function = fuzz.gauss2mf(crying_intensity_range, 0.5, 0.6, 0.8, 1.7)
    crying_intensity_medium_function = fuzz.gaussmf(crying_intensity_range, 1.6, 4.5)
    crying_intensity_high_function = fuzz.smf(crying_intensity_range, 5, 7.9)

    walk_after_how_much_time_range = np.arange(0, 5, 0.1)
    walk_now_function = fuzz.zmf(walk_after_how_much_time_range, 0, 0.5)
    walk_after_a_while_function = fuzz.gaussmf(walk_after_how_much_time_range, 0.4, 0.8)
    walk_later_function = fuzz.gaussmf(walk_after_how_much_time_range, 0.6, 1.9)
    walk_after_couple_of_hours_function = fuzz.smf(walk_after_how_much_time_range, 2.3, 3.8)

    def convert_last_time_peed(last_time_peed_in_hours):
        now = fuzz.interp_membership(last_time_peed_range, last_time_peed_now_function, last_time_peed_in_hours)
        couple_of_hours = fuzz.interp_membership(last_time_peed_range, last_time_peed_couple_of_hours_function, last_time_peed_in_hours)
        many_hours = fuzz.interp_membership(last_time_peed_range, last_time_peed_many_hours_function, last_time_peed_in_hours)
        return [now, couple_of_hours, many_hours]

    def convert_crying_intensity(crying_intensity):
        none = fuzz.interp_membership(crying_intensity_range, crying_intensity_none_function, crying_intensity)
        slight = fuzz.interp_membership(crying_intensity_range, crying_intensity_slight_function, crying_intensity)
        medium = fuzz.interp_membership(crying_intensity_range, crying_intensity_medium_function, crying_intensity)
        high = fuzz.interp_membership(crying_intensity_range, crying_intensity_high_function, crying_intensity)
        return [none, slight, medium, high]

    last_time_peed_converted = convert_last_time_peed(last_time_peed_raw)
    crying_intensity_converted = convert_crying_intensity(crying_intensity_raw)

    rules = [
        np.fmax(last_time_peed_converted[-1], crying_intensity_converted[-1]),
        np.fmin(last_time_peed_converted[0], np.fmax(crying_intensity_converted[1], crying_intensity_converted[0])),
        np.fmin(last_time_peed_converted[1], crying_intensity_converted[0]),
        np.fmin(last_time_peed_converted[1], crying_intensity_converted[2]),
        np.fmin(last_time_peed_converted[1], crying_intensity_converted[1])
    ]

    walk_now = np.fmin(rules[0], walk_now_function)
    walk_after_a_while = np.fmin(rules[-2], walk_after_a_while_function)
    walk_later = np.fmin(rules[-1], walk_later_function)
    walk_after_couple_of_hours = np.fmin(rules[1], walk_after_couple_of_hours_function)

    aggregated = np.fmax(walk_now, np.fmax(walk_after_a_while, np.fmax(walk_later, walk_after_couple_of_hours)))
    result = fuzz.defuzz(walk_after_how_much_time_range, aggregated, 'centroid')

    return result