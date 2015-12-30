import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
from datetime import date





def load_csv(csv_file):
	'load csv file to list of dictionaries'
	try:
		data = []
		raw_data = csv.DictReader(open(csv_file))
		print "Data loaded!" 
		for each_row in raw_data:
			data.append(each_row)
		return data
	except ValueError:
		print "Error: " + ValueError	
		return []

def filter_rows_by_value(data_dictionaries, field, value):
	'filter rows validating one field, normally from a discrete set of values'
	filtered_rows = filter(lambda each_row: each_row[field] == value, data_dictionaries)
	#print "rows filtered by value = ", len(filtered_rows)
	return filtered_rows

def filter_rows_by_value_negative_logic(data_dictionaries, field, value):
	'filter rows validating not equal to one field, normally from a discrete set of values'
	filtered_rows = filter(lambda each_row: each_row[field] != value, data_dictionaries)
	#print "rows filtered by value = ", len(filtered_rows)
	return filtered_rows

def filter_rows_by_date(data_dictionaries, since, until):
	'Filter rows validating dates. "since" and "until" are tuples "(year, month, day)"'
	since_date = date(since[0], since[1], since[2])
	until_date = date(until[0], until[1], until[2])
	filtered_rows = []
	for each_row in data_dictionaries:
		each_date_list = each_row["dteday"].split('-')
		each_date = date(int(each_date_list[0]), int(each_date_list[1]), int(each_date_list[2]))
		if since_date <= each_date <= until_date:
			filtered_rows.append(each_row)
	#print "rows filtered by date = ", len(filtered_rows)
	return filtered_rows


def get_time_series(data_dictionaries, since, until, value_field):
	'get a vector (one column of data) representing numeric measurements over an interval of time'
	since_date = date(since[0], since[1], since[2])
	until_date = date(until[0], until[1], until[2])
	time_axis = []
	value_axis = []
	for each_row in data_dictionaries:
		each_date_list = each_row["dteday"].split('-')
		each_date = date(int(each_date_list[0]), int(each_date_list[1]), int(each_date_list[2]))
		if since_date <= each_date <= until_date:
			time_axis.append(each_row['instant'])
			value_axis.append(each_row[value_field])
	#print "vector lenght selected by date = ", len(value_axis)
	values = [float(x) for x in value_axis]
	return time_axis, values



def get_time_series_stats(data_dictionaries, since, until, value_field, stat):
	'get the basic statistics sum, average, max, min of a time series'
	since_date = date(since[0], since[1], since[2])
	until_date = date(until[0], until[1], until[2])
	time_axis = []
	value_axis = []
	for each_row in data_dictionaries:
		each_date_list = each_row["dteday"].split('-')
		each_date = date(int(each_date_list[0]), int(each_date_list[1]), int(each_date_list[2]))
		if since_date <= each_date <= until_date:
			time_axis.append(each_row['instant'])
			value_axis.append(each_row[value_field])
	#print "vector lenght selected by date = ", len(value_axis)
	values = [int(x) for x in value_axis]
	if stat == 'sum':
		return sum(values)
	elif stat == 'average':
		return sum(values)/float(len(values))
	elif stat == 'max':
		return max(values)
	elif stat == 'min':
		return min(values)
	else:
		return 0

def graph_bars_2groups(group_1, group_2, label_tuple_x, label_1, label_2):
	fig, ax = plt.subplots()
	index = np.arange(len(group_1))
	bar_width = 0.35
	rects1 = plt.bar(index, group_1, bar_width, label=label_1, color='b')
	rects2 = plt.bar(index + bar_width, group_2, bar_width, label=label_2, color='r')
	plt.xticks(index + bar_width, label_tuple_x)
	plt.tight_layout()
	plt.legend()
	plt.show()


def graph_pie_chart(labels, sizes):
	plt.pie(sizes, labels=labels)
	plt.show()


def graph_2D(X,Y, x_label, y_label):
	plt.plot(X, Y, 'r')
	plt.grid(True)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.show()

def multi_graph_2D(vectors_list, x_label, y_label):
	for each_vector_pair in vectors_list:
		plt.plot(each_vector_pair[0], each_vector_pair[1])
	plt.grid(True)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.show()







# Report Figure 1
def a_1():
	'First look at the total of bike rentals'
	# get the time series the whole rental bikes i.e. field 'cnt'
	time_instant, all_rentals = get_time_series(all_data, (2011,1,1), (2012,12,31), 'cnt')
	graph_2D(time_instant, all_rentals, 'day of the year', 'total of rentals')

