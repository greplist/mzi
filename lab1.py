def caesar(string, key, alphabet):
    return ''.join([chr((ord(c) - ord('a') + key) % alphabet + ord('a')) for c in string])


if __name__ == '__main__':
    s = 'abz'
    i = caesar(s, 27, 26)
    o = caesar(i, -27, 26)
    print(s, i, o)
