# Public-Scrubbed-CSV-Cleaner

All scrubbed information will be replaced with a generic word, for example "company" instead of the name of the company.

WARNINGS: 
  - {pandas is a required non-standard python module that is imported in this script. This script will not run without it.}
  - {The .csv file must be in the same project folder as the python script. This can be changed by hardcoding a path to the location of the      file on your system.}

FURTHER WARNINGS IN THE README WILL BE CONTAINED IN {}

This is a Python ver 3.7 script designed to clean exported "-" .csv files for "Company".

The flow of this script is as follows:
  - Opens the .csv file
  - Deletes rows that do not contain the desired type in the 'type' column {Type is default as "column type"}
  - Separates the staff column into a staff code column and staff location column
  - Creates and populates the date column using information from the start time column
  - Cleans the start and end time columns of extraneous information such as time zone and date
  - Populates the length column by calculating the delta between the start and end time columns
  - Creates and populates a day of the week column using information from the date column
  - Reformats the column names to be uppercase and arranged in a more readable order
