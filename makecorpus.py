from trackdata import Source, Snapshot

source = Source(token="13c92330f143c002fcae55ced845162251632a42",
                sha="ce94abb8ab1dfefbfc0baaad8dccaa197d821355",
                repo="https://github.com/corynezin/data.git")

snapshot = Snapshot(token="13c92330f143c002fcae55ced845162251632a42",
                    branch='makecorpus',
                    repo="https://github.com/corynezin/nextLetter.git")

with snapshot as s:
    with source.writer('output.txt', __file__) as w:
        for file_content in w.get("aclImdb/train/pos/"):
            w.write(file_content)
