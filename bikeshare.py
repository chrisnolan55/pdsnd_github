import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'desktop/project/chicago.csv',
              'new york': 'desktop/project/new_york_city.csv',
              'washington': 'desktop/project/washington.csv' }

month_choices = ['january','february','march','april','may','june','none']
day_choices = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','none']

#Obtain information from the end user with regard to city and filter data
def get_filters():
    print('Let\'s explore some Bikeshare Data! Please follow the prompts to further drill down into the available data')
    city=input('Please select a city to invesitgate: New York, Chicago, or Washington. \n ---Response:').lower()
    while city not in CITY_DATA:
            try:
                print('There was an error in your selection- please choose a valid city to view Bikeshare Data')
                city=input('Please select a city to invesitgate: New York, Chicago, or Washington \n ---Response:').lower()
                break
            except ValueError:
                print('Oops! Please input a valid selection')

# End user to select a month btw Jan and June- If the user inputs something else the while loop will ask them to reinuput thier answer until satisfied
    month=input('Please select a month from January through June to view Bikeshare Data- Please input "none" to select no month filter\n ---Response: ').lower()
    while month not in month_choices:
            try:
                print('There was an error in your selection- please select a valid month to filter Bikeshare Data')
                month=input('Please select a month from January through June to filter Bikeshare Data \n Please input "none" for no month filter. \n ---Response: ')
                break
            except ValueError:
                print('Oops! Please input a valid selection')

# end user to select a day- If the user inputs something else the while loop will ask them to reinuput thier answer
    day=input('Please select a specific day to view Bikeshare Data- Please input "none" for no day filter \n ---Response:').lower()
    while day not in day_choices:
        try:
            print('There was an error in your selection- please select a valid day to filter Bikeshare Data')
            month=input('Please select a day from Sunday through Saturday to filter bikeshare data \n Please input "none" for no day filter. \n ---Response: ')
            break
        except ValueError:
            print('Oops! Please input a valid selection')
    print('-'*100)
    print('You are viewing Bikeshare Data for the city of:', city.upper(), 'in the month of', month.upper(), 'for the day of', day.upper())
    print('-'*100)
    return city, month, day

##Dataframe using the selected city, month, and day
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
#convert start time and end time to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
#extract hour day and month from start time to create their own columns
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day
    df['month'] = df['Start Time'].dt.month
#filter by month if requested
    if month != 'none':
# use the index of the months list to get the corresponding int
        month = month_choices.index(month) + 1
# filter by month to create the new dataframe
        df = df[df['month'] == month]
# filter by day of week if applicable
    if day != 'none':
# filter by day of week to create the new dataframe
        day = day_choices.index(day) + 1
        df = df[df['day_of_week'] == day]
        # df = df[df['day_of_week'] == day.title()]
    return df
#Displays statistics on the most frequent times of travel
def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
# display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    frequent_hour=df['hour'].mode()[0]
    print('The most popular hour in which trips were started is:', frequent_hour)
# display the most common day of week
    df['day_of_week']=df['Start Time'].dt.day
    frequent_day = calendar.day_name[df['day_of_week'].mode()[0]]
    print('The most popular day of the week for trips is:', frequent_day)
# display the most common month
    df['month'] = df['Start Time'].dt.month
    frequent_month = calendar.month_name[df['month'].mode()[0]]
    print('The most popular month for trips is:', frequent_month)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip Information...\n')
    start_time = time.time()
# display most commonly used start station
    common_start_station= df['Start Station'].mode()[0]
    print('\nThe most commonly used start station for trips is:', common_start_station)
# display most commonly used end station
    common_end_station= df['End Station'].mode()[0]
    print('\nThe most commonly used end station for trips is:', common_end_station)
# display most frequent combination of start station and end station trip
    station_combination=df.loc[:, 'Start Station':'End Station'].mode()[0:]
    print('The most frequent combination of start and end station is:', station_combination)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
# display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is', total_travel_time)
# display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

def user_stats(df):
# Displays statistics on bikeshare users

    print('\nCalculating User Stats...\n')
    start_time = time.time()

# Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(user_type_count)

# Display counts of gender Gender and Birth Year available for NYC and Chicago ONLY- Gender info not available for Washington
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("Sorry, there is no data available due to your city selection.")

# Display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = df['Birth Year'].min()
      print('\n The earliest birth year is:', Earliest_Year)
    except KeyError:
      print("Sorry, there is no data available due to your city selection.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('The most recent birth year is:', Most_Recent_Year)
    except KeyError:
      print("Sorry, there is no data available due to your city selection.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('The most common birth year is:', Most_Common_Year)
    except KeyError:
      print("Sorry, there is no data available due to your city selection.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

#Displas 5 lines of raw data and asks the user if they would like to see more
def display_raw_data(df):
    row_index=0
    display=input("Would you like to view raw trip data? Please respond 'yes' or 'no' \n ---Response:").lower()
    while True:
        if display == 'no':
            return
        if display == 'yes':
            print(df[row_index: row_index +5])
            row_index = row_index +5
            display=input("Would you like to view raw trip data? Please respond 'yes' or 'no' \n ---Response:").lower()
    else:
        print("\n Please type 'yes' or 'no' with regard to your desire to see raw data.")
        return display_raw_data(df, current_line)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
