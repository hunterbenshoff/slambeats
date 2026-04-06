#!/usr/bin/env python3
"""
Daily Spotify playlist updater for slambeatsdotkill.
Keeps the last 3 days' albums in the playlist — mirrors the Pit's 3-day window.
"""

import os, requests, base64, json
from datetime import date, timedelta

CLIENT_ID     = os.environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
REFRESH_TOKEN = os.environ['SPOTIFY_REFRESH_TOKEN']
PLAYLIST_ID   = '4mZFXJ8NgaKQ01SxZBdAAX'

# ── ALBUMS — must match index.html exactly ────────────────────────────────────
ALBUMS = [
    ["Black Sabbath", "Black Sabbath", 1970, "Classic Metal"],
    ["Paranoid", "Black Sabbath", 1970, "Classic Metal"],
    ["Master of Reality", "Black Sabbath", 1971, "Classic Metal"],
    ["Vol. 4", "Black Sabbath", 1972, "Classic Metal"],
    ["Sabbath Bloody Sabbath", "Black Sabbath", 1973, "Classic Metal"],
    ["Sabotage", "Black Sabbath", 1975, "Classic Metal"],
    ["Heaven and Hell", "Black Sabbath", 1980, "Classic Metal"],
    ["Mob Rules", "Black Sabbath", 1981, "Classic Metal"],
    ["British Steel", "Judas Priest", 1980, "Classic Metal"],
    ["Screaming for Vengeance", "Judas Priest", 1982, "Classic Metal"],
    ["Defenders of the Faith", "Judas Priest", 1984, "Classic Metal"],
    ["Painkiller", "Judas Priest", 1990, "Classic Metal"],
    ["Iron Maiden", "Iron Maiden", 1980, "Classic Metal"],
    ["Killers", "Iron Maiden", 1981, "Classic Metal"],
    ["The Number of the Beast", "Iron Maiden", 1982, "Classic Metal"],
    ["Piece of Mind", "Iron Maiden", 1983, "Classic Metal"],
    ["Powerslave", "Iron Maiden", 1984, "Classic Metal"],
    ["Somewhere in Time", "Iron Maiden", 1986, "Classic Metal"],
    ["Seventh Son of a Seventh Son", "Iron Maiden", 1988, "Classic Metal"],
    ["Fear of the Dark", "Iron Maiden", 1992, "Classic Metal"],
    ["On Through the Night", "Def Leppard", 1980, "Classic Metal"],
    ["High 'n' Dry", "Def Leppard", 1981, "Classic Metal"],
    ["Pyromania", "Def Leppard", 1983, "Classic Metal"],
    ["Wheels of Steel", "Saxon", 1980, "Classic Metal"],
    ["Strong Arm of the Law", "Saxon", 1980, "Classic Metal"],
    ["Denim and Leather", "Saxon", 1981, "Classic Metal"],
    ["Lightning to the Nations", "Diamond Head", 1980, "Classic Metal"],
    ["Ace of Spades", "Motörhead", 1980, "Classic Metal"],
    ["Iron Fist", "Motörhead", 1982, "Classic Metal"],
    ["Orgasmatron", "Motörhead", 1986, "Classic Metal"],
    ["Bomber", "Motörhead", 1979, "Classic Metal"],
    ["Overkill", "Motörhead", 1979, "Classic Metal"],
    ["Kill 'Em All", "Metallica", 1983, "Thrash Metal"],
    ["Ride the Lightning", "Metallica", 1984, "Thrash Metal"],
    ["Master of Puppets", "Metallica", 1986, "Thrash Metal"],
    ["...And Justice for All", "Metallica", 1988, "Thrash Metal"],
    ["Peace Sells... but Who's Buying?", "Megadeth", 1986, "Thrash Metal"],
    ["So Far, So Good... So What!", "Megadeth", 1988, "Thrash Metal"],
    ["Rust in Peace", "Megadeth", 1990, "Thrash Metal"],
    ["Countdown to Extinction", "Megadeth", 1992, "Thrash Metal"],
    ["Reign in Blood", "Slayer", 1986, "Thrash Metal"],
    ["South of Heaven", "Slayer", 1988, "Thrash Metal"],
    ["Seasons in the Abyss", "Slayer", 1990, "Thrash Metal"],
    ["Spreading the Disease", "Anthrax", 1985, "Thrash Metal"],
    ["Among the Living", "Anthrax", 1987, "Thrash Metal"],
    ["State of Euphoria", "Anthrax", 1988, "Thrash Metal"],
    ["Persistence of Time", "Anthrax", 1990, "Thrash Metal"],
    ["Fistful of Metal", "Anthrax", 1984, "Thrash Metal"],
    ["Bonded by Blood", "Exodus", 1985, "Thrash Metal"],
    ["Fabulous Disaster", "Exodus", 1989, "Thrash Metal"],
    ["Impact Is Imminent", "Exodus", 1990, "Thrash Metal"],
    ["The Ultra-Violence", "Death Angel", 1987, "Thrash Metal"],
    ["Frolic Through the Park", "Death Angel", 1988, "Thrash Metal"],
    ["Feel the Fire", "Overkill", 1985, "Thrash Metal"],
    ["Taking Over", "Overkill", 1987, "Thrash Metal"],
    ["Under the Influence", "Overkill", 1988, "Thrash Metal"],
    ["The Years of Decay", "Overkill", 1989, "Thrash Metal"],
    ["Horrorscope", "Overkill", 1991, "Thrash Metal"],
    ["Speak English or Die", "Stormtroopers of Death", 1985, "Thrash Metal"],
    ["Terrible Certainty", "Kreator", 1987, "Thrash Metal"],
    ["Pleasure to Kill", "Kreator", 1986, "Thrash Metal"],
    ["Extreme Aggression", "Kreator", 1989, "Thrash Metal"],
    ["Coma of Souls", "Kreator", 1990, "Thrash Metal"],
    ["Eternal Devastation", "Destruction", 1986, "Thrash Metal"],
    ["Release from Agony", "Destruction", 1987, "Thrash Metal"],
    ["Infernal Overkill", "Destruction", 1985, "Thrash Metal"],
    ["Sentence of Death", "Destruction", 1984, "Thrash Metal"],
    ["Persecution Mania", "Sodom", 1987, "Thrash Metal"],
    ["Agent Orange", "Sodom", 1989, "Thrash Metal"],
    ["In the Sign of Evil", "Sodom", 1984, "Thrash Metal"],
    ["Tapping the Vein", "Forbidden", 1990, "Thrash Metal"],
    ["Forbidden Evil", "Forbidden", 1988, "Thrash Metal"],
    ["Game Over", "Nuclear Assault", 1986, "Thrash Metal"],
    ["Handle with Care", "Nuclear Assault", 1989, "Thrash Metal"],
    ["The System Has Failed", "Megadeth", 2004, "Thrash Metal"],
    ["Endgame", "Megadeth", 2009, "Thrash Metal"],
    ["Scream Bloody Gore", "Death", 1987, "Death Metal"],
    ["Leprosy", "Death", 1988, "Death Metal"],
    ["Spiritual Healing", "Death", 1990, "Death Metal"],
    ["Human", "Death", 1991, "Death Metal"],
    ["Individual Thought Patterns", "Death", 1993, "Death Metal"],
    ["Symbolic", "Death", 1995, "Death Metal"],
    ["The Sound of Perseverance", "Death", 1998, "Death Metal"],
    ["Seven Churches", "Possessed", 1985, "Death Metal"],
    ["Altars of Madness", "Morbid Angel", 1989, "Death Metal"],
    ["Blessed Are the Sick", "Morbid Angel", 1991, "Death Metal"],
    ["Covenant", "Morbid Angel", 1993, "Death Metal"],
    ["Domination", "Morbid Angel", 1995, "Death Metal"],
    ["Like an Everflowing Stream", "Dismember", 1991, "Death Metal"],
    ["Indecent and Obscene", "Dismember", 1993, "Death Metal"],
    ["Left Hand Path", "Entombed", 1990, "Death Metal"],
    ["Clandestine", "Entombed", 1991, "Death Metal"],
    ["Dawn of Possession", "Immolation", 1991, "Death Metal"],
    ["Here in After", "Immolation", 1996, "Death Metal"],
    ["Mortal Throne of Nazarene", "Incantation", 1994, "Death Metal"],
    ["Onward to Golgotha", "Incantation", 1992, "Death Metal"],
    ["Suffocation", "Suffocation", 1991, "Death Metal"],
    ["Effigy of the Forgotten", "Suffocation", 1991, "Death Metal"],
    ["Pierced from Within", "Suffocation", 1995, "Death Metal"],
    ["Breeding the Spawn", "Suffocation", 1993, "Death Metal"],
    ["Eaten Back to Life", "Cannibal Corpse", 1990, "Death Metal"],
    ["Butchered at Birth", "Cannibal Corpse", 1991, "Death Metal"],
    ["Tomb of the Mutilated", "Cannibal Corpse", 1992, "Death Metal"],
    ["The Bleeding", "Cannibal Corpse", 1994, "Death Metal"],
    ["Vile", "Cannibal Corpse", 1996, "Death Metal"],
    ["Gallery of Suicide", "Cannibal Corpse", 1998, "Death Metal"],
    ["Gore Obsessed", "Cannibal Corpse", 2002, "Death Metal"],
    ["Kill", "Cannibal Corpse", 2006, "Death Metal"],
    ["Evisceration Plague", "Cannibal Corpse", 2009, "Death Metal"],
    ["Torture", "Cannibal Corpse", 2012, "Death Metal"],
    ["A Skeletal Domain", "Cannibal Corpse", 2014, "Death Metal"],
    ["Red Before Black", "Cannibal Corpse", 2017, "Death Metal"],
    ["Violence Unimagined", "Cannibal Corpse", 2021, "Death Metal"],
    ["Mental Funeral", "Autopsy", 1991, "Death Metal"],
    ["Severed Survival", "Autopsy", 1989, "Death Metal"],
    ["Acts of the Unspeakable", "Autopsy", 1992, "Death Metal"],
    ["The Gallery", "Dark Tranquillity", 1995, "Melodic Death Metal"],
    ["The Mind's I", "Dark Tranquillity", 1997, "Melodic Death Metal"],
    ["Projector", "Dark Tranquillity", 1999, "Melodic Death Metal"],
    ["Haven", "Dark Tranquillity", 2000, "Melodic Death Metal"],
    ["Damage Done", "Dark Tranquillity", 2002, "Melodic Death Metal"],
    ["The Slaughter of the Soul", "At the Gates", 1995, "Melodic Death Metal"],
    ["With Fear I Kiss the Burning Darkness", "At the Gates", 1993, "Melodic Death Metal"],
    ["Terminal Spirit Disease", "At the Gates", 1994, "Melodic Death Metal"],
    ["The Jester Race", "In Flames", 1996, "Melodic Death Metal"],
    ["Whoracle", "In Flames", 1997, "Melodic Death Metal"],
    ["Colony", "In Flames", 1999, "Melodic Death Metal"],
    ["Clayman", "In Flames", 2000, "Melodic Death Metal"],
    ["Versus the World", "Amon Amarth", 2002, "Melodic Death Metal"],
    ["Twilight of the Thunder God", "Amon Amarth", 2008, "Melodic Death Metal"],
    ["Surtur Rising", "Amon Amarth", 2011, "Melodic Death Metal"],
    ["Jomsviking", "Amon Amarth", 2016, "Melodic Death Metal"],
    ["A Velvet Creation", "Eucharist", 1993, "Melodic Death Metal"],
    ["Under the Weeping Moon", "My Dying Bride", 1992, "Doom Metal"],
    ["Turn Loose the Swans", "My Dying Bride", 1992, "Doom Metal"],
    ["The Angel and the Dark River", "My Dying Bride", 1995, "Doom Metal"],
    ["Iconoclast", "Symphony X", 2011, "Progressive Metal"],
    ["V: The New Mythology Suite", "Symphony X", 2000, "Progressive Metal"],
    ["The Divine Wings of Tragedy", "Symphony X", 1997, "Progressive Metal"],
    ["The Odyssey", "Symphony X", 2002, "Progressive Metal"],
    ["Focus", "Cynic", 1993, "Progressive Metal"],
    ["Traced in Air", "Cynic", 2008, "Progressive Metal"],
    ["Path of Totality", "Cynic", 2010, "Progressive Metal"],
    ["Control and Resistance", "Watchtower", 1989, "Technical Thrash"],
    ["Energetic Disassembly", "Watchtower", 1985, "Technical Thrash"],
    ["The Erosion of Sanity", "Gorguts", 1993, "Technical Death Metal"],
    ["Obscura", "Gorguts", 1998, "Technical Death Metal"],
    ["From Wisdom to Hate", "Gorguts", 2001, "Technical Death Metal"],
    ["Colored Sands", "Gorguts", 2013, "Technical Death Metal"],
    ["None So Vile", "Cryptopsy", 1996, "Technical Death Metal"],
    ["Whisper Supremacy", "Cryptopsy", 1998, "Technical Death Metal"],
    ["And Then You'll Beg", "Cryptopsy", 2000, "Technical Death Metal"],
    ["Once Was Not", "Cryptopsy", 2005, "Technical Death Metal"],
    ["Nespithe", "Demilich", 1993, "Technical Death Metal"],
    ["Anomalies", "Necrophagist", 2004, "Technical Death Metal"],
    ["Epitaph", "Necrophagist", 1999, "Technical Death Metal"],
    ["Calculating Infinity", "The Dillinger Escape Plan", 1999, "Mathcore"],
    ["Miss Machine", "The Dillinger Escape Plan", 2004, "Mathcore"],
    ["Ire Works", "The Dillinger Escape Plan", 2007, "Mathcore"],
    ["Option Paralysis", "The Dillinger Escape Plan", 2010, "Mathcore"],
    ["One of Us Is the Killer", "The Dillinger Escape Plan", 2013, "Mathcore"],
    ["Dissociation", "The Dillinger Escape Plan", 2016, "Mathcore"],
    ["Watched by the Dead", "Trap Them", 2011, "Metalcore"],
    ["Darker Handcraft", "Trap Them", 2011, "Metalcore"],
    ["Blissfucker", "Trap Them", 2014, "Metalcore"],
    ["Jane Doe", "Converge", 2001, "Metalcore"],
    ["You Fail Me", "Converge", 2004, "Metalcore"],
    ["No Heroes", "Converge", 2006, "Metalcore"],
    ["Axe to Fall", "Converge", 2009, "Metalcore"],
    ["All We Love We Leave Behind", "Converge", 2012, "Metalcore"],
    ["The Dusk in Us", "Converge", 2017, "Metalcore"],
    ["Petitioning the Empty Sky", "Cave In", 1998, "Metalcore"],
    ["Until Your Heart Stops", "Cave In", 2000, "Metalcore"],
    ["Reinventing Axl Rose", "Against Me!", 2002, "Punk"],
    ["Searching for a Former Clarity", "Against Me!", 2005, "Punk"],
    ["New Wave", "Against Me!", 2007, "Punk"],
    ["White Crosses", "Against Me!", 2010, "Punk"],
    ["Transgender Dysphoria Blues", "Against Me!", 2014, "Punk"],
    ["Bad Brains", "Bad Brains", 1982, "Hardcore Punk"],
    ["Rock for Light", "Bad Brains", 1983, "Hardcore Punk"],
    ["I Against I", "Bad Brains", 1986, "Hardcore Punk"],
    ["Suffer", "Bad Religion", 1988, "Hardcore Punk"],
    ["No Control", "Bad Religion", 1989, "Hardcore Punk"],
    ["Against the Grain", "Bad Religion", 1990, "Hardcore Punk"],
    ["Generator", "Bad Religion", 1992, "Hardcore Punk"],
    ["Recipe for Hate", "Bad Religion", 1993, "Hardcore Punk"],
    ["Stranger Than Fiction", "Bad Religion", 1994, "Hardcore Punk"],
    ["The Gray Race", "Bad Religion", 1996, "Hardcore Punk"],
    ["Live at the Roxy", "Bad Religion", 1984, "Hardcore Punk"],
    ["How Could Hell Be Any Worse?", "Bad Religion", 1982, "Hardcore Punk"],
    ["Into the Unknown", "Bad Religion", 1983, "Hardcore Punk"],
    ["Damaged", "Black Flag", 1981, "Hardcore Punk"],
    ["My War", "Black Flag", 1984, "Hardcore Punk"],
    ["Slip It In", "Black Flag", 1984, "Hardcore Punk"],
    ["Loose Nut", "Black Flag", 1985, "Hardcore Punk"],
    ["In My Head", "Black Flag", 1985, "Hardcore Punk"],
    ["Everything Went Black", "Black Flag", 1983, "Hardcore Punk"],
    ["The First Four Years", "Black Flag", 1983, "Hardcore Punk"],
    ["Nervous Breakdown", "Black Flag", 1979, "Hardcore Punk"],
    ["Six Pack", "Black Flag", 1981, "Hardcore Punk"],
    ["Dez Cadena", "Black Flag", 1983, "Hardcore Punk"],
    ["Live '84", "Black Flag", 1984, "Hardcore Punk"],
    ["Who's Got the 10 1/2?", "Black Flag", 1986, "Hardcore Punk"],
    ["Wasted Again", "Black Flag", 1987, "Hardcore Punk"],
    ["Minor Threat", "Minor Threat", 1981, "Hardcore Punk"],
    ["Out of Step", "Minor Threat", 1983, "Hardcore Punk"],
    ["Complete Discography", "Minor Threat", 1989, "Hardcore Punk"],
    ["Misfits", "Misfits", 1982, "Horror Punk"],
    ["Walk Among Us", "Misfits", 1982, "Horror Punk"],
    ["Earth A.D./Wolfs Blood", "Misfits", 1983, "Horror Punk"],
    ["Static Age", "Misfits", 1996, "Horror Punk"],
    ["Famous Monsters", "Misfits", 1999, "Horror Punk"],
    ["American Psycho", "Misfits", 1997, "Horror Punk"],
    ["Friction", "Misfits", 1999, "Horror Punk"],
    ["Project 1950", "Misfits", 2003, "Horror Punk"],
    ["The Devil's Rain", "Misfits", 2011, "Horror Punk"],
    ["Descendents", "Descendents", 1986, "Hardcore Punk"],
    ["Milo Goes to College", "Descendents", 1982, "Hardcore Punk"],
    ["Enjoy!", "Descendents", 1986, "Hardcore Punk"],
    ["All", "Descendents", 1987, "Hardcore Punk"],
    ["I Don't Want to Grow Up", "Descendents", 1985, "Hardcore Punk"],
    ["Liveage!", "Descendents", 1987, "Hardcore Punk"],
    ["Two Things at Once", "Descendents", 1988, "Hardcore Punk"],
    ["Everything Sucks", "Descendents", 1996, "Hardcore Punk"],
    ["Cool to Be You", "Descendents", 2004, "Hardcore Punk"],
    ["Hypercaffium Spazzinate", "Descendents", 2016, "Hardcore Punk"],
    ["9th and Walnut", "Descendents", 2021, "Hardcore Punk"],
    ["Victim in Pain", "Agnostic Front", 1984, "Hardcore Punk"],
    ["Cause for Alarm", "Agnostic Front", 1986, "Hardcore Punk"],
    ["Liberty and Justice For...", "Agnostic Front", 1987, "Hardcore Punk"],
    ["Live at CBGB 1989", "Agnostic Front", 1989, "Hardcore Punk"],
    ["One Voice", "Agnostic Front", 1992, "Hardcore Punk"],
    ["Break Down the Walls", "Youth of Today", 1986, "Hardcore Punk"],
    ["We're Not in This Alone", "Youth of Today", 1988, "Hardcore Punk"],
    ["Infectious Grooves", "Infectious Grooves", 1991, "Funk Metal"],
    ["Sarsippius' Ark", "Infectious Grooves", 1993, "Funk Metal"],
    ["Groove Family Cyco", "Infectious Grooves", 1994, "Funk Metal"],
    ["Mas Borracho", "Infectious Grooves", 2000, "Funk Metal"],
    ["Vulgar Display of Power", "Pantera", 1992, "Groove Metal"],
    ["Far Beyond Driven", "Pantera", 1994, "Groove Metal"],
    ["The Great Southern Trendkill", "Pantera", 1996, "Groove Metal"],
    ["Cowboys from Hell", "Pantera", 1990, "Groove Metal"],
    ["Power Metal", "Pantera", 1988, "Groove Metal"],
    ["Projects in the Jungle", "Pantera", 1984, "Groove Metal"],
    ["I Am the Night", "Pantera", 1985, "Groove Metal"],
    ["Metal Magic", "Pantera", 1983, "Groove Metal"],
    ["Reinventing the Steel", "Pantera", 2000, "Groove Metal"],
    ["Sepultura", "Sepultura", 1987, "Groove Metal"],
    ["Schizophrenia", "Sepultura", 1987, "Groove Metal"],
    ["Beneath the Remains", "Sepultura", 1989, "Groove Metal"],
    ["Arise", "Sepultura", 1991, "Groove Metal"],
    ["Chaos A.D.", "Sepultura", 1993, "Groove Metal"],
    ["Roots", "Sepultura", 1996, "Groove Metal"],
    ["In the Eyes of Death", "Massacre", 1992, "Death Metal"],
    ["From Beyond", "Massacre", 1991, "Death Metal"],
    ["Back from Beyond", "Massacre", 2014, "Death Metal"],
    ["Killing Is My Business... and Business Is Good!", "Megadeth", 1985, "Thrash Metal"],
    ["The World Needs a Hero", "Megadeth", 2001, "Thrash Metal"],
    ["The Right to Go Insane", "Overkill", 2010, "Thrash Metal"],
    ["Ironbound", "Overkill", 2010, "Thrash Metal"],
    ["White Devil Armory", "Overkill", 2014, "Thrash Metal"],
    ["The Grinding Wheel", "Overkill", 2017, "Thrash Metal"],
    ["The Wings of War", "Overkill", 2019, "Thrash Metal"],
    ["Scorched", "Cannibal Corpse", 2023, "Death Metal"],
    ["Chaos Horrific", "Cannibal Corpse", 2023, "Death Metal"],
    ["Bleed for Ancient Gods", "Incantation", 1995, "Death Metal"],
    ["Diabolical Conquest", "Incantation", 1998, "Death Metal"],
    ["Blasphemy", "Incantation", 2002, "Death Metal"],
    ["Primordial Domination", "Incantation", 2006, "Death Metal"],
    ["Vanquish in Vengeance", "Incantation", 2012, "Death Metal"],
    ["Profane Nexus", "Incantation", 2017, "Death Metal"],
    ["Sect of Vile Divinities", "Incantation", 2020, "Death Metal"],
    ["The 25th Hour", "Terror", 2015, "Hardcore Punk"],
    ["Total Retaliation", "Terror", 2018, "Hardcore Punk"],
    ["No Spiritual Surrender", "Terror", 2019, "Hardcore Punk"],
]

