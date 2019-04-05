def convert_list_headers_to_dictionary(headers: list):
    from httpserver.util.parser import parse_header

    headers_dict = {}

    for header in headers:
        (key, value) = parse_header(header)
        headers_dict[key] = value

    return headers_dict
