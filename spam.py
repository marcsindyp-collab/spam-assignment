import re
import sys

def load_keywords():
    return [
        "free","winner","won","congratulations","act now","limited time","click here","urgent",
        "offer expires","risk free","no cost","guaranteed","buy now","cheap","discount","earn money",
        "make money","investment","refund","credit card","account update","verify your account",
        "password","lottery","prize","cash bonus","claim now","exclusive deal","medical","private loan"
    ]

def _make_pattern(keyword):
    esc = re.escape(keyword)
    if " " in keyword:
        esc = esc.replace(r"\ ", r"\s+")
        return re.compile(r"(?i)" + esc)
    else:
        return re.compile(r"(?i)\b" + esc + r"\b")

def compute_spam_score(message, keywords):
    found = {}
    score = 0
    for kw in keywords:
        pat = _make_pattern(kw)
        matches = pat.findall(message)
        if matches:
            found[kw] = len(matches)
            score += len(matches)
    return score, found

def classify_score(score):
    if score == 0:
        return "Very unlikely — no spam words detected."
    elif score <= 2:
        return "Unlikely — a few suspicious words."
    elif score <= 5:
        return "Possibly spam — multiple suspicious words."
    elif score <= 10:
        return "Likely spam — many indicators found."
    else:
        return "Almost certainly spam — very high score."

def main():
    keywords = load_keywords()
    print("Paste or type the email message. End with Ctrl+D (Linux/macOS) or Ctrl+Z then Enter (Windows):")
    try:
        message = sys.stdin.read()
    except KeyboardInterrupt:
        return

    score, found = compute_spam_score(message, keywords)
    print("\n--- Spam Analysis Result ---")
    print(f"Spam score: {score}")
    print(f"Likelihood: {classify_score(score)}")

    if found:
        print("\nTriggered keywords:")
        for k,v in found.items():
            print(f"  {k}: {v}")
    else:
        print("No keywords matched.")

if __name__ == "__main__":
    main()