# Report Figure 2
def a_2():
	'over all comparison between years'
	# get the time series per year of the total rental bikes i.e. field 'cnt'
	time_instant_2011, all_rental_2011 = get_time_series(all_data, (2011,1,1), (2011,12,31), 'cnt')

	# note 2012 is leap-year and 29 febrary will be remueved for better day-to-day comparison
	all_rental_2012_no_leap_year = filter_rows_by_value_negative_logic(all_data, 'dteday', '2012-02-29')
	time_instant_2012, all_rental_2012 = get_time_series(all_rental_2012_no_leap_year, (2012,1,1), (2012,12,31), 'cnt')

	#basic statistics of each year
	reg_2011 = get_time_series_stats(all_data, (2011,1,1), (2011,12,31), 'registered', 'sum')
	cas_2011 = get_time_series_stats(all_data, (2011,1,1), (2011,12,31), 'casual', 'sum')
	cnt_2011 = get_time_series_stats(all_data, (2011,1,1), (2011,12,31), 'cnt', 'sum')
	reg_2012 = get_time_series_stats(all_data, (2012,1,1), (2012,12,31), 'registered', 'sum')
	cas_2012 = get_time_series_stats(all_data, (2012,1,1), (2012,12,31), 'casual', 'sum')
	cnt_2012 = get_time_series_stats(all_data, (2012,1,1), (2012,12,31), 'cnt', 'sum')


	print "-------------------"
	print "Statistics of 2011:"
	print "Registered rentals: ", reg_2011
	print "Casual rentals: ", cas_2011
	print "Total of rentals: ", cnt_2011
	print "Registered to casual ratio: ", reg_2011 / float(cas_2011)
	print "-------------------"
	print "Statistics of 2012:"
	print "Registered rentals: ", reg_2012
	print "Casual rentals: ", cas_2012
	print "Total of rentals: ", cnt_2012
	print "Registered to casual ratio: ", reg_2012 / float(cas_2012)

	# plot both bike rental of two years in the same X axis 
	multi_graph_2D([[time_instant_2011, all_rental_2011],[time_instant_2011, all_rental_2012]], 'day of the year', 'total of rentals')

# Report Figure 3
def a_3():
	'comparison between casual and registered people'
	# get the time series casual users i.e. field 'casual'
	time_instant_casual, casual_users = get_time_series(all_data, (2011,1,1), (2012,12,31), 'casual')

	# note 2012 is leap-year and 29 febrary will be remueved for better day-to-day comparison
	registered_no_leap_year = filter_rows_by_value_negative_logic(all_data, 'dteday', '2012-02-29')
	time_instant_registered, registered_users = get_time_series(registered_no_leap_year, (2011,1,1), (2012,12,31), 'registered')
	
	
	print casual_users
	# compute the standard deviation in both years of the number of rentals by casual and registered users
	casual_std = np.std(casual_users)
	registered_std = np.std(registered_users)
	print "mean of daily casual rentals: ", get_time_series_stats(all_data, (2011,1,1), (2012,12,31), 'casual', 'average')
	print "mean of daily registered rentals: ", get_time_series_stats(all_data, (2011,1,1), (2012,12,31), 'registered', 'average')
	print "Standard deviation of casual rentals: ", casual_std
	print "Standard deviation of registered rentals: ", registered_std

	# plot both type of usuers separately in both years
	multi_graph_2D([[time_instant_casual, casual_users],[time_instant_registered, registered_users]], 'day of the year', 'total of rentals')

