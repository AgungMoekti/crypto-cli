import json
from time import time
import urllib.parse
import hashlib
import hmac
import requests
import os

red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
blue="\033[1;34m"
magenta="\033[1;35m"
cyan="\033[1;36m"
reset="\033[0m"

version = '1.1'
f = open('user.json')
data = json.load(f)
user_id = data['user_detail']['id']
user_pw = data['user_detail']['pw']
url = 'https://indodax.com/tapi'
APIkey = str.encode(user_id)
secret = str.encode(user_pw)
jam = int(time()*1000)


def auth():
    payload = {
        'method': 'getInfo',
        'timestamp': jam,
        'recvWindow': jam + 5000
    }

    paybytes = urllib.parse.urlencode(payload).encode('utf8')
    #   print(paybytes)

    sign = hmac.new(secret, paybytes, hashlib.sha512).hexdigest()
    #print(sign)

    headers = {
        'Key': APIkey,
        'Sign': sign,
    }

    r = requests.post(url, headers=headers, data=payload)
    result = r.json()['success']

    if (result < 1):
        err = r.json()['error']
        return err
    else:
        return "Login successfuly"

def price(a,b):
    pair = a + '_' + b
    api_indodax = requests.get('https://indodax.com/api/tickers')
    raw = api_indodax.json()
    harga = raw['tickers'][pair]['buy']
    vol = raw['tickers'][pair]['vol_'+b]
    if b == 'idr':
        print(f'{magenta}='*6,'Trade Confirmation','='*6,'\n')
        print(f'{green}Curren Price of {pair} : Rp{int(harga):,}')
        print(f'Curren Volume {pair} : Rp{int(vol):,}')
    else:
        print(f'{magenta}='*6,'Trade Confirmation','='*6,'\n')
        print(f'{green}Curren Price {pair} : ${harga}')
        print(f'Curren Volume {pair} : ${vol}')

def coin(a,b):
    pair = a + '_' + b
    api_indodax = requests.get('https://indodax.com/api/tickers')
    raw = api_indodax.json()
    harga = raw['tickers'][pair]['buy']
    vol = raw['tickers'][pair]['vol_'+b]
    if b == 'idr':
        print(f'{magenta}\n','='*6,'Information','='*6)
        print(f'{green}Curren Price {pair} : Rp{int(harga):,}')
        print(f'Curren Volume {pair} : Rp{int(vol):,}')
    else:
        print(f'{green}Curren Price {pair} : ${harga}')
        print(f'Curren Volume {pair} : ${vol}')

    


def balance():
    payload = {
        'method': 'getInfo',
        'timestamp': jam,
        'recvWindow': jam + 5000
    }

    paybytes = urllib.parse.urlencode(payload).encode('utf8')
    #   print(paybytes)

    sign = hmac.new(secret, paybytes, hashlib.sha512).hexdigest()
    #print(sign)

    headers = {
        'Key': APIkey,
        'Sign': sign,
    }

    r = requests.post(url, headers=headers, data=payload)
    balance = r.json()['return']['balance']['idr']
    return balance


def trade(code,pair,type,amount_idr,amount_coin,price):
        token = code + '_' + pair
        payload ={
            'method':'trade',
            'timestamp':jam,
            'recvWindow':jam + 5000,
            'pair':token,
            'type':type,
            'price':price,
            'idr':amount_idr,
            code:amount_coin
        }

        paybytes = urllib.parse.urlencode(payload).encode('utf8')
        #print(paybytes)

        sign = hmac.new(secret, paybytes, hashlib.sha512).hexdigest()
        #print(sign)

        headers = {
        'Key': APIkey,
        'Sign': sign,
        }

        r = requests.post(url, headers=headers, data=payload)
        print(f'{magenta}='*6,'Send Transaction Sucssesfuly','='*6,'\n')
        orderid = r.json()['return']['order_id']
        receive = r.json()['return']['receive_'+code]
        
        remain = r.json()['return']['remain_rp']
        print(f'{green}Detail Transaction : ')
        print(f'Receive : {receive}')
        print(f'Remain Rp : {int(remain):,}')
        print(f'Transaction id : {orderid}')


def buy(code,pair,amount_idr,price):
    trade(code=code,pair=pair,amount_idr=amount_idr,price=price,type='buy',amount_coin='')


def sell(code,pair,amount_coin,price):
    trade(code=code,pair=pair,type='sell',amount_coin=amount_coin,amount_idr='')


def menu():
    while True:
        os.system('clear')
        print(f"{magenta}="*6,"Consol Buy Indodax","="*6)
        print(f'{green}Menu :')
        print('1.Check Balance')
        print('2.Buy Crypto')
        print('3.Sell Crypto')
        print('4.Check Coin Price')
        print('5.Exit')
        print(end="\n")
        print(f"{blue}Version {version}")
        print(f'{magenta}='*6,'INPUT','='*6)
        pilihan = int(input(f'{cyan}Enter Choice Menu : '))

        if pilihan == 1:
            print(f'{green}Balance : Rp{balance():,}')
            repeat = str(input('Back? (y/n) : '))
            if repeat == 'y':
                continue
            else:
                print(f'{red}End Program...')
                break


        elif pilihan == 2:
            print('Note : Make Sure You Have Enough Balance To Buy Or It Will Crash!\n')
            a = str(input('Enter Coin Code (btc/eth/bnb) :'))
            b = str(input('Enter Pair (idr/usdt) :'))
            c = str(input('Enter Amount Rupiah : Rp.'))
            d = str(input('Enter Buying Price : Rp.'))
            price(a=a,b=b)
            conti = str(input('Continue Buy? (y/n) : '))
            if conti == "y":
                buy(code=a,pair=b,amount_idr=c,price=d)
            else:
                print('Canceled')
            repeat = str(input(f'{green}Back? (y/n) : '))
            if repeat == 'y':
                continue
            else:
                print(f'{red}End Program...')
                break

        elif pilihan == 3:
            print('Note : Make Sure You Have The Coin To Sell Or It Will Crash!\n')
            a = str(input('Enter Coin Code (btc/eth/bnb) : '))
            b = str(input('Enter Pair (idr/usdt) : '))
            c = str(input('Enter Amount Coin : Rp. '))
            d = str(input('Enter Selling Price : '))
            price(a=a,b=b)
            conti = str(input('Continue Sell? (y/n) : '))
            if conti == "y":
                sell(code=a,pair=b,amount_coin=c,price=d)
            else:
                print('Canceled')
            repeat = str(input(f'{cyan}Back? (y/n) : '))
            if repeat == 'y':
                continue
            else:
                print(f'{red}End Program...')
                break
        elif pilihan == 4:
            print(f'{red}Note : The Price Based On indodax.com\n')
            a = str(input(f'{cyan}Enter Coin Symbol (btc/eth/bnb) : '))
            b = str(input('Enter Coin Pair (idr/usdt) : '))
            try:
                coin(a,b)
            except:
                print(f'{red}Upps error. Try again')
            repeat = str(input(f'{cyan}Back? (y/n) : '))
            if repeat == 'y':
                continue
            else:
                print(f'{red}End Program...')
                break

        elif pilihan == 5:
            print(f'{red}End Program...')
            break

        else:
            print(f'{red}Error : Error Input')
            repeat = str(input(f'{cyan}Back? (y/n) :'))
            if repeat == 'y':
                continue
            else:
                print(f'{red}End Program...')
                break
if(auth() == "Login successfuly"):
    menu()
else:
    print(f"{red}{auth()}")
