import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content, scrape_website_with_pages
from parse import parse_with_gemini

st.title("AI Web Scraper")
url = st.text_input("Enter a Website URL: ")

scrape_mode = st.radio("Select scraping mode:", ["Single Page", "Multiple Pages"])



if st.button("Scrape Site"):
    st.write(f"Scraping ({scrape_mode})...")

    all_cleaned_content = []

    if scrape_mode == "Single Page":

        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)
        all_cleaned_content.append(cleaned_content)
    
    elif scrape_mode == "Multiple Pages":
        all_html_pages = scrape_website_with_pages(url, max_pages = 5)

        for page_number, result in enumerate(all_html_pages, start=1):
            st.write(f"Processing page {page_number}")
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            all_cleaned_content.append(cleaned_content)

    combined_cleaned_content = "\n".join(all_cleaned_content)

    st.session_state.dom_content = combined_cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", combined_cleaned_content, height=300)

    print(f"Scraped and processed {'1 page' if scrape_mode == 'Single Page' else f'{len(all_cleaned_content)} pages'}")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_gemini(dom_chunks, parse_description)
            st.write(result)



