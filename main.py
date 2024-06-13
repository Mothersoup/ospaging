#
import os
from collections import deque


def readfile(filename: str):
    if not os.path.exists(filename):
        filename += '.txt'
    with open(filename, 'r') as file:
        # read algo and page size
        algorithm, pagesize = map(int, file.readline().strip().split())
        data = file.readline().strip()
        pageorder = list(map(int, data))
        return algorithm, pagesize, pageorder


class PageReplacementAlgorithm:
    def __init__(self, page_size: int, filename: str):
        self.page_size = page_size
        self.pages = []
        self.replace = 0
        self.page_faults = 0
        if not os.path.exists(filename):
            self.filename = filename + ".txt"
        else:
            self.filename = filename
        self.file = None

        # page input 的型別是int

    def access_page(self, page: int):
        raise NotImplementedError

    # -> int means return integer
    def replace_page(self) -> int:
        raise NotImplementedError

    def show_page_fragment(self):
        for i in self.pages[::-1]:
            self.file.write(str(i))

    def open_file(self, mode: str):
        self.file = open("out_" + self.filename, mode)


# return algo type, pageSize, pageorder


class FIFOPageReplacement(PageReplacementAlgorithm):
    # 裡面page_size 是整數型別 : int 宣告
    def __init__(self, page_size: int, filename: str):
        # 用 super 呼叫富類建構子建構一個屬於FIFO 的 page fragment
        super().__init__(page_size, filename)

    def access_page(self, page: int):
        self.file.write(str(page) + "\t")
        haselement = True
        # 沒有的話要輸出 page fault 同時更新page fault 次數
        if page not in self.pages:
            haselement = False
            self.page_faults += 1
            if len(self.pages) >= self.page_size:
                self.replace_page()
            self.pages.append(page)
        self.show_page_fragment()
        if not haselement:
            self.file.write("\tF\n")
        else:
            self.file.write("\n")

    # 回傳被刪除的元素
    def replace_page(self) -> int:
        # FIFO：移除最先進入的頁面
        # 又左邊是最先進入的元素所以左邊先出去
        self.replace += 1
        if len(self.pages) > 0:
            oldest_page = self.pages.pop(0)
            # 刪除元素
            return oldest_page

    def simulation(self, data: list):
        self.file.writelines("--------------FIFO-----------------------\n")
        for e in data:
            self.access_page(e)
        self.file.write("Page Fault = " + str(self.page_faults) + "  Page Replaces = " + str(self.replace) + "  Page "
                                                                                                             "Frames "
                                                                                                             "= " +
                        str(self.page_size) + "\n")


class LRUPageReplaceMent(PageReplacementAlgorithm):
    def __init__(self, page_size: int, filename: str):
        # 用 super 呼叫富類建構子建構一個屬於FIFO 的 page fragment
        super().__init__(page_size, filename)

    def access_page(self, page: int):
        self.file.write(str(page) + "\t")
        haselement = True
        # 沒有的話要輸出 page fault 同時更新page fault 次數
        if page not in self.pages:
            haselement = False
            if len(self.pages) >= self.page_size:
                self.replace_page()
            self.pages.append(page)
        else:
            # 有成功paging 的話要更新歷史
            indexOfPaging = self.pages.index(page)
            temp = self.pages.pop(indexOfPaging)
            self.pages.append(temp)
        self.show_page_fragment()
        if not haselement:
            self.page_faults += 1
            self.file.write("\tF\n")
        else:
            self.file.write("\n")

    # 回傳被刪除的元素
    def replace_page(self) -> int:
        # LRU：移除歷史最久的沒被使用的
        # 又左邊是最先進入的元素所以左邊先出去
        self.replace += 1
        if len(self.pages) > 0:
            oldest_page = self.pages.pop(0)
            # 刪除元素
            return oldest_page

    def simulation(self, data: list):
        self.file.writelines("--------------LRU-----------------------\n")
        for e in data:
            self.access_page(e)
        self.file.write("Page Fault = " + str(self.page_faults) + "  Page Replaces = " + str(self.replace) + "  Page "
                                                                                                             "Frames "
                                                                                                             "= " +
                        str(self.page_size) + "\n")


class LFU(PageReplacementAlgorithm):
    def __init__(self, page_size: int, filename: str):
        # 用 super 呼叫富類建構子建構一個屬於FIFO 的 page fragment
        super().__init__(page_size, filename)
        # 用地圖去紀錄對應的page 使用次數
        self.map = {}

    def access_page(self, page: int):
        self.file.write(str(page) + "\t")
        haselement = True
        # 沒有的話要輸出 page fault 同時更新page fault 次數
        if page not in self.pages:
            haselement = False
            if len(self.pages) >= self.page_size:
                self.replace_page()
            self.pages.append(page)
            self.map[page] = 1
            # add to map or updating map
        else:
            self.map[page] += 1
            # map section
        self.show_page_fragment()
        if not haselement:
            self.page_faults += 1
            self.file.write("\tF\n")
        else:
            self.file.write("\n")

    def replace_page(self) -> int:
        self.replace += 1
        if len(self.pages) > 0:
            # inf means infinity
            filtered_map = {key: self.map[key] if key in self.map else float('inf') for key in self.pages}
            min_value = min(filtered_map.values())
            min_keys = [key for key, value in filtered_map.items() if value == min_value]
            # 刪除元素
            for element in self.pages:
                if element in min_keys:
                    self.pages.remove(element)
                    return 0
        # debug section
        print("error ")
        return -1

    def simulation(self, data: list):
        self.file.writelines("--------------Least Frequently Used Page Replacement-----------------------\n")
        for e in data:
            self.access_page(e)
        self.file.write("Page Fault = " + str(self.page_faults) + "  Page Replaces = " + str(self.replace) + "  Page "
                                                                                                             "Frames "
                                                                                                             "= " +
                        str(self.page_size) + "\n")


