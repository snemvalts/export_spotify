#!/usr/bin/python3
import requests
import sys
import time


songs = []

def main():
	if(len(sys.argv) < 2):
		print(len(sys.argv))
		print("Please pass in the OAuth token (with the following scope: user-library-read ) as the first argument and the user name as the second argument")
		return
	token = str(sys.argv[1])
	headers = {
		"Authorization": "Bearer "+token
	}
	getSaved(headers)

def getSaved(headers):
	print("Getting saved songs")
	done = False
	count = 0
	while(not done):
		params = {
			"limit": 50,
			"offset": count*50
		}
		r = requests.get("https://api.spotify.com/v1/me/tracks",headers=headers, params=params)
		#something went wrong
		if(r.status_code > 400):
			print("Error: "+str(r.status_code)+" "+r.json()["error"]["message"])
			return
		#if they've stopped sending us
		elif(len(r.json()["items"]) == 0):
			done = True
			print("Got all saved songs")
			writeToDisk()

		elif(r.status_code == 200):
			print("Got batch #"+str(count))
			data = r.json()
			#iterate items
			for i in data["items"]:
				#track name, comma seperated artists
				string = i["track"]["name"] + " by "
				for j,artist in enumerate(i["track"]["artists"]):
					if(len(i["track"]["artists"]) == j+1):
						string+= artist["name"]
						continue
					string+= artist["name"]+", "
				#if it's an album, add album
				if(i["track"]["album"]["album_type"] == "album"):
					string+= " in "+i["track"]["album"]["name"]

				songs.append(string)

		else:
			done = True
			print("Failed to get batch #"+str(count+1)+", error code: "+str(r.status_code))
			writeToDisk()
		count+=1
		#Prevents excess, disable this if you want faster
		time.sleep(2)

def writeToDisk():
	file = open("spotify_saved.txt","w")
	for item in songs:
		file.write(str(item))
		file.write("\u000A")

	file.close()
	print("Done writing to spotify_saved.txt")

main()
