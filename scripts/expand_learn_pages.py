#!/usr/bin/env python3
"""Second-pass content expansion for the /learn/ tree, flagged as thin-content by
audit_adsense.py. Adds 2 more facts + vocabulary + a short activity to each leaf
page (animal/bird/body-part/letter), and an intro/FAQ blurb to each hub/index page.
Idempotent: skips a file if it already contains the 'quick-facts-extra' marker class.
"""
import re

LEAF_CONTENT = {
    "learn/animals/cat.html": (
        ["A group of cats is called a \"clouder.\"", "Cats sleep for up to 16 hours a day — more than almost any other pet!"],
        ["paw", "purr", "whiskers", "feline"],
        "Try meowing like a cat and see if a real cat (or a friend) meows back!",
    ),
    "learn/animals/dog.html": (
        ["A dog's sense of smell is up to 100,000 times stronger than a human's.", "A dog wagging its tail usually means it's happy and excited."],
        ["bark", "paw", "leash", "breed"],
        "Practice teaching a pretend trick, like \"sit\" or \"shake,\" to a stuffed animal dog!",
    ),
    "learn/animals/horse.html": (
        ["Horses can sleep standing up because their legs can lock in place.", "A baby horse is called a foal."],
        ["gallop", "mane", "foal", "hooves"],
        "Gallop around the room like a horse and count how many big steps you take!",
    ),
    "learn/animals/lion.html": (
        ["A lion's roar can be heard from up to 5 miles away.", "Female lions do most of the hunting for their pride."],
        ["roar", "mane", "pride", "hunt"],
        "Practice your best (and friendliest) lion roar!",
    ),
    "learn/animals/monkey.html": (
        ["Monkeys use their tails to help balance while climbing trees.", "Many monkeys live together in a group called a troop."],
        ["swing", "troop", "tail", "climb"],
        "Pretend to swing from tree to tree, just like a monkey!",
    ),
    "learn/animals/zebra.html": (
        ["Every zebra's stripe pattern is unique, just like a human fingerprint.", "Zebras live together in herds for safety from predators."],
        ["stripes", "herd", "predator", "mane"],
        "Draw your own zebra and give it a one-of-a-kind stripe pattern!",
    ),
    "learn/birds/duck.html": (
        ["Duck feathers are waterproof, which helps them stay dry while swimming.", "Ducks often fly long distances together in a V-shaped flock."],
        ["waddle", "webbed feet", "pond", "flock"],
        "Practice waddling like a duck across the room!",
    ),
    "learn/birds/eagle.html": (
        ["Eagles have incredible eyesight — about 4 times sharper than a human's.", "Eagles build huge nests, sometimes several feet wide, high in trees or cliffs."],
        ["talons", "soar", "nest", "prey"],
        "Stretch your arms out wide like an eagle's wings and pretend to soar!",
    ),
    "learn/birds/flamingo.html": (
        ["Flamingos are pink because of the shrimp and algae they eat.", "Flamingos often stand on one leg to help keep warm."],
        ["wading", "flock", "beak", "pink"],
        "See how long you can stand on one leg, just like a flamingo!",
    ),
    "learn/birds/hen.html": (
        ["A hen can lay about one egg almost every day.", "Hens cluck to talk to their chicks."],
        ["cluck", "coop", "chick", "lay"],
        "Practice your best hen cluck and count how many pretend eggs you can collect!",
    ),
    "learn/birds/hummingbird.html": (
        ["Hummingbirds can flap their wings up to 80 times every second.", "They are the only birds that can fly backwards."],
        ["hover", "nectar", "flutter", "tiny"],
        "Flutter your arms as fast as you can — can you keep it up like a hummingbird?",
    ),
    "learn/birds/owl.html": (
        ["Owls can turn their heads almost all the way around — about 270 degrees!", "Most owls are nocturnal, meaning they're awake at night and sleep during the day."],
        ["nocturnal", "hoot", "talons", "silent"],
        "Practice a soft owl \"hoot\" and slowly turn your head like an owl looking around.",
    ),
    "learn/birds/parrot.html": (
        ["Some parrots can live for over 50 years.", "Parrots are very social birds and often live in flocks in the wild."],
        ["mimic", "flock", "beak", "colorful"],
        "Try repeating a silly word back and forth, just like a parrot copying sounds!",
    ),
    "learn/birds/peacock.html": (
        ["Only male peacocks grow the giant, colorful tail feathers used to attract mates.", "A peacock's tail can have over 200 feathers."],
        ["feathers", "display", "male", "colorful"],
        "Spread your arms out wide like a peacock showing off its beautiful tail!",
    ),
    "learn/birds/pigeon.html": (
        ["Pigeons are excellent navigators and have even been trained to deliver messages.", "They can recognize themselves in a mirror — a rare skill among animals."],
        ["coo", "flock", "navigate", "wings"],
        "Practice a soft pigeon \"coo\" sound and see who can copy it best!",
    ),
    "learn/birds/sparrow.html": (
        ["Sparrows are one of the most common birds found in cities and towns.", "They often build nests in small, hidden spots like rooftops or bushes."],
        ["chirp", "nest", "flock", "perch"],
        "Listen outside for a sparrow's chirp — how many can you count?",
    ),
    "learn/body-parts/arms.html": (
        ["Your arm bends at the elbow, letting you fold it in half.", "Arm muscles get stronger the more you use them, like when you play and lift things."],
        ["elbow", "muscle", "reach", "hug"],
        "Do 5 gentle arm stretches and count out loud as you go!",
    ),
    "learn/body-parts/ears.html": (
        ["Your ears help you balance, not just hear!", "The smallest bones in your whole body are found inside your ear."],
        ["hearing", "sound", "balance", "listen"],
        "Close your eyes and try to guess a sound just by listening carefully.",
    ),
    "learn/body-parts/eyes.html": (
        ["Your eyes blink about 15-20 times every minute without you even noticing.", "The colored part of your eye is called the iris, and everyone's is a little different."],
        ["blink", "iris", "see", "vision"],
        "Try a staring contest with a friend — who blinks first?",
    ),
    "learn/body-parts/feet.html": (
        ["Each foot has 26 bones — more than a quarter of all the bones in your body!", "Your feet help you balance, walk, run, and jump."],
        ["toes", "balance", "heel", "sole"],
        "Try hopping on one foot and then the other — which is easier for you?",
    ),
    "learn/body-parts/hands.html": (
        ["Each hand has 27 bones, which is why your fingers can bend and move so easily.", "Your fingerprints are completely unique — no one else has the same pattern."],
        ["fingers", "grip", "fingerprint", "palm"],
        "Press your hand onto paper and look closely at your own fingerprint pattern.",
    ),
    "learn/body-parts/head.html": (
        ["Your skull protects your brain, the control center for your whole body.", "Your head holds your eyes, ears, nose, and mouth — most of your senses!"],
        ["skull", "brain", "senses", "protect"],
        "Nod your head yes and shake it no — notice how many muscles that takes!",
    ),
    "learn/body-parts/legs.html": (
        ["Your legs have some of the strongest muscles and bones in your whole body.", "Legs help you walk, run, jump, and kick."],
        ["muscle", "knee", "kick", "strong"],
        "See how high you can jump using just your leg muscles!",
    ),
    "learn/body-parts/mouth.html": (
        ["Your mouth helps you eat, talk, sing, and smile.", "Adults have 32 teeth, but kids start out with about 20 smaller baby teeth."],
        ["teeth", "tongue", "smile", "chew"],
        "Practice saying a silly tongue twister as fast as you can!",
    ),
    "learn/body-parts/nose.html": (
        ["Your nose can recognize thousands of different smells.", "Breathing through your nose helps warm and clean the air before it reaches your lungs."],
        ["sniff", "smell", "breathe", "nostrils"],
        "Close your eyes and try to guess a smell, like an orange or a flower.",
    ),
    "learn/body-parts/stomach.html": (
        ["Your stomach uses special juices to help break down the food you eat.", "It takes a few hours for your stomach to fully digest a meal."],
        ["digest", "tummy", "energy", "hungry"],
        "Talk about your favorite healthy snack that gives your stomach energy to play.",
    ),
    "learn/alphabets/letter-c.html": (
        ["The letter C can sound soft, like in \"city,\" or hard, like in \"cat.\"", "C is used in some of the most common words in English."],
        [],
        "Can you find 3 things in your room that start with the letter C?",
    ),
    "learn/alphabets/letter-d.html": (
        ["D comes right after C and before E in the alphabet.", "The letter D always makes a strong \"duh\" sound at the start of a word."],
        [],
        "Try drawing a dog, a duck, or a dinosaur — they all start with D!",
    ),
    "learn/alphabets/letter-e.html": (
        ["E is a vowel, which means it can be a whole word by itself, like \"eye\"!", "E is one of the most commonly used letters in the English language."],
        [],
        "Can you think of an animal whose name starts with E?",
    ),
    "learn/alphabets/letter-l.html": (
        ["L comes right after K and before M in the alphabet.", "To make the L sound, your tongue touches the top of your mouth."],
        [],
        "Try saying \"Lions like lemons\" three times fast!",
    ),
    "learn/alphabets/letter-m.html": (
        ["M is made by pressing your lips together and humming — try it!", "Many yummy foods start with M, like milk and mango."],
        [],
        "Can you name 3 foods that start with the letter M?",
    ),
    "learn/alphabets/letter-n.html": (
        ["N comes right after M and before O in the alphabet.", "The letter N makes a soft, nasal sound when you say it."],
        [],
        "Try naming an animal that starts with N, like \"newt\" or \"narwhal\"!",
    ),
    "learn/alphabets/letter-o.html": (
        ["O is a vowel, and your mouth makes a round shape to say it.", "O can sound different in words like \"dog\" and \"go.\""],
        [],
        "Can you spot 3 round things in your room, just like the letter O?",
    ),
    "learn/alphabets/letter-r.html": (
        ["R can be a tricky sound for young learners to practice saying clearly.", "R comes right after Q and before S in the alphabet."],
        [],
        "Try saying \"Red rabbits run really fast\" three times!",
    ),
    "learn/alphabets/letter-s.html": (
        ["S makes a hissing sound, just like a snake — sssss!", "S is one of the most common letters to start English words."],
        [],
        "Can you hiss like a snake while making the S sound?",
    ),
    "learn/alphabets/letter-v.html": (
        ["V is one of the less common letters to start English words.", "To say V, your top teeth gently touch your bottom lip."],
        [],
        "Can you think of an animal that starts with V, like \"vulture\"?",
    ),
    "learn/alphabets/letter-w.html": (
        ["W is sometimes called \"double u\" because of how it's shaped.", "W comes right after V and before X in the alphabet."],
        [],
        "Try naming things that start with W, like water or watermelon!",
    ),
    "learn/alphabets/letter-x.html": (
        ["X is one of the rarest letters to start a word in English.", "Many words use X in the middle or at the end instead, like \"fox\" or \"box.\""],
        [],
        "Can you think of a word that ends in X, like \"box\" or \"fox\"?",
    ),
    "learn/alphabets/letter-y.html": (
        ["Y can act like a vowel in words such as \"my\" and \"happy.\"", "Y comes right after X and before Z in the alphabet."],
        [],
        "Can you think of a food that starts with Y, like a yellow \"yam\"?",
    ),
    "learn/alphabets/letter-z.html": (
        ["Z is the very last letter of the English alphabet!", "Z makes a buzzing sound, just like a bee — zzzzz!"],
        [],
        "Try buzzing like a bee while making the Z sound!",
    ),
}

