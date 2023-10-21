# Program that implements the FIFO, LRU and OPT page replacement
# algorithms.
# 22/04/2023
# Done by Taahir Suleman - SLMTAA007
from random import randint # import used to generate the random integers contained in the random page-reference string.
from queue import Queue # used for the FIFO queue used in implementing the FIFO page replacement algorithm.
import sys
def pageReference(pagesSize):
  # function used to generate the random page-reference string
  i = 0
  pages = [] # initialises an empty array to contain the reference string
  while(i < pagesSize): # loops through the empty array to add a random integer between 0 and 9 at each index.
    temp = randint(0,9) # generates a random integer between 0 and 9
    pages.append(temp) # appends the above generated random number to the end of the array.
    i += 1
  print("The random page-replacement String is:") 
  print(pages) # prints out the randomly generated page-reference string - used to determine the correctness of the algorithm.
  return pages
def FIFO(size, pages):
  # function that implements the FIFO page replacement algorithm with a specific number of frames in memory (size) and a randomly generated page-reference string.
  pageFaults = 0 # incremented at each page fault to determine how many page faults occur in a specific execution of the FIFO algorithm.
  fifoQueue = Queue(size) # creates a FIFO queue with the max size of the number of frames in memory - used to determine what was first in when implementing the FIFO algorithm.
  memory = set() # creates an unordered set to represent the current set of pages in memory - used to quickly determine whether a page is currently present in memory or not. 
  for p in pages:
    # iterates over the page-reference string.
    if(len(memory) < size and p not in memory):
      # if the pages in memory are not full yet and the page being referenced is not in memory - add it to the FIFO queue, add it to the memory set and increment the page faults by 1.
      pageFaults += 1
      fifoQueue.put(p)
      memory.add(p)
    elif(len(memory) == size and p not in memory):
      # if the pages in memory are full and the page being 
      # referenced is not in memory - remove the head of the FIFO 
      # queue from both the queue and the set, add the new page to 
      # the FIFO queue and memory set and increment the page faults 
      # by 1.
      pageFaults += 1
      temp = fifoQueue.get()
      memory.remove(temp)
      memory.add(p)
      fifoQueue.put(p)
  
  return pageFaults

def find(memoryArr, target, i):
  # used to search for an element target in an array memoryArr 
  # starting from the index i in the array.
  for j in range(i, len(memoryArr)):
    if(memoryArr[j] == target):
      return j # if the target is found, its index in memoryArr is returned.
  return -1 # if the target is not found, -1 is returned.

def optFind(pages, memoryArr, pointer):
  # method used to determine index in memory of the page that is
  # not referenced in the page-reference string for the longest 
  # period of time when determining which page will be replaced in
  # memory using the OPT page-replacement algorithm.
  maxIndex = -1 
  # used to determine the index in the pages array of the page that 
  # will not be used for the longest period of time - i.e., is not 
  # referenced in the pages array for the longest time relative 
  # to the other present pages in memory.
  memIndex = 0
  # used to assign and return the index of the page that will be
  # replaced in the memory array.
  for i in range(0, len(memoryArr)):
    # iterates over memory and determines the index of the next 
    # reference in the page-reference string of each page currently
    # in memory.
    index = find(pages, memoryArr[i], pointer)
    if(index == -1):
      # if a page currently in memory is never referenced again, its 
      # index in memory will be returned and it will be replaced in
      # memory.
      return i
    elif(index > maxIndex):
      # if the index of the next reference to the page in the 
      # page-reference string is higher than the current max index,
      # reassign the maxIndex and memIndex variables accordingly.
      maxIndex = index
      memIndex = i
  return memIndex

