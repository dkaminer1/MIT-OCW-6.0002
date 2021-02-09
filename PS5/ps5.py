# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy    # TODO
import math
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range( 1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    sol = []
    for int in degs:
        sol.append(pylab.polyfit(x , y , int))
    return sol

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """

    num = (y - estimated)
    mean = numpy.sum(y)/len(y)
    denom = y - mean
    for pt in range(len(y)):
        denom[pt] = denom[pt]**2
        num[pt] = num[pt]**2
    denom = numpy.sum(denom)
    num = numpy.sum(num)

    return (1-num/denom)
    

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    pylab.title('Temperature Over Time')
    pylab.xlabel('Years')
    pylab.ylabel('Celsius')
    pylab.plot(x, y, 'o', label = 'Data')
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], x)
        error = r_squared(y, estYVals)
        pylab.plot(x, estYVals,
                   label = 'Degree '\
                   + str(len(models[i])-1)\
                   + ', R2 = ' + str(round(error, 5)))
    pylab.legend(loc = 'best')    

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    yearcity_avg_dict = {}
    for year in years:
        yearcity_avg_dict[year] = 0
        for city in multi_cities:
            yeararray = climate.get_yearly_temp(city, year)
            yearcity_avg_dict[year] = yearcity_avg_dict[year] + numpy.sum(yeararray)/len(yeararray)
    for year in yearcity_avg_dict :
        yearcity_avg_dict[year] = yearcity_avg_dict[year]/len(multi_cities)
            
    return pylab.array(list(yearcity_avg_dict.values()))
    

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    windowed_avg = []
    for i in range(len(y)) :
        if i < window_length :
            windowed_avg.append(numpy.sum(y[:i+1])/(1+i))
        else :
            windowed_avg.append(numpy.sum(y[i+1-window_length : i+1]) / window_length)
#    print(windowed_avg)
    return windowed_avg
                                          
        

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    diff = y - estimated
    diff_total_sq = 0
    for i in range(len(diff)):
        diff_total_sq = diff_total_sq + diff[i]**2
    rmse = math.sqrt(diff_total_sq / len(diff) )
    return rmse
    
def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    year_avg_dict = {}
    std_dev_yr_list = []
    for year in years:
        year_avg_dict[year] = 0
        for city in multi_cities:
            yeararray = climate.get_yearly_temp(city, year)
            year_avg_dict[year] += yeararray/len(multi_cities)
        
        year_sq_val = 0
        year_array = year_avg_dict[year]
        for i in range(len(year_array)) :
            year_sq_val += (year_array[i])**2 / len(year_array)
        year_std = math.sqrt((year_sq_val - (numpy.sum(year_array)/len(year_array))**2))
        std_dev_yr_list.append(year_std)
    return pylab.array(std_dev_yr_list)


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    pylab.title('Std Dev Over Time')
    pylab.xlabel('Years')
    pylab.ylabel('TempStdDev')
    pylab.plot(x, y, 'o', label = 'Data')
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], x)
        error = rmse(y, estYVals)
        pylab.plot(x, estYVals,
                   label = 'Degree: '\
                   + str(len(models[i])-1)\
                   + ', rmse = ' + str(round(error, 5)))
    pylab.legend(loc = 'best') 

if __name__ == '__main__':
    pass
    # Part A.4
#    datafile = Climate('data.csv')
#    temp_ny_jan10 = []
#    for year in TRAINING_INTERVAL :
#        temp_ny_jan10.append(datafile.get_daily_temp('NEW YORK', 1, 10, year))
#    models = generate_models(TRAINING_INTERVAL, temp_ny_jan10 , [1])
#    evaluate_models_on_training(TRAINING_INTERVAL, temp_ny_jan10, models)
    
    # Part B
#    datafile = Climate('data.csv')
#    temp_ny = (list(gen_cities_avg(datafile,['NEW YORK'], TRAINING_INTERVAL)))
#    models = generate_models(TRAINING_INTERVAL, temp_ny , [1])
#    evaluate_models_on_training(TRAINING_INTERVAL, temp_ny, models)    
    
    
    # Part C
#    datafile = Climate('data.csv')
#    temp_city_avg = (list(gen_cities_avg(datafile,CITIES, TRAINING_INTERVAL)))
#    models = generate_models(TRAINING_INTERVAL, temp_city_avg, [1])
#    evaluate_models_on_training(TRAINING_INTERVAL, temp_city_avg, models)    

            
    # Part D.2
#    datafile = Climate('data.csv')
#    temp_city_avg = (list(gen_cities_avg(datafile,CITIES, TRAINING_INTERVAL)))
#    city_moving_avg = moving_average(temp_city_avg, 5)
#    models = generate_models(TRAINING_INTERVAL, city_moving_avg, [1])       
#    evaluate_models_on_training(TRAINING_INTERVAL, city_moving_avg, models)    



    # Part E
#    datafile = Climate('data.csv')
#    temp_std = gen_std_devs(datafile, CITIES, TRAINING_INTERVAL)
#    temp_moving_std = moving_average(temp_std, 5)
#    models = generate_models(TRAINING_INTERVAL, temp_moving_std, [1])
#    evaluate_models_on_testing(TRAINING_INTERVAL, temp_moving_std, models)