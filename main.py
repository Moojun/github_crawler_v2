import requests
from datetime import datetime
import csv

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': '[Enter your GitHub Token]',
    'X-GitHub-Api-Version': '2022-11-28',
}

# https://api.github.com/search/repositories?q=stars:>0&sort=stars&per_page=100
# params = {
# 'q': "stars:>=10000",
# 'language': "Java",
# 'sort': 'stars',
# 'order': 'desc',
# 'page': 1,
# 'per_page': 100
# }

# Base API Endpoint
base_api_url = 'https://api.github.com/'

# Create .csv file
file_name = "top100JavaStars_" + str(datetime.now().date()) + ".csv"
with open(file_name, 'w', newline='') as csvfile:
    write_to_csv = csv.writer(csvfile, delimiter=',')
    write_to_csv.writerow(["repo_name", "description", 'stars', 'forks',
                           'license', 'open_issues_count', 'main_language'])

for page in range(1, 2):
    # Building the Search API URL
    URL = base_api_url + 'search/repositories'

    try:
        # response = requests.get(URL, params=params, headers=headers).json()
        response = requests.get("https://api.github.com/search/repositories?q=stars:>10000+language:Java&sort=stars"
                                "&order=desc&per_page=100",
                                headers=headers).json()
    except Exception as e:
        print(f"Exception occurred:\n{e}")
        print("maybe your GitHub token is wrong")
        break

    # Parsing through the response of the search query
    for item in response['items']:

        # Append to the CSV file
        with open(file_name, 'a', newline='') as csvfile:
            write_to_csv = csv.writer(csvfile, delimiter=',')

            repo_name = item['name']
            repo_description = item['description']
            repo_stars = item['stargazers_count']
            repo_forks = item['forks_count']
            repo_open_issues_count = item['open_issues_count']
            repo_main_language = item['language']
            repo_url = item['url']
            repo_crated_at = item['created_at']
            repo_updated_at = item['updated_at']

            # Check the license
            if item['license']:
                repo_license = item['license']['name']
            else:
                repo_license = "NO LICENSE"

            write_to_csv.writerow([repo_name, repo_description, repo_stars, repo_forks,
                                   repo_license, repo_open_issues_count, repo_main_language])

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     get_result()
