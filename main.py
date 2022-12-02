import requests
import time
from pprint import pprint
from io import BytesIO
import pygame

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = '' #Paste Access Token Here
white = (255, 255, 255)
DEFAULT_IMAGE_SIZE = (480, 480)

def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    if response.status_code != 200:
        return 

    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = json_resp['item']['artists']
    album_image = json_resp['item']['album']['images'][0]['url']

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link,
        "album_image": album_image
    }

    return current_track_info


def probeNowPlaying():
    pygame.init()
    surface = pygame.display.set_mode((800,640))
    #pygame.display.set_caption('Image')
    displayImage = pygame.image.load('default.jpg')
    rect = displayImage.get_rect()
    rect.center = (320,320)


    current_track_id = None
    surface.fill((0, 0, 0))
    surface.blit(displayImage, rect)

    while True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()

        # bookImage = pygame.image.load('book.gif')
        # rect = bookImage.get_rect()
        # rect.center = (320,320)
        # surface.blit(bookImage, rect)
        
        pygame.display.update()

        current_track_info = get_current_track(ACCESS_TOKEN)
        if current_track_info != None:
            if current_track_info['id'] != current_track_id:
                surface.fill((0, 0, 0))
                pprint(current_track_info,indent=4,)
                print(current_track_info['track_name'])
                current_track_id = current_track_info['id']
                #Show Image
                img_response = requests.get(current_track_info['album_image'])
                albumCover = pygame.image.load(BytesIO(img_response.content))
                # albumCover = pygame.transform.scale(albumCover, DEFAULT_IMAGE_SIZE)
                rect = albumCover.get_rect()
                rect.center = (320,320)
                # rect.center = (240,240)
                surface.blit(albumCover, rect)
                #Show Text
                #song
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render(current_track_info['track_name'], True, white)
                text = pygame.transform.rotate(text, 90)
                text_rect = text.get_rect()
                text_rect.bottomleft = (690,600)
                surface.blit(text, text_rect)

                #artist 
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(current_track_info['artists'], True, white)
                text = pygame.transform.rotate(text, 90)
                text_rect = text.get_rect()
                text_rect.bottomleft = (730,600)
                surface.blit(text, text_rect)

                pygame.display.update()
                
        else:
            surface.fill((0, 0, 0))
            rect = displayImage.get_rect()
            rect.center = (320,320)
            surface.blit(displayImage, rect)
        
        time.sleep(2)


probeNowPlaying()
