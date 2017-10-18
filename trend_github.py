import numpy as np
import pandas as pd
import seaborn as sns
#%pylab inline
import re

df = pd.read_csv('../hacker-news-corpus/hacker_news_sample.csv')
df.info()

github = df.loc[df['url'].fillna('').str.contains('://github.com')].copy()


def get_user_project(link):
    lst = re.findall(
        r"^http[s]?://github.com/([-a-zA-Z0-9_]+)(/[-a-zA-Z0-9_]+)?(/.*)?$", link)
    if len(lst) > 0:
        user = lst[0][0]
        if user == '':
            return None
        project = lst[0][1].lstrip('/')
        if project == '':
            return None
        return "%s/%s" % (user, project)
    else:
        return None


limit = 100
github['user_project'] = github['url'].apply(get_user_project)
github = github.dropna(subset=['user_project'])
github['user_project'] = github['user_project'].str.lower()
#github = github.sort_values(by='score', ascending=False)
top_projects_score = github.groupby(
    'user_project')['score'].sum().sort_values(ascending=False)
names, scores = list(top_projects_score.index), list(top_projects_score.values)
names, scores = names[:limit], scores[:limit]
print('Usernames/Projectnames which are most appreciated by the HN community')
print('-' * 70)
for n, s in zip(names, scores):
    print('{:55} {:10}'.format(n, s))

import matplotlib.pyplot as plt
from wordcloud import WordCloud

plt.subplots(figsize=(12, 12))
wordcloud = WordCloud(
    background_color='white',
    width=1024,
    height=768
).generate(" ".join(github['title']))
wordcloud.to_file("word_cloud_github.png")
plt.imshow(wordcloud)
plt.axis('off')
# plt.show()
plt.savefig('plot_word_cloud_github.png', dpi=200)
plt.clf()
plt.cla()
plt.close()

github[['user_project', 'title', 'score']].sort_values(
    by='score', ascending=False)[0:100]
