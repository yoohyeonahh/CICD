import os

print("MY_GITHUB_TOKEN:", os.environ.get('MY_GITHUB_TOKEN'))

from datetime import datetime
from pytz import timezone
from crawling_yes24 import parsing_beautifulsoup, extract_book_data
from github_utils import get_github_repo, upload_github_issue

def main():
    try:
        access_token = os.environ['MY_GITHUB_TOKEN']
    except KeyError:
        print("Error: 'MY_GITHUB_TOKEN' environment variable not set.")
        return

    repository_name = "github-action-with-python"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    yes24_it_new_product_url = "https://www.yes24.com/Product/Category/AttentionNewProduct?pageNumber=1&pageSize=24&categoryNumber=001001003"
    
    try:
        soup = parsing_beautifulsoup(yes24_it_new_product_url)
        print("Successfully parsed BeautifulSoup.")
    except Exception as e:
        print(f"Error parsing BeautifulSoup: {e}")
        return
    
    issue_title = f"YES24 IT 신간 도서 알림({today_date})"
    
    try:
        upload_contents = extract_book_data(soup)
        print("Successfully extracted book data.")
    except Exception as e:
        print(f"Error extracting book data: {e}")
        return

    try:
        repo = get_github_repo(access_token, repository_name)
        print("Successfully retrieved GitHub repo.")
    except Exception as e:
        print(f"Error getting GitHub repo: {e}")
        return
    
    try:
        upload_github_issue(repo, issue_title, upload_contents)
        print("Upload GitHub Issue Success!")
    except Exception as e:
        print(f"Error uploading GitHub issue: {e}")

if __name__ == "__main__":
    main()
