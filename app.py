
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

#create new df
gss_clean2 = gss_clean[['income','sex','job_prestige']]

#new feature that breaks job_prestige into 6 cat. with equal ranges
gss_clean2['job_prestige_group'] = pd.cut(gss_clean2.job_prestige, bins = [15,25,35,45,55,65,80], labels = ['very low', 'low', 'medium', 'moderate', 'high', 'very high'])

#drop rows with na
gss_clean2 = gss_clean2.dropna()


markdown_text = '''

Gender Wage Gap:

The gender wage gap refers to the difference in earnings between women and men. According to the 2018 Census Bureau, women of all races earned, on average, only 82 cents for ever $1 earned by men of all races. It is important to note that the wage gap is larger for most women of color and that these gaps reflect the ratio of earnings across all industries. Calculating the wage gap is not simple; for example the gaps do not take into account differences in years of experience, hours worked, or discrimination laws. For this reason, is important to study the complexities of the wage gap to ensure economic security and equality for all.

For more information about the gender wage gap refer to: https://www.americanprogress.org/issues/women/reports/2020/03/24/482141/quick-facts-gender-wage-gap/

General Social Survey:

The General Social Survey (GSS) provides insight into the growing complexity of American society by monitoring changes in both social characteristics and attitudes since 1792. It contains data about a myriad of topics, to include income, psychological well-being, and morality. It collects data via a survey and according to the GSS website listed below, the GSS is the only full-probability, personal-interview survey designed to monitor the information outlined above.

For more information refer to the GSS website: http://www.gss.norc.org/About-The-GSS

'''

gss_bar = gss_clean.groupby('sex', sort=False).male_breadwinner.value_counts().reset_index(name = 'count')


#create dark bar
fig_3b = px.bar(gss_bar, x='male_breadwinner', y='count', color='sex', 
             labels={'male_breadwinner':'Male Breadwinner', 'count':'Count'}, 
                template = "plotly_dark",
             barmode = 'group')
fig_3b.update_layout(font_family="Courier New",
    font_color="white",
    title_font_family="Courier",
    title_font_color="white",
    legend_title_font_color="white")


#create dark scatter and change font
fig_4b = px.scatter(gss_clean, x='job_prestige', y = 'income', 
                 color = 'sex',
                 height=600, width=600,
                 trendline = 'ols',
                 template = "plotly_dark",
                 labels = {'job_prestige':'Occupational Prestige','income':'Income'},
                 hover_data = ['education', 'socioeconomic_index'])

fig_4b.update(layout=dict(title=dict(x=0.5)))
fig_4b.update_layout(font_family="Courier New",
    font_color="white",
    title_font_family="Courier",
    title_font_color="white",
    legend_title_font_color="white")

#create dark box
fixBox_6b = px.box(gss_clean2, x = 'income', y ='sex', color = 'sex',
                facet_col = 'job_prestige_group', facet_col_wrap = 2,
                   template = "plotly_dark",
                color_discrete_map = {'male':'blue', 'female':'red'})
fixBox_6b.update(layout_showlegend = False)
fixBox_6b.update_layout(font_family="Courier New",
    font_color="white",
    title_font_family="Courier",
    title_font_color="white",
    legend_title_font_color="white")


#create app
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(
    [
       
        #title
        html.H1("Exploring the General Social Survey (GSS)", style={'backgroundColor':'green'}),
        
        #markdown text
        dcc.Markdown(children = markdown_text),
        
       
        html.Div([
            
        #problem 3
        html.H2("Breadwinner by Gender"),        
        dcc.Graph(figure=fig_3b)
            
        ], style = {'width':'30%', 'float':'left'}),
        
        html.Div([
            
        #problem 4
        html.H2("Income and Job Prestige by Gender"),        
        dcc.Graph(figure=fig_4b)
            
        ], style = {'width':'68%', 'float':'right'}),
        
        
        #problem 6
        html.H2("Income and Job Prestige Category by Gender"),        
        dcc.Graph(figure=fixBox_6b)
    
    ]
)

#launch dash
if __name__ == '__main__':
    app.run_server(debug=True)


