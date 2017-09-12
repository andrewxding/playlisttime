import requests
import base64
import json
import sys
import random
import urllib
import time
class Da():
    def __init__(self, cid, secret):
        self.client_id = cid
        self.client_secret = secret
        self.url = 'https://accounts.spotify.com/api/token'
        self.solved = False
        self.titles = []
    def getToken(self):
        data = {
          "grant_type":    "client_credentials",
        }
        r = requests.post(self.url , data=data, auth = (self.client_id, self.client_secret))
        res = json.loads(r.content.decode('utf-8'))
        res['access_token']
        return res['access_token']

    def getPlaylist(self,token, user='1258151442', playlist = '4GmmoZP2BmGZwKaAr98iYZ'):
        url = 'https://api.spotify.com/v1/users/'+user+'/playlists/'+playlist
        headers = {'Authorization': 'Bearer ' + token}
        r = requests.get(url, headers=headers)
        playlist = json.loads(r.content.decode('utf-8'))
        tracks = playlist['tracks']
        mytracks = []
        for t in tracks['items']:
            #print(t['track'])
            mytracks.append(t['track'])
        return mytracks
    def getSongs(self, tracks, target):
        self.solved= False
        self.subset_sum(tracks, target)
        return self.titles
    def subset_sum(self,numbers, target, partial=[]):
        if self.solved:#add option to tolerance
            return
        tolerance = 30
        s= 0
        for p in partial:
            s+=(p['duration_ms']/1000)
        # check if the partial sum is equals to target
        if s >= target-tolerance and s<= target+tolerance:
            titles = []
            for n in partial:
                titles.append(n['name'])
            self.solved = True
            self.titles = titles
            return 
        if s > target+tolerance:
            #print("target")
            return  # if we reach the number why bother to continue

        for i in range(len(numbers)):
            n = numbers[i]
            remaining = numbers[i+1:]
            self.subset_sum(remaining, target, partial + [n]) 

    def createPlaylist(self,token, userid, name, public=False, collaborative=False, description=""):
        url = 'https://api.spotify.com/v1/users/'+ userid+'/playlists'
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
        data = json.dumps({'name': name, 'public': public, 'collaborative': collaborative, 'description': description})
        r = requests.post(url, headers=headers, data=data)
        print(r.content)
        return json.loads(r.content.decode('utf-8'))['id']
    def authorizeUser(self,user):
        query = urllib.parse.urlencode({'client_id': user, 'response_type': 'token', 'redirect_uri': "http://localhost:8000/callback", 
            'scope': 'playlist-modify-public playlist-modify-private'})#change for client id
        url = 'https://accounts.spotify.com/authorize?' + query
        print('Location:'+url)
    def getTracks(self, tracks, token):
        uris = []
        for track in tracks:
            params = {'Authorization':'Bearer ' + token}
            query = urllib.parse.urlencode([('q',track),('type', 'track'), ('limit', '1')])
            r = requests.get('https://api.spotify.com/v1/search?' + query, headers=params)
            body = json.loads(r.content.decode('utf-8'))
            uris.append(body['tracks']['items'][0]['uri'])
        return uris
    def addTracksToPlaylist(self, tracks, playlist, user, token):
        url = 'https://api.spotify.com/v1/users/%s/playlists/%s/tracks' %(user, playlist)
        print(url)
        headers = {'Authorization': 'Bearer '+ token, 'Content-Type': 'application/json'}
        print(tracks)
        body = json.dumps({'uris': tracks})
        r=requests.post(url, headers=headers, data=body)
        print(r.content)


if __name__ == "__main__":
    me = Da()
    token = me.getToken()
    tracks = me.getPlaylist(token)
    random.shuffle(tracks)
    songs = me.getSongs(tracks, int(sys.argv[1]))
    uris = me.getTracks(songs, token)

    me.authorizeUser(me.client_id)
    token = input('Enter token')
    user = input('Enter user id, not username')
    playlistname = input('Enter name of new playlist')
    playlistid = me.createPlaylist(token, user, playlistname)
    me.addTracksToPlaylist(uris, playlistid, user, token)

    


