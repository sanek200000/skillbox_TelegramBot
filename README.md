# skillbox_TelegramBot

# План
1. написать программу

# Как работает API rapidapi.com
1. locations/v3/search 
    - предоставляет ответ по выбранной локации из которого нужно вытянуть id локации (gaiaId)
    - фильтруем по ключу sr -> num -> type = "CITY"
    - берем:
        - city = sr -> num ->regionNames -> fullName (='Нью-Йорк, Нью-Йорк, США')
        - gaiaId = sr -> num -> gaiaId (='2621')
2. properties/v2/list
    - предоставляет ответ с информацией по отелям: id отеля,название, цена. Ожидает от вас id локации (gaiaId)
    - берем:
        - hotels_list = data -> propertySearch -> properties
        - hotel_id = hotels_list -> num -> id (='23033777')
        - hotel_name = hotels_list -> num -> name (='Friends Homestay - Hostel')
        - price = hotels_list -> num -> price -> lead -> amount (=105.716)
3. properties/v2/detail 
    - предоставляет ответ с подробной информацией об отеле: точный адрес, фотографии. Ожидает от вас id отеля
    - берем:
        - address = data -> propertyInfo -> summary -> location -> address -> addressLine (="24 Kugu Street, Riga, LV-1048")
        - images = data -> propertyInfo -> propertyGallery -> images -> num -> image -> url ("https://images.trvl-media.com/lodging/1000000/20000/10200/10159/1064be5b.jpg?impolicy=resizecrop&rw=500&ra=fit")
