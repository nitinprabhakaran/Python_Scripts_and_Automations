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

def get_current_and_previous_2nd_tuesday():
    today = datetime.today()
    year = today.year
    current_month = today.month

    # Get the second Tuesday of the current month
    second_tuesday_this_month = get_nth_weekday(year, current_month, weekday=1, n=2)

    # Determine the previous month and year
    if current_month == 1:
        previous_month = 12
        previous_month_year = year - 1
    else:
        previous_month = current_month - 1
        previous_month_year = year

    # Get the second Tuesday of the previous month
    second_tuesday_last_month = get_nth_weekday(previous_month_year, previous_month, weekday=1, n=2)

    return second_tuesday_last_month, second_tuesday_this_month

if __name__ == "__main__":
    previous_2nd_tuesday, current_2nd_tuesday = get_current_and_previous_2nd_tuesday()
    print(f"Previous month's 2nd Tuesday: {previous_2nd_tuesday.strftime('%Y-%m-%d')}")
    print(f"Current month's 2nd Tuesday: {current_2nd_tuesday.strftime('%Y-%m-%d')}")