# Report Figure 4
def a_4():
	'comparison between rentals, feeling temperature and humidity'
	# get the time series for total rentals i.e. field 'cnt', windspeed,  feeling temperature and humidity
	time_instant_cnt, total_rentals = get_time_series(all_data, (2011,1,1), (2012,12,31), 'cnt')
	time_instant_hum, humidity = get_time_series(all_data, (2011,1,1), (2012,12,31), 'hum')
	time_instant_atemp, feeling_temperature = get_time_series(all_data, (2011,1,1), (2012,12,31), 'atemp')
	time_instant_windspeed, windspeed = get_time_series(all_data, (2011,1,1), (2012,12,31), 'windspeed')

	s_hum = 3000
	scaled_humidity = [s_hum*x for x in humidity]
	
	s_atemp = 5000
	scaled_feeling_temperature = [s_atemp*x for x in feeling_temperature]

	s_windspeed = 5000
	scaled_windspeed = [s_windspeed*x for x in windspeed]

	print "-------------------"
	print "Coeficient of correlation of bike rentals and feeling temperature: ", np.corrcoef(total_rentals, feeling_temperature)[1,0]
	print "Coeficient of correlation of bike rentals and windspeed: ", np.corrcoef(total_rentals, windspeed)[1,0]
	print "Coeficient of correlation of bike rentals and humidity: ", np.corrcoef(total_rentals, humidity)[1,0]
	

	# plot both type of usuers separately in both years
	multi_graph_2D([[time_instant_cnt, total_rentals],[time_instant_hum, scaled_humidity],[time_instant_atemp, scaled_feeling_temperature], [time_instant_windspeed, scaled_windspeed]], 'day of the period 2011-2012', 'total of rentals vs windspeed vs temperature vs humidity')