def OPT(size, pages):
  # method used to replace the page that is not referenced in the 
  # page-reference string for the longest when replacing a page in
  # memory.
  pageFaults = 0
  memory = [] # array used to represent physical memory.
  capacity = size # capacity of memory - used to determine when memory is full and page replacement needs to begin.
  pointer = 0 # points to the current position in the page reference string.
  for i in pages:
    # iterates over the page-reference string.
    if(find(memory, i, 0) == -1 and capacity > 0):
      # if the page being referenced is not currently in memory and
      # memory is not full, simply add the page to the end of memory.
      memory.append(i)
      pointer += 1
      pageFaults += 1
      capacity -= 1
    elif (find(memory, i, 0) == -1 and capacity == 0):
      # if the page being referenced is not currently in memory and
      # memory is full, determine the index of the page in memory
      # that will not be referenced in the page reference string
      # for the longest and replace it.
      index = optFind(pages, memory, (pointer+1)) # starts the search for the page that will not be referenced for the longest from pointer+1 so as to not consider the page replacing them.
      memory[index] = i # replaces the page in memory with the page currently being referenced.
      pointer += 1 # points to the next reference in the page-reference string.
      pageFaults += 1
    else:
      # when a hit occurs, i.e. a page is referenced that is already in memory, only the pointer needs to be incremented.
      pointer += 1
  return pageFaults

def LRU(size, pages):
  pageFaults = 0
  memory = set() # creates an unordered set to represent the current set of pages in memory - used to quickly determine whether a page is currently present in memory or not. 
  lruDict = {} # dictionary used to determine which page in memory has been recently used, i.e least recently referenced.
  for i in range(len(pages)):
    # for every reference in the page reference string, the LRU
    # dictionary which is used to determine the least recently used
    # reference must be updated with the reference itself being
    # the key and the value being the index of that reference in the
    # page reference string.
    lruDict[pages[i]] = i
    if(len(memory) < size and pages[i] not in memory):
      # if the frames in memory are not full yet and the page being 
      # referenced is not in memory - add it to the memory set and 
      # increment the page faults by 1.
      pageFaults += 1
      memory.add(pages[i])
    elif(len(memory) == size and pages[i] not in memory):
      # if the page being referenced is not currently in memory and
      # memory is full, the index of the least recently used page
      # must be determined.
      lruIndex = 1000000 # sets the index large initially so that it may be used to incrementally determine a minimum index
      pageFaults += 1 # increments page faults by one.
      for j in memory:
        # increments through every page currently in memory to
        # determine which page has the minimum index in the LRU
        # dictionary, which will indicate which page has been least
        # recently used/referenced.
        if(lruDict[j] < lruIndex):
          # if the index of the current page being looked at in memory is less than the current minimum index, reassign the lruIndex to this index .
          temp = j # used to determine which page specifically must be removed from the dictionary and memory once the least recently used page has been found.
          lruIndex = lruDict[j]
      del lruDict[temp] # removes the element in the dictionary of the page that will be removed from memory.
      memory.remove(temp) # removes the page from memory.
      memory.add(pages[i]) # adds the new (currently referenced) page to memory - it was already added to the dictionary above.
  
  return pageFaults
      


def main():
  size = int(sys.argv[1]) # retrieves the number of frames in memory from the command-line argument.
  checkInput = input("Please enter the desired page-reference String size:\n") # requests the user to input their desired size for the random page-reference string.
  if(checkInput.isdigit()):
    # ensures that the user input is in the correct format, i.e. an integer.
    pagesSize = eval(checkInput) 
  else:
    # if the user input is not a string, keep requesting user to input an integer for the page-reference string size until a valid input is made.
    while(checkInput.isdigit() == False):
      checkInput = input("Size entered is invalid - please enter an integer value for your desired page reference String size\n")
    pagesSize = eval(checkInput) 
  pages = pageReference(pagesSize) # generates the page-reference string and assigns it to pages.
  print ('FIFO ', FIFO(size,pages), ' page faults.') # prints how many page faults occurred when implementing the FIFO algorithm on the random page-reference string with the given size of memory.
  print ('LRU ', LRU(size,pages), ' page faults.') # prints how many page faults occurred when implementing the LRU algorithm on the random page-reference string with the given size of memory.
  print ('OPT ', OPT(size, pages), ' page faults.') # prints how many page faults occurred when implementing the OPT algorithm on the random page-reference string with the given size of memory.

if __name__ == "__main__":
  if len(sys.argv) != 2:
    # exception used in the case that the user does not supply the command-line argument required for the memory size.
    print ('Please ensure this program is used as follows: python3 paging.py [number of page frames]')
  else:
    main()