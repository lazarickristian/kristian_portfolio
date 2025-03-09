from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from bs4 import BeautifulSoup
from .pdf_report import generate_pdf

BASE_URL = "https://www.transfermarkt.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

LEAGUES = {
    "Premier League": "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1",
    "La Liga": "https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1",
    "Bundesliga": "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1",
    "Serie A": "https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1",
    "Ligue 1": "https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1",
    "SuperSport HNL": "https://www.transfermarkt.com/1-hnl/startseite/wettbewerb/KR1",
}

def get_seasons(league_url):
    """Scrape available seasons for a selected league."""
    response = requests.get(league_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    seasons = {}
    for option in soup.select("select[name='saison_id'] option"):
        season = option.text.strip()
        season_id = option['value']
        seasons[season] = season_id
    
    return seasons

def get_league_logo(league_url):
    response = requests.get(league_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    profile_container = soup.find("div", class_="data-header__profile-container")
    img_tag = profile_container.find("img")

    return img_tag["src"]

def get_clubs(league_url, season_id):
    """Scrape clubs for a selected league and season."""
    season_url = f"{league_url}/plus/0?saison_id={season_id}"
    response = requests.get(season_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_table = soup.select_one("table.items tbody")

    clubs = {}
    for club in main_table.select("td.hauptlink a"):
        club_name = club.text.strip()
        if club_name and "href" in club.attrs:
            club_url = BASE_URL + club['href']
            clubs[club_name] = club_url
    
    return clubs

def get_squad(club_url):
    base_link = "https://www.transfermarkt.com"
    response = requests.get(club_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    squad = []
    for row in soup.select("table.items tbody tr"):  
        player_data = row.select("td")
        if len(player_data) > 5:
            name = row.find("td", class_="hauptlink").text.strip()
            player_link = row.find("td", class_="hauptlink").find("a")["href"]
            age = row.find_all("td", class_="zentriert")[1].text.strip()
            position = row.find("td", class_="zentriert")['title']
            number = row.find("td", class_="zentriert").text.strip()
            squad.append({"Name": name, 'Age':age, "Position": position, 'Number':number, 'Player_Link': base_link+player_link})
    
    return squad

def get_club_logo(club_url):
    response = requests.get(club_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    profile_container = soup.find("div", class_="data-header__profile-container")
    img_tag = profile_container.find("img")

    return img_tag["src"]

def get_fixtures(club_url):
    base_link = "https://www.transfermarkt.com"
    fixtures_url = club_url.replace("startseite", "spielplan")
    response = requests.get(fixtures_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    table_containers = soup.find_all("div", class_="box")
    fixtures = {}

    for table_container in table_containers:
        if table_container.find('h2', class_='content-box-headline--inverted'):
            table = table_container.find('table')
            competition = table_container.find('h2').text.strip()
            matches = []
            for row in table.find_all("tr")[1:]:  
                date = row.find_all("td")[1].text.strip()
                opponent = row.find_all("td")[6].text.strip()
                result = row.find_all("td")[9].text.strip()
                result_link = row.find_all("td")[9].find("a")["href"]
                matches.append({"Date": date, "Opponent": opponent, "Result": result, 'Result_Link': base_link+result_link})
            fixtures[competition] = matches

    return fixtures

def scrape_clubs(request):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ You need to log in to access this page.")
        return redirect(reverse('login') + f'?next={request.path}')
    
    """Handles form submission, scrapes Transfermarkt, and reloads page with results."""
    selected_league = None
    selected_league_logo = None
    selected_season = None
    selected_club = None
    seasons = {}
    clubs = {}
    squad = []

    if "league" in request.GET:
        selected_league = request.GET.get("league")
        if selected_league in LEAGUES:
            league_url = LEAGUES[selected_league]
            seasons = get_seasons(league_url)  
            selected_league_logo = get_league_logo(league_url)
    
    if "season" in request.GET and selected_league:
        selected_season = request.GET.get("season")
        league_url = LEAGUES[selected_league]
        clubs = get_clubs(league_url, seasons[selected_season])

    if "club" in request.GET and selected_league and selected_season:
        selected_club = request.GET.get("club")
        selected_club_url = clubs[selected_club]
        selected_club_logo = get_club_logo(selected_club_url)

        return render(request, "football/success.html", {
            "selected_season": selected_season,
            "selected_club"  : selected_club,
            "selected_club_url" : selected_club_url,
            'selected_club_logo' : selected_club_logo,
        })

    return render(request, "football/football_scrape.html", {
        "leagues": LEAGUES,
        "seasons": seasons,
        "clubs": clubs,
        "selected_league": selected_league,
        "selected_league_logo": selected_league_logo,
        "selected_season": selected_season,
        "selected_club"  : selected_club,
        'squad' : squad
    })

def success(request):
    
    if "download" in request.GET:
        selected_season = request.GET.get("selected_season")
        selected_club = request.GET.get("selected_club")
        selected_club_url = request.GET.get("selected_club_url")
        selected_club_logo = request.GET.get("selected_club_logo")

        squad = get_squad(selected_club_url)
        selected_club_fixtures = get_fixtures(selected_club_url)
        user = request.user       

        pdf_buffer = generate_pdf(selected_club, selected_club_logo, selected_season, squad, selected_club_fixtures, user)
        response = FileResponse(pdf_buffer, as_attachment=True, filename=f"{selected_club}_report.pdf")
        return response