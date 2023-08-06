def clean_list(l):
    c = []
    for k in l:
        try:
            cleaned_str = (
                f"{k}".replace(",", "")
                .replace('"', "'")
                .replace('\n', '')
                .replace('\r', '')
                .replace('\t', '')
                .replace("\\", "")
            )
            cleaned_str.encode('utf-8')  # Try encoding the cleaned string
            c.append(cleaned_str)
        except UnicodeEncodeError:
            # Handle the case where encoding fails
            c.append("UNABLE_TO_ENCODE")
    return c
