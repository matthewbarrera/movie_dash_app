import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np

# import plotly.graph_objects as go
# This never worked for me
# Coding was complicated without this since every doc for plotly used go
# But whenever I loaded this import, it always failed to work

# Ideally, open directly from folder rather than from parent folder
# Run the file with: python3 app.py

# Load the dataset I downloaded from Kaggle
# https://www.kaggle.com/datasets/omkarborikar/top-10000-popular-movies
file_name = 'Top_10000_Movies.csv'
movies_df = pd.read_csv(file_name, lineterminator='\n')
movies_df = movies_df[['original_title', 'tagline', 'revenue', 'genre', 'release_date']]
movies_df_filtered = movies_df.dropna()

# This is an array for the revenue bracket
revenue_bracket_df = pd.array(['Less than $1M',
                               '$1M to less than $10M',
                               '$10M to less than $100M',
                               '$100M to less than $500M',
                               '$500M to less than $1B',
                               '$1B and above'], dtype=str)
# This is an array for colors associated with revenue bracket
colors_df = pd.array(['#003F5C',
                      '#444E86',
                      '#955196',
                      '#DD5182',
                      '#FF6E54',
                      '#FFA600'], dtype=str)

'''
# Testing:
print(movies_df_filtered.original_title)
print(movies_df_filtered.tagline)
print(movies_df_filtered.revenue)
print(movies_df_filtered.genre)
print(movies_df_filtered.release_date)

#------------------------------------------------------------------

For the desired columns, we want:
 + First Chart: Length of Tagline vs Revenue
(1) tagline --> String with no "" or '' (aabbcc no quotes)
(1) revenue --> Int (###### no decimal)
Checklist

 + Second Chart: Punctuation of Tagline vs Revenue
(2) tagline
(2) revenue
Dropdown

 + Third Chart: Genre vs Revenue
(3) genre --> ("['genre1', 'genre2', 'genre3']" / "['genre']")
(3) revenue
Checklist

 + Fourth Chart: Release Date vs Revenue
(4) release_date --> (year-month-day / ####-##-##)
(4) revenue
Range Slider

Print out types of columns with: print(movies_df.dtypes)
tagline               object
revenue                int64
genre                 object
release_date          object
'''

#We have four interaction components
# Options of row2 child1 checklist --> Checklist to Choose Revenue Bracket(s)
row2_child1_checklist = dcc.Checklist(id = "row2_checklist",
                                      options = revenue_bracket_df,
                                      value = [],
                                      inline = True);

# Options of row2 child2 dropdown --> Dropdown to Choose Either Yes or No
row2_child2_dropdown = dcc.Dropdown(id = "row2_dropdown",
                                    options = ['Yes', 'No'],
                                    value = None,
                                    placeholder = 'Select an option',
                                    style = dict(width = 150));

# Options of row3 child1 checklist --> Checklist to Choose Genre(s)
# This component requries more manual work to create distinct checkboxes
unique_genres_in_movies = []
for i in movies_df_filtered.genre:
    genre_text = i.split(",")
    for j in genre_text:
        j = j.replace('[', '')
        j = j.replace(']', '')
        j = j.replace('\'', '')
        if j.startswith(' '):
            j = j[0].replace(' ', '')
        if j not in unique_genres_in_movies and j != "":
            #print(j)
            unique_genres_in_movies.append(j)
row3_child1_checklist = dcc.Checklist(id = "row3_checklist",
                                      options = unique_genres_in_movies,
                                      value = [],
                                      inline = True);

'''
# Temporarily commenting out the fourth graph --> Having trouble declaring a MIN and a MAX
# Options of row3 child2 rangeSlider --> RangeSlider to Choose Release Date Year(s)
row3_child2_rangeSlider = dcc.RangeSlider(id = "row3_rangeslider",
                                          min = movies_df.sort_values(by=['release_date'], inplace=True)[0],
                                          max = movies_df.release_date.agg(['max']),
                                          step = 10,
                                          value = [movies_df.release_date.agg(['min']), movies_df.release_date.agg(['max'])],
                                          allowCross = False,
                                          tooltip = {"placement": "bottom", "always_visible": True});
'''
                                          
app = dash.Dash(__name__)

# X is made here
max_length = -1
for i in movies_df_filtered.tagline:
    if len(i) > max_length:
        max_length = len(i)
        #Testing
        #print(max_length)