# ── Date algorithm — must match JS exactly ────────────────────────────────────
def date_hash(s):
    h = 5381
    for c in s:
        h = ((h << 5) + h + ord(c)) & 0xFFFFFFFF
    h = (((h ^ (h >> 16)) & 0xFFFFFFFF) * 0x45d9f3b) & 0xFFFFFFFF
    h = (((h ^ (h >> 16)) & 0xFFFFFFFF) * 0x45d9f3b) & 0xFFFFFFFF
    return (h ^ (h >> 16)) & 0xFFFFFFFF

def seeded_shuffle(length, seed):
    a = list(range(length))
    s = seed
    for i in range(length - 1, 0, -1):
        s = (((s ^ (s >> 16)) & 0xFFFFFFFF) * 0x45d9f3b) & 0xFFFFFFFF
        s = (((s ^ (s >> 16)) & 0xFFFFFFFF) * 0x45d9f3b) & 0xFFFFFFFF
        s = (s ^ (s >> 16)) & 0xFFFFFFFF
        j = s % (i + 1)
        a[i], a[j] = a[j], a[i]
    return a

def get_album_for_date(d):
    year = d.year
    order = seeded_shuffle(len(ALBUMS), date_hash(str(year)))
    start = date(year, 1, 1)
    day = (d - start).days
    pos = day % len(order)
    if day > 0:
        prev_pos = (day - 1) % len(order)
        if ALBUMS[order[pos]][1] == ALBUMS[order[prev_pos]][1]:
            pos = (pos + 1) % len(order)
    return ALBUMS[order[pos]]

