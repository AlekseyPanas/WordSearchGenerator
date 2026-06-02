import pdfgen
from puzzlegen import Puzzle

PUZZLES = [
    # Test
    Puzzle(23, [
        "ВОДА", "ВОГОНЬ", "ЗЕМЛЯ", "НЕБО", "ВІТЕР",
        "ДЕРЕВО", "КАМІНЬ", "РІЧКА", "ГОРА", "МОРЕ",
        "СОНЦЕ", "МІСЯЦЬ", "ЗІРКА", "ХМАРА", "ДОЩ",
        "КІНЬ", "ВОВК", "ОРЕЛ", "ЛИСИЦЯ", "ВЕДМІДЬ",
        "ХЛІБ", "МОЛОКО", "ЯБЛУКО", "ЦИБУЛЯ", "ЧАСНИК",
        "СЕРЦЕ", "ДУША", "МРІЯ", "СИЛА", "ВОЛЯ",
    ], "Знайди слова", True),

    # Test
    Puzzle(23, [
    "Lantern",
    "Gravel",
    "Whisper",
    "Orchard",
    "Marble",
    "Velocity",
    "Cactus",
    "Ember",
    "Harbor",
    "Velvet",
    "Glacier",
    "Compass",
    "Timber",
    "Ripple",
    "Furnace",
    "Sapphire",
    "Meadow",
    "Anchor",
    "Paradox",
    "Thunder",
    "Carousel",
    "Quartz",
    "Mirage",
    "Sparrow",
    "Eclipse"], "Find Words", False),

    # Fears
    Puzzle(23, ["Water", "Dependence", "Highway", "Spiders", "Butterflies", "Airplanes",
                "Sounds", "Heights", "Family", "Motorcycles", "Phone", "Darkness", "Tickles",
                "Getting Chased", "Lose Mia", "Debt", "Loneliness", "People", "Bad Luck", "Chronic Illness",
                "Giving Birth", "Aging", "Loss Control", "Rejection", "Unknown"],
           "Olenka's Fears", False),

    Puzzle(23, [
        "Blood", "Bugs", "Worms", "Eye Surgery", "Loneliness", "Ocean", "Skiing", "Amnesia", "Weight Gain",
        "Chronic Illness", "Computer Damage", "Family", "Heights", "Darkness", "Dependence", "Loss Freedom",
        "Betrayal", "Loss Control", "Claustrophobia", "Snakes", "Space", "Apocalypse", "Diving", "Erectile Dysfunction",
        "Blindness"
    ], "Lyosha's Fears", False),

    # On My Table
    Puzzle(23, [
        "Bush Rose", "Brushes", "Beads", "Perfumes", "Facial Sponges",
        "QTips", "Foundation", "Micellar Water", "Toner", "Mascara",
        "Scissors", "Clippers", "Freser", "Chargers", "Lipstick",
        "Cotton Pads", "Mirror", "Earrings", "Embroidery", "Milling Machine",
        "Bracelet", "Claw Clip", "Ring", "Makeup Removal Wipes", "Sunglasses",
    ], "On Your Table <3", True),

    # Films Shows
    Puzzle(23, ["Постукай в мої Двері", "Будиночок на щастя", "Свати", "Джинні і Джорджіа", "Життя по Визову",
                "Папик", "Скліфасовский", "Кухня", "Готель Елеон", "Гранд", "Моя Вина", "Хазяйка",
                "Снайпер", "Ботоферма", "Спіймати Кайдаша", "Жіночий Лікар", "Код", "Слідство Екстрасенсів",
                "Венздей", "Останній Москаль", "Скажені Сусіди", "Слід", "Лікарка", "Контрабас", "Коза Ностра"],
               "Фільми та серіали Оленки", True),

    Puzzle(23, ["Breaking Bad", "Game of Thrones", "Harry Potter", "Avatar", "Grey's Anatomy",
                "Outer Banks", "RWBY", "Silo", "Severance", "Sluga Naroda", "The Hundred", "Black Mirror",
                "Better Call Saul", "Arcane", "Last Kingdom", "Stranger Things", "Squid Game", "Walking Dead",
                "Silicon Valley", "Rick and Morty", "", "", "", "", ""],
           "Lyosha's Movies and Shows", False),


    # Phil it
    Puzzle(23, ["Тебе Немає Тут", "Пірнаю", "Свобода", "Немає Неба", "Мені Тебе Бракує", "Така як ти",
                "Голоси", "Її немає", "", "", "", "", "", "", "", "",
                "", "", "", "", "", "", "", "", "", ], "Пісні Philit", True),

    # Emotions
    Puzzle(23, ["Bossy", "Feisty", "Stubborn", "Horny", "Loving", "Not Talking", "Pissed off",
                "Tickling", "Playful", "Motivating", "Doomer", "Sad", "Nostalgic", "Normal", "Immersed in Music",
                "Sleepy", "Varenik", "Independent Woman", "Competitive", "Excited", "Zayibalasya",
                "Impatient", "Caring", "Focused", "Revenge"], "Olenka's Emotions", True),

    # Lviv
    Puzzle(23, ["Resne Two", "Resne One", "Highschool One Hundred", "Lviv", "Potocki Palace",
                "King Danylo Monument", "Lviv National Medical University", "Muzey Khvorob Lyudyny",
                "Rebernya", "Tram", "", "", "", "", "", "",
                "", "", "", "", "", "", "", "", "", ], "Лвів", True),

    # Makeup
    Puzzle(23, ["Foundation", "Maskara", "Lipstick", "Blush", "Dr Althea", "Micellar Water", "Eyeshadow",
                "Eyeliner", "Toner", "Makeup Wipes", "Cotton Pads", "Teardrop Sponge", "Cerave", "", "", "",
                "", "", "", "", "", "", "", "", "", ], "Makeup", True),

    # Clothes
    Puzzle(23, ["Black Jeans", "White Jeans", "Vishivanka", "", "", "", "",
                "", "", "", "", "", "", "", "", "",
                "", "", "", "", "", "", "", "", "", ], "Clothes", True),

    # Lyosha
    Puzzle(23, ["Paragliding", "Hiking", "Mountains", "Motorcycle", "Computer",
                "Programming", "Nerdy", "Creativity", "Writing", "Magengaard", "Professor",
                "Reading", "Philosophy", "Clumsy", "Elephant", "Road Trips",
                "Italian", "Panas", "Aleksey", "Robotics", "Weight Lifting", "Drawing",
                "Scifi Fantasy", "Aries", "Organizational"], "Lyosha", True),

    # Travel
    Puzzle(23, ["Sunrise", "Mattress", "Phoenix", "Frontier", "Starbucks", "Coffee", "Sequoia",
                "AFrame", "Redwoods", "Cactus", "San Francisco", "Golden Gate Bridge", "Car", "Airplane",
                "Roadtrip", "Cactus Lyosha", "Angeles Crest Highway", "Ortega Highway", "ATV",
                "New Yurt City", "Yosemite", "Mandarins", "Fireplace", "Record Player", "GPS"], "Travel", True),

    # Favorite Flowers
    Puzzle(23, ["Ranunculus", "Peonies", "Bush Rose", "Roses", "Lavender", "Carnations",
                "", "", "", "", "", "", "", "", "", "",
                "", "", "", "", "", "", "", "", ""], "Favorite Flowers", True),

    # New York
    Puzzle(23, ["Vitya", "Misplaced Pots", "Construction", "No Bathroom", "Curtis",
                "Tottenville", "Car Sleeping", "Great Kills", "Wolfs Pond", "First Sex", "Miller Field",
                "Long Drives", "Boardwalk", "Verazzano", "IKEA", "Brooklyn",
                "Time Square", "Dima", "Emma", "Raccoons", "Yacht Docks", "Relationship Principles",
                "Our Tree", "Cameras", "Piano"], "New York", True),

    # Vermont
    Puzzle(23, ["Claremont", "Springfield", "Perkinsville", "Sand Hill Trail",
                "Ascutney", "Morningside", "Myra", "Ricky", "Gerda", "Liska", "Liquidation", "Reservoir Dam",
                "Ladoga", "Olya", "By the River", "First Date", "Villagers Ice Cream", "Milk Farm", "Rubber Boat",
                "Secret Love", "Stress", "Movie Nights", "First Kiss", "Black Wardrobe", "Attic"], "Vermont", True),

    # California
    Puzzle(23, ["Botan Sushi", "Laguna Beach", "Verano Place", "Irvine", "Los Angeles",
                "UC Irvine", "Irvine Valley College", "Maintenance", "Moving In", "Top of the World", "", "",
                "Vanilla Street Bakery", "San Diego", "Irina Fedyshyn", "Easter Basket", "DMV",
                "Verano Towers", "Furnishing", "Fort Bragg", "Sequoia", "Highway One",
                "Natalya", "LAX", "Teddy Bear"], "California", True),

    # Perfumes
    Puzzle(23, ["Yves Libre", "Yves Berry Crush", "Gucci Bloom", "Light Blue",
                "Black Opium", "Good Girl", "", "", "", "", "", "", "", "", "", "",
                "", "", "", "", "", "", "", "", "", ], "Perfumes", True),

    # Mia
    Puzzle(23, ["Mia", "Delectables", "Bird", "Cat Tree", "Purring", "Hiding", "Butt Upwards",
                "Petting", "Soft", "Bunny", "Zoomies", "Scratchpost", "Litterbox", "Purina Pro Plan",
                "Nulo", "Tiny Paws and Whiskers", "Sneezing", "Grey", "White", "Windows", "Rescue", "Antibiotic",
                "Meow", "Couch", "Boogers"], "Mia", True),

    # New Jersey
    Puzzle(23, ["Chestnut Street", "Sushi Boy", "Eighteenth Birthday", "First License", "Netcost",
                "Burlington", "Marina", "Instacart", "Dahnerts Lake County Park", "Sadko Trans", "Orest",
                "Escape", "Parking Lot", "Motorcycle", "Accident", "Passat", "Swing", "Dog", "Roses",
                "Heart Pillow", "Makeup Table", "", "", "", ""], "New Jersey", True),

    # Cars
    Puzzle(23, ["Audi Q Five", "Audi Q Seven", "Audi A Four", "Audi A Six", "Mercedes GLE", "GMC Yukon",
                "BMW M Eight", "BMW M Four", "BMW X Five", "BMW X Seven", "Passat", "Toyota Sienna", "Tesla",
                "Honda CRV", "", "", "", "", "", "", "", "", "", "", ""], "Cars", True),

    # Hobbies
    Puzzle(23, ["Bead Embroidery", "Word Search", "Shows and Movies", "Driving", "Reading",
                "Painting by Numbers", "Jigsaw Puzzles", "Battleships", "Photography", "Photo Editing",
                "Video Editing", "Tik Tok", "Being the Boss", "Being an amazing girlfriend", "sleeping",
                "Truck Simulator", "Music", "Volleyball", "Ping Pong", "Tennis", "Calligraphy",
                "Cooking", "Ice Skating", "Nature Walks", "Phone Games"], "Hobbies", True),

    # Food
    Puzzle(23, ["Guacamole", "Ukrainian Ragu", "Pasta with Milk", "Crepes", "Shawarma", "Cheeseburger",
                "Chicken Nuggets", "Fries", "Shrimp Pasta", "Smoked Mackerel", "Salmon", "Sushi",
                "Smoked Salmon Waffle", "Macarons", "Steak", "Edamame",
                "Raw Peas", "Cucumber", "Liver Pate", "Solyanka", "Runa", "Sprats", "Condensed Milk",
                "Vanilla Ice cream", "KitKat"], "Favorite Food", True),

]


for puzzle in PUZZLES:
    pdfgen.generate_wordsearch_pdf(
        grid=puzzle.word_grid,
        words=puzzle.word_bank,
        output_path=f"{puzzle.title}.pdf",
        title=puzzle.title,
        show_solution=False,
        is_uk=puzzle.isUk
    )

    pdfgen.generate_wordsearch_pdf(
        grid=puzzle.word_grid,
        words=puzzle.word_bank,
        output_path=f"{puzzle.title}_SOL.pdf",
        title=puzzle.title,
        show_solution=True,
        is_uk=puzzle.isUk
    )