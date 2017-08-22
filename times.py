import requests
import base64
import json
import sys
import random


client_id = 'f19c760ba4b14c5390f21a7a8c7a93c9'
client_secret = '092e7ee6b39749a5a14e9c714eeae349'
url = 'https://accounts.spotify.com/api/token'
def getToken():
    data = {
      "grant_type":    "client_credentials",
    }
    r = requests.post(url , data=data, auth = (client_id, client_secret))
    res = json.loads(r.content.decode('utf-8'))
    res['access_token']
    return res['access_token']

def getPlaylist(token):
    url = 'https://api.spotify.com/v1/users/1258151442/playlists/4GmmoZP2BmGZwKaAr98iYZ'
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers)
    playlist = json.loads(r.content.decode('utf-8'))
    tracks = playlist['tracks']
    mytracks = []
    for t in tracks['items']:
        #print(t['track'])
        mytracks.append(t['track'])
    return mytracks
def subset_sum(numbers, target, partial=[]):
    tolerance = 30
    s= 0
    for p in partial:
        s+=(p['duration_ms']/1000)
    # check if the partial sum is equals to target
    if s >= target-tolerance and s<= target+tolerance: 
        titles = ",".join(n['name'] for n in partial)
        print(titles + "\n" + str(s))
    if s > target+tolerance:
        #print("target")
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, partial + [n]) 
def getDuraction(track):
    return track['duration_ms']

if __name__ == "__main__":
    token = getToken()
    tracks = getPlaylist(token)
    random.shuffle(tracks)
    # for time in tracks:
    #     print(time['name'])
    subset_sum(tracks, int(sys.argv[1]))


