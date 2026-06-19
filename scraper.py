import requests
from bs4 import BeautifulSoup
import smtplib, ssl, os
from email.mime.text import MIMEText
from datetime import datetime

def get_praz_tenders():
    url = "https://www.praz.gov.zw/index.php?option=com_content&view=category&id=50&Itemid=137"
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, 'lxml')
    tenders = []
    for row in soup.select('.tender-table tr')[1:]: 
        cols = row.find_all('td')
        if len(cols) >= 3:
            title = cols[1].get_text(strip=True)
            deadline = cols[2].get_text(strip=True)
            tenders.append(f"PRAZ: {title} | Deadline: {deadline}")
    return tenders

def send_email(body):
    if not body:
        print("No new tenders found.")
        return
    
    msg = MIMEText("\n".join(body))
    msg['Subject'] = f"PRAZ Tender Alert - {datetime.now().strftime('%d %b %Y')}"
    msg['From'] = os.environ['EMAIL_ADDRESS']
    msg['To'] = os.environ['TO_EMAIL']
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(os.environ['EMAIL_ADDRESS'], os.environ['EMAIL_PASSWORD'])
        server.send_message(msg)
    print("Email sent!")

if __name__ == "__main__":
    all_tenders = get_praz_tenders()
    send_email(all_tenders)
