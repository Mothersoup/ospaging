import os
import threading
import time
from collections import deque
from datetime import datetime
import multiprocessing
import queue


def readfile(filename: str):
    if not os.path.exists(filename):
        filename += '.txt'

    try:
        with open(filename, 'r') as file:
            # read slice and algo
            slice_c = int(input("請輸入要切成幾份\n"))
            algo_input = input("請輸入方法編號:( 方法1, 方法2, 方法3, 方法4 )\n")
            local_dataset = []
            for line in file:
                # remove any padding
                number = int(line.strip())
                local_dataset.append(number)

            return slice_c, int(algo_input), local_dataset  # 確保返回整數
    except FileNotFoundError:
        print("檔案不存在")
    except ValueError:
        print("檔案內容格式錯誤，請確保檔案中的內容是有效的數字")
    return None, None, None


class basebubblesort(object):

    def __init__(self, filename: str, local_slice: int):
        self.local_slice = local_slice
        if not os.path.exists(filename):
            self.filename = filename + ".txt"
        else:
            self.filename = filename
        self.file = None

    def bubblesort(self, local_dataset: list) -> list:
        for i in range(len(local_dataset) - 1):
            for j in range(len(local_dataset) - 1):
                if local_dataset[j] > local_dataset[j + 1]:
                    local_dataset[j], local_dataset[j + 1] = local_dataset[j + 1], local_dataset[j]
        return local_dataset
    def sorting(self, local_dataset: list):
        if self.file is None:
            print("檔案未開啟，請先呼叫 open_file 方法。")
            return

        start_time = time.time()  # recording start time
        self.bubblesort(local_dataset)
        end_time = time.time()  # recording end time
        self.output(local_dataset, start_time, end_time)

    def output(self, local_dataset: list, start_time: float, end_time: float):
        self.file.write("Sort :" + "\n")
        for i in local_dataset:
            self.file.write(str(i) + "\n")

        self.file.write("CPU Time: " + str(end_time - start_time) + "\n")
        now = datetime.now()
        output_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        output_time += output_time + "+8:00"
        self.file.write("Output Time: " + output_time + "\n")

    def open_file(self, mode: str, local_algo: str):
        self.filename = self.filename[:-4]
        self.file = open(self.filename + "_output" + str(local_algo) + ".txt", mode)  # 確保加上.txt

    def removedata(self):
        if self.file:
            self.file.close()  # 確保關閉檔案
        self.file = None
        self.filename = None

    def split_data(self, local_dataset: list, k: int):
        local_slice = int(len(local_dataset) / k)
        frag_datasets = []
        frag_data = []
        
        for i in range(len(local_dataset)):
            frag_data.append(local_dataset[i])
            if (i + 1) % local_slice == 0:
                frag_datasets.append(frag_data)
                frag_data = [] 
    

        if frag_data:
            frag_datasets.append(frag_data)     
        
        return frag_datasets


class oneProcess(basebubblesort):
    def __init__(self, filename: str, local_slice: int):
        super().__init__(filename, local_slice)

    def merge_frag(self, first_lis: list, second_lis: list):
        first_lis = deque(first_lis)
        second_lis = deque(second_lis)
        local_result = []

        while len(first_lis) != 0 and len(second_lis) != 0:
            if first_lis[0] < second_lis[0]:
                local_result.append(first_lis.popleft())
            else:
                local_result.append(second_lis.popleft())

        local_result.extend(first_lis)
        local_result.extend(second_lis)

        return local_result

    def merge(self, frag_sets: list):
        while len(frag_sets) > 1:
            local_merge_result = []
            for i in range(0, len(frag_sets), 2):
                if i + 1 < len(frag_sets):
                    local_merge_result.append(self.merge_frag(frag_sets[i], frag_sets[i + 1]))
                else:
                    local_merge_result.append(frag_sets[i])

            frag_sets = local_merge_result

        return frag_sets

    def sorting(self, local_dataset: list):
        if self.file is None:
            print("檔案未開啟，請先呼叫 open_file 方法。")
            return

        start_time = time.time()  # start recording
        frags_dataset = self.split_data(local_dataset, self.local_slice)
        for frag in frags_dataset:
            # bubble sort every frags
            self.bubblesort(frag)
        result = self.merge(frags_dataset)
        end_time = time.time()
        self.file.write("Sort :" + "\n")
        for i in result:
            for j in i:
                self.file.write(str(j) + "\n" )

        self.file.write("CPU Time: " + str(end_time - start_time) + "\n")
        now = datetime.now()
        output_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        output_time += output_time + "+8:00"
        self.file.write("Output Time: " + output_time + "\n")
        
