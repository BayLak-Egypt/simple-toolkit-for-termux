import secrets
import color

DESCRIPTION = "Lorem Ipsum Placeholder Text Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea",
    "commodo", "consequat", "duis", "aute", "irure", "dolor", "in", "reprehenderit",
    "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla",
    "pariatur", "excepteur", "sint", "occaecat", "cupidatat", "non", "proident",
    "sunt", "in", "culpa", "qui", "officia", "deserunt", "mollit", "anim", "id", "est", "laborum"
]

def generate_lorem_words(count: int = 10) -> str:
    """Generate a random sequence of Lorem Ipsum words."""
    selected = [secrets.choice(LOREM_WORDS) for _ in range(count)]
    text = " ".join(selected)
    return text.capitalize() + "."

def generate_lorem_paragraphs(paragraph_count: int = 2, words_per_paragraph: int = 30) -> list:
    """Generate multiple paragraphs of Lorem Ipsum text."""
    paragraphs = []
    for _ in range(paragraph_count):
        para = generate_lorem_words(words_per_paragraph)
        paragraphs.append(para)
    return paragraphs

def run():
    print(color.color_text("--- Lorem Ipsum Generator ---", COLOR))
    
    try:
        para_count = int(input("How many paragraphs to generate? (default 2): ").strip() or "2")
        if para_count < 1:
            para_count = 1
    except ValueError:
        para_count = 2

    try:
        word_count = int(input("Words per paragraph? (default 25): ").strip() or "25")
        if word_count < 5:
            word_count = 5
    except ValueError:
        word_count = 25

    paragraphs = generate_lorem_paragraphs(para_count, word_count)

    print(color.color_text(f"\n[+] Generated Placeholder Text:\n", color.GREEN))
    for idx, para in enumerate(paragraphs, 1):
        print(f"  [Paragraph {idx}]\n  {para}\n")
