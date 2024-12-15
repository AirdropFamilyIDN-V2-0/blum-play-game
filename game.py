import argparse
import random
import threading
from urllib.parse import parse_qs, unquote
import cloudscraper
import time
from datetime import datetime, timezone
from payload import get_payload
from payload.payload import get_payloads
start_time = datetime.now()
requests = cloudscraper.create_scraper()
from colorama import init, Fore, Style

def print_colored_message(message, color=Fore.WHITE):
    print(color + message)

def load_credentials():
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File query_id.txt tidak ditemukan.")
        return 
    except Exception as e:
        print("Terjadi kesalahan saat memuat query:", str(e))
        return 

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def get(id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None
        return tokens[str(id)]

def save(id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def update(id, new_token):
    tokens = json.loads(open("tokens.json").read())
    if str(id) in tokens.keys():
        tokens[str(id)] = new_token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))
    else:
        return None

def delete(id):
    tokens = json.loads(open("tokens.json").read())
    if str(id) in tokens.keys():
        del tokens[str(id)]
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))
    else:
        return None
    
def delete_all():
    open("tokens.json", "w").write(json.dumps({}, indent=4))


def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def make_request(method, url, headers=None, json=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, json=json)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json, data=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=json, data=data)
        else:
            raise ValueError("Invalid method.")
        
        if response.status_code >= 500:
            if retry_count >= 4:
                print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            retry_count += 1
        elif response.status_code >= 400:
            print_(f"Status Code: {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

        
def get_new_token(query_id):
    import json
    data = json.dumps({"query": query_id, "referralToken":'z2MpJGToqt'})
    headers = {
        'Content-Length': str(len(data)),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': "u=1, i",
        'Origin': 'https://telegram.blum.codes',
        "Lang": "en",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'content-type' :'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    }

    
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    time.sleep(2)
    print_(f"Getting Tokenss...")
    response = make_request('post',url, headers=headers, data=data)
    if response is not None:
        print_(f"Token Created")
        response_json = response.json()
        return response_json['token']['refresh']
    else:
        print_(f"Failed get token")
        return None

def get_user_info(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': "u=1, i",
        'Origin': 'https://telegram.blum.codes',
        "Lang": "en",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'content-type' :'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    }
    response =  response = make_request('get','https://gateway.blum.codes/v1/user/me', headers=headers)
    if response is not None:
        return response.json()

def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': "u=1, i",
        'Origin': 'https://telegram.blum.codes',
        "Lang": "en",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'content-type' :'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    }
    try:
        response =  response = make_request('get','https://game-domain.blum.codes/api/v1/user/balance', headers=headers)
        if response is not None:
            return response.json()
        else:
            print_(f"Failed getting data balance")
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Failed ")

def play_game(token):
    time.sleep(2)
    headers = {
        'Authorization': f'Bearer {token}',
        
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': "u=1, i",
        'Origin': 'https://telegram.blum.codes',
        "Lang": "en",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'content-type' :'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    }
    try:
        response = make_request('post','https://game-domain.blum.codes/api/v2/game/play', headers=headers)
        if response is not None:
            return response.json()
        else:
            return None
    except Exception as e:
        print_(f"Failed play game, Error {e}")

def claim_game(token, game_id, point, freeze):
    time.sleep(2)
    url = "https://game-domain.blum.codes/api/v2/game/claim"

    headers = {
        'Authorization': f'Bearer {token}',
       
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': "u=1, i",
        'Origin': 'https://telegram.blum.codes',
        "Lang": "en",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'content-type' :'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    }
    data = get_payloads(game_id, point, freeze)
    if data is not None:
        payload = {'payload' : data}
        try:
            response = make_request('post', url, headers=headers, data=json.dumps(payload))
            if response is not None:
                return response
            else:
                return None
        
        except Exception as e:
            print_(f"Failed Claim game, error: {e}")
    else:
        return None

def get_game_id(token):
    game_response = play_game(token)
    trying = 5
    if game_response is None or game_response.get('gameId') is None:
        while True:
            if trying == 0:
                break
            print_("Play Game : Game ID is None, retrying...")
            game_response = play_game(token)
            if game_response is not None:
                game_id = game_response.get('gameId', None)
            else:
                game_id = None
            if game_id is not None:
                return game_response['gameId']
                break
            else:
                print_('Game id Not Found, trying to get')
            trying -= 1
    else:
        return game_response['gameId']

def claim_balance(token):
    
    headers = {
        'Authorization': f'Bearer {token}',
        
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': "u=1, i",
        'Origin': 'https://telegram.blum.codes',
        "Lang": "en",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'content-type' :'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    }
    try:
        time.sleep(2)
        response = make_request('post','https://game-domain.blum.codes/api/v1/farming/claim', headers=headers)
        if response is not None:
            return response.json()
        else:
            print_("Failed Claim Balance")

    except Exception as e:
        print_(f"Failed claim balance, error: {e}")
    return None


import json

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")

def generate_token():
    queries = load_credentials()
    for index, query in enumerate(queries, start=1):
        parse = parse_query(query)
        user = parse.get('user')
        print_(f"Account {index}  | {user.get('username','')}")
        token = get(user['id'])
        if token == None:
            time.sleep(2)
            token = get_new_token(query)
            save(user.get('id'), token)

def get_verification():
    url = 'https://raw.githubusercontent.com/boytegar/BlumBOT/refs/heads/master/verif.json'
    data = requests.get(url=url)
    return data.json()

def get_data_payload():
    url = 'https://raw.githubusercontent.com/zuydd/database/main/blum.json'
    while True:
        data = make_request('get',url=url)
        if data is not None:
            return data.json()

def create_payload(game_id, point, dogs):

    trys = 5
    while True:
        if trys == 0:
            return None
        url = f'https://server2.ggtog.live/api/game'
        payload = {
                'gameId': game_id,
                'points': str(point),
                'dogs': dogs
            }
        response = make_request('post', url, json=payload)
        if response is not None:
            data = response.json()
            if "payload" in data:
                return data["payload"]
            return None
        trys -= 1

def find_by_id(json_data, id):
    for key, value in json_data.items():
        if key == id:
            return value
    return None

def worker(query, index):
    total_blum = 0
    delay_time = random.randint(3700, 3750) * 8
    start_time = time.time()

    useragents = getuseragent(index)
    parse = parse_query(query)
    user = parse.get('user')
    token = get(user['id'])
    if token is None:
        print_colored_message(f"Membuat token Akun {index} | {user.get('username', '')} ", Fore.BLUE)
        time.sleep(2)
        token = get_new_token(query)
        save(user.get('id'), token)

    balance_info = get_balance(token)
    if balance_info is None:
        print_colored_message("Gagal mendapatkan informasi", Fore.RED)
        return
    else:
        available_balance_before = balance_info['availableBalance']
        total_blum += float(available_balance_before)

    while balance_info['playPasses'] > 0:
        gameId = get_game_id(token)
        taps = random.randint(330, 400)
        delays = random.randint(31, 35)
        freeze = random.randint(4, 8)
        delays += (freeze * 5)
        time.sleep(delays)
        claim_response = claim_game(token, gameId, taps, freeze)
        while claim_response is not None:
            if claim_response.text == '{"message":"game session not finished"}':
                time.sleep(10)
                print_colored_message(f"Mainkan Game: Permainan masih berjalan, {user.get('username', '')}", Fore.YELLOW)
                claim_response = claim_game(token, gameId, taps, 0)
            elif claim_response.text == '{"message":"game session not found"}':
                print_colored_message("Mainkan Game: Permainan selesai", Fore.GREEN)
                break
            elif 'message' in claim_response and claim_response['message'] == 'Token is invalid':
                print_colored_message("Mainkan Game: Token tidak valid, mengambil token baru...", Fore.RED)
                token = get_new_token(query)
                save(user.get('id'), token)
                claim_response = claim_game(token, gameId, taps, freeze)
            else:
                break

        balance_info = get_balance(token)
        available_balance_after = balance_info['availableBalance']
        total_balance = float(available_balance_after) - float(available_balance_before)
        print_colored_message(
            f"Mainkan Game: Permainan selesai Akun {index} | {user.get('username', '')} Total Poin Blum = {round(total_blum)} Anda mendapatkan total {total_balance} Tiket Game    : {balance_info['playPasses']}",
            Fore.GREEN,
        )


        if balance_info['playPasses'] <= 0:
            print_colored_message("Tidak memiliki tiket untuk bermain", Fore.RED)
            break 
        else:
            balance_info = get_balance(token)


    end_time = time.time()
    delete_all()
    waktu_tunggu = delay_time - (end_time - start_time)
    if waktu_tunggu > 0:
        time.sleep(waktu_tunggu)


def main():
    delete_all()
    queries = load_credentials()
    threads = []

    for index, query in enumerate(queries, start=1):
        t = threading.Thread(target=worker, args=(query, index))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print_colored_message("Semua akun selesai! Memulai ulang dari akun pertama...", Fore.CYAN)

def start():
    print_colored_message("Mulai Auto Play Game...", Fore.BLUE)
    try:
        while True:
            try:
                main()
            except Exception as e:
                print_colored_message(f"Terjadi kesalahan: {str(e)}", Fore.RED)
    except KeyboardInterrupt:
        print_colored_message("Dihentikan oleh pengguna.", Fore.RED)

if __name__ == "__main__":
    start()
