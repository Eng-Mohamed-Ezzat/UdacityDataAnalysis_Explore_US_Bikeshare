import time
import pandas as pd
import numpy as np
import calendar as cl
import os

DATA_CITY = { 'All' : 'all',
              'Chicago': 'chicago.csv',
              'New york': 'new_york_city.csv',
              'Washington': 'washington.csv' }

DATA_Month = {
    0: 'All', 
    1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
    7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

DATA_Day = ['All'] + [d[0:3] for d in cl.day_name]

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
        msg = "Choose city:\n" \
        "[0]: All\n" \
        "[1]: Chicago\n" \
        "[2]: New York\n" \
        "[3]: Washington\n" \
        "Please type city name or number:"
        usrcity = input(msg)

        if usrcity.isnumeric() and int(usrcity) in range(len(DATA_CITY)) or usrcity.title() in DATA_CITY.keys():
            city = list(DATA_CITY.keys())[int(usrcity)] if usrcity.isnumeric() else usrcity.title() 
            break
        else:
            print("Wrong city Entry. :(")
    
    msg = "- You are choose {} {}.".format(city.title() if city.lower()!="all" else city.lower(),"city" if city.lower()!="all" else "cities")
    print(msg)
    
    # get user input for month (all, january, february, ... , june)

    while True:
        msg = "Choose month:\n" \
        "[0]: All\n" \
        "[?]: Month Number\n" \
        "Please type month name or number:"
        usrmonth = input(msg)

        if usrmonth.isnumeric() and int(usrmonth) in range(len(DATA_Month)) or usrmonth[:3].title() in DATA_Month.values():
            month = list(DATA_Month.values())[int(usrmonth)] if usrmonth.isnumeric() else usrmonth[:3].title() 
            break
        else:
            print("Wrong month Entry. :(")

    msg = "- You are choose {} {}.".format(month.lower(),"month" if month.lower() !="all" else "available monthes")
    print(msg)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        msg = "Choose day:\n" \
        "[0]: All\n" \
        "[?]: Day Name\n" \
        "Please type week day name or number:"
        usrday = input(msg)

        if usrday.isnumeric() and int(usrday) in range(len(DATA_Day)) or usrday[:3].title() in DATA_Day:
            day = DATA_Day[int(usrday)] if usrday.isnumeric() else usrday[:3].title() 
            break
        else:
            print("Wrong day Entry. :(")

    msg = "- You are choose {}{}.".format(day.lower(),"day" if day.lower()!="all" else " available days")
    print(msg)

    
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
    # Read data from csv file that represent the city 
    print("Loading {} city database to view {} month(s) and {} day(s).".format(city,month.lower(),day),end="")

    
    df = pd.read_csv("{}\\bikeshare-2\\{}".format(os.getcwd(),DATA_CITY['Chicago']),parse_dates=['Start Time','End Time'])
    print(".",end="")
    df['Month'] = [m[0:3] for m in df['Start Time'].dt.month_name()]
    print(".",end="")
    df['Day'] = [d[0:3] for d in df['Start Time'].dt.day_name()]
    print(".",end="")
    df['Start Hour'] = df['Start Time'].dt.hour
    print(".",end="")
    df['Trip from to'] = df['Start Station'] +" -> " + df['End Station']


    # Load Special
    df = df[(df.Day == (df.Day if day.lower()== 'all' else day)) & (df.Month == (df.Month if month.lower()=="all" else month))]    
    print(".")
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is {}.".format(df['Month'].mode()[0]))

    # display the most common day of week
    print("The most common day of week is {}.".format(df['Day'].mode()[0]))

    # display the most common start hour
    print("The most common start hour is {}.".format(df['Start Hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station: {}.".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station: {}.".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip:\n{}.".format(df['Trip from to'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time: {}.".format(df['Trip Duration'].sum()))


    # display mean travel time
    print("The mean travel time: {}.".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if "User Type" in df:
        myGroups = df.groupby(['User Type'])['User Type'].groups
        msg=""
        for k in myGroups:
            msg += "{}\t:{}\n".format(k,len(myGroups[k]))
        
        print("The counts of user types:\n{}".format(msg))
    else:
        print("The User Type Column not exist in the csv file.")

    # Display counts of gender
    if "Gender" in df:
        myGroups = df.groupby(['Gender'])['Gender'].groups
        msg=""
        for k in myGroups:
            msg += "{}\t:{}\n".format(k,len(myGroups[k]))
        
        print("The counts of gender:\n{}".format(msg))
    else:
        print("The Gender Column not exist in the csv file.")
    

    # Display earliest, most recent, and most common year of birth
  
    if "Birth Year" in df:
        earliest = int(df['Birth Year'].max())
        recent = int(df.loc[df.index[-1], 'Birth Year'])
        common = int(df['Birth Year'].mode()[0])
        print("The earliest is {}, most recent is {}, and most common year of birth is {}.".format(earliest,recent,common))
    else:
        print("The Birth Year Column not exist in the csv file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # city, month, day = get_filters()
        # df = load_data(city, month, day)
        print("==================================================")
        df=load_data('Chicago', 'May', 'Fri')
        time_stats(df)

        station_stats(df)
        
        trip_duration_stats(df)

        user_stats(df)
        break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
