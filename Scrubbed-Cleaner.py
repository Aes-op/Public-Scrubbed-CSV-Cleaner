import pandas as pd
import calendar
from datetime import datetime

# Attempts to open specified file as dataframe
def attemptToOpenFile(strName):
    try:
        pd.read_csv("{}".format(strName))
    except:
        print("The specified file could not be opened. Please ensure that the name is correct.\n")
        print("Windows filenames cannot contain the following reserved characters <, >, :, \", /, \, |, ?, or *.\n")
        return 0
    return 1


# Opens and returns the specified .csv file
def csvOpen(strName):
    file = pd.read_csv("{}".format(strName))
    print("CSV Opened\n")
    return file


# Filters all rows to only rows that contained the specified text in the column 'type'
def filterRowsToDesiredType(strDesiredType, df):
    print(datetime.now())
    df = df[df['type'] == '"scrubbed" Service']
    df = df.reset_index()
    df = df.drop(columns=['type'])
    df = df.dropna(axis=0, subset={'id', 'start time', 'end time', 'location', 'customer', 'customer id',
                                   'customer no show', 'state', 'staff', 'staff id'})
    print(datetime.now())
    print("Rows Filtered.\n")
    return df


# Function return the staff code/location, with handling for incorrect data
def splitStaffCode(strCode, mode):
    if '-' in str(strCode):
        splitItem = strCode.split('-')
        if mode == 'return code':
            return splitItem[0]
        elif mode == 'return location':
            return splitItem[1].strip()
    elif mode == 'return location':
        return ''
    else:
        return strCode

# The splitting in this module is based upon the standard formatting of the data when exported by the program the company uses  
def cleanCSV(df):
    print(datetime.now())
    # Renames 'staff' column to 'staff code'
    df = df.rename(columns={'staff': 'Staff code'})
    # Separates the staff column into staff code and staff location columns
    df['Staff location'] = df['Staff code'].map(lambda x: splitStaffCode(x, 'return location'))
    df['Staff code'] = df['Staff code'].map(lambda x: splitStaffCode(x, 'return code'))
    # Creates and populates the date column
    df['Date'] = df['start time'].map(lambda x: (str(x).split('T'))[0])
    # Cleans the start and end time columns
    df['start time'] = df['start time'].map(lambda x: ((str(x).split('T'))[1].split('-'))[0])
    df['end time'] = df['end time'].map(lambda x: ((str(x).split('T'))[1].split('-'))[0])
    # Populates the day of the week column using the calendar.day_name function and the date
    df['Day of the week'] = df['Date'].map(lambda x: calendar.day_name[(datetime.strptime(x, '%Y-%m-%d')).weekday()])
    # Populates the length column by calculating the difference between the end and start times
    df['length'] = pd.to_timedelta(df['end time']) - pd.to_timedelta(df['start time'])
    df['length'] = df['length'].map(lambda x: str(x).split('days ')[1])
    print(datetime.now())
    print("CSV File Cleaned! \n")
    return df


fileFoundVar = 0
while fileFoundVar == 0:
    fileToOpenName = input("What is the name of the .csv file that should be cleaned? \n"
                           "(The file type \".csv\" will be appended at the end of the input and please keep in mind "
                           "that Windows filenames cannot contain the following reserved characters "
                           "<, >, :, \", /, \, |, ?, or *. ): ") + ".csv"
    print("\n")
    fileFoundVar = attemptToOpenFile(fileToOpenName)
dfMain = csvOpen(fileToOpenName)
dfMain = filterRowsToDesiredType('"scrubbed" Service', dfMain)
dfMain = cleanCSV(dfMain)
dfMain = dfMain.rename(columns={'index': 'Index', 'id': 'ID', 'start time': 'Start time', 'end time': 'End time',
                        'length': 'Length', 'location': 'Location', 'customer': 'Customer',
                        'customer id': 'Customer ID', 'customer no show': 'Customer no show',
                        'state': 'State', 'staff id': 'Staff ID', 'notes': 'Notes'})
# Rearranges the columns into a more easily readable format
dfMain = dfMain[['Index', 'ID', 'Date', 'Day of the week', 'Start time', 'End time', 'Length', 'Location',
         'Customer', 'Customer ID', 'Customer no show', 'State', 'Staff code', 'Staff location', 'Staff ID',
         'Notes']]
writeFileCompleteVar = 0
while writeFileCompleteVar == 0:
    try:
        writeFile = input("What should the cleaned .csv file be saved as? \n"
                          "(The file type \".csv\" will be appended at the end of the input "
                          "and please keep in mind that Windows filenames cannot contain the following "
                          "reserved characters <, >, :, \", /, \, |, ?, or *. ): ") + ".csv"
        dfMain.to_csv("{}".format(writeFile))
        writeFileCompleteVar = 1
    except:
        print("The file could not be saved as {}. It may already exist or use reserved characters. "
              "Please enter a different name for the file.".format(writeFile))       
print("\n.csv file has been saved\n")