LEAF_BLOCK = """
<!-- Quick Facts Extra Block (auto-added: thin-content remediation) -->
<div class="quick-facts-extra" style="max-width:640px;margin:24px 0;padding:18px 20px;background:#f4f8ff;border-left:5px solid #4a90d9;border-radius:12px;text-align:left;font-size:1em;color:#333;line-height:1.6;">
  <h2 style="margin:0 0 8px;font-size:1.15em;color:#1B2A5B;">More to Discover</h2>
  <ul style="margin:0 0 12px;padding-left:22px;">
{facts}
  </ul>{vocab}
  <p style="margin:0;"><strong>Try This:</strong> {activity}</p>
</div>
"""


def build_leaf_block(entry):
    facts, vocab, activity = entry
    facts_html = "\n".join(f"    <li>{f}</li>" for f in facts)
    vocab_html = ""
    if vocab:
        vocab_html = f'\n  <p style="margin:0 0 10px;"><strong>New words to learn:</strong> {", ".join(vocab)}</p>'
    return LEAF_BLOCK.format(facts=facts_html, vocab=vocab_html, activity=activity)


HUB_TYPE_B = {
    "learn/alphabets/index.html": (
        "About This Alphabet Hub",
        "Every letter has its own page here, with words that start with it, tracing tips, and fun facts to explore. Learning letter names and sounds is the foundation kids need before they can read whole words.",
        [
            ("What order should kids learn letters in?", "There's no single right order — many families start with the letters in a child's own name, since those feel personal and motivating."),
            ("How long does it take to learn the alphabet?", "Most kids recognize all 26 letters by name between ages 4 and 5, though sounds usually take a bit longer to master."),
        ],
    ),
    "learn/animals/index.html": (
        "About This Animal Hub",
        "Each animal page here includes where it lives, what it eats, and fun facts kids love to share. Learning about animals builds early science vocabulary and curiosity about the natural world.",
        [
            ("Why do kids love learning about animals?", "Animals are colorful, make interesting sounds, and connect to stories and pretend play kids already enjoy, which makes new vocabulary stick."),
            ("What's a good way to extend animal learning at home?", "Visit a zoo, watch a nature documentary together, or ask your child to act out how their favorite animal moves and sounds."),
        ],
    ),
    "learn/birds/index.html": (
        "About This Bird Hub",
        "Each bird page here covers habitat, diet, and fun facts about how that bird lives and sounds. Birds are a great introduction to biology because kids can spot many of them right outside their window.",
        [
            ("Why are birds a good first science topic for kids?", "Birds are easy to observe in real life, which turns learning into a hands-on activity kids can practice on a walk or from a window."),
            ("What skill does birdwatching build?", "Careful observation — noticing color, size, and sound — is the same skill scientists use, and it's a great early habit to build."),
        ],
    ),
    "learn/body-parts/index.html": (
        "About This Body Parts Hub",
        "Each page here explains what a body part does and shares fun, age-appropriate facts. Learning body part names helps kids describe how they feel and follow simple instructions.",
        [
            ("Why is learning body parts important for young kids?", "It helps children communicate needs clearly, like pointing to where something hurts, and builds early body awareness."),
            ("What's a fun way to practice at home?", "Play a simple game like \"Simon Says\" using body part names — touch your nose, wiggle your toes, and so on."),
        ],
    ),
}

