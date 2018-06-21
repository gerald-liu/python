import argparse
from pytube import YouTube, Playlist

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="URL of the video")
ap.add_argument("-l", "--list", help="URL of the playlist")
ap.add_argument("-d", "--dest", help="Download destination")
args = vars(ap.parse_args())

if args['video'] is not None:
    YouTube(args['video']).streams.first().download(args['dest'])
elif args['list'] is not None:
    Playlist(args['list']).download_all(args['dest'])