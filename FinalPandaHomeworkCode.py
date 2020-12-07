#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[5]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = r'C:\Users\14403\Desktop\school2.csv'
student_data_to_load = r'C:\Users\14403\Desktop\students2.csv'

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Calculate the percentage of students who passed math **and** reading (% Overall Passing)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[6]:


# Calculate the total number of schools
total_school = len(school_data_complete['school_name'].unique())
# Calculate the total number of students
total_student = school_data_complete['student_name'].count()
# Calculate the total budget
total_budget = sum(school_data_complete['budget'].unique())
# Calculate the average math score
average_math_score = school_data_complete['math_score'].mean()
# Calculate the average reading score
average_reading_score = school_data_complete['reading_score'].mean()
# Calculate the overall passing rate
overall_passing_score = (average_math_score + average_reading_score)/2
# Calculate the percentage of students with a passing math score (70 or greater)
passing_math_score = (school_data_complete[school_data_complete['math_score']>=70]['student_name'].count()/total_student)*100
# Calculate the percentage of students with a passing reading score (70 or greater)
passing_reading_score = (school_data_complete[school_data_complete['reading_score']>=70]['student_name'].count()/total_student)*100

# Create a dataframe to hold the above results and formatting
district = {
    'Total Schools':total_school,
    'Total Student':'{:,}'.format(total_student),
    'Total Budget':'${:,.2f}'.format(total_budget),
    'Average Math Score':average_math_score,
    'Average Reading Score':average_reading_score,
    '% Passing Math':passing_math_score,
    '% Passing Reading':passing_reading_score,
    '% Overall Passing Score':[overall_passing_score],  
}

district_summary = pd.DataFrame(district)
district_summary


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * % Overall Passing (The percentage of students that passed math **and** reading.)
#   
# * Create a dataframe to hold the above results

# In[7]:


# Grouped our complete data frame by school name 
grouped_school = school_data_complete.groupby(['school_name'])
# Calculate the total student for each school
total_student = grouped_school.size()
# Get the school type for each school
school_type = grouped_school['type'].first()
# Calculate the total budget for each school
total_budget = grouped_school['budget'].first()
# Calculate the budget per student for each school
t_budget_per_student = total_budget/total_student
# Calculate the average math score for each school
average_math_score = grouped_school['math_score'].mean()
# Calculate the average reading score for each school
average_reading_score = grouped_school['reading_score'].mean()
# Calculate the percentange of passing math score for each school
grouped_passing_math = school_data_complete[school_data_complete['math_score']>=70].groupby(['school_name']).size()
percent_passing_math = (grouped_passing_math/total_student)*100
# Calculate the percentange of passing math score for each school
grouped_passing_reading = school_data_complete[school_data_complete['reading_score']>=70].groupby(['school_name']).size()
percent_passing_reading = (grouped_passing_reading/total_student)*100
# Calculate the overall passing score for each school
percent_overall_passing = (percent_passing_math + percent_passing_reading)/2

# Create a dataframe to hold the above results
school={
    'School Type': school_type,
    'Total Students':total_student,
    'Total School Budget': total_budget,
    'Per Student Budget': t_budget_per_student,
    'Average Math Score': average_math_score,
    'Average Reading Score': average_reading_score,
    '% Passing Math': percent_passing_math,
    '% Passing Reading': percent_passing_reading,
    '% Overall Passing Rate': percent_overall_passing,
}
school_summary = pd.DataFrame(school)
# Create a copy of school summary data frame before formatting to be able to use the numeric data on original data frame later
displayed_school_summary = school_summary.copy()
# Formatting the display data frame
displayed_school_summary['Per Student Budget'] = displayed_school_summary['Per Student Budget'].map('${:,.2f}'.format)
displayed_school_summary['Total School Budget'] = displayed_school_summary['Total School Budget'].map('${:,.2f}'.format)
displayed_school_summary.index.name = None


# ## Top Performing Schools (By % Overall Passing)

# * Sort and display the top five performing schools by % overall passing.

# In[8]:


