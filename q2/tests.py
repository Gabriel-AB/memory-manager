from unittest import TestCase

from .main import Memory, Page, Process, VirtualMemory


class PageTestCase(TestCase):
    def test_create_a_page(self):
        page = Page(5)
        self.assertEqual(page.size, 5)


class ProcessTestCase(TestCase):
    def setUp(self):
        self.parameteres = {
            "id": 1,
            "name": "Download image",
            "size": 20,
            "page_size": 5
        }
        self.process = Process(**self.parameteres)

    def test_create_a_process(self):
        self.assertEqual(self.process.id, self.parameteres["id"])
        self.assertEqual(self.process.name, self.parameteres["name"])
        self.assertEqual(self.process.size, self.parameteres["size"])

    def test_get_process_max_number_of_pages(self):
        self.assertEqual(self.process.max_number_of_pages, 4)

    def test_substitute_pages(self):
        page = Page(5)
        self.process.allocate(page)
        for _ in range(self.process.max_number_of_pages - 1):
            self.process.allocate(Page(5))
        res = self.process._substitute(Page(5))
        self.assertEqual(res, page)

    def test_allocate_pages(self):
        page = Page(5)
        self.process.allocate(page)
        for _ in range(self.process.max_number_of_pages - 1):
            self.process.allocate(Page(5))
        self.process.allocate(Page(5))
        self.assertEqual(self.process.pages.qsize(), self.process.max_number_of_pages)


class MemoryTestCase(TestCase):
    def setUp(self):
        self.memory = Memory(20)
        self.processes: list[Process] = []
        for i in range(1, 5):
            self.processes.append(Process(i, f"Process {i}", 5, 1))

    def test_create_memory(self):
        self.assertEqual(self.memory.max_size, 20)

    def test_process_allocation(self):
        [self.memory.allocate(process) for process in self.processes]
        self.assertEqual(sum([process.size for process in self.processes]), 20)

    def test_process_allocation_order(self):
        [self.memory.allocate(process) for process in self.processes]            
        for i in range(1, self.memory.processes.qsize() + 1):
            process = self.memory.processes.get()
            self.assertEqual(process.id, i)

    def test_memory_explosion(self):
        with self.assertRaises(Exception) as context:
            parameteres = {
                "id": 1,
                "name": "Download image",
                "size": 20
            }
            for _ in range(2):
                self.memory.allocate(Process(**parameteres), raise_exception=True)    
        self.assertTrue("Max memory size exceeded.", str(context.exception))

class VirtualMemoryTestCase(TestCase):
    def setUp(self):
        self.virtual_memory = VirtualMemory(25)
    
    def test_create_virtual_memory(self):
        self.assertEqual(self.virtual_memory.max_size, 25)
