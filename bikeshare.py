import time
import datetime #allows us to use a conversion from numerical datetime to a specific day of the week
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities_set = {'new york', 'chicago', 'washington'}
    while True: 
        city = input('Please choose a city. Valid options are "chicago", "new york", or "washington".').lower()
        if city not in cities_set:
            print('Sorry, your selection is invalid. Please try again. \n')
            continue
        else:
            print('You chose ' + str(city) + '. \n')
            break


    # TO DO: get user input for month (all, january, february, ... , june)
    month_set = {'january', 'february', 'march', 'april', 'may', 'june'}
    while True:
        month = input('Please select a month of interest from January to June inclusive, or "all" to consider all months.').lower()
        if month not in month_set:
            if month == 'all':
                print('Okay, considering all months. \n')
                break
            elif month != 'all':
                print('Sorry, your selection is invalid. Please try again. \n')
                continue
        else:
            print('You chose ' + str(month) + '. \n')
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days_set = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    while True:
        day = input('Please select a day of interest, or "all" to consider all days.').lower()
        if day not in days_set:
            if day == 'all':
                print('Okay, considering all days. \n')
                break
            elif day != 'all':
                print('Sorry, your selection is invalid. Please try again. \n')
                continue
        else:
            print('You chose ' + str(day) + '. \n')
            break

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
    #First load the selected city.
    if city == 'chicago':
        csv = 'chicago.csv'
    elif city == 'new york':
        csv = 'new_york_city.csv'
    else:
        csv = 'washington.csv'
    df = pd.read_csv(csv) #load the required city
    
    df['Start Time'] = pd.to_datetime(df['Start Time']) #convert Start Time to a datetime 
    df['End Time'] = pd.to_datetime(df['End Time']) #convert End Time to a datetime
    df['weekday'] = df['Start Time'].dt.day_name().str.lower() #will output the name of the day of the week. Lower-case to prevent problems.
    df['month'] = df['Start Time'].dt.month_name().str.lower() #will output the name of the month for each row. Lower-case to prevent problems
    
    #Apply filter for the chosen day of the week: 
    if day != 'all':
        df = df[df['weekday'] == day] #Filters our dataframe to specifically trips which start on the day selected.
    
    #Apply filter for the chosen month:    
    if month != 'all':
        df = df[df['month'] == month] #Filters our dataframe to specifically trips which start in the month selected.
    
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month was ' + most_common_month)
    

    # TO DO: display the most common day of week
    most_common_day = df['weekday'].mode()[0]
    print('The most common day was ' + most_common_day)

    # TO DO: display the most common start hour
    most_common_start_hour = (df['Start Time'].dt.hour).mode()[0] #Pull the most common hour from the start times, from 0 to 23.
    print('The most common hour was ' + str(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0] #Pulls the most commonly-used start station.
    print('The most commonly used start station was ' + most_common_start_station + '\n')
    
    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0] #Pulls the most commonly-used end station.
    print('The most commonly used end station was ' + most_common_end_station + '\n')

    # TO DO: display most frequent combination of start station and end station trip
    df['Combined start-end'] = df[['Start Station', 'End Station']].apply(lambda x: '#'.join(x), axis=1) #We use a lambda function because the more 'simple' method did not seem to work. We use # because this symbol doesn't appear in any of the cells so it makes splitting easy. 
    most_common_SE_pair_joined = df['Combined start-end'].mode()
    most_common_SE_pair = most_common_SE_pair_joined[0].split('#')
    print('The most frequent combination of start station and end station was starting at ' + most_common_SE_pair[0] + ' and ending at ' + most_common_SE_pair[1] + '\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # This question is unclear so I have assumed that "total travel time" refers to the sum of travel durations for all trips in the dataframe and I have assumed the units is "minutes". 
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was ' + str(total_travel_time) + ' minutes. \n')
    

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time was ' + str(mean_travel_time) + ' minutes. \n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types: \n')
    print(df['User Type'].value_counts())
    print('\n')

    # TO DO: Display counts of gender
    #Gender exists only for New York and Chicago data. Therefore we first filter on whether city is correct. 
    if 'Gender' in df.columns:
        print('Counts of user genders: \n')
        print(df['Gender'].value_counts())
        print('\n')
          
    # TO DO: Display earliest, most recent, and most common year of birth
    #Birth data only exists for Chicago and New York. Therefore first filter on whether city is correct.
    if 'Birth Year' in df.columns:
          print('Birth data: \n')
          earliest_year = df['Birth Year'].min() 
          print('The earliest year of birth was ' + str(earliest_year) + '\n') #Note: for New York this appears to be 1885 which seems like a mistake. 
          latest_year = df['Birth Year'].max() 
          print('The most recent year of birth was ' + str(latest_year) + '\n')
          most_common_year = df['Birth Year'].mode()
          print('The most common year of birth was ' + str(most_common_year[0]) + '\n')
        
          
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    start = 0
    end = 5
    while True:
        while True:
            options_set = {'y', 'n'}
            user_choice = input('Would you like to see 5 rows of raw data from your selected dataframe? Y/N  ').lower()
            if user_choice not in options_set: 
                print('Sorry, you must choose Y or N. \n')
                continue
            else: 
                break 
        if user_choice == 'y':
            print(df.iloc[np.arange(start, end)])
            start += 5
            end += 5
            print('Select Y again to see the next 5 rows of data, or N to end.')
        else:
            break

        
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
