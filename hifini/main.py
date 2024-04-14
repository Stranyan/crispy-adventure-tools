import get_index_data
import get_songpage_data
import get_music

index_data = get_index_data.get_result()

for i in index_data:
    link = i['link']
    music_info = get_songpage_data.get_result(link)
    if isinstance(music_info, dict):
        name = music_info['title'] + '-' + music_info['author']
        music_link = music_info['url']
        get_music.get_result(music_link, name)
    else:
        print(music_info)