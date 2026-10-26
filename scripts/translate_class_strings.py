#!/usr/bin/env python3
import struct
import sys
from pathlib import Path

TRANSLATIONS = {
    "Shop": "Boutique",
    "Do you want to \u00a7fsprint\u00a7r?": "Veux-tu \u00a7fsprinter\u00a7r ?",
    "Do you want to \u00a7ffly\u00a7r?": "Veux-tu \u00a7fvoler\u00a7r ?",
    "Perform a \u00a7fjump\u00a7r?": "Effectuer un \u00a7fsaut\u00a7r ?",
    "Get \u00a7fexploded\u00a7r?": "Être \u00a7fexplosé\u00a7r ?",
    "Get hit by \u00a7f": "Être frappé par \u00a7f",
    "Get exploded by \u00a7f": "Être explosé par \u00a7f",
    "Interact with \u00a7f": "Interagir avec \u00a7f",
    "Attack \u00a7f": "Attaquer \u00a7f",
    "Use \u00a7f": "Utiliser \u00a7f",
    "Place \u00a7f": "Placer \u00a7f",
    "Craft \u00a7f": "Fabriquer \u00a7f",
    "Throw away \u00a7f": "Jeter \u00a7f",
    "Move \u00a7f": "Déplacer \u00a7f",
    "Stop asking me to jump \u2014 250": "Arrête de me demander de sauter - 250",
    "Stop asking me to attack \u2014 400": "Arrête de me demander d'attaquer - 400",
    "Stop asking me to sprint \u2014 350": "Arrête de me demander de sprinter - 350",
    "Stop asking me to fly \u2014 500": "Arrête de me demander de voler - 500",
    "Sold for ": "Vendu pour ",
    " coins.": " pièces.",
    "You already bought that.": "Tu as déjà acheté cet article.",
    "Purchased: no more jump confirmations!": "Acheté : plus de confirmations pour sauter !",
    "Purchased: no more attack confirmations!": "Acheté : plus de confirmations pour attaquer !",
    "Purchased: no more sprint confirmations!": "Acheté : plus de confirmations pour sprinter !",
    "Purchased: no more fly confirmations!": "Acheté : plus de confirmations pour voler !",
    "Not enough coins.": "Pas assez de pièces.",
    "Use ": "Utiliser ",
    "Get exploded by ": "Être explosé par ",
    "Get ": "Être ",
    "exploded": "explosé",
    "Get hit by ": "Être frappé par ",
    " for ": " pour ",
    " damage?": " dégâts ?",
    "Interact with ": "Interagir avec ",
    "Attack ": "Attaquer ",
    " denied your command.": " a refusé votre commande.",
    "Place ": "Placer ",
    "Craft ": "Fabriquer ",
    "Throw away ": "Jeter ",
    "Move ": "Déplacer ",
    "Replaying the failsafe...": "Relancement du mécanisme de secours...",
    "Failsafe state reset for this world.": "État du mécanisme de secours réinitialisé pour ce monde.",
    "GRACE": "GRÂCE",
    "CINEMATIC": "CINÉMATIQUE",
    "ACTIVE": "ACTIF",
    "[Everything Consent] ": "[Tout Demande Consentement] ",
    "Phase: ": "Phase : ",
    "World age: ": "Âge du monde : ",
    " (game time ": " (temps de jeu ",
    "Grace: ": "Période de grâce : ",
    " until the failsafe)": " avant le mécanisme de secours)",
    "Popups: ": "Fenêtres de confirmation : ",
    "failsafe playing": "mécanisme de secours en cours",
    "not active yet": "pas encore actif",
    "Cinematic seen: ": "Séquence cinématique vue : ",
    "Runaway buttons: ": "Boutons d'échappement : ",
    "off ": "désactivés ",
    " (in ": " (dans ",
    "Tampering detected": "Modification non autorisée détectée",
    "⚠ TAMPERING DETECTED ⚠": "⚠ MODIFICATION NON AUTORISÉE ⚠",
    "Deleting world": "Suppression du monde",
    "Reinitializing...": "Réinitialisation...",
    "Multiple Game files corrupted...": "Plusieurs fichiers du jeu sont corrompus...",
    "Game failsafe activated...": "Mécanisme de secours du jeu activé...",
    "Failsafe loading": "Chargement du mécanisme de secours",
    "Failsafe Loaded": "Mécanisme de secours chargé",
    "Initialized done.": "Initialisation terminée.",
    "Do you want to ": "Veux-tu ",
    "Are you REALLY sure about this?": "Es-tu VRAIMENT sûr de ça ?",
    "Think carefully – this cannot be un-thought.": "Réfléchis bien : impossible de revenir sur cette décision.",
    "Do you accept full responsibility for the outcome?": "Acceptes-tu l'entière responsabilité des conséquences ?",
    "Is this genuinely how you want to spend your time?": "C'est vraiment comme ça que tu veux passer ton temps ?",
    "The consequences, whatever they may be, are yours.": "Quelles qu'elles soient, les conséquences seront les tiennes.",
    "Please confirm. Again. As always. Forever.": "Merci de confirmer. Encore. Comme toujours. Pour toujours.",
    "We simply must be certain. Absolutely certain.": "Nous devons en être sûrs. Absolument sûrs.",
    "This decision is final and possibly legally binding.*": "Cette décision est définitive et peut-être juridiquement contraignante.*",
    "Have you consulted everyone you needed to consult?": "As-tu consulté toutes les personnes nécessaires ?",
    "Just double-checking, because we care. A lot.": "On vérifie juste une dernière fois, parce qu'on tient à toi. Beaucoup.",
    "Confirm Action": "Confirmer l'action",
    "✔ Yes, do it": "✔ Oui, fais-le",
    "✘ No, never mind": "✘ Non, laisse tomber",
    "⚠ HOLD ON!": "⚠ ATTENDS !",
    "Perform a ": "Effectuer un ",
    "Sell": "Vendre",
    "SELL": "VENDRE",
    "SELL for ": "VENDRE pour ",
    "SELL (empty)": "VENDRE (vide)",
    "Buy": "Acheter",
    "Owned: no more jump prompts": "Possédé : plus de demandes de saut",
    "Stop asking me to jump – 250": "Arrête de me demander de sauter - 250",
    "Owned: no more attack prompts": "Possédé : plus de demandes d'attaque",
    "Stop asking me to attack – 400": "Arrête de me demander d'attaquer - 400",
    "Owned: no more sprint prompts": "Possédé : plus de demandes de sprint",
    "Stop asking me to sprint – 350": "Arrête de me demander de sprinter - 350",
    "Owned: no more fly prompts": "Possédé : plus de demandes de vol",
    "Stop asking me to fly – 500": "Arrête de me demander de voler - 500",
    "[Annoyance] Loaded. From now on you must confirm literally everything. You're welcome.": "[Agacement] Chargé. À partir de maintenant, tu dois littéralement tout confirmer. De rien.",
}

