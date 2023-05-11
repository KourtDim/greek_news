import streamlit as st
import requests
import bs4 as bs
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS


def connect(url):
    page = requests.get(url)
    soup = bs.BeautifulSoup(page.text,"lxml")
    return soup

@st.cache
def fetch_data():
	article_titles = []
	article_dates = []
	article_urls = []
	article_origin = []

	#### in.gr ####

	url_politics_ingr = 'https://www.in.gr/politics/'
	soup = connect(url_politics_ingr)
	articles = soup.findAll('article')


	for a in articles:
	    article_titles.append(a.find('div',{'class':'mask-title'}).find('h3').text)
	    date = a.find('div',{'class':'flex-meta'}).text
	    if len(date)!=21:
	        article_dates.append(date.split('  ')[2].strip())
	    else:
	        article_dates.append(date.strip())
	    article_urls.append(a.find('a',{'class':'tile relative-title'}).get('href'))
	    article_origin.append('in.gr')

	#### lifo.gr ####    
		    
	url_politics_lifo = 'https://www.lifo.gr/now/politics'
	soup = connect(url_politics_lifo)
	articles = soup.find('div',{'class':'w-950 news-articles'}).findAll('div',{'class':'px-4'})

	for a in articles:
	    article_titles.append(a.find('h3').text.split('  ')[2])
	    article_dates.append(a.find('div',{'class':'m-0 p-0 fedranormal fs-5-v fs-4-v-lg lh-17-v darkGrayText'}).find('time').get('datetime'))
	    article_urls.append(a.find('h3').find('a').get('href'))
	    article_origin.append('lifo.gr')
		    

	#### dikaiologitika.gr ####

	url_politics_dikaiologitika = 'https://www.dikaiologitika.gr/eidhseis/politikes-eidhseis'
	soup = connect(url_politics_dikaiologitika)
	articles = soup.find('div',{'class':'itemListLowerGrid'}).findAll('div',{'class':'catItemBody'})

	for a in articles:
	    article_titles.append(a.find('h3',{'class':'catItemTitle'}).text.strip())
	    article_dates.append(a.find('span',{'class':'catItemDateCreated'}).text)
	    article_urls.append('https://www.dikaiologitika.gr/{}'.format(a.find('h3',{'class':'catItemTitle'}).find('a').get('href')))
	    article_origin.append('dikaiologitika.gr')
		    

	#### enimerotiko.gr ####

	url_politics_enimerotiko = 'https://www.enimerotiko.gr/politiki/'
	soup = connect(url_politics_enimerotiko)
	articles = soup.findAll('div',{'class':'card-content'})

	for a in articles:
	    article_titles.append(a.find('a').text.strip())
	    article_dates.append(a.find('p',{'class':'time mb-3'}).text)
	    article_urls.append(a.find('a').get('href'))
	    article_origin.append('enimerotiko.gr')
		   

	#### zougla.gr ####
	url_politics_zougla = 'https://www.zougla.gr/politiki/main'
	soup = connect(url_politics_zougla)
	articles = soup.findAll('div',{'class':'secondary_story_content'})
	
	for a in articles:
	    article_titles.append(a.find('a').text.strip())
	    article_dates.append(a.find('p',{'class':'date'}).text)
	    article_urls.append(a.find('a').get('href'))
	    article_origin.append('zougla.gr')


	df = pd.DataFrame({'title':article_titles,
		                  'date':article_dates,
		                  'url':article_urls,
		                 'origin':article_origin})    
	return(df)


st.set_page_config(layout="wide")
df=fetch_data()




option = st.sidebar.selectbox('select website',options=np.sort(df.origin.unique()))


temp_df = df.loc[df['origin']==option]

st.title('Τιτλοι αρθρων απο: {}'.format(option))

for t,u in zip(temp_df.title.head(10),temp_df.url.head(10)):
	st.markdown('- [{}]({})'.format(t,u))

#https://www.e-tetradio.gr/Article/22316/ta-20-koryfaia-enhmerwtika-site-toy-ellhnikoy-internet
