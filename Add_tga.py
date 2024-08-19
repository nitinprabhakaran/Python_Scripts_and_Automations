from datetime import datetime, timedelta

def get_nth_weekday(year, month, weekday, n):
    """Get the nth occurrence of a weekday in a given month and year."""
    # Find the first day of the month
    first_day = datetime(year, month, 1)
    # Find the first occurrence of the desired weekday
    first_occurrence = first_day + timedelta(days=(weekday - first_day.weekday() + 7) % 7)
    # Calculate the nth occurrence
    nth_occurrence = first_occurrence + timedelta(weeks=n-1)
    return nth_occurrence

def get_previous_and_next_2nd_tuesday():
    today = datetime.today()
    year = today.year
    month = today.month

    # Calculate the 2nd Tuesday of the current month
    second_tuesday_this_month = get_nth_weekday(year, month, weekday=1, n=2)

    if today > second_tuesday_this_month:
        # If today is after the 2nd Tuesday of this month, calculate next 2nd Tuesday
        # and previous 2nd Tuesday in the next/previous months
        previous_2nd_tuesday = second_tuesday_this_month
        if month == 12:
            next_2nd_tuesday = get_nth_weekday(year + 1, 1, weekday=1, n=2)
        else:
            next_2nd_tuesday = get_nth_weekday(year, month + 1, weekday=1, n=2)
    else:
        # If today is before or on the 2nd Tuesday of this month, calculate next 2nd Tuesday
        # and previous 2nd Tuesday in the previous/next months
        next_2nd_tuesday = second_tuesday_this_month
        if month == 1:
            previous_2nd_tuesday = get_nth_weekday(year - 1, 12, weekday=1, n=2)
        else:
            previous_2nd_tuesday = get_nth_weekday(year, month - 1, weekday=1, n=2)

    return previous_2nd_tuesday, next_2nd_tuesday

if __name__ == "__main__":
    previous_2nd_tuesday, next_2nd_tuesday = get_previous_and_next_2nd_tuesday()
    print(f"Previous 2nd Tuesday: {previous_2nd_tuesday.strftime('%Y-%m-%d')}")
    print(f"Next 2nd Tuesday: {next_2nd_tuesday.strftime('%Y-%m-%d')}")