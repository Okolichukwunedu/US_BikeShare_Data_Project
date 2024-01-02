import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
        cities = ["chicago", "new york city", "washington"]
        city = input('Enter city to analyse (Chicago, New York city, Washington): ').lower()
        if city in cities:
            break
        else:
            print("You have not entered a valid city name")

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['All', 'January', 'February', 'March', 'April', 'June', 'May', 'June']
        month = input("Enter month to filter by (All, January......, June): " ).title()
        if month in months:
            break
        else:
            print("You have not entered a valid month")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = input("Enter day of the week to filter by (Monday, Tuesday,.....,Sunday: ").title()
        if day in day_of_week:
            break
        else:
            print("Please input a valid day_of_week")

    print('-'*40)
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

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
    most_month = df['month'].value_counts().idxmax()
    print ('Most common month is {}'.format(most_month))

    # TO DO: display the most common day of week
    most_day = df['day_of_week'].value_counts().idxmax()
    print ('Most common day of week is {}'.format(most_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_hour = df['hour'].value_counts().idxmax()
    print ('Most common hour of day is {}'.format(most_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_start_station = df['Start Station'].value_counts().idxmax()
    print (' Most common Start Station used is {}'.format(com_start_station))

    # TO DO: display most commonly used end station
    com_end_station = df['End Station'].value_counts().idxmax()
    print (' Most common End Station is {}'.format(com_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['comb_station']=df['Start Station'] + " and " + df['End Station']
    com_comb_station = df['comb_station'].mode()[0]
    print (' Most common combination of Station used is {}'.format(com_comb_station))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print ('Total time of Travel is {}'.format(total_time))


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print ('the mean time of travel is {}'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("The User types and their counts: \n {}".format(user_type))

    # TO DO: Display counts of gender
    #Because the 'Gender and 'Birth Year' columns contain missing values (NaN)s and so we use a try function block to manage the Key Errors
    try:
        gender_count = df['Gender'].value_counts()
        print('The Gender types and their counts are: \n {}'.format(gender_count))
    except KeyError:
        print("Value missing for this User")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_YOB = df['Birth Year'].min()
        recent_YOB = df['Birth Year'].max()
        most_YOB = df['Birth Year' ].value_counts().idxmax()
        print('Oldest birth year of customers: {}., \n Birth year of youngest customer: {}., \n Most common Birth Year: {}.'.format(earliest_YOB, recent_YOB, most_YOB))
    except KeyError:
        print("this value is missing birth year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
