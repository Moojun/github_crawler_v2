
headers = {
    "Accept": "application/vnd.github+json",
    'Authorization': '[Enter your GitHub Token]',
    "X-GitHub-Api-Version": "2022-11-28",
}

# https://api.github.com/search/repositories?q=stars:>0&sort=stars&per_page=100
params = {
    # 'q': "stars:>=10000",
    # 'language': "Java",
    # 'sort': 'stars',
    # 'order': 'desc',
    "page": 1,
    "per_page": 100
}
