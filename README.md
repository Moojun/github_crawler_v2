# Github Public Data Crawler using GitHub RESTAPI

> [reference link](https://github.com/Jindae/github_crawler)



GitHub REST API를 이용하여 Repository 정보를 수집하는 Crawler 입니다.

`settings.py` 의 'Authorization'에 자신의 GitHub Token 을 입력한 뒤 사용이 가능합니다. 

현재 코드는 stars >= 10000, language: Java, stars가 많은 순으로 GitHub Repository에 대한 정보를 수집하도록 작성되어 있으며, 23.03.11 기준 총 194개의 프로젝트가 해당 기준을 만족합니다.

결과 데이터의 sample은 `Top194JavaStarsRepo_2023-03-12.csv` 에서 확인이 가능합니다. 

Repository의 pull_requests의 개수는 `BeautifulSoup` lib를 사용한 웹 크롤링으로 가져오도록 되어 있으며, 그 외의 column은 GitHub REST API를 사용해서 가져옵니다. 

response data에 대한 자세한 정보는 [GitHub RESTAPI](https://docs.github.com/en/rest/search?apiVersion=2022-11-28), `Search repositories` 에서 확인이 가능합니다. 