class mutiProcess( oneProcess):
    # only static method can apply process so change buubleSort to static here
    @staticmethod
    def bubblesort( local_dataset : list ) -> list :
        for i in range(len(local_dataset) - 1):
            for j in range(len(local_dataset) - 1):
                if local_dataset[j] > local_dataset[j + 1]:
                    local_dataset[j], local_dataset[j + 1] = local_dataset[j + 1], local_dataset[j]
        return local_dataset
    
    @staticmethod
    def merge_frag( pair_list : list ) -> list :
        first_lis, second_lis = pair_list[0], pair_list[1]
        first_lis = deque(first_lis)
        second_lis = deque(second_lis)
        local_result = []

        while len(first_lis) != 0 and len(second_lis) != 0:
            if first_lis[0] < second_lis[0]:
                local_result.append(first_lis.popleft())
            else:
                local_result.append(second_lis.popleft())

        local_result.extend(first_lis)
        local_result.extend(second_lis)
        return local_result
    
    def __init__(self, filename: str, local_slice: int):
        super().__init__(filename, local_slice)

        
    def sort_with_single_process(self, local_list : list ) -> list :
        with multiprocessing.Pool(processes=1) as pool:
            result = pool.apply(   mutiProcess.bubblesort   , (local_list,))
        return result

    def merge_sorted_list_with_muti_process( self, sorted_list : list ) -> list :
        pairs_to_merge = []
        with multiprocessing.Pool( self.local_slice - 1 ) as pool:
            while len(sorted_list ) >= 2:
                pairs_to_merge.clear()
                # range( start, end , padding )
                for i in range( 0,  len ( sorted_list ), 2 ):
                    # else list is odd
                    if i + 1 < len(sorted_list):
                        pair = sorted_list[i:i + 2]
                    else:
                        pair = [sorted_list[i], []] 
                    pairs_to_merge.append(pair)
                sorted_list = pool.map( mutiProcess.merge_frag, pairs_to_merge)
            if len(sorted_list) == 1:
                return sorted_list[0]
        
        return sorted_list[0] if sorted_list else []


    def sorting(self, local_dataset: list) -> list:
        frags_dataset = self.split_data(local_dataset, self.local_slice)
        start_time = time.time()  # recording start time
        with multiprocessing.Pool( self.local_slice ) as pool:
            local_result = pool.map(self.bubblesort, frags_dataset)
        local_result = self.merge_sorted_list_with_muti_process( local_result )
        end_time = time.time()  # recording start time
        self.file.write("Sort : " + "\n")
        for i in local_result:
            self.file.write(str(i) + "\n" )

        self.file.write("CPU Time: " + str(end_time - start_time) + "\n")
        now = datetime.now()
        output_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        output_time += output_time + "+8:00"
        self.file.write("Output Time: " + output_time + "\n")
        #print( local_result )
        
class mutithread( mutiProcess):
    def __init__(self, filename: str, local_slice: int):
        super().__init__(filename, local_slice)



    @staticmethod
    def bubblesort( local_dataset : list, local_result : queue ) -> list :
        for i in range(len(local_dataset) - 1):
            for j in range(len(local_dataset) - 1):
                if local_dataset[j] > local_dataset[j + 1]:
                    local_dataset[j], local_dataset[j + 1] = local_dataset[j + 1], local_dataset[j]
        local_result.put(local_dataset)


    @staticmethod
    def merge_frag( pair_list : list, local_result : queue ) -> list :
        first_lis, second_lis = pair_list[0], pair_list[1]
        first_lis = deque(first_lis)
        second_lis = deque(second_lis)
        local__result = []

        while len(first_lis) != 0 and len(second_lis) != 0:
            if first_lis[0] < second_lis[0]:
                local__result.append(first_lis.popleft())
            else:
                local__result.append(second_lis.popleft())

        local__result.extend(first_lis)
        local__result.extend(second_lis)
        local_result.put(local__result)
    

    def sorting( self, local_dataset ):
        threads = []
        result_queue = queue.Queue()
        frags_dataset = self.split_data(local_dataset, self.local_slice)
        start_time = time.time()  # recording start time
        #--------------------------------
        # create threads and start them
        for i in range( self.local_slice ):
            t = threading.Thread(target=mutithread.bubblesort, args=(frags_dataset[i], result_queue ))
            threads.append(t)
            t.start()
        # waiting all threads finish
        for i in threads:
            i.join()
            
        # gain data from finished thread
        
        #-------------------------------- sort frag here
        
        sorted_frag = []
        merge_threads = []
        while not result_queue.empty():
            sorted_frag.append(result_queue.get())
            
        #-------------------------------- gain frag here
        result_merge_queue = queue.Queue()
        
        while len( sorted_frag ) > 1:
            pairs_to_merge = []
            # wrap 2 data prepare for going thread
            for i in range( 0, len( sorted_frag ), 2 ):
                if i + 1 < len(sorted_frag):
                    pairs_to_merge.append((sorted_frag[i], sorted_frag[i + 1]))
                else: # padding if not odd
                    pairs_to_merge.append((sorted_frag[i], []))
            # clear origin frag cause all wrap 
            sorted_frag.clear()
            for pair in pairs_to_merge:
                merge_thread = threading.Thread(target = mutithread.merge_frag, args = (pair, result_merge_queue ) )
                merge_threads.append(merge_thread)
                merge_thread.start()

            for merge_thread in merge_threads:
                merge_thread.join()
            
            while not result_merge_queue.empty():
                sorted_frag.append( result_merge_queue.get())
                
        local_result = sorted_frag[0] if sorted_frag else []
        end_time = time.time()  
        self.output(local_result, start_time, end_time)
    
            
if __name__ == '__main__':
    # command first input
    fileName = input("Please enter FileName (eg. input1, input1.txt): \t")
    while fileName != "0":
        slice_count, algo, dataset = readfile(fileName)
        # FIFO
        if algo == 1:
            task = basebubblesort(fileName, slice_count)
            task.open_file("w", algo)
            task.sorting(dataset)
            task.removedata()

        elif algo == 2:
            task = oneProcess(fileName, slice_count)
            task.open_file("w", algo)
            task.sorting(dataset)
            task.removedata()
        elif algo == 3:
            task = mutiProcess(fileName, slice_count)
            task.open_file("w", algo)
            task.sorting( dataset)
            task.removedata()
        elif algo == 4:
            task = mutithread(fileName, slice_count)
            task.open_file("w", algo)
            task.sorting( dataset)
            task.removedata()
        fileName = input("Please enter FileName (eg. input1, input1.txt): \t")