def patch_class(data):
    if data[:4] != b"\xca\xfe\xba\xbe":
        return data, 0
    cp_count = struct.unpack_from(">H", data, 8)[0]
    entries = {}
    string_indexes = set()
    pos = 10
    i = 1
    while i < cp_count:
        start = pos
        tag = data[pos]
        pos += 1
        if tag == 1:
            length = struct.unpack_from(">H", data, pos)[0]
            pos += 2 + length
        elif tag in (3, 4):
            pos += 4
        elif tag in (5, 6):
            pos += 8
            entries[i] = (tag, start, pos)
            i += 1
        elif tag in (7, 8, 16, 19, 20):
            index = struct.unpack_from(">H", data, pos)[0]
            pos += 2
            if tag == 8:
                string_indexes.add(index)
        elif tag in (9, 10, 11, 12, 17, 18):
            pos += 4
        elif tag == 15:
            pos += 3
        else:
            raise ValueError(f"Unsupported class constant-pool tag {tag}")
        entries[i] = (tag, start, pos)
        i += 1

    out = bytearray(data[:10])
    changed = 0
    pos = 10
    i = 1
    while i < cp_count:
        tag = data[pos]
        start = pos
        pos += 1
        if tag == 1:
            length = struct.unpack_from(">H", data, pos)[0]
            raw = data[pos + 2:pos + 2 + length]
            pos += 2 + length
            if i in string_indexes:
                try:
                    value = raw.decode("utf-8")
                except UnicodeDecodeError:
                    value = raw.decode("utf-8", errors="replace")
                replacement = TRANSLATIONS.get(value, value)
                encoded = replacement.encode("utf-8")
                if replacement != value:
                    changed += 1
                out.append(tag)
                out.extend(struct.pack(">H", len(encoded)))
                out.extend(encoded)
            else:
                out.extend(data[start:pos])
        elif tag in (3, 4):
            pos += 4
            out.extend(data[start:pos])
        elif tag in (5, 6):
            pos += 8
            out.extend(data[start:pos])
            i += 1
        elif tag in (7, 8, 16, 19, 20):
            pos += 2
            out.extend(data[start:pos])
        elif tag in (9, 10, 11, 12, 17, 18):
            pos += 4
            out.extend(data[start:pos])
        elif tag == 15:
            pos += 3
            out.extend(data[start:pos])
        i += 1
    out.extend(data[pos:])
    return bytes(out), changed

root = Path(sys.argv[1])
total = 0
for path in root.rglob("*.class"):
    patched, count = patch_class(path.read_bytes())
    if count:
        path.write_bytes(patched)
        total += count

print(f"Translated {total} Java string constants.")
if total < 25:
    raise SystemExit(f"Expected to translate at least 25 strings, got {total}.")
