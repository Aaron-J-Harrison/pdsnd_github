import time
import pandas as pd
import numpy as np
import datetime as dt
import tablulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - returns a list containing integers (int) of
        the selected monthts
        (str) day - returns a list of days (str) for filtering the
        bikeshare data
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington).
    # Make the input case INSENSITIVE
    city = (input("""What city would you like to view?
    (chicago, new york city, washington) or type 'all'
    to view all city data: """)).lower()

    # Add error handling for invalid user imput
    # Make the input case INSENSITIVE
    while city not in ['chicago', 'new york city', 'washington', 'all']:
        print("""Data for {} is not available, please select another city
    (chicago, new york city, washington) or 'all' to view all city data: """
    .format(city))
        city = input('City: ').lower()
    if city == 'all':
        city = ['chicago', 'new york city', 'washington']

    # Check whether the user wants to filter the data.
    # Make the input case INSENSITIVE
    by_monthday = input(
    'Would you like to filter by month or day data (yes/no)? ').lower()

    # Add error handling for invalid user imput
    while by_monthday not in ['yes', 'no']:
        by_monthday = input(
        'Would you like to filter by month or day data (yes/no)? ').lower()

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    if by_monthday == 'yes':
        # Determine what month the user wants to filter on
        month = (input("""Which month do you want to view?
        Type 'all' to view all month data: """).title())
        # Add error handling for invalid user imput
        while (month not in months) and (month != 'All'):
            print("""Data for {} is not available, please select another month.
            Type the full month name please!""".format(month))
            month = input("""Which month do you want to view?
            Type 'all' to view all month data.""").title()

        if month in months:
            # Convert month to an int which can be used to filter the data
           month = months.index(month)+1
        else:
            month = [1, 2, 3, 4, 5, 6]

        # Deterine what day the user wants to filter on
        day = input("""Which weekday do you want to view?
        Enter 'all' to view all weekdays: """).title()

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']

        # Add error handling for invalid user imput
        while (day not in days) and (day != 'All'):
            print("""Data for {} is not available, please select another day.
            Type the full day name please!""".format(day))
            day = input("""Which weekday do you want to view?
            Enter 'all' to view all weekdays: """).title()
        if day == 'All':
           day = days

    # Sets the defult values of day and month for downstream applications
    else:
        day = days
        month = [1, 2, 3, 4, 5, 6]

    print('-'*79)

    # Return the key values so they can be input into downstream functions
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and
    day if applicable.

    Returns:
        (str) city - name of the city to analyze
        (int) month - returns a list containing integers (int)
        of the selected monthts
        (str) day - returns a list of days (str) for filtering
        the bikeshare data

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        the dataframe also contains the new columns 'month',
        'day_of_week' and 'hour'
    """
    # Create an empty dataframe to append data sets too
    df = pd.DataFrame()

    # Determine if user imput 'all' then pass the list of cities into
    # a for loop
    if type(city) == list:
        # Iterate over each city imput
        for x in city:
            loaded_data = pd.read_csv(CITY_DATA[x])
            df = df.append(loaded_data, ignore_index = True)
    else:
        df = pd.read_csv(CITY_DATA[city])

    # Create additional data columns for use in downstream analysis and convert
    # them to the correct data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['End Time'] = pd.to_datetime(df['End Time'])

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    # Apply filtering by selecting rows with specific months and days
    # Only apply filters when 'All' option is not selected
    if month != [1, 2, 3, 4, 5, 6]:
        df = df[df['month'] == month]

    if day != days:
        df = df[df['day_of_week'] == day]

    # Return the filtered dataframe
    return df
    print(df)

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print("""Statistics on most frequent times of travel
    """)

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    # Display the most common month
    if month == [1, 2, 3, 4, 5, 6]:
        top_month = (df['month'].mode(dropna=True)).tolist()[0]
        print("""{} is the most common month to use the bikeshare"""
        .format(months[top_month-1]))
    else:
        view_month = months[month-1]
        print("You selected to view {}".format(view_month))

    # Display the most common day of week
    if day == days:
        top_dow = df['day_of_week'].mode(dropna=True)[0]
        print("{} is the most common day of the week to use the bikeshare"
        .format(top_dow))
    else:
        print("You have selected data from {}'s in the dataset".format(day))

    # Display the most common start hour
    top_hour = df['hour'].mode(dropna=True)[0]
    top_hour = dt.time(top_hour)
    print("{} is the most common start hour to use the bikeshare"
    .format(str(top_hour)))
    print('-'*79)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print("""Displaying statistics on most popular stations in trips analysed
    """)

    # Display most commonly used start station
    top_start = df['Start Station'].mode(dropna=True)[0]
    print("{} is the most common bikeshare start station".format(top_start))

    # Display most commonly used end station
    top_end = df['End Station'].mode(dropna=True)[0]
    print("{} is the most common bikeshare destination".format(top_end))

    # Display most frequent combination of start station and end station trip
    # Create a new varible called "trip" which should be unique for each
    # Start/End combination. Then determine the mode of that column
    df["Trip"] = df['Start Station'] + " to " + df['End Station']
    top_trip = df["Trip"].mode(dropna=True)[0]
    print("The most common trip is {}".format(top_trip))

    print('-'*79)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("""Displaying data on the total and average trip duration
    """)

    # Display total travel time
    total_time = sum(df['Trip Duration'])
    print("The total amount bikeshare ride time is {} minutes"
    .format(total_time))

    # Display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The average bikeshare ride is {} minutes".format(mean_time))
    print('-'*79)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("""Displaying statistics on bikeshare users
    """)

    # Display counts of user types
    print(pd.value_counts(df['User Type']))

    # Display counts of gender
    # Add error handling for datasets without Gender infomation
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts(dropna=True)
        print(gender_counts)
    else:
        print('Gender infomation was not collected for this city')

    # Display earliest, most recent, and most common year of birth
    # Add error handling for datasets without Gender infomation
    if 'Birth Year' in df:
        most_recent_dob = df['Birth Year'].max(skipna = True)
        earliest_dob = df['Birth Year'].min(skipna = True)
        most_common_dob = (df['Birth Year'].mode(dropna = True)).tolist()
        print("The most recent birth year for riders was {}"
        .format(most_recent_dob))
        print("The earliest birth year for riders was {}"
        .format(earliest_dob))
        print("The most common birth year for riders was {}"
        .format(most_common_dob[0]))
    else:
        print('Date of birth infomation not collected for this city')
    print('-'*79)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_raw_data = (input(
        'Would you like to view the raw data (yes/no)? ')).lower()

        # Make sure all data is visible
        pd.set_option("display.max_rows", None, "display.max_columns", None)

        # All user to visualise the raw data
        # use If/Else statements to handle incorrect user imputs
        i=0
        while True:
            display_data = input(
            '\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if display_data.lower() != 'yes':
                break
            print(tabulate(df_default.iloc[np.arange(0+i,5+i)], headers ="keys"))
            i+=5

        restart = input('\nWould you like to restart the program? (yes/no).\n')

        if restart != 'yes':
            break

if __name__ == "__main__":
	main()
