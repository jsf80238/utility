import enum
import random
import string

WORD_LIST = ("which", "would", "their", "there", "about", "other", "could", "first", "these", "years", "where", "after", "those", "still", "being", "world", "might", "never", "under", "while", "three", "state", "found", "again", "place", "since", "every", "until", "water", "think", "house", "night", "going", "asked", "group", "right", "point", "given", "order", "later", "often", "least", "along", "thing", "power", "among", "began", "sense", "means", "hands", "taken", "quite", "words", "death", "times", "light", "money", "shall", "above", "seems", "whose", "today", "known", "field", "heard", "study", "areas", "voice", "woman", "stood", "child", "force", "value", "leave", "level", "party", "lines", "music", "alone", "basis", "women", "wrote", "moved", "hours", "stage", "costs", "added", "third", "space", "board", "heart", "tried", "miles", "makes", "shown", "class", "doing", "terms", "floor", "bring", "range", "paper", "needs", "sound", "close", "story", "cases", "table", "stand", "issue", "front", "start", "weeks", "girls", "ideas", "color", "total", "stock", "trade", "comes", "peace", "using", "below", "month", "piece", "cause", "forms", "sales", "truth", "plant", "works", "court", "labor", "trial", "lower", "image", "based", "earth", "steps", "types", "gives", "blood", "lived", "doubt", "plane", "horse", "visit", "parts", "plans", "speak", "ahead", "radio", "write", "reach", "spent", "press", "serve", "staff", "mouth", "faith", "scene", "teeth", "built", "rates", "meant", "price", "sides", "knows", "fight", "claim", "style", "glass", "early", "share", "trees", "seven", "shows", "older", "eight", "drive", "books", "funds", "noted", "names", "carry", "enemy", "spoke", "units", "takes", "touch", "break", "facts", "cover", "build", "learn", "hotel", "shape", "sight", "begin", "chief", "named", "dance", "event", "fixed", "cells", "fully", "speed", "lives", "offer", "drink", "enter", "union", "favor", "looks", "train", "river", "poems", "anode", "rules", "watch", "index", "check", "frame", "youth", "knife", "store", "items", "faces", "forth", "allow", "wants", "walls", "calls", "drawn", "maybe", "unity", "twice", "signs", "block", "broke", "phase", "dress", "chair", "ought", "plays", "birth", "yards", "fifty", "sleep", "honor", "drove", "north", "homes", "model", "dream", "ended", "score", "rifle", "finds", "exist", "tests", "smile", "liked", "metal", "aside", "taste", "goods", "songs", "south", "shook", "apply", "avoid", "truly", "minds", "loved", "spite", "firms", "scale", "theme", "daily", "truck", "roads", "worry", "rooms", "wheel", "notes", "prove", "motor", "spend", "games", "chest", "depth", "title", "crowd", "phone", "grass", "dozen", "guess", "wagon", "flesh", "whole", "views", "raise", "agree", "begun", "angle", "waves", "faced", "hopes", "trust", "towns", "hoped", "chain", "novel", "worse", "swung", "bonds", "limit", "apart", "boats", "stone", "trend", "threw", "humor", "birds", "fears", "anger", "bills", "sheet", "feels", "curve", "taxes", "agent", "shoes", "count", "saved", "enjoy", "fired", "cross", "occur", "grown", "drama", "foods", "round", "snake", "wages", "bound", "acres", "pilot", "brain", "heads", "shore", "porch", "cloth", "catch", "teach", "holds", "ships", "bread", "match", "shift", "brush", "throw", "pride", "focus", "smoke", "atoms", "skill", "shear", "tired", "award", "judge", "goals", "turns", "steel", "knees", "holes", "track", "reply", "edges", "chose", "noise", "stick", "admit", "hills", "moves", "guide", "error", "kinds", "seeds", "mixed", "ratio", "grant", "doors", "guard", "human", "bombs", "grade", "yield", "paint", "waste", "urged", "smell", "clerk", "blame", "lying", "meets", "owned", "tells", "coast", "swept", "guest", "lists", "tools", "tends", "filed", "guilt", "route", "fewer", "beach", "owner", "badly", "prior", "leads", "worst", "roles", "sugar", "dying", "cards", "crime", "stems", "proof", "lunch", "bride", "burst", "ocean", "grace", "tears", "hurry", "fruit", "forty", "armed", "ruled", "spots", "panel", "stuff", "poets", "pages", "fence", "dates", "piano", "films", "slave", "shock", "loans", "hence", "helps", "split", "shots", "trips", "movie", "tasks", "strip", "argue", "trail", "bench", "arise", "wound", "marks", "pound", "verse", "laugh", "hated", "drugs", "voted", "merit", "grain", "opera", "shade", "refer", "scope", "shoot", "slept", "fiber", "newly", "corps", "storm", "meals", "ranch", "cents", "cried", "dried", "shirt", "entry", "suits", "cloud", "charm", "stars", "beard", "march", "cited", "drill", "hired", "wings", "woods", "aimed", "actor", "yours", "cycle", "tubes", "wines", "clear", "widow", "bases", "treat", "adult", "stuck", "falls", "lands", "rocks", "belly", "radar", "habit", "norms", "posts", "fifth", "green", "dealt", "panic", "grows", "honey", "fault", "souls", "foams", "worth", "delay", "keeps", "races", "teams", "thank", "skirt", "heels", "pause", "mines", "craft", "shame", "trace", "roots", "cabin", "votes", "banks", "solve", "ranks", "flash", "sixth", "pitch", "clock", "motel", "suite", "queen", "newer", "crack", "sweat", "devil", "slide", "screw", "sauce", "cheek", "lungs", "input", "stake", "males", "clubs", "plate", "wiped", "swing", "drank", "sheep", "mercy", "winds", "loves", "likes", "label", "spell", "lobby", "dated", "midst", "slope", "rises", "bones", "tales", "fever", "realm", "pupil", "boots", "glued", "essay", "folks", "arose", "talks", "camps", "coach", "prize", "toast", "brick", "crops", "crash", "acted", "gains", "cream", "fluid", "drops", "dairy", "drift", "tooth", "relax", "brass", "sixty", "faded", "glory", "grams", "marry", "grasp", "balls", "sport", "crown", "uncle", "codes", "chart", "logic", "brand", "flood", "chaos", "tanks", "quote", "rests", "bears", "clean", "print", "flame", "stall", "farms", "sites", "abuse", "nurse", "shops", "draft", "fires", "joint", "quest", "reads", "squad", "waved", "opens", "steam", "lover", "short", "breed", "shake", "magic", "shell", "twist", "piled", "lined", "alarm", "wives", "orbit", "great", "bunch", "liver", "gonna", "spray", "bunks", "opium", "graph", "serum", "boost", "drain", "wider", "react", "tract", "parks", "blast", "ninth", "trick", "knock", "pools", "burns", "stove", "alter", "onion", "tones", "cease", "sweep", "straw", "razor", "ideal", "deals", "cared", "onset", "soils", "fails", "debut", "seats", "paths", "loses", "upset", "candy", "boxes", "pains", "drums", "bored", "alike", "backs", "flung", "vigor", "grave", "draws", "wrong", "lemon", "usage", "stare", "dared", "pairs", "attic", "width", "nails", "swore", "clung", "lever", "adopt", "ivory", "tries", "dough", "imply", "sells", "taxed", "walks", "gates", "tumor", "media", "doses", "gloom", "decay", "patch", "fists", "prose", "blade", "files", "beams", "chill", "arrow", "globe", "loose", "nerve", "maids", "layer", "purse", "blues", "buddy", "maker", "sorts", "tower", "couch", "aloud", "raced", "quiet", "sizes", "hairs", "virus", "ridge", "sadly", "shelf", "eaten", "irony", "gauge", "dolls", "hymen", "wires", "crest", "gifts", "fleet", "aided", "exert", "flies", "rebel", "organ", "slice", "array", "tires", "lodge", "juice", "wired", "drunk", "elite", "debts", "shaft", "curse", "bands", "plain", "final", "bloom", "meats", "grill", "climb", "vapor", "mills", "rider", "sexes", "waist", "posse", "crawl", "crept", "rally", "feeds", "spark", "mates", "unite", "stole", "lease", "chase", "theft", "freed", "fancy", "merge", "monks", "rides", "risen", "clues", "loads", "thumb", "paste", "brace", "mount", "scars", "sings", "grief", "saint", "rolls", "paced", "cigar", "coats", "creep", "tents", "swear", "dimly", "upper", "polls", "sewer", "seeks", "homer", "glove", "filly", "timed", "thigh", "skies", "coins", "pulse", "steer", "surge", "glaze", "rated", "tours", "wheat", "choke", "elder", "awoke", "seams", "await", "troop", "brief", "beans", "salad", "angel", "gland", "pants", "agony", "ghost", "blown", "cites", "hints", "topic", "evils", "haste", "pulls", "rails", "brood", "resin", "roast", "reins", "quill", "black", "quack", "pelts", "wrist", "ditch", "vases", "skiff", "mayor", "setup", "urges", "elect", "wreck", "bites", "blows", "mound", "ankle", "slump", "peaks", "niece", "boast", "dread", "gross", "white", "steak", "flour", "baked", "major", "grips", "raged", "peril", "vines", "eased", "borne", "domes", "blend", "thief", "bless", "stamp", "kills", "plots", "minus", "cooks", "poles", "wrath", "deeds", "cares", "belts", "peers", "cliff", "flair", "dwell", "jokes", "motif", "quick", "pills", "horns", "bosom", "repel", "spare", "chuck", "apple", "coals", "stern", "scrap", "awake", "palms", "bloat", "alert", "slips", "bacon", "modes", "alibi", "knelt", "traps", "ruins", "mouse", "creek", "stool", "quirt", "trunk", "enact", "facto", "minor", "forum", "waged", "repay", "slums", "bowed", "fraud", "mails", "stops", "cheer", "roses", "posed", "speck", "equal", "edged", "buses", "greet", "chore", "paces", "socks", "barge", "skins", "reign", "bluff", "links", "sands", "dunes")
LENGTH = 5

