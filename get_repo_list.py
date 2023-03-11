import requests
import csv
from module import create_repo_list_csv
from module import handle_request_exception
from module import get_pr_nums
from settings import headers
from settings import params


def main():
    csv_file_name = create_repo_list_csv()

    while True:
        response = requests.get("https://api.github.com/search/repositories?q=stars:>10000+language:Java&sort=stars"
                                "&order=desc", params=params,
                                headers=headers)
        try:
            response.raise_for_status()
            response = response.json()

        except Exception as e:
            print(f"Exception occurred:\n{e}")
            cmd, auth, sleep_sec = handle_request_exception(response, headers)
            if cmd == 'break':
                break
            elif cmd == 'continue':
                continue

        if not response['items']:
            print("response['items'] is Empty!")
            break

        # Parsing through the response of the search query
        for item in response['items']:

            # Append to the CSV file
            with open(csv_file_name, 'a', newline='') as csvfile:
                write_to_csv = csv.writer(csvfile, delimiter=',')

                repo_name = item['name']
                repo_user = item['owner']['login']
                repo_html_url = item['html_url']
                repo_id = item['id']
                repo_node_id = item['node_id']
                repo_description = item['description']
                repo_stars = item['stargazers_count']
                repo_forks = item['forks_count']
                repo_prs = get_pr_nums(repo_user, repo_name)
                repo_language = item['language']
                repo_api_url = item['url']
                repo_created_at = item['created_at']
                repo_updated_at = item['updated_at']
                repo_pushed_at = item['pushed_at']

                # Check the license
                if item['license']:
                    repo_license = item['license']['name']
                else:
                    repo_license = "NO LICENSE"

                write_to_csv.writerow([repo_name, repo_user, repo_html_url, repo_id,
                                       repo_node_id, repo_description, repo_stars,
                                       repo_forks, repo_prs, repo_language, repo_api_url,
                                       repo_created_at, repo_updated_at, repo_pushed_at, repo_license])

        params['page'] += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