HUB_B_BLOCK = """
<!-- Quick Facts Hub Block (auto-added: thin-content remediation) -->
<div class="quick-facts-extra" style="max-width:900px;margin:24px auto;padding:20px 24px;background:#f4f8ff;border-radius:14px;text-align:left;font-size:1em;color:#333;line-height:1.6;">
  <h2 style="margin:0 0 8px;font-size:1.2em;color:#1B2A5B;">{title}</h2>
  <p style="margin:0 0 14px;">{intro}</p>
{faqs}
</div>
"""

FAQ_ITEM = """  <p style="margin:0 0 6px;font-weight:700;color:#1B2A5B;">{q}</p>
  <p style="margin:0 0 12px;">{a}</p>
"""


def build_hub_b_block(entry):
    title, intro, faqs = entry
    faqs_html = "".join(FAQ_ITEM.format(q=q, a=a) for q, a in faqs)
    return HUB_B_BLOCK.format(title=title, intro=intro, faqs=faqs_html)


HUB_TYPE_A_EXTRA = {
    "learn/numbers/index.html": (
        " Recognizing a number by sight (like \"7\") and counting that high out loud are two separate skills, and both take practice. "
        "At home, look for numbers on clocks, mailboxes, and calendars to make counting part of everyday life. "
        "Zero is a special number too — it means \"none,\" and understanding it is an important early milestone."
    ),
    "learn/scientists/index.html": (
        " Many of these scientists started out as curious kids who asked lots of questions, just like your child does every day. "
        "You don't need a lab to think like a scientist — noticing, asking \"why,\" and testing an idea is enough to get started. "
        "Reading about a new scientist together is also a great way to talk about persistence, since most discoveries took many tries to get right."
    ),
}


