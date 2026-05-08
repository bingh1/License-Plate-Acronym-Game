#!/usr/bin/env python3
import sys, random, re, os

WORDLIST = "/usr/share/dict/american-english"

COLORADO = {
    'A': ['alpine','altitude','aspen','aurora','avalanche','arapahoe','ahead'],
    'B': ['boulder','brewery','blizzard','bison','backcountry','breathtaking','boots'],
    'C': ['colorado','continental','chairlift','canyon','crisp','craft','cold'],
    'D': ['denver','downhill','dusty','dude','dusk','divide','drifting'],
    'E': ['elevation','elk','epic','endeavor','evergreen','endless','extreme'],
    'F': ['fourteener','fresh','flatiron','frozen','flow','frontier','fluffy'],
    'G': ['gondola','glades','gnar','golden','groomer','gorge','glacier'],
    'H': ['highline','hops','hardpack','hiking','holler','howling','harvest'],
    'I': ['icy','iconic','inversion','incline','indie'],
    'J': ['jagged','juniper','joyful','jolting','journey'],
    'K': ['keystone','kinetic','keen','keg'],
    'L': ['lager','lift','lodge','locals','loamy','lofty','legend'],
    'M': ['mountain','mogul','mesa','marmot','moose','meadow'],
    'N': ['nordic','natural','narrow','notorious','nimble'],
    'O': ['outdoors','overlook','oxygen','open'],
    'P': ['powder','peak','pint','ponderosa','pass','pristine'],
    'Q': ['quiet','quaking','quartz'],
    'R': ['rockies','ripping','rustic','ranch','ridge','roaring','rugged'],
    'S': ['shred','summit','ski','slopes','snowpack','saloon','stoke'],
    'T': ['telluride','tundra','trail','trees','toasty'],
    'U': ['untracked','upstream','untamed','uphill'],
    'V': ['vail','vertical','vast','valley','vista','vibrant'],
    'W': ['wildfire','whiteout','wilderness','wapiti','wild','windy','western'],
    'X': ['xtreme'],
    'Y': ['yonder','yeti','yellow','yearning'],
    'Z': ['zeal','zipline','zenith','zero'],
}

FALLBACK_WORDS = [
    "apple","able","arrow","anchor","amber","angle","agent","above","angry","alive",
    "brave","bright","broad","brown","break","bring","brush","build","blend","black",
    "clean","clear","cloud","count","cover","craft","creek","crisp","crush","cycle",
    "daily","dance","dark","dawn","deep","delta","dense","drift","drive","drops",
    "early","earth","eight","ember","empty","enter","equal","every","exact","extra",
    "faint","fancy","fast","field","final","first","fixed","flame","flash","float",
    "giant","given","glass","glide","glow","grace","grand","grant","grasp","great",
    "habit","happy","harsh","heavy","hello","helps","herbs","high","hints","holds",
    "ideal","image","inner","input","inter","intro","iron","island","issue","ivory",
    "joint","judge","juice","jumps","just","jaunt","jewel","jolt","jazzy","jiffy",
    "keeps","kicks","kinds","knack","knife","knock","knows","kudos","kinship","keen",
    "large","laser","later","layer","leads","learn","leave","lemon","level","light",
    "magic","major","maker","march","match","might","minor","mixed","model","motor",
    "named","nerve","never","night","noble","noise","north","noted","novel","nudge",
    "often","order","other","outer","owned","oaken","ocean","offer","olive","onset",
    "paint","paper","patch","pause","peace","phase","pilot","pixel","place","plain",
    "quest","quick","quiet","quirk","quota","quote","quill","qualm","quaff","quake",
    "radar","radio","raise","range","rapid","ratio","reach","ready","realm","rebel",
    "safer","sauce","scale","scene","score","scout","serve","seven","shade","shake",
    "table","taken","taste","teach","teams","thick","thing","think","third","those",
    "under","unity","until","upper","urban","ultra","usage","usual","utter","upward",
    "valid","value","vapor","verse","video","vigor","viral","visit","vital","vivid",
    "wagon","watch","water","waves","weave","wedge","weigh","weird","whole","wider",
    "xenon","xeric","yards","yield","young","yours","youth","yummy","yearn","yodel",
    "zebra","zesty","zippy","zonal","zones","zooms","zappy","zilch","zings","zoned",
]

def extract_plate_letters(image_path):
    import easyocr
    print("Loading OCR model (first run may take a minute)...")
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_path)

    # Filter out common plate non-letter text before extracting
    IGNORE = {'COLORADO', 'COLORFUL', 'COLORFULL', 'USA', 'STATE'}
    raw = ' '.join([text for _, text, conf in results if conf > 0.2 and text.upper() not in IGNORE])
    letters = re.sub(r'[^A-Za-z]', '', raw).upper()

    if len(letters) < 2:
        raise ValueError("Could not read any letters from the image. Try a clearer photo.")

    return letters[:7]

def load_words():
    by_letter = {}
    if os.path.isfile(WORDLIST):
        with open(WORDLIST) as f:
            words = [w.strip().lower() for w in f if re.match(r'^[a-z]{3,10}$', w.strip())]
    else:
        words = FALLBACK_WORDS
    for w in words:
        by_letter.setdefault(w[0], []).append(w)
    return by_letter

def pick_word(letter, dict_words, used):
    co_words = COLORADO.get(letter.upper(), [])
    random.shuffle(co_words)
    for w in co_words:
        if w not in used:
            return w
    candidates = dict_words.get(letter.lower(), [])
    random.shuffle(candidates)
    for w in candidates:
        if w not in used:
            return w
    return letter + "..."

def make_acronym(letters, dict_words):
    used = set()
    words = []
    for letter in letters:
        w = pick_word(letter, dict_words, used)
        used.add(w)
        words.append(w)
    return ' '.join(words)

def highlight(phrase):
    bold_green = '\033[1;32m'
    reset = '\033[0m'
    words = phrase.split()
    return ' '.join(f"{bold_green}{w[0].upper()}{reset}{w[1:]}" for w in words)

def main():
    if len(sys.argv) < 2:
        print("Usage: python plate.py <letters OR image_path>")
        print("  python plate.py ABC")
        print("  python plate.py images/test1.jpg")
        sys.exit(1)

    arg = sys.argv[1]

    if os.path.isfile(arg):
        ext = os.path.splitext(arg)[1].lower()
        if ext in ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'):
            print(f"\n\033[1m Reading plate from image...\033[0m")
            try:
                letters = extract_plate_letters(arg)
                print(f"\033[90mDetected letters: {letters}\033[0m")
            except Exception as e:
                print(f"\033[31mError: {e}\033[0m")
                sys.exit(1)
        else:
            print(f"Unsupported file type: {ext}")
            sys.exit(1)
    else:
        letters = re.sub(r'[^A-Za-z]', '', arg).upper()

    if len(letters) < 2:
        print("Need at least 2 letters.")
        sys.exit(1)

    print(f"\n\033[1m  Colorado Plate: {'-'.join(letters)}\033[0m\n")

    dict_words = load_words()

    for i in range(5):
        phrase = make_acronym(letters, dict_words)
        print(f"  {i+1}. {highlight(phrase)}")

    print()

if __name__ == '__main__':
    main()