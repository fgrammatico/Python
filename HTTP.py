import requests
    
url = 'https://api.spotify.com/v1/me/playlists'
headers = {'Accept':'Accept: "application/vnd.rn+json"','Content-Type':'Content-Type: "application/vnd.rn+json"','Authorization':'token="BQCPmSvqXl8IdOmrVDBpIGuyCsuAVuxsmW3uS-_ACmJbRD0aM7hmN27GNMh8lvDWAiBN7WtItnso9pwprKVeso6edidwjMkESzbqNUqzIkNAo-PEAG-67LJHwAFgXsALSuOdWtaWQxdBTWou8GOLXSMlc5jEDG2AefXY45jLXw""'}
r = requests.get(url,headers=headers)
print (r.status_code)
data = r.json()
print (data)