tagline_lengths = np.arange(len(movies_df_filtered.tagline))
# Y is made here
revenue_amounts = [0] * len(tagline_lengths)
# Hover_data is made here
movie_title_tracker = [''] * len(tagline_lengths)

max_revenue = -1
for i in movies_df_filtered.revenue:
    if i > max_revenue:
        max_revenue = i
        #Testing
        #print(max_revenue)
#Testing
#print(tagline_lengths)
#print(len(tagline_lengths))
fig1 = px.scatter(  x = [0, max_length],
                    y = [0, max_revenue],
                    color_discrete_sequence = colors_df,
                    title = 'Length of Movie Tagline vs. Revenue'
                    )
fig1.update_layout( xaxis_title = 'Length of Movie Tagline (Num. of Words)',
                    yaxis_title = 'Revenue (In USD)',
                    legend_title = 'Revenue Brackets',
                    xaxis = dict(
                        tickmode = 'array',
                        tickvals = np.arange(0, max_length, max_length/10)),
                    yaxis = dict(
                        tickmode = 'array',
                        tickvals = np.arange(0.0, max_revenue, max_revenue/10))
                    )
fig1.update(    layout_showlegend=True)
fig1.show()

# X refers to the revenue brackets array created above
# Y is made here --> We need to match each revenue bracket to a number
movie_punctuation_bins = [0] * len(revenue_bracket_df)
#Testing
#print(len(revenue_bracket_df))
fig2 = px.pie(values = movie_punctuation_bins,
              labels = revenue_bracket_df,
              color_discrete_sequence = colors_df,
              title = 'Punctuation of Movie Tagline vs. Revenue')
fig2.update_traces( textinfo = 'percent+label+value',
                    hovertemplate = "Num. of Movies: %{value}<br>Revenue Bracket: %{label}")
fig2.update(    layout_showlegend=True)
fig2.show()

# X refers to the unique genres array created when making component 3
# Y is made here --> We need to match each revenue bracket of a genre/genres to a number
movie_revenue_bins = [0] * len(revenue_bracket_df)
#Testing
#print(len(unique_genres_in_movies))
#print(unique_genres_in_movies)
#print(movie_bins)
fig3 = px.bar(  x = revenue_bracket_df,
                y = movie_revenue_bins,
                color_discrete_sequence = colors_df,
                title = 'Genre(s) of Movie vs. Number of Movies'
            )
fig3.update_layout( xaxis_title = 'Genre(s)',
                    yaxis_title = 'Num. of Movies',
                    legend_title = 'Revenue Brackets',
                    yaxis = dict(
                        tickmode = 'array',
                        tickvals = np.arange(0.0, max_revenue, max_revenue/10))
                    )
fig3.update(    layout_showlegend=True)
fig3.show()

'''
All Rows Contained within a Parent

 o Row 1 = Title
 o Row 2
   + Child 1 = Scatterplot & Checklist Component & Hover Feature
   + Child 2 = Pie Chart & Dropdown Component
 o Row 3
   + Child 1 = Bar Chart & Checklist Component
   + Child 2 = Stacked Bar Chart & Range Slider Component
'''
app.layout = html.Div(className = 'parent_div', children=[
    html.Div(id = 'row1', children = [html.H1("Movie Revenue Analysis")]),
    html.Div(id = 'row2', children = [
        html.Div(className = 'row2_child1', children = [
            dcc.Graph(id = 'graph1', figure = fig1, style = dict(width = '100%')),
            row2_child1_checklist,
            #html.Div(id = 'row2_child1_hover-data')
        ]),
        html.Div(className = 'row2_child2', children = [
            dcc.Graph(id = 'graph2', figure = fig2, style = dict(width = '100%')),
            row2_child2_dropdown
        ]),
    ]),
    html.Div(id = 'row3', children = [
        html.Div(className = 'row3_child1', children = [
            dcc.Graph(id = 'graph3', figure = fig3, style = dict(width = '100%')),
            row3_child1_checklist
        ]),
        '''
        html.Div(className = 'row3_child2', children = [
            html.Div(dcc.Graph(id = 'graph4'), style = dict(width = '100%')),
            row3_child2_rangeSlider
        ]),
        '''
    ])
])

# START OF CALLBACK CODE

# row2_child1_checklist ~ Component Interactivity
@app.callback(Output("graph1","figure"),
              Input('row2_checklist', 'value'),
              prevent_initial_call=True)
