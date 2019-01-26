import os
Months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}

for filename in os.listdir("."):
  originalDateTime = filename.split(' ') //example: 18-Jan-2019 - 23-21-03.jpg
  date = originalDateTime[0] //18-Jan-2019
  datesplit = date.split('-') // '18', 'Jan', '2019'
  dayOfMonth = datesplit[0] //18
  month = datesplit[1] //Jan
  year = datesplit[2] //2019
  newFileName = year + '-' + Months.get(month, "none") + '-' + dayOfMonth + ' - ' + originalDateTime[2]
  print newFileName // 2019-01-18 - 23-21-03
  os.rename(filename, newFileName)