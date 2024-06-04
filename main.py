#
import os


class PageReplacementAlgorithm:
    # page input 的型別是int
    def access_page(self, page: int):
        raise NotImplementedError

    # -> int means return integer
    def replace_page(self) -> int:
        raise NotImplementedError


# return algo type, pageSize, pageorder
def readfile(filename: str):
    if not os.path.exists(filename):
        filename += '.txt'
    with open(filename, 'r') as file:
        # read algo and page size
        algorithm, pagesize = map(int, file.readline().strip().split())
        data = file.readline().strip()
        pageorder = list(map(int, data))
        return algorithm, pagesize, pageorder


if __name__ == '__main__':
    # command first input
    print("os paging replacement")
    print(readfile(input(" Please enter FileName (eg.input1 、input1.txt) :  \t")))