def update_graph1(r2_checklist_value):
    print('fig1 update called')
    if(r2_checklist_value is not None):
        # If r2_checklist_value is Option A, B, C, D, E, and/or F, show those data points
        firstOption = False
        secondOption = False
        thirdOption = False
        fourthOption = False
        FifthOption = False
        SixthOption = False
        # Iterate through all r2 values (OptionA? OptionA and OptionC? How many checkboxes marked?)
        for i in r2_checklist_value:
            # For each item in the r2 checklist marked off, compare with revenue_bracket_df
            # [0, 1, 2, 3, 4, 5]:
            if i == revenue_bracket_df[0]:
                firstOption = True
            elif i == revenue_bracket_df[1]:
                secondOption = True
            elif i == revenue_bracket_df[2]:
                thirdOption = True
            elif i == revenue_bracket_df[3]:
                fourthOption = True
            elif i == revenue_bracket_df[4]:
                FifthOption = True
            elif i == revenue_bracket_df[5]:
                SixthOption = True
        tagline_lengths = [0.0] * len(movies_df_filtered.tagline)
        revenue_amounts = [0] * len(tagline_lengths)
        movie_title_tracker = [''] * len(tagline_lengths)
        #Testing
        #print(revenue_amounts)
        #print(firstOption)
        #print(secondOption)

        counter = 0 # This is for placing items into arrays
        # We can't look through the data unless we do this? It worked for graph2
        tagline_graphed = movies_df_filtered.loc[movies_df_filtered.tagline.str.contains('')]
        for curr_movie, curr_revenue, curr_tagline in zip(tagline_graphed.original_title,
                                                          tagline_graphed.revenue,
                                                          tagline_graphed.tagline):
            # For each tagline length, we need to find their value using:
            # Go through the movie dataset entirely once
            # Within each iteration, compare the current data to all lengths 0 to max_length
            # max_length is 241
            # Then post that length of current data to tagline_length

            # As such, the outer loop is movies_df_filtered
            # Inner loop will be max_length, or 0 to 241 since length is 242
            # This works because minimum length is 0 and maximum length is 242

            # HOWEVER --> We don't care about inserting data in tagline_lengths IF it's option is NOT TRUE
            # Therefore, if we find that the current data is within an option and is true, we can move on
            # The current data only needs to match with 1 reveue bracket to proceed
            # If we didn't continue for any of the options, then the current data must be part of a false flag
            # In this instance, we continue
            if (curr_revenue < 1000000.0) and (firstOption == True):
                # Not only do we know this option is VALID (Marked in checklist) but we can use to set Y
                revenue_amounts[counter] = curr_revenue
                movie_title_tracker[counter] = curr_movie
            elif (curr_revenue >= 1000000.0) and (curr_revenue < 10000000.0) and (secondOption == True):
                revenue_amounts[counter] = curr_revenue
                movie_title_tracker[counter] = curr_movie
            elif (curr_revenue >= 10000000.0) and (curr_revenue < 100000000.0) and (thirdOption == True):
                revenue_amounts[counter] = curr_revenue
                movie_title_tracker[counter] = curr_movie
            elif (curr_revenue >= 100000000.0) and (curr_revenue < 500000000.0) and (fourthOption == True):
                revenue_amounts[counter] = curr_revenue
                movie_title_tracker[counter] = curr_movie
            elif (curr_revenue >= 500000000.0) and (curr_revenue < 1000000000.0) and (FifthOption == True):
                revenue_amounts[counter] = curr_revenue
                movie_title_tracker[counter] = curr_movie
            elif (curr_revenue >= 1000000000.0) and (SixthOption == True):
                revenue_amounts[counter] = curr_revenue
                movie_title_tracker[counter] = curr_movie
            else:
                tagline_lengths[counter] = None
                revenue_amounts[counter] = None
                movie_title_tracker[counter] = None
                counter += 1
                continue
            for j in np.arange(max_length):
                if len(curr_tagline) == j:
                    tagline_lengths[counter] = j
                    #Testing
                    #print(tagline_lengths)
                    #print(curr_movie)
                    counter += 1
                    # Reminder that i = current movies_df_filtered.id
                    # We used movies_df_filtered.id to ensure that we can accurately recall each scatterpoint to it's movie title
                    # Once we find the match, no need to sort through other data points
                    break

        fig1 = px.scatter(  x = tagline_lengths,
                            y = revenue_amounts,
                            color = revenue_amounts,
                            color_discrete_sequence = colors_df,
                            title = 'Length of Movie Tagline vs. Revenue')
        fig1.update_layout( xaxis_title = 'Length of Movie Tagline (Num. of Words)',
                            yaxis_title = 'Revenue (In USD)',
                            legend_title = 'Revenue Brackets',
                            xaxis = dict(
                                tickmode = 'array',
                                tickvals = np.arange(0, max_length, max_length/10)),
                            yaxis = dict(
                                tickmode = 'array',
                                tickvals = np.arange(0, max_revenue, max_revenue/10)),
                            )
        fig1.update(    layout_showlegend=True)
        #Testing
        #print("finished update1")
        return fig1
    else:
        raise PreventUpdate