class MFU(LFU):
    def __init__(self, page_size: int, filename: str):
        super().__init__(page_size, filename)

    # 回傳被刪除的元素
    def replace_page(self) -> int:
        # MFU：移除使用最少的
        self.replace += 1
        if len(self.pages) > 0:
            # inf means infinity
            filtered_map = {key: self.map[key] if key in self.map else float('-inf') for key in self.pages}
            max_value = max(filtered_map.values())
            max_keys = [key for key, value in filtered_map.items() if value == max_value]
            # 刪除元素
            for element in self.pages:
                if element in max_keys:
                    self.pages.remove(element)
                    return 0
        # debug section
        print("error ")
        return -1

    def access_page(self, page: int):
        self.file.write(str(page) + "\t")
        haselement = True
        # 沒有的話要輸出 page fault 同時更新page fault 次數
        if page not in self.pages:
            haselement = False
            if len(self.pages) >= self.page_size:
                self.replace_page()
            self.pages.append(page)
            self.map[page] = 1
            # add to map or updating map
        else:
            self.map[page] += 1
            # map section

        self.show_page_fragment()
        if not haselement:
            self.page_faults += 1
            self.file.write("\tF\n")
        else:
            self.file.write("\n")

    def simulation(self, data: list):
        self.file.writelines("--------------Most Frequently Used Page Replacement -----------------------\n")
        for e in data:
            self.access_page(e)
        self.file.write("Page Fault = " + str(self.page_faults) + "  Page Replaces = " + str(self.replace) + "  Page "
                                                                                                             "Frames "
                                                                                                             "= " +
                        str(self.page_size) + "\n")


class LFUAndLRU(LFU):
    def __init__(self, page_size: int, filename: str):
        super().__init__(page_size, filename)

    def replace_page(self) -> int:
        # LFU：移除使用最少的 並 LRU paging 沒有出問題時要調換順序
        self.replace += 1
        if len(self.pages) > 0:
            # inf means infinity
            filtered_map = {key: self.map[key] if key in self.map else float('inf') for key in self.pages}
            min_value = min(filtered_map.values())
            min_keys = [key for key, value in filtered_map.items() if value == min_value]
            # 刪除元素
            for element in self.pages:
                if element in min_keys:
                    self.pages.remove(element)
                    return 0
        # debug section
        print("error ")
        return -1

    def access_page(self, page: int):
        self.file.write(str(page) + "\t")
        haselement = True
        # 沒有的話要輸出 page fault 同時更新page fault 次數
        if page not in self.pages:
            haselement = False
            if len(self.pages) >= self.page_size:
                self.replace_page()
            self.pages.append(page)
            self.map[page] = 1
            # add to map or updating map
        else:
            self.map[page] += 1
            indexOfPaging = self.pages.index(page)
            temp = self.pages.pop(indexOfPaging)
            self.pages.append(temp)
            # map section

        self.show_page_fragment()
        if not haselement:
            self.page_faults += 1
            self.file.write("\tF\n")
        else:
            self.file.write("\n")

    def simulation(self, data: list):
        self.file.writelines("--------------Least Frequently Used LRU Page Replacement-----------------------\n")
        for e in data:
            self.access_page(e)
        self.file.write("Page Fault = " + str(self.page_faults) + "  Page Replaces = " + str(self.replace) + "  Page "
                                                                                                             "Frames "
                                                                                                             "= " +
                        str(self.page_size) + "\n")


if __name__ == '__main__':
    # command first input
    fileName = input("Please enter FileName (eg. input1, input1.txt): \t")
    while fileName != "0":
        print("os paging replacement")
        algorithm, pagesize, pageorder = readfile(fileName)
        # FIFO
        if algorithm == 1:
            algo = FIFOPageReplacement(pagesize, fileName)
            algo.open_file("w")
            algo.simulation(pageorder)

        elif algorithm == 2:
            algo = LRUPageReplaceMent(pagesize, fileName)
            algo.open_file("w")
            algo.simulation(pageorder)
        elif algorithm == 3:
            algo = LFU(pagesize, fileName)
            algo.open_file("w")
            algo.simulation(pageorder)
        elif algorithm == 4:
            algo = MFU(pagesize, fileName)
            algo.open_file("w")
            algo.simulation(pageorder)
        elif algorithm == 5:
            algo = LFUAndLRU(pagesize, fileName)
            algo.open_file("w")
            algo.simulation(pageorder)
        elif algorithm == 6:
            algos = [
                FIFOPageReplacement(pagesize, fileName),
                LRUPageReplaceMent(pagesize, fileName),
                LFU(pagesize, fileName),
                MFU(pagesize, fileName),
                LFUAndLRU(pagesize, fileName)
            ]
            # 第一次要蓋檔
            for index, algo in enumerate(algos):
                algo.open_file("w" if index == 0 else "a")
                algo.simulation(pageorder)
                if index != len(algos) - 1:
                    algo.file.write("\n")
                algo.file.close()
        fileName = input("Please enter FileName (eg. input1, input1.txt): \t")