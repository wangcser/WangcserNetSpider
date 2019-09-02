```
from bs4 import BeautifulSoup

soup = BeautifulSoup(web, "lxml")

html = soup.prettify()

获取标题 print(soup.title.text)

```