# Report Figure 5
def a_5():
	'Statistics by weather category and rentals'
	# get the time series for casual and regular users by weather category
	clear = filter_rows_by_value(all_data, 'weathersit', '1')
	cloudy = filter_rows_by_value(all_data, 'weathersit', '2')
	light_rain = filter_rows_by_value(all_data, 'weathersit', '3')
	heavy_rain = filter_rows_by_value(all_data, 'weathersit', '4')

	casual_clear = get_time_series_stats(clear, (2011,1,1), (2012,12,31), 'casual', 'sum')
	registered_clear = get_time_series_stats(clear, (2011,1,1), (2012,12,31), 'registered', 'sum')

	casual_cloudy = get_time_series_stats(cloudy, (2011,1,1), (2012,12,31), 'casual', 'sum')
	registered_cloudy = get_time_series_stats(cloudy, (2011,1,1), (2012,12,31), 'registered', 'sum')

	casual_light_rain = get_time_series_stats(light_rain, (2011,1,1), (2012,12,31), 'casual', 'sum')
	registered_light_rain = get_time_series_stats(light_rain, (2011,1,1), (2012,12,31), 'registered', 'sum')

	casual_heavy_rain = get_time_series_stats(heavy_rain, (2011,1,1), (2012,12,31), 'casual', 'sum')
	registered_heavy_rain = get_time_series_stats(heavy_rain, (2011,1,1), (2012,12,31), 'registered', 'sum')

	labels = ['casual_clear', 'registered_clear', 'casual_cloudy', 'registered_cloudy', 'casual_light_rain', 'registered_light_rain', 'casual_heavy_rain', 'registered_heavy_rain']
	sizes =  [casual_clear, registered_clear, casual_cloudy, registered_cloudy, casual_light_rain, registered_light_rain, casual_heavy_rain, registered_heavy_rain]

	print "-------------------"
	print "Registered users in clear weather: ", registered_clear
	print "Casual users in clear weather: ", casual_clear
	print "Registered users in cloudy weather: ", registered_cloudy
	print "Casual users in cloudy weather: ", casual_cloudy
	print "Registered users in light rain weather: ", registered_light_rain
	print "Casual users in light rain weather: ", casual_light_rain
	print "Registered users in heavy rain weather: ", registered_heavy_rain
	print "Casual users in heavy rain weather: ", casual_heavy_rain

	print "Avergage daily rental in clear weather: ", get_time_series_stats(clear, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Avergage daily rental in cloudy weather: ", get_time_series_stats(cloudy, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Avergage daily rental in light rain weather: ", get_time_series_stats(light_rain, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Avergage daily rental in heavy rain weather: 0"

	graph_pie_chart(labels, sizes)

# Report Figure 6
def a_6():
	'Statistics by weather category'
	# get the time series for casual and regular users by weather category
	clear = filter_rows_by_value(all_data, 'weathersit', '1')
	cloudy = filter_rows_by_value(all_data, 'weathersit', '2')
	light_rain = filter_rows_by_value(all_data, 'weathersit', '3')
	heavy_rain = filter_rows_by_value(all_data, 'weathersit', '4')

	total_clear_days = len(clear)
	total_cloudy_days = len(cloudy)
	total_light_rain_days = len(light_rain)
	total_heavy_rain_days = len(heavy_rain)
	

	labels = ['clear', 'cloudy', 'light_rain', 'heavy_rain']
	sizes =  [total_clear_days, total_cloudy_days, total_light_rain_days, total_heavy_rain_days]

	print "-------------------"
	print "Days with clear weather: ", total_clear_days
	print "Days with cloudy weather: ", total_cloudy_days
	print "Days with light rain weather: ", total_light_rain_days
	print "Days with heavy rain weather: ", total_heavy_rain_days
	
	graph_pie_chart(labels, sizes)

# Report Figure 7
def a_7():
	'Comparison between average days of the week'
	# remove holidays to consider them separately
	all_data_no_holidays = filter_rows_by_value(all_data, 'holiday', '0')
	only_holidays = filter_rows_by_value(all_data, 'holiday', '1')

	sundays = filter_rows_by_value(all_data_no_holidays, 'weekday', '0')
	mondays = filter_rows_by_value(all_data_no_holidays, 'weekday', '1')
	tuesdays = filter_rows_by_value(all_data_no_holidays, 'weekday', '2')
	wednesdays = filter_rows_by_value(all_data_no_holidays, 'weekday', '3')
	thursdays = filter_rows_by_value(all_data_no_holidays, 'weekday', '4')
	fridays = filter_rows_by_value(all_data_no_holidays, 'weekday', '5')
	saturdays = filter_rows_by_value(all_data_no_holidays, 'weekday', '6')

	casual_sundays = get_time_series_stats(sundays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_sundays = get_time_series_stats(sundays, (2011,1,1), (2012,12,31), 'registered', 'average')

	casual_mondays = get_time_series_stats(mondays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_mondays = get_time_series_stats(mondays, (2011,1,1), (2012,12,31), 'registered', 'average')

	casual_tuesdays = get_time_series_stats(tuesdays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_tuesdays = get_time_series_stats(tuesdays, (2011,1,1), (2012,12,31), 'registered', 'average')

	casual_wednesdays = get_time_series_stats(wednesdays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_wednesdays = get_time_series_stats(wednesdays, (2011,1,1), (2012,12,31), 'registered', 'average')

	casual_thursdays = get_time_series_stats(thursdays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_thursdays = get_time_series_stats(thursdays, (2011,1,1), (2012,12,31), 'registered', 'average')

	casual_fridays = get_time_series_stats(fridays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_fridays = get_time_series_stats(fridays, (2011,1,1), (2012,12,31), 'registered', 'average')

	casual_saturdays = get_time_series_stats(saturdays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_saturdays = get_time_series_stats(saturdays, (2011,1,1), (2012,12,31), 'registered', 'average')

	casual_holidays = get_time_series_stats(only_holidays, (2011,1,1), (2012,12,31), 'casual', 'average')
	registered_holidays = get_time_series_stats(only_holidays, (2011,1,1), (2012,12,31), 'registered', 'average')

	
	casuals = (casual_mondays, casual_tuesdays, casual_wednesdays, casual_thursdays, casual_fridays, casual_saturdays, casual_sundays, casual_holidays)
	registereds = (registered_mondays, registered_tuesdays, registered_wednesdays, registered_thursdays, registered_fridays, registered_saturdays, registered_sundays, registered_holidays)

	print "-------------------"
	print "Mondays registered to casual ratio: ", registered_mondays/casual_mondays
	print "Tuesdays registered to casual ratio: ", registered_tuesdays/casual_tuesdays
	print "Wednesdays registered to casual ratio: ", registered_wednesdays/casual_wednesdays
	print "Thursdays registered to casual ratio: ", registered_thursdays/casual_thursdays
	print "Fridays registered to casual ratio: ", registered_fridays/casual_fridays
	print "Saturdays registered to casual ratio: ", registered_saturdays/casual_saturdays
	print "Sundays registered to casual ratio: ", registered_sundays/casual_sundays
	print "Holidays registered to casual ratio: ", registered_holidays/casual_holidays

	print "Average daily rental on Mondays: ", get_time_series_stats(mondays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Average daily rental on tuesdays: ", get_time_series_stats(tuesdays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Average daily rental on wednesdays: ", get_time_series_stats(wednesdays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Average daily rental on thursdays: ", get_time_series_stats(thursdays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Average daily rental on fridays: ", get_time_series_stats(fridays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Average daily rental on saturdays: ", get_time_series_stats(saturdays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Average daily rental on sundays: ", get_time_series_stats(sundays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	print "Average daily rental on holidays: ", get_time_series_stats(only_holidays, (2011,1,1), (2012,12,31), 'cnt', 'average')
	
	graph_bars_2groups(casuals, registereds, ('Monday', 'Tuesday', 'Wedsnesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Holiday'), 'Casual users', 'Registered users')

# Report Figure 9
def a_9():
	'Hourly average of casual and registered rentals on Fridays'
	Fridays = filter_rows_by_value(all_data_hourly, 'weekday', '5')

	F_0 = filter_rows_by_value(Fridays, 'hr', '0')
	F_1 = filter_rows_by_value(Fridays, 'hr', '1')
	F_2 = filter_rows_by_value(Fridays, 'hr', '2')
	F_3 = filter_rows_by_value(Fridays, 'hr', '3')
	F_4 = filter_rows_by_value(Fridays, 'hr', '4')
	F_5 = filter_rows_by_value(Fridays, 'hr', '5')
	F_6 = filter_rows_by_value(Fridays, 'hr', '6')
	F_7 = filter_rows_by_value(Fridays, 'hr', '7')
	F_8 = filter_rows_by_value(Fridays, 'hr', '8')
	F_9 = filter_rows_by_value(Fridays, 'hr', '9')
	F_10 = filter_rows_by_value(Fridays, 'hr', '10')
	F_11 = filter_rows_by_value(Fridays, 'hr', '11')
	F_12 = filter_rows_by_value(Fridays, 'hr', '12')
	F_13 = filter_rows_by_value(Fridays, 'hr', '13')
	F_14 = filter_rows_by_value(Fridays, 'hr', '14')
	F_15 = filter_rows_by_value(Fridays, 'hr', '15')
	F_16 = filter_rows_by_value(Fridays, 'hr', '16')
	F_17 = filter_rows_by_value(Fridays, 'hr', '17')
	F_18 = filter_rows_by_value(Fridays, 'hr', '18')
	F_19 = filter_rows_by_value(Fridays, 'hr', '19')
	F_20 = filter_rows_by_value(Fridays, 'hr', '20')
	F_21 = filter_rows_by_value(Fridays, 'hr', '21')
	F_22 = filter_rows_by_value(Fridays, 'hr', '22')
	F_23 = filter_rows_by_value(Fridays, 'hr', '23')

	F_0_casual = get_time_series_stats(F_0, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_1_casual = get_time_series_stats(F_1, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_2_casual = get_time_series_stats(F_2, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_3_casual = get_time_series_stats(F_3, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_4_casual = get_time_series_stats(F_4, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_5_casual = get_time_series_stats(F_5, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_6_casual = get_time_series_stats(F_6, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_7_casual = get_time_series_stats(F_7, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_8_casual = get_time_series_stats(F_8, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_9_casual = get_time_series_stats(F_9, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_10_casual = get_time_series_stats(F_10, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_11_casual = get_time_series_stats(F_11, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_12_casual = get_time_series_stats(F_12, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_13_casual = get_time_series_stats(F_13, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_14_casual = get_time_series_stats(F_14, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_15_casual = get_time_series_stats(F_15, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_16_casual = get_time_series_stats(F_16, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_17_casual = get_time_series_stats(F_17, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_18_casual = get_time_series_stats(F_18, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_19_casual = get_time_series_stats(F_19, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_20_casual = get_time_series_stats(F_20, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_21_casual = get_time_series_stats(F_21, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_22_casual = get_time_series_stats(F_22, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_23_casual = get_time_series_stats(F_23, (2011,1,1), (2012,12,31), 'casual', 'average')

	F_0_registered = get_time_series_stats(F_0, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_1_registered = get_time_series_stats(F_1, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_2_registered = get_time_series_stats(F_2, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_3_registered = get_time_series_stats(F_3, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_4_registered = get_time_series_stats(F_4, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_5_registered = get_time_series_stats(F_5, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_6_registered = get_time_series_stats(F_6, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_7_registered = get_time_series_stats(F_7, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_8_registered = get_time_series_stats(F_8, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_9_registered = get_time_series_stats(F_9, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_10_registered = get_time_series_stats(F_10, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_11_registered = get_time_series_stats(F_11, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_12_registered = get_time_series_stats(F_12, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_13_registered = get_time_series_stats(F_13, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_14_registered = get_time_series_stats(F_14, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_15_registered = get_time_series_stats(F_15, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_16_registered = get_time_series_stats(F_16, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_17_registered = get_time_series_stats(F_17, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_18_registered = get_time_series_stats(F_18, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_19_registered = get_time_series_stats(F_19, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_20_registered = get_time_series_stats(F_20, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_21_registered = get_time_series_stats(F_21, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_22_registered = get_time_series_stats(F_22, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_23_registered = get_time_series_stats(F_23, (2011,1,1), (2012,12,31), 'registered', 'average')

	casuals = (F_0_casual, F_1_casual, F_2_casual, F_3_casual, F_4_casual, F_5_casual, F_6_casual, 
		F_7_casual, F_8_casual, F_9_casual, F_10_casual, F_11_casual, F_12_casual, F_13_casual, F_14_casual, 
		F_15_casual, F_16_casual, F_17_casual, F_18_casual, F_19_casual, F_20_casual, F_21_casual, F_22_casual, F_23_casual)

	registereds = (F_0_registered, F_1_registered, F_2_registered, F_3_registered, F_4_registered, F_5_registered, F_6_registered,
		F_7_registered, F_8_registered, F_9_registered, F_10_registered, F_11_registered, F_12_registered, F_13_registered, F_14_registered,
		F_15_registered, F_16_registered, F_17_registered, F_18_registered, F_19_registered, F_20_registered, F_21_registered, 
		F_22_registered, F_23_registered)

	label_tuple_x = ('1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm',
		'1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm', '12 pm')

	graph_bars_2groups(casuals, registereds, label_tuple_x, 'Casual users', 'Registered users')

# Report Figure 8
def a_8():
	'Hourly average of casual and registered rentals on Wednesdays'
	Wednesdays = filter_rows_by_value(all_data_hourly, 'weekday', '3')

	F_0 = filter_rows_by_value(Wednesdays, 'hr', '0')
	F_1 = filter_rows_by_value(Wednesdays, 'hr', '1')
	F_2 = filter_rows_by_value(Wednesdays, 'hr', '2')
	F_3 = filter_rows_by_value(Wednesdays, 'hr', '3')
	F_4 = filter_rows_by_value(Wednesdays, 'hr', '4')
	F_5 = filter_rows_by_value(Wednesdays, 'hr', '5')
	F_6 = filter_rows_by_value(Wednesdays, 'hr', '6')
	F_7 = filter_rows_by_value(Wednesdays, 'hr', '7')
	F_8 = filter_rows_by_value(Wednesdays, 'hr', '8')
	F_9 = filter_rows_by_value(Wednesdays, 'hr', '9')
	F_10 = filter_rows_by_value(Wednesdays, 'hr', '10')
	F_11 = filter_rows_by_value(Wednesdays, 'hr', '11')
	F_12 = filter_rows_by_value(Wednesdays, 'hr', '12')
	F_13 = filter_rows_by_value(Wednesdays, 'hr', '13')
	F_14 = filter_rows_by_value(Wednesdays, 'hr', '14')
	F_15 = filter_rows_by_value(Wednesdays, 'hr', '15')
	F_16 = filter_rows_by_value(Wednesdays, 'hr', '16')
	F_17 = filter_rows_by_value(Wednesdays, 'hr', '17')
	F_18 = filter_rows_by_value(Wednesdays, 'hr', '18')
	F_19 = filter_rows_by_value(Wednesdays, 'hr', '19')
	F_20 = filter_rows_by_value(Wednesdays, 'hr', '20')
	F_21 = filter_rows_by_value(Wednesdays, 'hr', '21')
	F_22 = filter_rows_by_value(Wednesdays, 'hr', '22')
	F_23 = filter_rows_by_value(Wednesdays, 'hr', '23')

	F_0_casual = get_time_series_stats(F_0, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_1_casual = get_time_series_stats(F_1, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_2_casual = get_time_series_stats(F_2, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_3_casual = get_time_series_stats(F_3, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_4_casual = get_time_series_stats(F_4, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_5_casual = get_time_series_stats(F_5, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_6_casual = get_time_series_stats(F_6, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_7_casual = get_time_series_stats(F_7, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_8_casual = get_time_series_stats(F_8, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_9_casual = get_time_series_stats(F_9, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_10_casual = get_time_series_stats(F_10, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_11_casual = get_time_series_stats(F_11, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_12_casual = get_time_series_stats(F_12, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_13_casual = get_time_series_stats(F_13, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_14_casual = get_time_series_stats(F_14, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_15_casual = get_time_series_stats(F_15, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_16_casual = get_time_series_stats(F_16, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_17_casual = get_time_series_stats(F_17, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_18_casual = get_time_series_stats(F_18, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_19_casual = get_time_series_stats(F_19, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_20_casual = get_time_series_stats(F_20, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_21_casual = get_time_series_stats(F_21, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_22_casual = get_time_series_stats(F_22, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_23_casual = get_time_series_stats(F_23, (2011,1,1), (2012,12,31), 'casual', 'average')

	F_0_registered = get_time_series_stats(F_0, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_1_registered = get_time_series_stats(F_1, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_2_registered = get_time_series_stats(F_2, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_3_registered = get_time_series_stats(F_3, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_4_registered = get_time_series_stats(F_4, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_5_registered = get_time_series_stats(F_5, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_6_registered = get_time_series_stats(F_6, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_7_registered = get_time_series_stats(F_7, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_8_registered = get_time_series_stats(F_8, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_9_registered = get_time_series_stats(F_9, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_10_registered = get_time_series_stats(F_10, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_11_registered = get_time_series_stats(F_11, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_12_registered = get_time_series_stats(F_12, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_13_registered = get_time_series_stats(F_13, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_14_registered = get_time_series_stats(F_14, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_15_registered = get_time_series_stats(F_15, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_16_registered = get_time_series_stats(F_16, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_17_registered = get_time_series_stats(F_17, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_18_registered = get_time_series_stats(F_18, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_19_registered = get_time_series_stats(F_19, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_20_registered = get_time_series_stats(F_20, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_21_registered = get_time_series_stats(F_21, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_22_registered = get_time_series_stats(F_22, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_23_registered = get_time_series_stats(F_23, (2011,1,1), (2012,12,31), 'registered', 'average')

	casuals = (F_0_casual, F_1_casual, F_2_casual, F_3_casual, F_4_casual, F_5_casual, F_6_casual, 
		F_7_casual, F_8_casual, F_9_casual, F_10_casual, F_11_casual, F_12_casual, F_13_casual, F_14_casual, 
		F_15_casual, F_16_casual, F_17_casual, F_18_casual, F_19_casual, F_20_casual, F_21_casual, F_22_casual, F_23_casual)

	registereds = (F_0_registered, F_1_registered, F_2_registered, F_3_registered, F_4_registered, F_5_registered, F_6_registered,
		F_7_registered, F_8_registered, F_9_registered, F_10_registered, F_11_registered, F_12_registered, F_13_registered, F_14_registered,
		F_15_registered, F_16_registered, F_17_registered, F_18_registered, F_19_registered, F_20_registered, F_21_registered, 
		F_22_registered, F_23_registered)

	label_tuple_x = ('1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm',
		'1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm', '12 pm')

	graph_bars_2groups(casuals, registereds, label_tuple_x, 'Casual users', 'Registered users')

# Report Figure 10
def a_10():
	'Hourly average of casual and registered rentals on Sundays'
	Sundays = filter_rows_by_value(all_data_hourly, 'weekday', '0')

	F_0 = filter_rows_by_value(Sundays, 'hr', '0')
	F_1 = filter_rows_by_value(Sundays, 'hr', '1')
	F_2 = filter_rows_by_value(Sundays, 'hr', '2')
	F_3 = filter_rows_by_value(Sundays, 'hr', '3')
	F_4 = filter_rows_by_value(Sundays, 'hr', '4')
	F_5 = filter_rows_by_value(Sundays, 'hr', '5')
	F_6 = filter_rows_by_value(Sundays, 'hr', '6')
	F_7 = filter_rows_by_value(Sundays, 'hr', '7')
	F_8 = filter_rows_by_value(Sundays, 'hr', '8')
	F_9 = filter_rows_by_value(Sundays, 'hr', '9')
	F_10 = filter_rows_by_value(Sundays, 'hr', '10')
	F_11 = filter_rows_by_value(Sundays, 'hr', '11')
	F_12 = filter_rows_by_value(Sundays, 'hr', '12')
	F_13 = filter_rows_by_value(Sundays, 'hr', '13')
	F_14 = filter_rows_by_value(Sundays, 'hr', '14')
	F_15 = filter_rows_by_value(Sundays, 'hr', '15')
	F_16 = filter_rows_by_value(Sundays, 'hr', '16')
	F_17 = filter_rows_by_value(Sundays, 'hr', '17')
	F_18 = filter_rows_by_value(Sundays, 'hr', '18')
	F_19 = filter_rows_by_value(Sundays, 'hr', '19')
	F_20 = filter_rows_by_value(Sundays, 'hr', '20')
	F_21 = filter_rows_by_value(Sundays, 'hr', '21')
	F_22 = filter_rows_by_value(Sundays, 'hr', '22')
	F_23 = filter_rows_by_value(Sundays, 'hr', '23')

	F_0_casual = get_time_series_stats(F_0, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_1_casual = get_time_series_stats(F_1, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_2_casual = get_time_series_stats(F_2, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_3_casual = get_time_series_stats(F_3, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_4_casual = get_time_series_stats(F_4, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_5_casual = get_time_series_stats(F_5, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_6_casual = get_time_series_stats(F_6, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_7_casual = get_time_series_stats(F_7, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_8_casual = get_time_series_stats(F_8, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_9_casual = get_time_series_stats(F_9, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_10_casual = get_time_series_stats(F_10, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_11_casual = get_time_series_stats(F_11, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_12_casual = get_time_series_stats(F_12, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_13_casual = get_time_series_stats(F_13, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_14_casual = get_time_series_stats(F_14, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_15_casual = get_time_series_stats(F_15, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_16_casual = get_time_series_stats(F_16, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_17_casual = get_time_series_stats(F_17, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_18_casual = get_time_series_stats(F_18, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_19_casual = get_time_series_stats(F_19, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_20_casual = get_time_series_stats(F_20, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_21_casual = get_time_series_stats(F_21, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_22_casual = get_time_series_stats(F_22, (2011,1,1), (2012,12,31), 'casual', 'average')
	F_23_casual = get_time_series_stats(F_23, (2011,1,1), (2012,12,31), 'casual', 'average')

	F_0_registered = get_time_series_stats(F_0, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_1_registered = get_time_series_stats(F_1, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_2_registered = get_time_series_stats(F_2, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_3_registered = get_time_series_stats(F_3, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_4_registered = get_time_series_stats(F_4, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_5_registered = get_time_series_stats(F_5, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_6_registered = get_time_series_stats(F_6, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_7_registered = get_time_series_stats(F_7, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_8_registered = get_time_series_stats(F_8, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_9_registered = get_time_series_stats(F_9, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_10_registered = get_time_series_stats(F_10, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_11_registered = get_time_series_stats(F_11, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_12_registered = get_time_series_stats(F_12, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_13_registered = get_time_series_stats(F_13, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_14_registered = get_time_series_stats(F_14, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_15_registered = get_time_series_stats(F_15, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_16_registered = get_time_series_stats(F_16, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_17_registered = get_time_series_stats(F_17, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_18_registered = get_time_series_stats(F_18, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_19_registered = get_time_series_stats(F_19, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_20_registered = get_time_series_stats(F_20, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_21_registered = get_time_series_stats(F_21, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_22_registered = get_time_series_stats(F_22, (2011,1,1), (2012,12,31), 'registered', 'average')
	F_23_registered = get_time_series_stats(F_23, (2011,1,1), (2012,12,31), 'registered', 'average')

	casuals = (F_0_casual, F_1_casual, F_2_casual, F_3_casual, F_4_casual, F_5_casual, F_6_casual, 
		F_7_casual, F_8_casual, F_9_casual, F_10_casual, F_11_casual, F_12_casual, F_13_casual, F_14_casual, 
		F_15_casual, F_16_casual, F_17_casual, F_18_casual, F_19_casual, F_20_casual, F_21_casual, F_22_casual, F_23_casual)

	registereds = (F_0_registered, F_1_registered, F_2_registered, F_3_registered, F_4_registered, F_5_registered, F_6_registered,
		F_7_registered, F_8_registered, F_9_registered, F_10_registered, F_11_registered, F_12_registered, F_13_registered, F_14_registered,
		F_15_registered, F_16_registered, F_17_registered, F_18_registered, F_19_registered, F_20_registered, F_21_registered, 
		F_22_registered, F_23_registered)

	label_tuple_x = ('1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm',
		'1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm', '12 pm')

	graph_bars_2groups(casuals, registereds, label_tuple_x, 'Casual users', 'Registered users')







# load data into memory
all_data = load_csv('day.csv')
all_data_hourly = load_csv('hour.csv')

# Graph generation. Uncomment function a_1 to a_10 to display graph and statistics 
# Numbering in functions correspond to Figures in the report
a_1()
#a_2()
#a_3()
#a_4()
#a_5()
#a_6()
#a_7()
#a_8()
#a_9()
#a_10()

 