# Pie Chart
# row2_child2_dropdown ~ Component Interactivity
@app.callback(Output("graph2","figure"),
              Input('row2_dropdown', 'value'),
              prevent_initial_call=True)
def update_graph2(r2_dropdown_value):
    print('fig2 update called')
    if(r2_dropdown_value is not None):
        # If r2_dropdown_value is YES, we want movies with taglines that have puncutation
        # If NO, then we want movies with taglines that do not have punctuation
        # '{', '}', '(', ')', '[', ']']
        pattern = '\.|\,|\!|\?|\:|\;|\'|\"|\{|\}|\[|\]|\(|\)'
        if r2_dropdown_value == 'Yes':
            #Testing
            #print('yes found')
            tagline_graphed = movies_df_filtered.loc[~movies_df_filtered.tagline.str.contains(pattern)]
        elif r2_dropdown_value == 'No':
            tagline_graphed = movies_df_filtered.loc[movies_df_filtered.tagline.str.contains(pattern)]
        # Find count of movies in each revenue bracket
        # Don't forget to reset the bins each time we update! Otherwise they accumulate over button presses!
        movie_punctuation_bins = [0, 0, 0, 0, 0, 0]
        # Index 0 = Less than $1mil
        # Index 1 = $1mil to less than $10mil
        # ... etc.
        # Values will be the counts of movies AND the Labels will be the revenue brackets
        for i in tagline_graphed.revenue:
            if (i < 1000000.0):
                movie_punctuation_bins[0] += 1
            elif (i >= 1000000.0) and (i < 10000000.0):
                movie_punctuation_bins[1] += 1
            elif (i >= 10000000.0) and (i < 100000000.0):
                movie_punctuation_bins[2] += 1
            elif (i >= 100000000.0) and (i < 500000000.0):
                movie_punctuation_bins[3] += 1
            elif (i >= 500000000.0) and (i < 1000000000.0):
                movie_punctuation_bins[4] += 1
            elif (i >= 1000000000.0):
                movie_punctuation_bins[5] += 1
        fig2 = px.pie(values = movie_punctuation_bins,
                      labels = revenue_bracket_df,
                      color_discrete_sequence = colors_df,
                      title = 'Punctuation of Movie Tagline vs. Revenue')
        fig2.update_traces( textinfo = 'percent+label+value',
                            textposition = 'auto',
                            textfont_size = 8,
                            hovertemplate = "Num. of Movies: %{value}<br>Revenue Bracket: %{label}")
        fig2.update(    layout_showlegend = True)
        fig2.show()
        #Print for testing
        #print(movie_punctuation_bins)
        return fig2
    else:
        raise PreventUpdate

# row3_child1_checklist ~ Component Interactivity
@app.callback(Output("graph3","figure"),
              Input('row3_checklist', 'value'),
              prevent_initial_call=True)
