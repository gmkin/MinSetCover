# MinSetCover
Finding the Min Set Cover for given subsets

Runs with python3
Usage:	python MinCoverSet.py INPUT_FILE

RUns with java
Usage:	javac MinSetCover.java && java MinSetCover INPUT_FILE

Input: 
Max number of elements
Number of subsets/lines to follow
(subsets)

Output:
(subsets in min cover set)
[Can be configured to ouput time]

Thought process:
Recommended usage: python
This problem can be thought of as graph, where the points are are elements in the universal set and the edges are given by the complete graph of the subsets inputed.  As such, you can map each of the points to a number detailing which vertices are covered.  As such, you can quickly perform set operations, such as intersection and union very quickly using bitwise manipulation.  

First the program computes the greedy algorithm, which is at most log(Max number of elements) away from the optimal solution.  Then it recursively finds the next suitable subset by checking which subset contains an exclusive element or the most uncovered bits (much like greedy except we explore other posibilites too).

Unit Testing and Benchmarking results are seperated.
