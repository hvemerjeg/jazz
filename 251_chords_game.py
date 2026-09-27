from random import choice
import os
from time import sleep

NOTES = "CDEFGAB"
MAJOR_KEYS = ["CMaj", "BbMaj", "AbMaj", "GbMaj", "EMaj", "DMaj", "BMaj", "AMaj", "GMaj", "FMaj", "EbMaj", "DbMaj"] # Ignore enharmonics
MINOR_KEYS = []
SHARPS_SEQUENCE = "FCGDAEB"
FLATS_SEQUENCE = "BEADGCF"
BASE_MAJOR_KEYS = ["CMaj", "FMaj"] # List of keys that do not follow the pattern
# Create minor base minor keys list

def menu():
    print("Welcome to the II-V-I progression game!")
    print("This game is meant to practive II-V-I progression for Jazz learners")
    print("You will be asked about a II-V-I progression in a random key")
    print("You can choose to practice only II-V-I major, minor or both")
    print("1) Major")
    print("2) Minor")
    print("3) Both")
    print("4) Random chord in major keys (only II-V-I)")
    print("5) Major with three note voicing")

def findAccidental(note:str, key:str):
    if key in BASE_MAJOR_KEYS:
        if key == "FMaj" and note == "B":
            return "B" + "b"
        return note
    # implement logic for minor
    root = key.replace("Maj", "").replace("min", "")
    if "Maj" in key:
        if "b" in root:
            flats = FLATS_SEQUENCE[:FLATS_SEQUENCE.index(root.replace("b", "")) + 2]
            if note in flats:
                return note + "b"
        elif "#" in root:
            sharps = SHARPS_SEQUENCE[:SHARPS_SEQUENCE.index(NOTES[NOTES.index(root.replace("#", "")) - 1]) + 1]
            if note in sharps:
                return note + "#"
        else:
            # Since any altered note that we have in the list of Majors is flat...
            sharps = SHARPS_SEQUENCE[:SHARPS_SEQUENCE.index(NOTES[NOTES.index(root.replace("#", "")) - 1]) + 1]
            if note in sharps:
                return note + "#"
    return note

def findProgression(key:str, progression:str):
    altered_note = key.replace("Maj", "").replace("min", "") # note with alteration (in case that it has). add half dimished #fixme
    note = altered_note.replace("#", "").replace("b", "")
    if key not in MAJOR_KEYS and key not in BASE_MAJOR_KEYS:
        raise ValueError("Key was not found")
    if progression == "Maj_II-V-I":
        ii = findAccidental(NOTES[(NOTES.index(note) + 1) % len(NOTES)], key) + "min7"
        v = findAccidental(NOTES[(NOTES.index(note) + 4) % len(NOTES)], key) + "7"
        i = key + "7"
    return [ii, v, i]

def threeNoteVoicing(chord:str, key:str):
    altered_note = chord.replace("Maj7", "").replace("min7", "").replace("7", "")
    note = altered_note.replace("#", "").replace("b", "")
    root = altered_note
    third = findAccidental(NOTES[(NOTES.index(note) + 2) % len(NOTES)], key)
    seventh = findAccidental(NOTES[(NOTES.index(note) + 6) % len(NOTES)], key)
    return [root, third, seventh]

def Maj_II_V_I(voicing=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    current = choice(MAJOR_KEYS)
    print(f"Play II-V-I in the key of {current} on your instrument")
    #chords_input = input(f"Insert II-V-I chords of {current} (e.g. F#min7, B7, EMaj7): ").split(", ")
    current_progression = findProgression(current, "Maj_II-V-I")
    for indx, degree in enumerate(["II", "V", "I"]):
        chord_input = input(f"Insert {degree} chord of {current} (e.g. F#min7): ")
        if chord_input != current_progression[indx]:
            print(f"Incorrect response {chord_input}. The correct answer is {current_progression[indx]}")
        else:
            print(f"{chord_input} is correct!")

        if voicing == "three_note":
            notes = threeNoteVoicing(current_progression[indx], current)
            note_input = input(f"Insert notes of voicing {voicing} for chord {current_progression[indx]} (e.g. C, E, B): ").split(", ")
            if note_input != notes:
                print(f"Incorrect response {note_input}. The correct answer is {notes}")
            else:
                print(f"{note_input} is correct!")

    MAJOR_KEYS.remove(current)
    input("Press enter")


def Min_II_V_I():
    raise NotImplementedError

def randomChord(progression:str):
    os.system('cls' if os.name == 'nt' else 'clear')
    all_chords = list()
    current_keys = MAJOR_KEYS if progression == "Maj_II-V-I" else MINOR_KEYS
    for k in current_keys:
        all_chords.extend(findProgression(k, progression))
    while len(all_chords):
        current = choice(all_chords)
        print(f"Play {current} on your instrument")
        input("Press enter")
        all_chords.remove(current)

def main():
    menu()
    game_mode = input("Which mode do you want to play (1, 2, 3, 4 or 5): ")
    if game_mode == "1":
        while len(MAJOR_KEYS):
            Maj_II_V_I()
    elif game_mode == "2":
        pass
    elif game_mode == "3":
        pass
    elif game_mode == "4":
        randomChord("Maj_II-V-I")
    elif game_mode == "5":
        while len(MAJOR_KEYS):
            Maj_II_V_I("three_note")

if __name__ == "__main__":
    main()
