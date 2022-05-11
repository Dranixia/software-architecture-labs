# Lab 2: Hazelcast Basics

## Requirments:

```
pip install -r requirements.txt
```

## Results

### Task 1

Hazelcast installed

### Task 2 

![](img/task2.png)

### Task 3

Distributed Map with 3 nodes:

![](img/task3_1.png)

After deleting 1 of the nodes: 

![](img/task3_2.png)

### Task 4

Without locking:

![](img/task4_1.png)

Optimistic locking:

![](img/task4_2.png)

Pessimistic locking:

![](img/task4_3.png)

### Task 5

The bounding of queue must be made using .xml file.

If there is no reading and the queue is filled, the writer will wait until the queue is popped.

During reading from 2 clients, there were no data races, and all the values were properly read and printed.
