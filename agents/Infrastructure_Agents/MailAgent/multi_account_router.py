# multi_account_router.py

from mail_config import MAIL_ACCOUNTS

def resolve_account_key(user_input: str):
    """
    Versucht, das richtige Gmail-Konto aus der Nutzereingabe zu erkennen.
    Wenn unklar, wird Rückfrage erzeugt.
    """

    user_input = user_input.lower()

    if "office" in user_input or "gordonholding" in user_input:
        return "office"
    if "business" in user_input or "barrygordon" in user_input:
        return "business"
    if "privat" in user_input or "gordonmunich" in user_input:
        return "private"

    # Wenn nicht automatisch erkennbar → Rückfrage
    print("❓ Bitte gib an, welches Konto du verwenden möchtest:")
    print("A: office@gordonholding.de")
    print("B: business@barrygordon")
    print("C: gordon.munich@gmail.com")
    answer = input("Deine Wahl (A, B, C oder E-Mail-Adresse): ").strip().lower()

    if answer in ["a", "office"]:
        return "office"
    elif answer in ["b", "business"]:
        return "business"
    elif answer in ["c", "private", "gordonmunich"]:
        return "private"
    elif answer in MAIL_ACCOUNTS:
        return answer
    else:
        print("⚠️ Keine gültige Auswahl erkannt. Abbruch.")
        return None
