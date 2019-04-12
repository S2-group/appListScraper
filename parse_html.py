import glob
import csv
import os.path
from bs4 import BeautifulSoup


def parse_category(raw_category : str) -> str:
    raw_category = raw_category.strip()
    # Handle all the games subcategories
    if raw_category == 'Casual':
        return 'Games'
    if raw_category == 'Sports Games':
        return 'Games'
    if raw_category == 'Simulation':
        return 'Games'
    if raw_category == 'Strategy':
        return 'Games'
    if raw_category == 'Casino':
        return 'Games'
    if raw_category == 'Card':
        return 'Games'
    if raw_category == 'Racing':
        return 'Games'
    if raw_category == 'Puzzle':
        return 'Games'
    if raw_category == 'Trivia':
        return 'Games'
    if raw_category == 'Educational':
        return 'Games'
    if raw_category == 'Action':
        return 'Games'
    if raw_category == 'Board':
        return 'Games'
    if raw_category == 'Role Playing':
        return 'Games'
    if raw_category == 'Arcade':
        return 'Games'
    if raw_category == 'Adventure':
        return 'Games'
    if raw_category == 'Word':
        return 'Games'
    if raw_category == 'Music':
        return 'Games'
    return raw_category

# Find all html files
apps = []
for file_name in glob.glob("pages/*.html"):
    # Open file
    file = open(file_name)
    # Parse file
    soup = BeautifulSoup(file, 'html.parser')
    # Find the table with app info
    app_table = soup.find("tbody", {'data-ref': 'main'})
    # Iterate over table rows
    for t_row in app_table.find_all('tr'):
        # Iterate over columns
        app = {}
        for index, t_col in enumerate(t_row.find_all('td')):
            # Scrape app ranking in its category according to app annie
            if index == 0:
                app.update({'rank': int(t_col.text)})
            # Scrape app name, app store url, package name, author name, author url,
            # author nationality, in-app-purchases flag
            elif index == 1:
                app_info = t_col.find_all('a', {'class': 'app-link'})
                app_name = app_info[0].text.strip()
                app_url = app_info[0].get('href')
                package_name = app_url[22:-9]
                try:
                    author_info = t_col.find_all('div', {'class': 'company-info'})
                except AttributeError:
                    pass
                try:
                    author_name = author_info[0].text.strip()
                except IndexError:
                    app_name = 'NA'
                try:
                    author_url = author_info[0].find('a', {'class': 'company-link'}).get('href')
                except IndexError:
                    author_url = 'NA'
                try:
                    author_nationality = author_info[0].find('img', {'class': 'flag'}).get('data-helptip')[14:]
                except (IndexError, AttributeError):
                    author_nationality = 'NA'
                in_app_purchases = True if t_col.find('span', {'class': 'iap-info'}) is not None else False
                app.update({
                            'app_name': app_name,
                            'store_url': app_url,
                            'package_name': package_name,
                            'author_name': author_name,
                            'author_url': author_url,
                            'author_nationality': author_nationality,
                            'in_app_purchases': in_app_purchases
                            })
            elif index == 4:
                # Parse gross rank
                rank_string = t_col.text.strip()
                app.update({'grossing_rank': int(rank_string) if rank_string != '500+' else 500})
            elif index == 6:
                # Parse new free rank
                rank_string = t_col.text.strip()
                app.update({'new_free_rank': int(rank_string) if rank_string != '500+' else 500})
            elif index == 8:
                # Parse category
                category = parse_category(t_col.text)
                app.update({'category': category})
            elif index == 9:
                # Parse rating
                app.update({'annie_rating': float(t_col.text) if t_col.text != 'N/A' else 'NA'})
            elif index == 10:
                # Parse ratings count
                app.update({'annie_rating_count': int(t_col.text.replace(',', '')) if t_col.text != 'N/A' else 'NA'})
            elif index == 11:
                # Parse release date
                app.update({'annie_release_date': t_col.text})
            elif index == 12:
                # Parse last update date
                app.update({'annie_last_update': t_col.text})
        apps.append(app)


for app in list({v['package_name']: v for v in apps}.values()):
    filename = 'apps_no_dups.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as out_file:
        writer = csv.writer(out_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writerow(app.keys())
        writer.writerow(app.values())
        out_file.flush()
        out_file.close()
