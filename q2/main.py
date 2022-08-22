from __future__ import annotations

import random
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Process:
    id: int
    name: str
    size: int

def create_process(id: int, size: int):
    return Process(id, f"Process {id}", size)


@dataclass
class Page:
    def __init__(self, size: int, process: Process):
        self.size = size
        self.process = process
        self.id = uuid4()


class Memory:
    def __init__(self, max_size: int):
        self.max_size: int = max_size
        self.pages: list[Page] = []
        self.current_size: int = 0


class MemoryError(Exception):
    pass


def move_page_to_memory(memory: Memory, page: Page):
    if (memory.current_size + page.size) <= memory.max_size:
        memory.pages.append(page)
        memory.current_size += page.size
    else:
        raise MemoryError("Max memory size exceeded.")


def remove_page_from_memory(memory: Memory, page: Page):
    memory.pages.remove(page)
    memory.current_size -= page.size


class VirtualMemory:
    def __init__(self, max_size):
        self.max_size = max_size
        self.pages: list[Page] = []
        self.current_size: int = 0


def move_page_to_virtual_memory(virtual_memory: Memory, page: Page):
    if virtual_memory.current_size + page.size <= virtual_memory.max_size:
        virtual_memory.pages.append(page)
        virtual_memory.current_size += page.size
    else:
        raise Exception("Max virtual memory size exceeded.")


def remove_page_from_virtual_memory(virtual_memory: Memory, page: Page):
    virtual_memory.pages.remove(page)
    virtual_memory.current_size -= page.size


def create_process_pages(process: Process, page_size: int):
    pages: list[Page] = []
    number_of_pages = process.size // page_size
    for _ in range(number_of_pages):
        pages.append(Page(page_size, process))
    return pages


def apply_fifo_substitution(memory: Memory, virtual_memory: VirtualMemory, page: Page) -> Page:
    popped = memory.pages.pop(0)
    memory.current_size -= popped.size
    move_page_to_virtual_memory(virtual_memory, popped)
    move_page_to_memory(memory, page)


def apply_lru_substitution(memory: Memory, virtual_memory: VirtualMemory, page: Page) -> Page:
    popped = memory.pages[0]
    memory.current_size -= popped.size
    move_page_to_virtual_memory(virtual_memory, popped)
    move_page_to_memory(memory, page)


def initial_setup():
    print("Enter the max memory size (MB):")
    max_memory_size = int(input())
    print("Enter max virtual memory size (MB):")
    max_virtual_memory_size = int(input())
    print("Enter page size (MB):")
    page_size = int(input())
    print("Enter the substitution algorithm. (1) for FIFO and (2) for LRU:")
    algorithm = int(input())
    return max_memory_size, max_virtual_memory_size, page_size, algorithm


def create_processes_from_file(path: str) -> list[Process]:
    processes = []
    with open(path) as f:
        for line in f.readlines():
            id, size = line.split()
            processes.append(create_process(int(id), int(size)))
    return processes


def print_memory_allocation_info(memory: Memory, virtual_memory: VirtualMemory, page_size: int):
    print("----------------------------------------------------")
    print("MEMORY ALLOCATION")
    print(f"Memory State/Capacity: {memory.current_size}/{memory.max_size}")
    print(f"Virtual Memory State/Capacity: {virtual_memory.current_size}/{virtual_memory.max_size}")
    fragmented = (memory.current_size % page_size) == 2
    print(f"Is Memory Fragmented?: {fragmented}")
    print(f"Pages Free/Allocated: {len(memory.pages)}/{len(virtual_memory.pages)}")


def main():
    path = "q2/in.txt"
    max_memory_size, max_virtual_memory_size, page_size, algorithm = initial_setup()
    memory = Memory(max_memory_size)
    virtual_memory = VirtualMemory(max_virtual_memory_size)
    page_references = []
    page_miss = 0

    processes = create_processes_from_file(path)

    for process in processes:
        page_references.extend(create_process_pages(process, page_size))

    print(f"Number of pages: {len(page_references)}")
    for _ in range(50):
        index = random.randint(0, len(page_references) - 1)
        page: Page = page_references[index]
        print(f"Page index: {index}")

        try:
            if page.id not in [page.id for page in memory.pages]:
                move_page_to_memory(memory, page)
                page_miss += 1
        except MemoryError:
            if algorithm == 1:
                apply_fifo_substitution(memory, virtual_memory, page)
            else:
                apply_lru_substitution(memory, virtual_memory, page)
        
        print_memory_allocation_info(memory, virtual_memory, page_size)

    print(f"Page misses: {page_miss}")


if __name__ == "__main__":
    main()
