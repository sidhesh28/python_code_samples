Problem Statement:
Class Scheduling

Imagine you are a student and you have a list of courses you want to take. Many of these courses have prerequisites which you must take before you can take that course. Your task is to write a program that finds an order that you can take each of the courses where all the prerequisites are satisfied.

## Specification

You may use any language you would like to implement your solution.
We're interested in how you solve problems in code, so please only use standard libraries.
If your implementation language lacks a JSON library feel free to include an open source JSON library.
Your submission should create an executable named `scheduler`. `scheduler` can also be a bash script invoking your program.
It will be invoked as follows: `./scheduler FILE_NAME`.
If your implementation language is not interpreted, please include a Makefile or other build script to generate your binary.
Do not submit a built executable.
Instructions on how to build your executable should be included in your README, be sure to specify what compiler version is needed.


#### Input
The first (and only) argument to the program will be a path to a [JSON](http://en.wikipedia.org/wiki/JSON) file containing class names and all (if any) prerequisites they have.
Examples:

* [math.json](#file-math-json)
* [physics.json](#file-physics-json)

#### Output

Each class name should be printed to standard out, one class per line.
It should be a valid ordering of classes such that you can take the classes in the order printed.
You are not allowed to take a class until you have taken its prerequisites.
There may be multiple valid orderings of courses. Any valid order will be considered correct.
See [examples](#examples) below if you are unsure.

If your program runs into errors, exit and print a message to standard error. The error message should begin with `Error:` and contain some context (e.g. `Error: No argument provided.`).

#### README

You should include a plaintext or [markdown](http://daringfireball.net/projects/markdown/syntax) file README.
It should contain anything you would have in a top level README if this was an open source or professional project.
We would also like you to share insight into why you designed your program the way you did.
Feel free to include any other files that help demonstrate your problem solving process (e.g. notes, drawings, tests, etc.).

##### Performance Analysis

In your README, include a section that describes the time complexity of your solution.

## Submission

Please send back the source code of your programs, any tests, and the script or executable we can use to run your program.
Please do not make a public repo with your solution, as we'd like to keep the details of the challenge private.

## Rubric

Your solution will be graded on correctness, program design/architecture, coding style, and performance.
We will be automatically testing your program for correctness.
We will also read the source.
Your submissions should be something you would be proud to submit to an open source project or on the job.
We expect this to take about two hours (with variation depending on your experience level).

## Examples

```
Input:

./scheduler math.json

Example Valid Output (there are others):

Algebra 1
Geometry
Algebra 2
Pre Calculus
```

```
Input: 

./scheduler physics.json

Example Valid Output (there are others):

Calculus
Differential Equations
Scientific Thinking
Intro to Physics
Relativity
```



Scheduler class takes a json file with list of courses and their pre-requisite courses as input, and prints a valid ordering of classes. 
A valid ordering would be all pre-requisite courses of a class are printed before the class.


Requirements:

Python 3.5.1


To run:

 ./scheduler <input json file>
 
 
Testing:

Test 'test_scheduler.py' file included. To run:

python -m unittest -v test_scheduler.py



Time Complexity:

To build the course list, the program loops through the input courses dict once, and then another time to add all pre-requisite courses for each course. This would take O(b) where b = number of courses. 

The course list is essentially a tree-like structure with each course being a node linked to its pre-requisite courses which are nodes themselves. Traversing through a tree in depth first manner takes O(bd) time where b = number of nodes and d = depth of the tree.

The program loops through all the courses once, and traverses through pre-requisite courses of each course.  A course is traversed through only once.
Time complexity is O(bd) time where b = number of nodes and d = depth of the tree.