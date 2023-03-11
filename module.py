import requests
from datetime import datetime
import csv
import json
from time import sleep
from bs4 import BeautifulSoup


def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        headers = config['headers']
        params = config['params']

    return headers, params


# Create csv file of Repository list
def create_repo_list_csv():
    file_name = "Top194JavaStarsRepo_" + str(datetime.now().date()) + ".csv"
    with open(file_name, 'w', newline='') as csvfile:
        write_to_csv = csv.writer(csvfile, delimiter=',')
        write_to_csv.writerow(['name', 'user', 'html_url', 'id', 'node_id',
                               'description', 'stars', 'forks', 'prs', 'language', 'api_url',
                               'created_at', 'updated_at', 'pushed_at', 'license'])
    return file_name


# Create csv file of Repository info
def create_repo_list_info_csv():
    file_name = "Top194JavaStarsRepoInfo_" + str(datetime.now().date()) + ".csv"
    with open(file_name, 'w', newline='') as csvfile:
        write_to_csv = csv.writer(csvfile, delimiter=',')
        write_to_csv.writerow(["name", 'id', 'node_id', 'owner', 'stars', 'forks', 'prs', 'language',
                               'created_at', 'updated_at', 'pushed_at', 'description'])
    return file_name


def print_log(msg):
    t = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{t}] {msg}")


def get_rate_limit(headers_arg):
    r = requests.get('https://api.github.com/rate_limit', headers=headers_arg)
    res = r.json()['rate']
    return res


def get_sleep_sec(t):
    sleep_sec = (datetime.fromtimestamp(t) - datetime.now()).total_seconds()
    return sleep_sec


def get_available_auth(headers):
    rates = {'auth': headers['Authorization'], 'rate': get_rate_limit(headers)}

    sleep_sec = get_sleep_sec(rates['rate']['reset'])
    if rates['rate']['remaining'] > 0 or sleep_sec < 0:
        return rates['auth'], 0

    sleep_sec = get_sleep_sec(rates[0]['rate']['reset'])

    return rates[0]['auth'], sleep_sec


def get_url(owner, repo_name):
    return f"https://api.github.com/repos/{owner}/{repo_name}"


def handle_request_exception(r, headers):
    # Handling exceptions. Sleep when rate limit exceeded.
    if r.status_code == 404 or r.status_code == 451:
        print_log("Error (%d) - %s " % (r.status_code, r.json()['message']))
        return 'break'
    elif r.status_code == 403:
        j = r.json()
        if 'message' in j and 'limit' in j['message']:
            auth, sleep_sec = get_available_auth(headers)
            if sleep_sec > 0:
                print_log(f"Limit exceeded. Sleeping {sleep_sec} seconds.")
                sleep(sleep_sec)
            else:
                print_log(f"Trying alternate credential - {auth[0]}")
            return 'continue', auth, sleep_sec
    return 'break'


# Using BeautifulSoup web Crawler to get the number of open_pr_nums and closed_pr_nums
def get_pr_nums(owner, repo_name):
    response = requests.get(f"https://github.com/{owner}/{repo_name}/pulls")
    soup = BeautifulSoup(response.content, 'html.parser')

    result = soup.find('body', class_="logged-out"). \
        find('div', class_="logged-out").find('div', class_="application-main"). \
        find('div').find('main').find(id="repo-content-turbo-frame"). \
        find('div', class_="no-wrap").select('a')

    open_pr_num = 0
    closed_pr_num = 0

    for text in result:
        text = text.get_text().replace("\n", "").replace(" ", "")

        if "Open" in text:
            text = text.strip("Open").replace(",", "")
            open_pr_num = int(text)
        elif "Closed" in text:
            text = text.strip("Closed").replace(",", "")
            closed_pr_num = int(text)

    return open_pr_num + closed_pr_num


