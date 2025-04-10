import streamlit as st

st.set_page_config(page_title="Doslovno pretraživanje korpusa", layout="wide")
st.title("🔎 Doslovno pretraživanje korpusa")

st.markdown("""
Unesi niz znakova točno onako kako se pojavljuje u korpusu. Možeš dodavati posebne znakove klikom ispod.
""")

# Specijalni znakovi iz prethodne analize (primjeri)
special_chars = ['ſ', 'ç', 'æ', 'œ']

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input("📝 Unesi izraz za pretraživanje:", "")

with col2:
    for char in special_chars:
        if st.button(f"{char}", key=f"spec_{char}"):
            query += char

if st.button("Pretraži") and query:
    try:
        with open("corpus.txt", "r", encoding="utf-8") as f:
            corpus = f.read()

        import re

        # Tokenizacija prema riječima
        tokens = [(m.group(), m.start(), m.end()) for m in re.finditer(r'\S+', corpus)]
        matches = [(tok, s, e) for tok, s, e in tokens if query in tok]

        def get_kwic(token_span, word_spans, context=3):
            token, start, end = token_span
            idx = next((i for i, (_, s, e) in enumerate(word_spans) if s == start and e == end), None)
            if idx is None:
                return token
            left = " ".join(word_spans[i][0] for i in range(max(0, idx - context), idx))
            right = " ".join(word_spans[i][0] for i in range(idx + 1, min(len(word_spans), idx + 1 + context)))
            return f"{left} **{token}** {right}"

        st.subheader(f"📄 Rezultati (KWIC): Ukupno: {len(matches)}")
        if matches:
            for m in matches:
                st.markdown(get_kwic(m, tokens))
        else:
            st.info("Nema rezultata za zadani upit.")

    except Exception as e:
        st.error(f"Greška: {e}")
