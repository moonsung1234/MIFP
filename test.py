def _split_data(data, size) :
    temp_data = ""
    data_list = []
    
    for i in range(len(data)) :
        if len((temp_data + data[i]).encode()) >= size :
            data_list.append(temp_data)

            temp_data = ""

        temp_data += data[i]

    return data_list

arr = _split_data("hello world 안녕하세요", 6)

print(arr)