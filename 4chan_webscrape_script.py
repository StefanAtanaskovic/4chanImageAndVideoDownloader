import requests
from bs4 import BeautifulSoup
import shutil
import os
import re


def download_content(link_list, format_type):
    '''
    downloads data and saves it the specified format
    takes two params, the first is a list of urls
    the second the format the the downloaded data should be saved as
    '''
    for ind, content_list in enumerate(link_list):
        content = requests.get(content_list, stream=True)
        with open(os.path.realpath('.') + f'/4chan/{image_folder_name}/{ind}.{format_type}', 'wb') as output_file:
            shutil.copyfileobj(content.raw, output_file)
        content.close()
        print(
            f'Downloading content - {ind + 1} out of {len(link_list)}', end='\r', flush=True)


# makes a folder named 4chan in the directory that contais this file
# if the folder 4Chan allready exists it dose nothing
try:
    os.mkdir(os.path.realpath('.') + "/4chan")
except FileExistsError:
    pass

# asks the user for the url of the 4chan thread
url = input('Inser the url: ')

# creates a folder inside the 4chan directory and names it by the users input
# if the new directory already exists it ask the user for a diferent name
while True:
    try:
        image_folder_name = input(
            'What do you want to call the folder that will contain the images: ')
        os.mkdir(os.path.realpath('.') + f"/4chan/{image_folder_name}")
        break
    except FileExistsError:
        print('A folder with that name allready exists, please try another')

# gets the thread html
four_chan_board = requests.get(url)
html = four_chan_board.text

# parses the html
soup = BeautifulSoup(html, 'html.parser')

# finds all the a tags and then makse a list conting the href values
list_of_hrefs = []
for link in soup.find_all('a'):
    list_of_hrefs.append(link.get('href'))

# splits the href list into two new lists
# once conting the image files and the other cotaning the video files
list_of_img_hrefs = []
list_of_video_hrefs = []
for href in list_of_hrefs:
    img_href = re.search('^.*\.jpg$|^.*\.jpeg$|^.*\.png$|^.*\.gif$', href)
    if img_href:
        href = href.replace('//', 'http://')
        list_of_img_hrefs.append(href)
        continue
    video_href = re.search('^.*\.webm$', href)
    if video_href:
        href = href.replace('//', 'http://')
        list_of_video_hrefs.append(href)

# turnes the lists into sets to remove the duplicates
unique_img_hrefs = set(list_of_img_hrefs)
unique_video_hrefs = set(list_of_video_hrefs)

# downloads the image and video files
print('Started downloading images...')
download_content(unique_img_hrefs, 'png')
print('\nFinished downloading images!')
print('Started downloading videos...')
download_content(unique_video_hrefs, 'webm')
print('\nFinished downloading videos!')
print('All dowloads finished!')
print('bye bye')