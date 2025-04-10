import streamlit as st

st.set_page_config(page_title="Doslovno pretraživanje korpusa", layout="wide")
st.title("🔎 Doslovno pretraživanje korpusa")

st.markdown("""
Unesi niz znakova točno onako kako se pojavljuje u korpusu. Možeš dodavati posebne znakove klikom ispod.
""")

# Specijalni znakovi iz prethodne analize (primjeri)
special_chars = ['ſ', 'ç', 'æ', 'œ']

# Inicijalizacija session_state za upit
if "query" not in st.session_state:
    st.session_state.query = ""

# Dodavanje posebnih znakova klikom
def append_char(c):
    current = st.session_state.get("query", "")
    st.session_state.query = current + c

col1, col2 = st.columns([3, 1])

with col1:
    st.text_area("📝 Unesi izraz za pretraživanje:", key="query", on_change=None)

with col2:
    for char in special_chars:
        if st.button(f"{char}", key=f"spec_{char}"):
            append_char(char)

query = st.session_state.query

if st.button("Pretraži") and query:
    try:
        with open("corpus.txt", "r", encoding="utf-8") as f:
            corpus = f.read()

        import re

        # Tokenizacija prema riječima
        tokens = [(m.group(), m.start(), m.end()) for m in re.finditer(r'\S+', corpus)]
        matches = [(tok, s, e) for tok, s, e in tokens if query in tok]

        def get_kwic(token_span, word_spans, context=3, full_text=""):
            token, start, end = token_span
            idx = next((i for i, (_, s, e) in enumerate(word_spans) if s == start and e == end), None)
            if idx is None:
                return token
            left = " ".join(word_spans[i][0] for i in range(max(0, idx - context), idx))
            right = " ".join(word_spans[i][0] for i in range(idx + 1, min(len(word_spans), idx + 1 + context)))
            page_markers = list(re.finditer(r"/\d+/", full_text))
            page = "?"
            for marker in reversed(page_markers):
                if marker.start() < start:
                    page = marker.group().strip("/")
                    break
            return f"{left} **{token}** {right}  _(str. {page})"

        st.subheader(f"📄 Rezultati (KWIC): Ukupno: {len(matches)}")
        if matches:
            for m in matches:
                st.markdown(get_kwic(m, tokens, full_text=corpus))
        else:
            st.info("Nema rezultata za zadani upit.")

    except Exception as e:
        st.error(f"Greška: {e}")
