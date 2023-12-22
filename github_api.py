from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials
import requests
import httplib2
import apiclient


app = Flask(__name__)
CREDENTIALS_FILE = 'cred.json'
spreadsheet_id = '1aza83M3lqa6qpZTktw790mu6A_JUbDBm3lf1Ae_w4GE'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive']
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


def github_api(username: str):
    url = f"https://api.github.com/users/{username}"
    user_data = requests.get(url).json()
    return [
        user_data['avatar_url'], user_data['bio'], user_data['blog'], user_data['company'], user_data['created_at'],
        user_data['email'], user_data['followers'], user_data['following'], user_data['login'],
        user_data['name'], user_data['location']
    ]


def google_sheets_api(username):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:K1000',
        majorDimension='COLUMNS'
    ).execute()
    num_users = len(values['values'][8]) + 1
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": f"A{num_users}:K{num_users}",
                    "majorDimension": "ROWS",
                    "values": [
                        github_api(username)
                    ]
                }
            ]
        }
    ).execute()


@app.route('/add_user', methods=['POST'])
def add_user():
    inp = request.get_json()
    username = inp["username"]
    google_sheets_api(username)
    return "1"


@app.route('/all_users', methods=['GET'])
def all_users():
    out_json = {}
    columns = ['avatar_url', 'bio', 'blog', 'company', 'created_at', 'email', 'followers', 'following', 'login', 'name',
               'location']

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:K1000',
        majorDimension='COLUMNS'
    ).execute()
    num_users = len(values['values'][8])

    for i in range(2, num_users):
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'A{i}:K{i}',
            majorDimension='COLUMNS'
        ).execute()
        username = values['values'][8][0]
        if username in out_json:
            continue
        out_json[username] = {}
        for key, val in zip(columns, values['values']):
            if len(val) == 0:
                continue
            out_json[username][key] = val[0]

    return out_json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