def update_graph3(r3_checklist_value):
    print('fig3 update called')
    if(r3_checklist_value is not None):
        # If r3_checklist_value is Genre A, B ... etc., include these genres in data collection
        gen_act = False
        gen_com = False
        gen_sci = False
        gen_hor = False
        gen_ani = False
        gen_cri = False

        gen_thr = False
        gen_fam = False
        gen_adv = False
        gen_wes = False
        gen_rom = False
        gen_dra = False

        gen_fan = False
        gen_war = False
        gen_doc = False
        gen_mys = False
        gen_mus = False
        gen_his = False

        gen_tv = False
        pattern = []
        # Iterate through all r3 values (OptionA? OptionA and OptionC? How many checkboxes marked?)
        for i in r3_checklist_value:
            # [0, 1, 2, 3, 4, 5, ... 17, 18]:
            if i == unique_genres_in_movies[0]:
                gen_act = True
                pattern.append(unique_genres_in_movies[0])
            elif i == unique_genres_in_movies[1]:
                gen_com = True
                pattern.append(unique_genres_in_movies[1])
            elif i == unique_genres_in_movies[2]:
                gen_sci = True
                pattern.append(unique_genres_in_movies[2])
            elif i == unique_genres_in_movies[3]:
                gen_hor = True
                pattern.append(unique_genres_in_movies[3])
            elif i == unique_genres_in_movies[4]:
                gen_ani = True
                pattern.append(unique_genres_in_movies[4])
            elif i == unique_genres_in_movies[5]:
                gen_cri = True
                pattern.append(unique_genres_in_movies[5])
            elif i == unique_genres_in_movies[6]:
                gen_thr = True
                pattern.append(unique_genres_in_movies[6])
            elif i == unique_genres_in_movies[7]:
                gen_fam = True
                pattern.append(unique_genres_in_movies[7])
            elif i == unique_genres_in_movies[8]:
                gen_adv = True
                pattern.append(unique_genres_in_movies[8])
            elif i == unique_genres_in_movies[9]:
                gen_wes = True
                pattern.append(unique_genres_in_movies[9])
            elif i == unique_genres_in_movies[10]:
                gen_rom = True
                pattern.append(unique_genres_in_movies[10])
            elif i == unique_genres_in_movies[11]:
                gen_dra = True
                pattern.append(unique_genres_in_movies[11])
            elif i == unique_genres_in_movies[12]:
                gen_fan = True
                pattern.append(unique_genres_in_movies[12])
            elif i == unique_genres_in_movies[13]:
                gen_war = True
                pattern.append(unique_genres_in_movies[13])
            elif i == unique_genres_in_movies[14]:
                gen_doc = True
                pattern.append(unique_genres_in_movies[14])
            elif i == unique_genres_in_movies[15]:
                gen_mys = True
                pattern.append(unique_genres_in_movies[15])
            elif i == unique_genres_in_movies[16]:
                gen_mus = True
                pattern.append(unique_genres_in_movies[16])
            elif i == unique_genres_in_movies[17]:
                gen_his = True
                pattern.append(unique_genres_in_movies[17])
            elif i == unique_genres_in_movies[18]:
                gen_tv = True
                pattern.append(unique_genres_in_movies[18])
        movie_revenue_bins = [0] * len(revenue_bracket_df)
        pattern_string = ''
        counter = 0
        for i in pattern:
            pattern_string += i
            if counter == (len(pattern)-1):
                continue
            else:
                pattern_string += '|'
                counter += 1

        #Testing
        print(pattern_string)
        # We can't look through the data unless we do this? It worked for graph2
        genre_graphed = movies_df_filtered.loc[movies_df_filtered.genre.str.contains(pattern_string)]
        for curr_genre, curr_revenue in zip(genre_graphed.genre,
                                            genre_graphed.revenue):
            if (curr_revenue < 1000000.0):
                # Not only do we know this option is VALID (Marked in checklist) but we can use to set Y
                movie_revenue_bins[0] += 1
            elif (curr_revenue >= 1000000.0) and (curr_revenue < 10000000.0):
                movie_revenue_bins[1] += 1
            elif (curr_revenue >= 10000000.0) and (curr_revenue < 100000000.0):
                movie_revenue_bins[2] += 1
            elif (curr_revenue >= 100000000.0) and (curr_revenue < 500000000.0):
                movie_revenue_bins[3] += 1
            elif (curr_revenue >= 500000000.0) and (curr_revenue < 1000000000.0):
                movie_revenue_bins[4] += 1
            elif (curr_revenue >= 1000000000.0):
                movie_revenue_bins[5] += 1
            else:
                continue

        fig3 = px.bar(  x = revenue_bracket_df,
                        y = movie_revenue_bins,
                        color_discrete_sequence = colors_df,
                        title = 'Genre(s) of Movie vs. Number of Movies'
                    )
        fig3.update_layout( xaxis_title = 'Genre(s)',
                        yaxis_title = 'Num. of Movies',
                        legend_title = 'Revenue Brackets',
                        yaxis = dict(
                            tickmode = 'array',
                            tickvals = np.arange(0.0, max_revenue, max_revenue/10))
                        )
        fig3.update(    layout_showlegend=True)
        fig3.show()
        return fig3
    else:
        raise PreventUpdate

# END OF CALLBACK CODE

if __name__ == '__main__':
    app.run_server(debug=True,port=5001)