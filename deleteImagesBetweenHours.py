# coding=utf-8
import os

for filename in os.listdir("."):
	if filename.startswith("c"):
		continue
	if filename.startswith("r"):
		continue
	if filename.startswith("d"):
		continue
        mystr=filename.split(' ')
        date = mystr[2]
        mystrsplit = date.split('-')
        hour = mystrsplit[0]
        minute = mystrsplit[1]
	if hour != '00':
		hour=hour.lstrip('0')
	#print 'hour: ', hour
	hour=int(hour)
	if hour < 20 and hour >9 or hour == '00' :
	#if hour =='00' or hour < 9:
		os.remove(filename)
		print date
