def extract_errors(file_stream):
    errors = []

    for line in file_stream:
        decoded_line = line.decode("utf-8")
        if "error" in decoded_line.lower():
            errors.append(decoded_line.strip())

    return errors