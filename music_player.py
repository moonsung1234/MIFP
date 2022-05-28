
music_list = []
music_index = 0
is_play = False

def save(music_name) :
    global music_list

    if is_play :
        print("재생중이므로 노래를 추가할 수 없습니다.")

    music_list.append(music_name)

def play() :
    global music_index, is_play

    print(music_list[music_index], " 가 재생되었습니다.")

    music_index += 1
    is_play = True













save("sorry")
save("celebrity")
save("gravity")
play()
play()
save("인생은한방")
play()


