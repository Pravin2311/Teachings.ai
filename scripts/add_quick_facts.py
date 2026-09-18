#!/usr/bin/env python3
"""One-time content-expansion pass for thin-content pages flagged by audit_adsense.py.

Inserts a self-contained "Quick Facts" info block (intro + fun facts + vocabulary)
right before the '<!-- Footer -->' marker shared by this batch of pages. Idempotent:
skips a file if it already contains the marker class 'quick-facts-box'.
"""
import re

CONTENT = {
    "Grammar.html": (
        "📝 Quick Grammar Guide",
        "Grammar is the set of simple rules that helps us put words together so sentences make sense. Learning a little grammar early helps kids speak and write more clearly.",
        [
            "A sentence needs a naming word (noun) and an action word (verb) to make sense.",
            "Nouns name people, places, or things — like \"dog\", \"school\", or \"apple\".",
            "Verbs are action words, like \"run\", \"jump\", or \"eat\".",
            "Adjectives describe nouns, like a \"big\" dog or a \"red\" apple.",
            "Every sentence should start with a capital letter and end with a punctuation mark.",
        ],
        ["noun", "verb", "adjective", "sentence"],
    ),
    "animals.html": (
        "🐶 Quick Facts: Animals",
        "Animals come in every shape and size, from tiny insects to giant elephants. Scratch to reveal each animal, hear its name, and learn where it lives!",
        [
            "Animals that live on farms, like cows and chickens, are called farm animals.",
            "Animals that live in the wild, like lions and elephants, are called wild animals.",
            "Baby animals often have special names, like \"cub\" for a lion or \"calf\" for a cow.",
            "Many animals make different sounds — roaring, mooing, or chirping — that help them communicate.",
            "Learning where an animal lives, called its habitat, helps kids understand how it survives.",
        ],
        ["animal", "habitat", "wild", "farm"],
    ),
    "animals-birds-sorting.html": (
        "🐾 Animals vs. Birds: What's the Difference?",
        "This sorting game helps kids tell animals and birds apart by their features. Birds have feathers, wings, and beaks — most other animals don't!",
        [
            "Birds are the only animals with feathers.",
            "Most birds can fly, but not all — like penguins and ostriches.",
            "Birds lay eggs, and so do many other animals like reptiles and fish.",
            "Mammals like dogs and cats have fur and feed their babies milk.",
            "Sorting by features is an early science skill called classification.",
        ],
        ["feathers", "wings", "beak", "classify"],
    ),
    "birds.html": (
        "🕊️ Quick Facts: Birds",
        "Birds are feathered animals found almost everywhere on Earth, from tiny hummingbirds to tall ostriches. Scratch to reveal each bird's name and sound!",
        [
            "Birds are the only animals in the world that have feathers.",
            "A baby bird hatches from an egg after its parents keep it warm.",
            "Some birds, like parrots, can copy sounds and even human words.",
            "Birds use their beaks differently — eagles tear meat, while hummingbirds sip nectar.",
            "Many birds migrate, flying thousands of miles to find food or warmer weather.",
        ],
        ["feather", "beak", "nest", "migrate"],
    ),
    "bodyparts.html": (
        "💪 Quick Facts: Body Parts",
        "Learning body parts helps kids describe how they feel and follow simple instructions like \"touch your nose.\" Scratch to reveal each part and hear its name!",
        [
            "Your body has over 200 bones that give it shape and support.",
            "Your heart beats about 100,000 times every single day.",
            "Your eyes can see millions of different colors.",
            "Your skin is your body's largest organ — it protects everything inside!",
            "Washing your hands often helps keep germs away and keeps you healthy.",
        ],
        ["body", "bones", "skin", "senses"],
    ),
    "colors.html": (
        "🌈 Quick Facts: Colors",
        "Colors are all around us, and learning their names helps kids describe the world and build early vocabulary. Scratch to reveal each color!",
        [
            "Red, blue, and yellow are called primary colors — you can't mix them from other colors.",
            "Mixing blue and yellow makes green.",
            "Mixing red and blue makes purple.",
            "Rainbows always show colors in the same order: red, orange, yellow, green, blue, indigo, violet.",
            "Different cultures sometimes connect colors to different feelings, like green for calm or red for excitement.",
        ],
        ["primary color", "mix", "shade", "rainbow"],
    ),
    "colours-sorting.html": (
        "🎨 Quick Facts: Color Sorting",
        "Sorting by color is one of the first math skills kids learn — it teaches grouping, comparing, and categorizing before counting even begins.",
        [
            "Sorting means putting things into groups that share something in common.",
            "Color sorting builds the same brain skills used later in math and science.",
            "You can sort the same objects more than one way — by color, size, or shape.",
            "Toddlers usually start sorting by color before they can sort by more than one feature at once.",
            "Practicing with real toys or laundry at home reinforces what kids learn in the game.",
        ],
        ["sort", "group", "match", "category"],
    ),
    "counting.html": (
        "🔢 Quick Facts: Counting",
        "Counting objects one by one teaches kids that each number stands for exactly one item — a key idea called one-to-one correspondence.",
        [
            "Touching each object as you count it helps kids avoid skipping or double-counting.",
            "Most children can count to 10 reliably by around age 4.",
            "Counting backward is a harder skill that usually comes a bit later.",
            "Real-life counting — stairs, snacks, toys — builds the same skill as the game.",
            "Recognizing a number written down (like \"5\") is a separate skill from counting aloud.",
        ],
        ["count", "number", "quantity", "one-to-one"],
    ),
    "countries.html": (
        "🏳️ Quick Facts: Countries",
        "There are 195 countries in the world today, each with its own flag, culture, and capital city. This game introduces kids to some of the most well-known ones.",
        [
            "The world has seven continents, and each one is home to many countries.",
            "Every country has its own flag, made of colors and symbols that mean something special.",
            "Russia is the largest country in the world by land area.",
            "Vatican City is the smallest country in the world.",
            "Learning about countries helps kids understand that people around the world live differently but share many of the same needs.",
        ],
        ["country", "continent", "capital", "flag"],
    ),
    "electronic-gadgets.html": (
        "💡 Quick Facts: Electronic Gadgets",
        "From phones to TVs, electronic gadgets are part of everyday life. This activity helps kids name common devices and understand what each one is used for.",
        [
            "A gadget is a small device made to do a useful job.",
            "Many gadgets need electricity or batteries to work.",
            "The first computers were as big as a whole room — today's phones are far more powerful.",
            "Talking about how gadgets work builds early curiosity about science and engineering.",
            "It's healthy to balance screen time with plenty of hands-on play.",
        ],
        ["gadget", "device", "battery", "technology"],
    ),
    "fantasy-world.html": (
        "👽 Quick Facts: Fantasy World",
        "Fantasy creatures like dragons and unicorns spark imagination and storytelling. Pretend play with fantasy characters helps kids build creativity and language skills.",
        [
            "Imaginative play helps children practice problem-solving in a safe, make-believe setting.",
            "Many fantasy creatures, like dragons, appear in stories from cultures all around the world.",
            "Pretend play boosts vocabulary because kids invent names, places, and situations.",
            "Storytelling with fantasy characters helps kids understand story structure — a beginning, middle, and end.",
            "Mixing fantasy play with real facts (like animal features) helps kids compare real and pretend.",
        ],
        ["imagination", "pretend", "creature", "story"],
    ),
    "flags-of-the-countries.html": (
        "🚩 Quick Facts: Flags of the World",
        "Every country has a flag with its own colors, shapes, and symbols. Flags help kids recognize countries and spark curiosity about geography.",
        [
            "Flag colors and symbols usually stand for something important in a country's history.",
            "Some flags share similar colors because of shared history or nearby location.",
            "Nepal's flag is the only national flag that isn't rectangle-shaped.",
            "The study of flags is called vermexillology.",
            "Recognizing flags is a fun way to start learning geography and world cultures.",
        ],
        ["flag", "symbol", "nation", "geography"],
    ),
    "fruits-vegetables-sorting.html": (
        "🥑 Quick Facts: Fruits vs. Vegetables",
        "Sorting fruits and vegetables teaches kids an important science skill: grouping foods by their features, like whether they grow from a flower (fruit) or a plant's other parts (vegetable).",
        [
            "A fruit grows from the flower of a plant and usually holds seeds.",
            "Vegetables can be roots (carrots), stems (celery), or leaves (spinach).",
            "Tomatoes and cucumbers are technically fruits, even though we treat them like vegetables in cooking!",
            "Eating a mix of fruits and vegetables gives kids important vitamins for growing strong.",
            "Sorting foods is a great way to talk about healthy eating habits with kids.",
        ],
        ["fruit", "vegetable", "seed", "sort"],
    ),
    "fruits.html": (
        "🍎 Quick Facts: Fruits",
        "Fruits come in many colors, shapes, and flavors. Scratch to reveal each fruit and learn its name while building early vocabulary.",
        [
            "A fruit grows from the flower of a plant and contains its seeds.",
            "Bananas are berries, but strawberries are not — botanically speaking!",
            "Apples float in water because they are about 25% air.",
            "Most fruits are naturally sweet and full of vitamins that help kids grow.",
            "Trying a new fruit is a fun way to practice describing taste, color, and shape.",
        ],
        ["fruit", "seed", "ripe", "vitamin"],
    ),
    "games.html": (
        "🎮 Quick Facts: Our Learning Games",
        "This hub gathers all of Teachings.ai's interactive games in one place — scratch-to-reveal subjects, drag-and-drop matching, and sorting activities for ages 3-7.",
        [
            "Playful, hands-on games help young children remember new words better than flashcards alone.",
            "Scratch-to-reveal games build anticipation and fine motor control as kids uncover each picture.",
            "Drag-and-drop matching games strengthen memory and hand-eye coordination.",
            "Sorting games teach categorization — a key early-math and early-science skill.",
            "All games on this page are free to play, with no download or sign-up required.",
        ],
        ["interactive", "match", "sort", "scratch-to-reveal"],
    ),
    "match-animals.html": (
        "🦁 Quick Facts: Matching Games",
        "Matching games ask kids to connect a picture with its correct name — a simple activity that builds memory, vocabulary, and attention span.",
        [
            "Matching games strengthen working memory, the skill used to hold information in mind briefly.",
            "Connecting a picture to a word helps kids build reading readiness before they can read.",
            "Getting an answer wrong and trying again teaches persistence in a low-pressure way.",
            "Talking about each animal's sound or habitat after matching extends the learning.",
            "Short, repeatable games like this fit well into a few minutes of daily practice.",
        ],
        ["match", "memory", "recognize", "vocabulary"],
    ),
    "match-numbers.html": (
        "🔢 Quick Facts: Number Matching",
        "This game asks kids to match numerals to the right quantity or word — an important step in connecting number symbols to real amounts.",
        [
            "Matching a numeral (like \"5\") to a group of 5 objects builds number sense.",
            "Number sense is the foundation for all later math, including addition and subtraction.",
            "Repetition helps numerals become instantly recognizable, just like letters do for reading.",
            "Kids usually recognize numbers by sight before they can write them accurately.",
            "Counting on fingers while matching reinforces the connection between numbers and quantities.",
        ],
        ["numeral", "quantity", "match", "number sense"],
    ),
    "match-shapes.html": (
        "🟦 Quick Facts: Shape Matching",
        "Matching shapes to their names helps kids recognize geometry all around them, from a square window to a triangular slice of pizza.",
        [
            "Shapes are defined by their number of sides and corners.",
            "A triangle has 3 sides, a square has 4 equal sides, and a circle has none.",
            "Recognizing shapes helps kids later understand letters, numbers, and even map reading.",
            "Pointing out shapes in everyday objects (a clock, a book, a plate) reinforces the game.",
            "Shape matching also builds visual discrimination — noticing small differences between similar images.",
        ],
        ["shape", "side", "corner", "match"],
    ),
    "match-words.html": (
        "🧩 Quick Facts: Word Matching",
        "Matching pictures to written words is an early-reading skill that helps kids connect objects with the letters that spell them.",
        [
            "Matching a picture to its word builds \"sight word\" recognition, used in early reading.",
            "Saying the word aloud while matching links the sound of a word to its spelling.",
            "Short, familiar words are easiest for beginning readers to match and remember.",
            "This kind of activity is a stepping stone toward independent reading.",
            "Repeating the same words in different games helps them stick in long-term memory.",
        ],
        ["match", "sight word", "spelling", "recognize"],
    ),
    "math.html": (
        "➕ Quick Facts: Simple Math",
        "This activity introduces addition and subtraction with small numbers — the building blocks kids need before tackling bigger math problems.",
        [
            "Addition means combining two groups to find a total.",
            "Subtraction means taking away from a group to find what's left.",
            "Using fingers, blocks, or drawings to count is a normal and helpful strategy for young learners.",
            "Kids usually master adding and subtracting numbers up to 10 before moving to bigger numbers.",
            "Everyday moments — splitting snacks or counting toys — are great real-life math practice.",
        ],
        ["addition", "subtraction", "total", "equation"],
    ),
    "nature-explorer.html": (
        "🌳 Quick Facts: Nature Explorer",
        "Nature is full of things to discover — trees, bugs, weather, and more. This activity builds curiosity about the outdoor world.",
        [
            "Spending time in nature helps children notice small details, like leaf shapes or insect legs.",
            "Trees produce the oxygen we breathe and provide homes for countless animals.",
            "Weather changes — like rain or wind — happen because of the sun heating the Earth unevenly.",
            "Observing nature closely is the same skill scientists use, called observation.",
            "Asking \"why\" questions during nature walks builds early scientific thinking.",
        ],
        ["nature", "observe", "habitat", "weather"],
    ),
    "numbers-alphabets-sorting.html": (
        "🔣 Quick Facts: Numbers & Letters Sorting",
        "This game asks kids to sort numbers and letters into separate groups — an early skill in telling apart different kinds of symbols.",
        [
            "Letters represent sounds, while numbers represent quantities — two very different jobs for symbols.",
            "Recognizing the difference between letters and numbers is a milestone before formal reading and math begin.",
            "Some symbols, like \"O\" and \"0\", can look alike and take extra practice to tell apart.",
            "Sorting symbols by type builds visual discrimination, a skill used throughout school.",
            "This activity blends two subjects — literacy and math — in one quick game.",
        ],
        ["symbol", "letter", "number", "sort"],
    ),
    "numbers.html": (
        "🔢 Quick Facts: Numbers",
        "Learning numbers 1-20 gives kids the foundation for counting, comparing, and eventually doing math. Scratch to reveal each number!",
        [
            "Most children learn to count to 10 before they can count to 20 in order.",
            "Recognizing a written number (like \"7\") is different from being able to count that high aloud.",
            "Numbers appear everywhere in daily life — on clocks, phones, houses, and calendars.",
            "Practicing numbers with real objects, not just pictures, strengthens understanding.",
            "Zero is a special number — it means \"none\" and took mathematicians centuries to fully understand!",
        ],
        ["number", "count", "digit", "order"],
    ),
    "odd-even-sorting.html": (
        "🧮 Quick Facts: Odd & Even Sorting",
        "Sorting numbers into odd and even groups helps kids notice patterns in numbers — an early step toward number sense and multiplication later on.",
        [
            "An even number can be split into two equal groups with nothing left over.",
            "An odd number always leaves one item left over when split into two groups.",
            "Even numbers always end in 0, 2, 4, 6, or 8.",
            "Odd numbers always end in 1, 3, 5, 7, or 9.",
            "Spotting number patterns like this builds a foundation for later math concepts.",
        ],
        ["odd", "even", "pattern", "group"],
    ),
    "odd-even.html": (
        "➗ Quick Facts: Odd & Even Numbers",
        "This activity helps kids tell odd numbers from even numbers by looking at the last digit — a handy shortcut once they learn it.",
        [
            "A number is even if it can be split evenly into two equal groups.",
            "A number is odd if one is left over when split into two groups.",
            "You can tell odd from even just by looking at the last digit of a number.",
            "Even and odd numbers always alternate when you count: 1 (odd), 2 (even), 3 (odd)...",
            "Understanding odd and even is useful later for skip counting and multiplication.",
        ],
        ["odd", "even", "digit", "split"],
    ),
    "organs.html": (
        "🫁 Quick Facts: Body Organs",
        "Organs are the parts inside your body that keep you alive and healthy, like your heart, lungs, and brain. This activity introduces kids to what's happening inside!",
        [
            "Your heart pumps blood all around your body, carrying oxygen to every part.",
            "Your lungs bring fresh air in and push used air back out when you breathe.",
            "Your brain controls everything you think, feel, and do.",
            "Your stomach helps break down food so your body can use its energy.",
            "Taking care of your body with healthy food, rest, and exercise keeps your organs strong.",
        ],
        ["organ", "heart", "lungs", "brain"],
    ),
    "patterns.html": (
        "🪄 Quick Facts: Patterns",
        "Patterns repeat in a predictable way, like red-blue-red-blue. Recognizing patterns is an early math skill that also helps with reading and problem-solving.",
        [
            "A pattern is something that repeats in a predictable order.",
            "Patterns can be made with colors, shapes, sounds, or even numbers.",
            "Finding what comes next in a pattern is called \"predicting.\"",
            "Patterns show up everywhere — in music, clothing, nature, and even days of the week.",
            "Pattern recognition is one of the earliest building blocks of algebra.",
        ],
        ["pattern", "repeat", "predict", "sequence"],
    ),
    "phonic-letter-sound.html": (
        "🔠 Quick Facts: Letter Sounds",
        "Learning the sound each letter makes is the first step toward reading. This is called phonics, and it helps kids sound out new words.",
        [
            "Phonics connects each letter (or group of letters) to the sound it makes.",
            "Some letters, like \"c,\" can make more than one sound depending on the word.",
            "Sounding out a word letter by letter is called \"decoding.\"",
            "Practicing letter sounds daily builds the foundation for reading whole words.",
            "Singing the alphabet is fun, but knowing letter sounds is what unlocks reading.",
        ],
        ["phonics", "sound", "letter", "decode"],
    ),
    "phonics.html": (
        "🔊 Quick Facts: Phonics",
        "Phonics teaches kids how letters and letter combinations connect to sounds, so they can sound out and read new words on their own.",
        [
            "Phonics is one of the most research-backed ways to teach reading.",
            "Blending sounds together (like c-a-t) helps kids read whole words.",
            "Some sounds are made by two letters together, like \"sh\" or \"ch.\"",
            "Reading aloud to kids builds the listening skills that make phonics easier to learn.",
            "Regular short phonics practice works better than long, infrequent sessions.",
        ],
        ["phonics", "blend", "decode", "sound"],
    ),
    "planets.html": (
        "🌎 Quick Facts: Planets",
        "Our solar system has eight planets circling the Sun. This activity introduces kids to space and helps them learn each planet's name.",
        [
            "There are eight planets in our solar system, and Earth is the third from the Sun.",
            "Jupiter is the largest planet — more than 1,300 Earths could fit inside it!",
            "Mercury is the closest planet to the Sun and also the smallest.",
            "Saturn is famous for its wide, beautiful rings made of ice and rock.",
            "A year on a planet is the time it takes to travel once around the Sun.",
        ],
        ["planet", "solar system", "orbit", "Sun"],
    ),
    "plants.html": (
        "🌱 Quick Facts: Plants",
        "Plants grow all around us and are essential to life on Earth. This activity teaches kids about different plants and how they grow.",
        [
            "Plants make their own food using sunlight, water, and air — a process called photosynthesis.",
            "Most plants need soil, water, and sunlight to grow strong.",
            "A seed can grow into a plant if it gets the right conditions.",
            "Plants release oxygen into the air, which people and animals need to breathe.",
            "Watching a seed sprout over a few weeks is a great hands-on science activity for kids.",
        ],
        ["plant", "seed", "sunlight", "grow"],
    ),
    "publicservice.html": (
        "🏛️ Quick Facts: Community Helpers",
        "Community helpers like firefighters, doctors, and police officers keep neighborhoods safe and healthy. This activity introduces kids to these important jobs.",
        [
            "Firefighters put out fires and rescue people and animals in emergencies.",
            "Doctors and nurses help people stay healthy and treat them when they're sick.",
            "Police officers help keep neighborhoods safe and assist people in trouble.",
            "Teachers help kids learn new things every day, just like this website does!",
            "Learning about community helpers builds gratitude and understanding of how neighborhoods work together.",
        ],
        ["community", "helper", "career", "service"],
    ),
    "rhyming.html": (
        "🧠 Quick Facts: Rhyming Words",
        "Rhyming words end with the same sound, like \"cat\" and \"hat.\" Recognizing rhymes builds phonemic awareness — a key early-reading skill.",
        [
            "Two words rhyme when their ending sounds match, even if the spelling is different.",
            "Rhyming helps kids notice the smaller sounds inside words, called phonemes.",
            "Nursery rhymes and silly rhyming songs are a fun, natural way to practice.",
            "Being able to hear rhymes is one of the strongest early predictors of reading success.",
            "Making up silly rhymes together is a great no-materials-needed learning game.",
        ],
        ["rhyme", "sound", "phoneme", "pattern"],
    ),
    "scientists.html": (
        "🔬 Quick Facts: Scientists",
        "Scientists ask questions and run experiments to learn how the world works. This activity introduces kids to famous scientists and what they discovered.",
        [
            "A scientist is someone who asks questions and tests ideas through observation and experiments.",
            "Marie Curie was a scientist who discovered new elements and won two Nobel Prizes.",
            "Albert Einstein developed ideas that changed how we understand space and time.",
            "Kids can act like scientists too — by asking \"why\" and testing their ideas!",
            "Every scientific discovery starts with curiosity and careful observation.",
        ],
        ["scientist", "experiment", "discover", "observe"],
    ),
    "sentences.html": (
        "📝 Quick Facts: Building Sentences",
        "A sentence is a group of words that expresses a complete thought. This activity helps kids practice putting words in the right order.",
        [
            "Every complete sentence needs a subject (who or what) and a verb (an action).",
            "Sentences start with a capital letter and end with a punctuation mark like a period.",
            "Reading sentences aloud helps kids notice if the words sound right together.",
            "Short, simple sentences are the easiest for beginning readers and writers to build.",
            "Practicing sentence order helps kids later write their own stories.",
        ],
        ["sentence", "subject", "verb", "punctuation"],
    ),
    "shapes.html": (
        "🟦 Quick Facts: Shapes",
        "Shapes are everywhere — from windows to wheels. This activity helps kids recognize and name common shapes like circles, squares, and triangles.",
        [
            "A circle has no corners or straight sides.",
            "A triangle has 3 sides and 3 corners.",
            "A square has 4 equal sides and 4 corners.",
            "Shapes with straight sides are called polygons.",
            "Spotting shapes in everyday objects — like a clock or a book — reinforces what kids learn here.",
        ],
        ["shape", "side", "corner", "circle"],
    ),
    "sight.html": (
        "👀 Quick Facts: Sight Words",
        "Sight words are common words — like \"the,\" \"and,\" and \"is\" — that kids learn to recognize instantly, without sounding them out.",
        [
            "Sight words make up a large share of the words in beginning reading books.",
            "Some sight words don't follow normal phonics rules, so kids memorize them by sight.",
            "Recognizing sight words instantly helps reading feel smoother and faster.",
            "Flashcards and repeated exposure are common ways to practice sight words.",
            "Mastering a core set of sight words is a major milestone in early reading.",
        ],
        ["sight word", "recognize", "reading", "memorize"],
    ),
    "vegetables.html": (
        "🥕 Quick Facts: Vegetables",
        "Vegetables come from many parts of a plant — roots, stems, and leaves. This activity helps kids name vegetables and learn where they come from.",
        [
            "Carrots are roots, celery is a stem, and spinach is a leaf — all different plant parts!",
            "Vegetables are packed with vitamins that help kids grow strong and healthy.",
            "Some foods we call vegetables, like tomatoes and peppers, are technically fruits.",
            "Growing a vegetable from a seed is a fun way to see how plants develop.",
            "Trying new vegetables helps kids build a wider range of tastes and textures they enjoy.",
        ],
        ["vegetable", "root", "stem", "leaf"],
    ),
    "vehicles.html": (
        "🚗 Quick Facts: Vehicles",
        "Vehicles help people and goods move from place to place — by road, rail, air, or water. This activity introduces kids to common types of vehicles.",
        [
            "Cars, buses, and trucks travel on roads and are called land vehicles.",
            "Airplanes and helicopters travel through the air.",
            "Boats and ships travel on water.",
            "Trains run on tracks and can carry many people or goods at once.",
            "Talking about how each vehicle moves builds early understanding of transportation and engineering.",
        ],
        ["vehicle", "transportation", "engine", "travel"],
    ),
    "word-matching.html": (
        "🔤 Quick Facts: Word Matching",
        "This activity asks kids to match words to their meanings or pictures, reinforcing vocabulary and early reading skills.",
        [
            "Matching a word to its meaning helps kids build reading comprehension, not just word recognition.",
            "Repetition across different games helps new vocabulary stick in long-term memory.",
            "Saying each word aloud while matching links its sound to its spelling.",
            "Vocabulary size in early childhood is closely linked to later reading success.",
            "Short, focused practice sessions work better for young learners than long ones.",
        ],
        ["vocabulary", "match", "meaning", "comprehension"],
    ),
}