def process_leaf(fname, entry):
    html = open(fname, encoding="utf-8").read()
    if "quick-facts-extra" in html:
        return "skip"
    if html.count('<div class="footer">') != 1:
        return "anchor-missing"
    block = build_leaf_block(entry)
    new_html = html.replace('<div class="footer">', block + '\n    <div class="footer">', 1)
    with open(fname, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_html)
    return "changed"


def process_hub_b(fname, entry):
    html = open(fname, encoding="utf-8").read()
    if "quick-facts-extra" in html:
        return "skip"
    if html.count('<div class="footer">') != 1:
        return "anchor-missing"
    block = build_hub_b_block(entry)
    new_html = html.replace('<div class="footer">', block + '\n    <div class="footer">', 1)
    with open(fname, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_html)
    return "changed"


def process_hub_a(fname, extra_text):
    html = open(fname, encoding="utf-8").read()
    if "quick-facts-extra-marker" in html:
        return "skip"
    marker = '<article class="t-seo">'
    if html.count(marker) != 1:
        return "anchor-missing"
    # insert extra_text right before the closing </p></article>
    old = None
    # find the article block and its closing tag
    idx = html.find(marker)
    close_idx = html.find("</article>", idx)
    if close_idx == -1:
        return "anchor-missing"
    insertion_point = html.rfind("</p>", idx, close_idx)
    if insertion_point == -1:
        return "anchor-missing"
    new_html = (
        html[:insertion_point]
        + f'<span class="quick-facts-extra-marker"></span>{extra_text}'
        + html[insertion_point:]
    )
    with open(fname, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_html)
    return "changed"


def main():
    results = {"changed": [], "skip": [], "anchor-missing": []}

    for fname, entry in LEAF_CONTENT.items():
        r = process_leaf(fname, entry)
        results[r].append(fname)

    for fname, entry in HUB_TYPE_B.items():
        r = process_hub_b(fname, entry)
        results[r].append(fname)

    for fname, extra in HUB_TYPE_A_EXTRA.items():
        r = process_hub_a(fname, extra)
        results[r].append(fname)

    for status, files in results.items():
        print(f"{status}: {len(files)}")
        for f in files:
            print("  ", f)


if __name__ == "__main__":
    main()
