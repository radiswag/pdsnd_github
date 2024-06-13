# Radiel Gebreselassie
## June 14, 2024

### Purpose:
The purpose of this project is to analyze bikeshare data from three major cities: Chicago, New York City, and Washington, D.C. The project aims to provide insights into bike usage patterns and demographics to support urban planning and transportation decision-making.

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Enter the city name (chicago, new york city, washington): ').lower()
            if city in CITY_DATA:
                break
            else:
                raise ValueError("Invalid city name.")
        except ValueError as e:
            print(e)

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        try:
            month = input('Enter the month (all, january, february, ... , june): ').lower()
            if month in months:
                break
            else:
                raise ValueError("Invalid month.")
        except ValueError as e:
            print(e)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        try:
            day = input('Enter the day of the week (all, monday, tuesday, ... sunday): ').lower()
            if day in days:
                break
            else:
                raise ValueError("Invalid day.")
        except ValueError as e:
            print(e)

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f'Most Common Month: {most_common_month}')

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {most_common_day}')

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {most_common_start_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f'Most Commonly Used Start Station: {most_common_start_station}')

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f'Most Commonly Used End Station: {most_common_end_station}')

    # display most frequent combination of start station and end station trip
    most_common_start_end_combination = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print(f'Most Common Trip from Start to End: {most_common_start_end_combination}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time} seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_travel_time} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'User Types:\n{user_types}')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'\nGender Counts:\n{gender_counts}')
    else:
        print('\nGender data not available for this city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f'\nEarliest Year of Birth: {earliest_year}')
        print(f'Most Recent Year of Birth: {most_recent_year}')
        print(f'Most Common Year of Birth: {most_common_year}')
    else:
        print('\nBirth Year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Displays 5 rows of data at a time based on user input."""
    start_loc = 0
    while True:
        raw_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
        if raw_data.lower() != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