BOX_TEMPLATE = """
<!-- Quick Facts Info Block (auto-added: thin-content remediation) -->
<section class="quick-facts-box" style="max-width:640px;margin:28px auto;padding:22px 24px;background:#f4f8ff;border-left:5px solid #4a90d9;border-radius:12px;text-align:left;font-size:1em;color:#333;line-height:1.6;box-shadow:0 4px 8px rgba(0,0,0,0.05);">
  <h2 style="margin:0 0 10px;font-size:1.25em;color:#1B2A5B;">{title}</h2>
  <p style="margin:0 0 12px;">{intro}</p>
  <p style="margin:0 0 6px;font-weight:700;color:#1B2A5B;">Fun Facts:</p>
  <ul style="margin:0 0 14px;padding-left:22px;">
{facts}
  </ul>
  <p style="margin:0;"><strong>New words to learn:</strong> {vocab}</p>
</section>
"""


def build_box(entry):
    title, intro, facts, vocab = entry
    facts_html = "\n".join(f"    <li>{f}</li>" for f in facts)
    return BOX_TEMPLATE.format(title=title, intro=intro, facts=facts_html, vocab=", ".join(vocab))


def main():
    changed = []
    skipped = []
    missing = []
    for fname, entry in CONTENT.items():
        try:
            html = open(fname, encoding="utf-8").read()
        except FileNotFoundError:
            missing.append(fname)
            continue
        if "quick-facts-box" in html:
            skipped.append(fname)
            continue
        if "<!-- Footer -->" not in html:
            missing.append(fname + " (no footer marker)")
            continue
        box = build_box(entry)
        new_html = html.replace("<!-- Footer -->", box + "\n<!-- Footer -->", 1)
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_html)
        changed.append(fname)

    print(f"Changed: {len(changed)}")
    for f in changed:
        print("  ", f)
    print(f"Skipped (already has box): {len(skipped)}")
    for f in skipped:
        print("  ", f)
    print(f"Missing/problem: {len(missing)}")
    for f in missing:
        print("  ", f)


if __name__ == "__main__":
    main()