class GuessResult(enum.Enum):
    NOT_GUESSED = ("not_guessed_gallery", None)
    GUESSED_EXACTLY_CORRECTLY = (None, "guessed_exactly_correctly_guessgrid")
    GUESSED_CORRECTLY = ("guessed_correctly_gallery", "guessed_correctly_guessgrid")
    GUESSED_INCORRECTLY = ("guessed_incorrectly_gallery", "guessed_incorrectly_guessgrid")

gallery_dict = dict()
for char in string.ascii_uppercase:
    gallery_dict[char] = GuessResult.NOT_GUESSED

correct_answer = random.choice(WORD_LIST)
correct_answer = "AFTER"
guess_list = list()
guess_list.append("RAISE")
guess_list.append("YOUNG")
guess_list.append("FASTS")
guess_list.append("ENTER")

while True:
    html = """<!DOCTYPE html>
        <html>
            <head>
                <style>
                  .not_guessed_gallery {color: black; background-color: #D7DBDD;}
                  .guessed_exactly_correctly_guessgrid {color: black; background-color: lightgreen; font-weight: bold;}
                  .guessed_correctly_gallery {color: blue; background-color: #D7DBDD;}
                  .guessed_correctly_guessgrid {color: black; background-color: blue;}
                  .guessed_incorrectly_gallery {color: red; background-color: #D7DBDD;}
                  .guessed_incorrectly_guessgrid {color: black; background-color: red;}
                  .empty_guess_square {color: white; background-color: #D7DBDD;}
                </style>
            </head>
            <body>"""
    # Print the guesses the player has made
    exactly_correct_letter_count = 0
    guesses_table_html = "<table>\n"
    for guess in guess_list:
        guesses_table_html += "<tr>\n"
        for guessed_letter, answer_letter in zip(guess, correct_answer):
            if guessed_letter in correct_answer:
                gallery_dict[guessed_letter] = GuessResult.GUESSED_CORRECTLY
                if guessed_letter == answer_letter:
                    guesses_table_html += f'<td class="{GuessResult.GUESSED_EXACTLY_CORRECTLY.value[1]}">{guessed_letter}</td>\n'
                    exactly_correct_letter_count += 1
                else:
                    guesses_table_html += f'<td class="{GuessResult.GUESSED_CORRECTLY.value[1]}">{guessed_letter}</td>\n'
            else:
                gallery_dict[guessed_letter] = GuessResult.GUESSED_INCORRECTLY
                guesses_table_html += f'<td class="{GuessResult.GUESSED_INCORRECTLY.value[1]}">{guessed_letter}</td>\n'
        guesses_table_html += "</tr>\n"
    if exactly_correct_letter_count != LENGTH:
        guesses_table_html += "<tr>"
        for _ in range(LENGTH):
            guesses_table_html += f'<td class="empty_guess_square">&nbsp;</td>'
        guesses_table_html += "</tr>"
    else:
        guesses_table_html += "</table>\n"
    html += guesses_table_html
    html += "<hr>\n"

    # Print the gallery of letters to choose from
    usage_table_html = "<table>\n"
    usage_table_html += "<tr>\n"
    for char, status in gallery_dict.items():
        style = status.value[0]
        usage_table_html += f'<td class="{style}">{char}</td>\n'
    usage_table_html += "</tr>\n"
    usage_table_html += "</table>\n"
    html += usage_table_html

    html += "</body> </html>"
    print(html)
    exit()
    guess = input("->").upper()
    # guess = ''.join(random.choices(string.ascii_uppercase, k=LENGTH))
    if len(guess) != LENGTH:
        print("Incorrect LENGTH!")
        continue
    if guess not in WORD_LIST:
        print("Not a playable word!")
        continue

    exactly_correct_letter_count = 0
    guess_result_list = list()
    for guessed_letter, answer_letter in zip(guess, correct_answer):
        if guessed_letter in correct_answer:
            gallery_dict[guessed_letter] = GuessResult.GUESSED_CORRECTLY
            if guessed_letter == answer_letter:
                guess_result_list.append(GuessResult.GUESSED_EXACTLY_CORRECTLY)
                exactly_correct_letter_count += 1
            else:
                guess_result_list.append(GuessResult.GUESSED_CORRECTLY)
        else:
            gallery_dict[guessed_letter] = GuessResult.GUESSED_INCORRECTLY
            guess_result_list.append(GuessResult.GUESSED_INCORRECTLY)
    if exactly_correct_letter_count == LENGTH:
        print("Solved!")
        exit()
    guess_list.append((guess, guess_result_list[:]))