# ── Spotify helpers ───────────────────────────────────────────────────────────
def get_access_token():
    auth = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
    res = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
    }, headers={'Authorization': f'Basic {auth}', 'Content-Type': 'application/x-www-form-urlencoded'})
    return res.json()['access_token']

def search_album(token, album, artist):
    q = f'album:{album} artist:{artist}'
    res = requests.get('https://api.spotify.com/v1/search', params={
        'q': q, 'type': 'album', 'limit': 5
    }, headers={'Authorization': f'Bearer {token}'})
    items = res.json().get('albums', {}).get('items', [])
    for item in items:
        if artist.lower() in item['artists'][0]['name'].lower():
            return item['uri']
    return None

def get_album_tracks(token, album_uri):
    album_id = album_uri.split(':')[-1]
    res = requests.get(f'https://api.spotify.com/v1/albums/{album_id}/tracks',
        params={'limit': 50},
        headers={'Authorization': f'Bearer {token}'})
    return [t['uri'] for t in res.json().get('items', [])]

def get_playlist_tracks(token):
    res = requests.get(f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks',
        params={'fields': 'items(track(uri,album(uri)))', 'limit': 100},
        headers={'Authorization': f'Bearer {token}'})
    return res.json().get('items', [])

def replace_playlist(token, track_uris):
    # Clear and replace all tracks
    requests.put(f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks',
        json={'uris': track_uris[:100]},
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    today = date.today()
    days = [today - timedelta(days=i) for i in range(3)]  # today, yesterday, 2 days ago
    albums = [get_album_for_date(d) for d in days]

    print(f'Target albums:')
    for i, (d, alb) in enumerate(zip(days, albums)):
        print(f'  {d}: {alb[0]} — {alb[1]}')

    token = get_access_token()
    all_tracks = []

    for alb in albums:
        album_name, artist = alb[0], alb[1]
        uri = search_album(token, album_name, artist)
        if uri:
            tracks = get_album_tracks(token, uri)
            all_tracks.extend(tracks)
            print(f'  ✓ Found: {album_name} ({len(tracks)} tracks)')
        else:
            print(f'  ✗ Not found on Spotify: {album_name} — {artist}')

    if all_tracks:
        replace_playlist(token, all_tracks)
        print(f'\n✅ Playlist updated with {len(all_tracks)} tracks across {len([a for a in albums])} albums.')
    else:
        print('\n⚠️  No tracks found — playlist not updated.')

if __name__ == '__main__':
    main()
