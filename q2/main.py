from __future__ import annotations

from queue import Queue
from uuid import uuid4


class Page:
    def __init__(self, size):
        self.size: int = size


class Process:
    def __init__(self, id: int, name: str, size: int, page_size: int) -> None:
        self.id: int = id
        self.name: str = name
        self.size: int = size
        self.page_size: int = page_size
        self.number_of_pages: int = 0
        self.max_number_of_pages: int = self._get_max_number_of_pages()
        self.pages: Queue = Queue()

    def allocate(self):
        page = Page(self.page_size)
        if self.number_of_pages + 1 <= self.max_number_of_pages:
            self.pages.put(page)
            self.number_of_pages += 1
        else:
            self._substitute(page)
    
    def _substitute(self, page: Page):
        dumped = self.pages.get()
        self.pages.put(page)
        return dumped

    def _get_max_number_of_pages(self):
        return self.size // self.page_size


class Memory:
    def __init__(self, max_size: int):
        self.size: int = 0
        self.max_size: int = max_size
        self.processes: Queue = Queue()

    def allocate(self, process: Process) -> Process | None:
        if self._predicted_memory_size(process) <= self.max_size:
            self.size += process.size
            self.processes.put(process)
        else:
            raise Exception("Max memory size exceeded.")

    def _predicted_memory_size(self, process: Process):
        return self.size + process.size


class VirtualMemory:
    def __init__(self, max_size: int):
        self.max_size: int = max_size


class PageReferenceService:
    def __init__(self):
        self.pages: Queue = Queue()
    
    def put(self, page: Page):
        self.pages.put(page)

    def get(self):
        page = self.pages.get()
        self.pages.put(page)
        return page


def create_process(size: int, page_size: int):
    id = uuid4()
    process = Process(id, f"Process {id}", size, page_size)
    for _ in process.max_number_of_pages():
        process.allocate(Page(page_size))
    return process


def apply_fifo_substitution(process: Process) -> Process:
    return process


def apply_lru_substitution(process: Process) -> Process:
    return process


def run_substitution_algorithm(process: Process):
    print("Select substitution algorithm. Enter (1) for FIFO and (2) LRU:")
    alternative = int(input())

    if alternative == 1:
        apply_fifo_substitution(process)
    else:
        apply_lru_substitution(process)


def initial_setup():
    print("Enter the max memory size (MB):")
    max_memory_size = int(input())
    print("Enter max virtual memory size (MB):")
    max_virtual_memory_size = int(input())
    print("Enter page size (MB):")
    page_size = int(input())
    return max_memory_size, max_virtual_memory_size, page_size

def print_memory_allocation_info(memory: Memory):
    print("----------------------------------------------------")
    print("MEMORY ALLOCATION")
    print(f"Memory State/Capacity: {memory.size}/{memory.max_size}")
    print(f"Is Memory Fragmented?: #TODO")
    print(f"Pages Free/Allocated: {2}/{2}")

def main():
    max_memory_size, max_virtual_memory_size, page_size = initial_setup()
    stop = False
    memory = Memory(max_memory_size)
    virtual_memory = VirtualMemory(max_virtual_memory_size)
    page_reference_service = PageReferenceService()
    free_pages = 0
    allocated_pages = 0

    while not stop:
        print("Enter the process size (MB):")
        size = int(input())
        process = create_process(size, page_size)

        
        
        # try:
        #     pass
        # except:
        #     run_substitution_algorithm(process)
        
        print_memory_allocation_info(memory)


    print_memory_allocation_info(memory)


if __name__ == "__main__":
    main()