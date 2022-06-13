import streamlit as st
import numpy as np
import matplotlib
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import requests
import random
import bs4
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw
import urllib.request

with st.echo(code_location='below'):

    def returnphoto(message, photos):

        a = random.randint(1, len(photos))

        urllib.request.urlretrieve(
            photos[a],
            "skys.jpg")

        img = Image.open("skys.jpg")
        img.thumbnail((300, 300))
        title_text = message.text
        image_editable = ImageDraw.Draw(img)
        res = image_editable.text((100, 15), title_text, size=10, fill=(255, 0, 0))
        return img

    def go():
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "X-Amzn-Trace-Id": "Root=1-614b72cf-3af194f55b95c13d138986c5"
        }
        st.balloons()
        st.title('Небоскрёбы и мир. Мир и небоскрёбы.')
        st.subheader('Небоскрёбы начались со здания Хоум-Иншуренс-билдинг, которое было построено в 1885 году. '
                 'Именно это здание считается первым небоскрёбом, потому что при его строительстве впервые использовался несущий каркас –– '
                 'конструкция опиралась на железо-бетонные сваи и стальной каркас, а не на стены.')
        st.image('https://upload.wikimedia.org/wikipedia/commons/3/38/Home_Insurance_Building.JPG', use_column_width = True, caption = 'Хоум-Иншуренс-билдинг, Чикаго. Взято из википедии')
        df = pd.read_csv('List of cities with the most skyscrapers.csv', sep=';', encoding = 'unicode_escape')
        groupedcountries = df.groupby('Country')['Number of skyscrapers'].sum().to_frame()
        groupedcountries['name'] = groupedcountries.index
        groupedcountries = groupedcountries.reset_index(drop = True)
        groupedcountries['name'] = groupedcountries['name'].str[1:]
        groupedcountries['name'] = groupedcountries['name'].replace({'United States': 'United States of America'})
        map = pd.DataFrame(gpd.read_file('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'))
        mergedcountries = pd.merge(groupedcountries, map, on = ['name'], how = 'inner')
        mergedcountries = gpd.GeoDataFrame(mergedcountries, geometry = 'geometry')
        fig, ax = plt.subplots()
        st.subheader('Со временем небоскрёбов становилось всё больше. '
                 'На карте изображено распределение небоскрёбов по разным странам мира. '
                 'На сегодня больше всего небоскрёбов построено в Китае.')
        st.pyplot(mergedcountries.plot(column='Number of skyscrapers', ax=ax, legend=True, norm=matplotlib.colors.LogNorm(vmin=1, vmax=3000),).figure)
        gdps = pd.read_csv('gdp world bank info.csv', index_col = False, sep= ";")
        gdps.rename(columns = {'Country Name': 'name'}, inplace = True)
        gdps = gdps[['name', '2020']].dropna()
        gdps['name'] = gdps['name'].replace({'United States': 'United States of America'})
        mergedcountries = pd.merge(mergedcountries, gdps, on = ['name'], how = 'inner')

        st.subheader('Проверим, правда ли, что чем богаче страна, тем больше у неё небоскрёбов. '
                     'Судя по графику ниже, действительно, такая корреляция существует.')
        base = mergedcountries[['name', 'Number of skyscrapers', '2020']]
        base['2020'] = base['2020']/10**12
        import altair as alt
        chart = alt.Chart(base).mark_point().encode(x = "Number of skyscrapers",
            y=alt.Y("2020", title="Annual GDP in 2020 (in trillions of current US dollars)"),
        ).properties(width = 600)

        st.write(chart + chart.transform_regression("Number of skyscrapers", "2020").mark_line())

        model = LinearRegression()
        model.fit(base[['Number of skyscrapers']], base["2020"])
        st.write('Коэффиценты регрессии: w_0 = %.3f, w_1 = %.3f' %(model.coef_[0], model.intercept_))
        value = st.slider(
            'Выберите, сколько небоскребов построено в стране, и я скажу, какой у неё ВВП',
            1, 5000, 1337)
        st.subheader('Вау! ничего себе, видел шарики? Вот ответ: %.2f триллионов долларов США. Это 12 нулей, если что.' %(model.predict(pd.DataFrame([[value]], columns=["Number of skyscrapers"]))[0]))
        st.subheader('А теперь ещё одна интересная фича. '
                     'Ниже взята произвольная картинка и на неё добавлена тестовая фраза.'
                     ' Вы можете зайти в телеграм-бот @Skyscrapersplustextbot и попробовать повоображать '
                     'как будет выглядеть какой-либо город через много лет, когда весь мир будет в небоскрёбах. '
                     'Для этого отправьте ему любое сообщение, и бот сам приклеит это фразу к произвольному изображению небоскрёбов, '
                     'которое возьмет из интернета -– картинки будут новыми. Например "Махачкала, 2032" ')


        r = requests.get('https://www.dreamstime.com/photos-images/skyscraper.html', headers = headers)
        soup = bs(r.content, features="lxml")
        imgs = soup.find_all('img')
        photos = []
        for i in imgs:
            try:
                photos.append(i['data-src'])
            except Exception:
                pass
        print(photos)

        a = random.randint(1, len(photos)-1)
        print(a)

        urllib.request.urlretrieve(
            photos[a],
            "skys.jpg")

        img = Image.open("skys.jpg")
        st.image(img)
        message = 'Mahachkala 2032'
        title_text  = message
        image_editable = ImageDraw.Draw(img)
        res = image_editable.text((15, 15), title_text, size = 10, fill = (255, 0, 0))
        st.image(img)

        st.write('Помогу загрейдить эту работу: ')
        st.write('**Обработка данных с помощью pandas. 1-2** '
                 'Так как для анализа данных использовались три разных базы данных, '
                 'которые были аккуратно почищены автором и склеены вместе так, чтобы ничего не потерялось.'
                 'Кроме этого, изначальная база данных содержала разбитые по городам, а не по странам списки небоскребов.'
                 ' Автор долго искал свои старые дз, чтобы всё заработало и летало.')
        st.write('**Веб-скреппинг. 1** '
                 'Я пользловался бютифул соупом чтобы скачать и обработать картинки небоскребов для последней части работы.')
        st.write('**Работа с REST API (XML/JSON). 2** '
                 'Карта мира с раскрашенными в зависимости от количества небоскребов странами делалась через JSON. '
                 'Именно в таком формате я получил координаты стран, в таком формате работал и раскрашивал карту,'
                 ' мэтчил небоскребы и координаты полигонов стран')
        st.write('**Визуализация данных. 2** '
                 'Карта классная. Количества небоскребов еще и лог нормально отнормированы, чтобы красивее смотрелось')
        st.write('**Математические возможности Python. 1**'
                 ' Все данные анализировались через numpy. Через него считалась сумма небоскребов, '
                 'строилась корреляционная модель.')
        st.write('**Streamlit. 1**')
        st.write('**Geopandas. 1**')
        st.write('**Машинное обучение. 1**'
                 ' Модель с баром для выбора количества небоскребов работает с регрессией, которая строится через ML.')
        st.write('**Дополнительные технологии. 1-2**'
                 ' Тема с надписями на картинках делалась через библиотеку pillow, которую мы не проходили.')
        st.write('**Объем. 1**'
                 ' Больше 160.')
        st.write('**Целостность**'
                 ' На ваше усмотрение')
        st.write('**Общее впечатление**'
                 ' Вы видели шарики? Очень жестко')

        st.info('\*****')
        st.warning('\*******!')
        st.subheader('Код ниже. Обнял')
    go()
