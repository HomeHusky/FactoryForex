from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def get_today_high_impact_news():
    url = "https://www.forexfactory.com/calendar.php"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    news_list = []

    # ForexFactory có cấu trúc bảng lịch, lọc rows ngày hôm nay và mức độ high
    rows = soup.select('tr.calendar__row')
    for row in rows:
        date_cell = row.select_one('td.calendar__date')
        if date_cell and today_str not in date_cell.get_text():
            continue

        impact_cell = row.select_one('td.calendar__impact span')
        if impact_cell and 'High' in impact_cell.get('title', ''):
            time_cell = row.select_one('td.calendar__time')
            event_cell = row.select_one('td.calendar__event')

            time_str = time_cell.text.strip() if time_cell else "N/A"
            event_title = event_cell.text.strip() if event_cell else "N/A"

            news_list.append({
                "time": time_str,
                "title": event_title,
                "impact": "High"
            })
    return news_list

@app.route('/api/news', methods=['GET'])
def news():
    news = get_today_high_impact_news()
    return jsonify(news)

if __name__ == '__main__':
    app.run(debug=True)
