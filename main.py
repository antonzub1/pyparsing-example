from pyparsing import (
    alphanums, Combine, DelimitedList, Group, Literal, nums,
    oneOf, OneOrMore, Optional, Suppress, Word
)

url_chars = alphanums + "-_.~%+"
fragment = Combine(Suppress("#") + Word(url_chars))("fragment")
scheme = oneOf("http https ftp file")("scheme")
host = Combine(DelimitedList(Word(url_chars), "."))("host")
port = Suppress(":") + Word(nums)("port")
user_info = Word(url_chars)("username") + Suppress(":") + Word(url_chars)("password") + Suppress("@")
query_pair = Group(Word(url_chars) + Suppress("=") + Word(url_chars))
query = Group(Suppress("?")) + DelimitedList(query_pair, "&")("query")
path = Combine(Suppress("/") + OneOrMore(~query + Word(url_chars + "/")))("path")
url_parser = (
    scheme
    + Suppress("://")
    + Optional(user_info)
    + host
    + Optional(port)
    + Optional(path)
    + Optional(query)
    + Optional(fragment)
)


def main():
    test_urls = [
        'http://www.notarealsite.com',
        'http://www.notarealsite.com/',
        'http://www.notarealsite.com:1234/',
        'http://bob:%243cr3t@www.notarealsite.com:1234/',
        'http://www.notarealsite.com/presidents',
        'http://www.notarealsite.com/presidents/byterm?term=26&name=Roosevelt',
        'http://www.notarealsite.com/presidents/26',
        'http://www.notarealsite.com/us/indiana/gary/population',
        'ftp://ftp.info.com/downloads',
        'http://www.notarealsite.com#moose',
        'http://bob:s3cr3t@www.notarealsite.com:8080/presidents/byterm?term=26&name=Roosevelt#bio',
    ]

    fmt = '{0:10s} {1}'

    for test_url in test_urls:
        print("URL:", test_url)

        tokens = url_parser.parseString(test_url)

        print(tokens, '\n')
        print(fmt.format("Scheme:", tokens.scheme))
        print(fmt.format("User name:", tokens.username))
        print(fmt.format("Password:", tokens.password))
        print(fmt.format("Host:", tokens.host))
        print(fmt.format("Port:", tokens.port))
        print(fmt.format("Path:", tokens.path))
        print("Query:")
        for key, value in tokens.query:
            print("\t{} ==> {}".format(key, value))
            print(fmt.format('Fragment:', tokens.fragment))
            print('-' * 60, '\n')


if __name__ == "__main__":
    main()
