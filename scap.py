from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Chrome(ChromeDriverManager().install())


prices = []  # List to store price of the product
categorys = []  # List to store category of the product
driver.get("https://www.flipkart.com")

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
for a in soup.findAll('a', href=True, attrs={'class': '_6WQwDJ T88g6k'}):
    price = a.find('div', attrs={'class': '_2tDhp2'})
    category = a.find('div', attrs={'class': '_3LU4EM'})
    prices.append(price.text)
    categorys.append(category.text)


df_product = pd.DataFrame(
    {'Categorys': categorys, 'Price': prices})
# df.to_csv('products.csv', index=False, encoding='utf-8')


zero = ['Milk', 'jaggery', 'salt', 'lassi', 'kajal', 'fresh',
        'vegetables', "prasad", "tender coconut water", ' honey', 'paneer']

five = ["PDS", "kerosene", "coal", "tea", "spectacles", "domestic LPG", "cashew nuts", "raisins", "packed paneer", "edible vegetable oil",
        "agarbatti", "footwear below Rs.500", "milk food for babies", " apparel below Rs.10,000", "coir mats", "matting", "floor coverings"]

twelve = ["Butter", "ghee", "almonds", "mobiles", "umbrellas", "packed coconut water",
          "preparations of vegetables", "fruits", "nuts", "chutney", "jam", "jelly"]

eighteen = ["Hair oil", "toothpaste", "computers", "pasta", " ice-cream", "printers",
            "CCTV", "staplers", "aluminum foil", "cornflakes", "computer monitors less than 17 inches"]

df_zero = pd.DataFrame({'Category': zero, "GST": 0})
df_five = pd.DataFrame({'Category': five, "GST": 5})
df_twelve = pd.DataFrame({'Category': twelve, "GST": 12})
df_eighteen = pd.DataFrame({'Category': eighteen, "GST": 18})

df_gst = pd.concat([df_zero, df_five, df_twelve,
                   df_eighteen], ignore_index=True)


print(df_gst['Category'].str.lower())


def check_all(sentence, ws):
    return all(w in sentence for w in ws)


def gstMap(df):
    for i in df_gst['Category'].str.lower():
        if any(check_all(i, word.split('+')) for word in df.lower()):
            return df_gst.loc[df_gst['Category'] == i, 'GST']


df_product['GST'] = df_product["Categorys"].apply(gstMap)
print(df_product)
