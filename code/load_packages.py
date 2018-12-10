
import time

# For webscrapping
import requests
from bs4 import BeautifulSoup

from os.path import join as pjoin
import os
from pathlib import Path

import pandas as pd
import numpy as np

import html

from lxml import html

# For persisting indexes in an external file
import pickle

import math

import nltk

# For word tokenization
from nltk.tokenize import RegexpTokenizer
# For stop words list
from nltk.corpus import stopwords
# For word stemming
from nltk.stem.snowball import SnowballStemmer

from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt