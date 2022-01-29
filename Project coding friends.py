#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load in the data
episodes = pd.read_csv(r"C:\Users\Dell\Downloads\friends_episodes.csv")
imdb = pd.read_csv(r"C:\Users\Dell\Downloads\friends_imdb.csv")


# In[2]:


# View the first 5 rows of the `episodes` dataframe
episodes.head()


# In[3]:


# View the first 5 rows of the `imdb` dataframe
imdb.head()


# In[4]:


# Print out the number of rows in each dataframe
print('episodes: {}'.format(len(episodes.index)))
print('imdb: {}'.format(len(imdb.index)))


# In[5]:


# Count the number of episodes in each season in the `episodes` dataframe, then sort by the season
print('Episodes\n {}'.format(episodes.value_counts('season').sort_index()))

print('')
# Count the number of episodes in each season in the `imdb` dataframe, then sort by the season
print('IMDB\n {}'.format(imdb.value_counts('season').sort_index()))


# In[6]:


# Print all rows for season 10 in the episodes dataframe
episodes[episodes['season']==10].head(20)


# In[7]:


# Remove episode 236 from the episodes dataframe, then print out the last 5 episodes in season 10 as well as the number of rows in the dataframe to verify that it worked
episodes = episodes[episodes['episode_num_overall'] != 236]

print('episodes: {}'.format(len(episodes.index)))
episodes[episodes['season']==10].tail()


# In[8]:


# Merge the two dataframes
df = pd.merge(episodes, imdb, how = 'left', left_on=['season', 'episode_num_in_season'], right_on=['season', 'episode_num'])

# Remove columns that we don't need
df.drop(['episode_num_in_season', 'title_x', 'episode_num_overall', 'title_y', 'prod_code', 'original_air_date_y'], axis=1, inplace=True)

# Clean up the column names
df.rename(columns={'original_air_date_x':'air_date'},inplace=True)

# Order the columns.  I like to do this because it is easier to interpret the data when looking at print outs of the first few rows
df = df[['season', 'episode_num', 'directed_by', 'written_by', 'air_date', 'us_viewers', 'imdb_rating', 'total_votes', 'desc']]

# Print the first 5 rows to make sure that the merge worked and that all the information is in df
df.head()


# In[9]:


# Create a list of all the main characters
characters = ['Monica', 'Rachel', 'Phoebe', 'Ross', 'Joey', 'Chandler']

# Using a loop, create a column for each character.  1 indicates the character is mentioned in the decription, 0 indicates they are not mentioned
for i in characters:
    df[i] = df['desc'].str.contains(i, case=False).astype(int)
    
# Remove the desc column, as it is no longer necessary
df.drop('desc', axis=1, inplace= True)

# Print first 5 rows to make sure we got what we wanted
df.head()


# In[10]:


# Create a new dataframe for character importance
char_importance = pd.melt(df, id_vars=['season', 'us_viewers', 'imdb_rating'], value_vars=characters, var_name='character', value_name='in_episode')

# Filtered `char_importance` to episodes that the characters appears in
char_importance = char_importance[char_importance['in_episode'] == 1]
char_importance.head()


# In[11]:


# Create Plot
plt.figure(figsize=(10,5)) 
sns.countplot(data=char_importance, y='character')
plt.suptitle('\'Friends\' Characters Importance', y = 1, fontsize=15)
plt.title('*Based on Appearance in Episode Description', y=.999, fontsize=10)


# In[12]:


# Create plot
plt.figure(figsize=(15,10)) 
sns.countplot(data=char_importance, y='season', hue='character')
plt.suptitle('\'Friends\' Characters Importance By Season', y = 1, fontsize=15)
plt.title('*Based on Appearance in Episode Description', y=1.09, fontsize=10)
plt.xlabel('Appearances')
plt.ylabel('Season')
plt.legend(title= 'Characters')


# In[13]:


# Create Average Views for each Character overall 
avg_char_views = char_importance[['character', 'imdb_rating']].groupby(['character']).mean().reset_index()

# Plot 
plt.figure(figsize=(10,10)) 
sns.barplot(x='imdb_rating', y='character', data=avg_char_views.sort_values('imdb_rating', ascending=False))
plt.suptitle('\'Friends\' Character Average IMDB Rating', fontsize=20)
plt.title('Entire Series - Based on IMDB Ratings of Episodes About Character', y=1.05, fontsize=10)
plt.xlabel('Average IMDB Rating')
plt.ylabel('Character')
plt.xlim([8.3, 8.5])


# In[14]:


# Prep data to be plotted
df['us_viewers'] = df['us_viewers'].astype(int)
df['written_by'] = df['written_by'].str.split('Teleplay', expand=True)[0]
df['written_by'] = df['written_by'].str.replace('Story by: ', '')

# writers dataframe. Group by the writers across entire series
writers_df = df[['written_by', 'us_viewers','imdb_rating']].groupby(['written_by']).mean().reset_index()

# How many episodes were done by each writing group
plt.figure(figsize=(15,12)) 
sns.countplot(data=df, y='written_by', order = df['written_by'].value_counts().index)
plt.suptitle('How Many Episodes of \'Friends\' Were Done by Each Writer? ', y = 1, fontsize=15)
plt.xlabel('Episodes')
plt.ylabel('Writing Team')


# In[15]:


# Plotting for each season individually, because one plot for all of them is unclear and difficult to read.
for i in df['season'].unique():
    plt.figure(figsize=(10,5)) 
    temp = df[df['season']==i]
    sns.countplot(data=temp, y='written_by', order = temp['written_by'].value_counts().index)
    plt.suptitle('How Many Episodes of \'Friends\' Were Done by Each Writer in Season {}?'.format(i), fontsize=15)
    plt.xlabel('Episodes')
    plt.ylabel('Writing Teams')


# In[16]:


# Create Plot
plt.figure(figsize=(15,12)) 
sns.barplot(x='us_viewers', y='written_by', data=writers_df.sort_values('us_viewers', ascending=False))
plt.suptitle('\'Friends\' Writer Team Average Number of Views per Episode', fontsize=20)
plt.title('Entire Series', y=1.05, fontsize=10)
plt.xlabel('Average Viewers per Episode \n(In Millions)')
plt.ylabel('Writers')


# In[17]:


# Create Plot
plt.figure(figsize=(10,7)) 
sns.countplot(data=df, y = 'directed_by', order = df['directed_by'].value_counts().index)
plt.suptitle('How many Episodes of \'Friends\' Was Each Directing Team Responsible For?', y = 1, fontsize=15)


# In[18]:


# writers dataframe. Group by the writers across entire series
directed_df = df[['directed_by', 'us_viewers','imdb_rating']].groupby(['directed_by']).mean().reset_index()

# plot
plt.figure(figsize=(15,12)) 
sns.barplot(x='imdb_rating', y='directed_by', data=directed_df.sort_values('imdb_rating', ascending=False))
plt.suptitle('\'Friends\' Each Directing Team\'s Average IMDB Rating Overall', fontsize=20)
plt.title('Entire Series', y=1.05, fontsize=10)
plt.xlabel('Average IMDB Rating')
plt.ylabel('Writers')


# In[19]:


# Create plots
for i in df['season'].unique():
    plt.figure(figsize=(10,5)) 
    temp = df[df['season']==i]
    sns.countplot(data=temp, y='directed_by', order = temp['directed_by'].value_counts().index)
    plt.suptitle('How Many Episodes of \'Friends\' Were Done by Each Directing Team in Season {}?'.format(i), fontsize=15)
    plt.xlabel('Episodes')
    plt.ylabel('Directing Team')


# In[ ]:




