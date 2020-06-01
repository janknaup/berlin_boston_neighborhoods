# Mapping Berlin Neighborhoods to Boston
Tourists travelling between cities seek different experience. Some may want to experience something 
very different from their daily life at home. Some may be less adventurous, seeking an experience that
varies on what they are comfortable with, but not too much. And others may be interested in comparing
cities and neighborhoods, to experience how countries, cities and people differ and where they are alike.  

An important part of the travel experience is accommodation, and a very popular choice are Airbnbs. 
Therefore it is interesting to compare Airbnb listings between cities. For this study, the cities
of Boston and Berlin are chosen, based on being roughly similar in size.

Three questions can help them to find the right neighborhood for their stay and for exploring:
1. Which neighborhoods are the most and least similar between the cities?
2. Which neighborhoods in Berlin most closely fit he niches of the individual Boston neighborhoods?
3. Which are the properties of the neighborhoods that are similar or different between the two cities?

The results of this analysis have been posted at
https://medium.com/@janknaup/this-is-what-berlin-would-look-like-if-you-teleported-its-neighborhoods-to-boston-fb1afe1b5022

## Data source
Data is copied from Kaggle. Due to the large size, ist cannot be easily kept within the git repository. 

For Boston, the listings.csv file needs to be placed in the data/boston subdirectory
https://www.kaggle.com/airbnb/boston?select=listings.csv

For Berlin, the listings_summary.csv file needs to be placed in the data/berlin subdirectory
https://www.kaggle.com/brittabettendorf/berlin-airbnb-data?select=listings_summary.csv

## Included Jupyter Notebooks

*   **Exploration.ipynb:**  
    Some exploratory analysis of the data set, including crude attempt at predicting review scores  
*   **Berlin_Boston_Neighbourhoods.ipynb:**
    The data analysis comparing neighborhoods between cities

## Method of analysis
The analysis heavily relies on descriptive statistics. Since the individual analyses rely on neighborhood means, plus 
standard deviations and valid row counts, the handling of missing values is straightforward, they can simply be ignored.
The pandas aggregate functions mean(), std(), sum() and count() only operate on the valid subset of each column. 
Imputation by replacing mean values would be unsuitable. While not changing the means, it would unduly reduce the 
standard deviations and inflate the sample counts, indicating a false sense of statistical significance in the 
subsequent analysis of factor influence using Student's t-value. The same argument applies to replacing NaN with
other values. In the pre-treatment of categorical factors, NaN values are taken into account by adding an N/A indicator
column to use unavailability as an additional factor. Since all subsequent analysis is based on aggregate values, 
further missing values will only occur if a factor is missing for a whole neighborhood. In practice, this only occured
in the case where a column only held valid values for one of the cities. In these cases, the whole column was excluded
as it effectively only holds a redundant indication that the two cities being compared are not the same.
For some columns listing unique values, such as picture URLs, presence columns mapping valid entries to 1 and NaN 
to 0 are used instead.

Flag columns, i.e. the amenities column, are split into 0/1 indicator columns per flag. Categorical columns are 
converted to 0/1 dummy indicator columns, dropping the first dummy value and adding a N/A column, in order to maintain 
linear independence of the indicator columns.

All boolean values are converted to 0/1 integer values. The use of numerical indicators for boolean values 
automatically provides a fraction of true values per column upon calculation of the mean, facilitating interpretation.

To avoid that the comparison is dominated by the well known, purely geographical differences between Boston and Berlin,
a number of columns are excluded, especially latitude, longitude, city, state, zipcode, country, street. Additionally, 
columns that only have valid values for one city, columns with only one valid category, ID type columns and columns
with too many individual categories or descriptive texts are excluded. The full lists are given in the notebeook.

### Raw Similarity Between Neighborhoods
For the first question, the neighbourhoods are compared by the cartesian distance between the vectors of listing 
property mean values, grouped by neighborhood. The mean values are range-normalized over the whole data set to
avoid skewed weighting of properties with different units. Only the distances between Berlin and Boston neighborhoods 
are  calculated for resource economy. By using unnormalized mean values, difference that are specific to city or country 
are included in the cartesian distance. I.e. it is not possible to distinguish if a difference is caused by features
peculiar to a neighborhood, their city, or even the country. Consequently, the results map only a small set of Berlin 
neighborhoods to Boston counterparts. Historical evidence corroborates the assumption that these districts are the 
most similar to American cities in general.

### Neighborhood Niches
For the second question, the range norm is applied to the neighborhood mean listing properties, grouped by city 
instead of globally. This way, overall differences between the two cities are removed and relative properties of the
neighborhoods within their cities are compared. As expected, this mapping leads to a greater spread, with only a 
few double-mappings. These mappings are manually transferred to maps of Boston and Berlin neighborhoods for 
illustration.

### Listing Property Influence
For the third question, Student's t-score or t-value (specifically, the absolute of the t-value) is chosen. It is a
common measure to determine whether a difference between two samples or subsets is statistically relevant or not, by
relating it to the standard deviation of the population. Relevance is determined by a threshold value taken from the
Student's distribution function. It should be kept in mind though, that the precision of these thresholds is dependent 
on the normality of the underlying population and sample distributions, which in practice is never given. I.e. the 
choice of t-value threshold for relevance is always somewhat arbitrary. I chose 2.364, the 95% threshold for two-sided
distributions of 100 specimens. 100 specimens is small enough to be reasonable sure most neighborhoods give enough 
samples, and a 95% level of significance is quite customary.    

A neighborhood-by neighborhood comparison of the listing properties is possible, but leads to a 3D matrix that is
extremely hard to analyze. The heatmap of t-scores per neighborhood shows that the selection of properties which set
a neighborhood apart from the average is quite heterogeneous.

As an example, the only neighborhoods that were reported as closest to each other in both normalizations, i.e. Spandau 
and Cambridge are analyzed in more detail. To this end, the t-scores of their respective listing properties with 
respect to the global average as well as to each other are compared. Those factors that make the listings similar 
with respect to the whole set will have a high t-score relative to the average and a low t-score relative to each other.

## Required software versions and libraries
Python >= 3.7

+ jupyter >= 1.0.0
+ pandas >= 0.25.3
+ matplotlib >= 3.1.2
+ seaborn >= 0.10.1
+ scikit learn 0.22.1