# Sort and display the top five schools by % passing rate
top_performing_schools = displayed_school_summary.sort_values(by='% Overall Passing Rate',ascending=False)
top_performing_schools.head()


# ## Bottom Performing Schools (By % Overall Passing)

# * Sort and display the five worst-performing schools by % overall passing.

# In[9]:


# Sort and display the five worst-performing schools
worst_performing_schools = displayed_school_summary.sort_values(by='% Overall Passing Rate')
worst_performing_schools.head()


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[10]:


# Calculate the average math score for students of 9th grade at each school
school_avg_math_9th = school_data_complete[school_data_complete['grade']=='9th'].groupby('school_name')['math_score'].mean()
# Calculate the average math score for students of 10th grade at each school
school_avg_math_10th = school_data_complete[school_data_complete['grade']=='10th'].groupby('school_name')['math_score'].mean()
# Calculate the average math score for students of 11th grade at each school
school_avg_math_11th = school_data_complete[school_data_complete['grade']=='11th'].groupby('school_name')['math_score'].mean()
# Calculate the average math score for students of 12th grade at each school
school_avg_math_12th = school_data_complete[school_data_complete['grade']=='12th'].groupby('school_name')['math_score'].mean()

# Create a dataframe to hold the above results
grade_math_score={
    '9th':school_avg_math_9th,
    '10th':school_avg_math_10th,
    '11th':school_avg_math_11th,
    '12th':school_avg_math_12th,
    }

math_score_by_grade = pd.DataFrame(grade_math_score)
math_score_by_grade.index.name = None
math_score_by_grade.head(20)


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[11]:


# Calculate the average reading score for students of 9th grade at each school
school_avg_reading_9th = school_data_complete[school_data_complete['grade']=='9th'].groupby('school_name')['reading_score'].mean()
# Calculate the average reading score for students of 10th grade at each school
school_avg_reading_10th = school_data_complete[school_data_complete['grade']=='10th'].groupby('school_name')['reading_score'].mean()
# Calculate the average reading score for students of 11th grade at each school
school_avg_reading_11th = school_data_complete[school_data_complete['grade']=='11th'].groupby('school_name')['reading_score'].mean()
# Calculate the average reading score for students of 12th grade at each school
school_avg_reading_12th = school_data_complete[school_data_complete['grade']=='12th'].groupby('school_name')['reading_score'].mean()

# Create a dataframe to hold the above results
grade_reading_score={
    '9th':school_avg_reading_9th,
    '10th':school_avg_reading_10th,
    '11th':school_avg_reading_11th,
    '12th':school_avg_reading_12th,
    }

reading_score_by_grade = pd.DataFrame(grade_reading_score)
reading_score_by_grade.index.name = None
reading_score_by_grade.head(20)


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[12]:



# Sample bins
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[13]:


# Create a new data frame by locating the desired columns
scores_spending = school_summary.loc[:,['Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','% Overall Passing Rate',]]
# Add a new columns named Spending Ranges (Per Student) and binning based off budget per student
scores_spending['Spending Ranges (Per Student)']= pd.cut(school_summary['Per Student Budget'],spending_bins,labels=group_names)
# Create a group based off of the bins
scores_spending = scores_spending.groupby('Spending Ranges (Per Student)').mean()
scores_spending.head()


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[14]:


# Sample bins
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[15]:


# Create a new data frame by locating the desired columns
scores_size = school_summary.loc[:,['Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','% Overall Passing Rate',]]
# Add a new columns named School Size and binning based off total students
scores_size['School Size']= pd.cut(school_summary['Total Students'],size_bins,labels=group_names)
# Create a group based off of the bins
scores_size = scores_size.groupby('School Size').mean()
scores_size.head()


# ## Scores by School Type

# * Perform the same operations as above, based on school type

# In[16]:


# Create a new data frame with our desired columns
scores_type = school_summary[['School Type','Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','% Overall Passing Rate',]]
# Create a group based off of the school type
scores_type = scores_type.groupby('School Type').mean()
scores_type.head()


# In[ ]:





# In[ ]:





# In[ ]:




