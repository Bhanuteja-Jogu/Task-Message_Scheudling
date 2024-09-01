import heapq
import math

hyper= 1

#taking all the tasks from the input into the list named tasks
tasks=[]

# sum variable stores the utilization factor (U)
sum=float(0)
numTasks= int(input("Enter number of tasks: "))
for i in range(numTasks):
    task=[]
    #taking each task parameters as a string input
    task= list(int(x) for x in input("Enter release time, execution time, period for Task "+str(i+1)+": ").split(" "))
    tasks.append(task)
    hyper= math.lcm(hyper,task[2])
    sum= sum+task[1]/task[2]

print("\nHyperperiod - "+ str(hyper),end="\n\n")
#print(tasks)

utilization= numTasks* (2**(1/numTasks)-1)
print("Sum of Ci/Pi: "+str(sum))
print("Utilization: "+str(utilization))
if sum> utilization: print("\n***RM Scheduling is not possible within deadlines***\n")
else: print("\nRM Schedule: \n")
newList= []
for i in range(len(tasks)):
    task= tasks[i]
    low= task[0]
    # task[0]- release time
    # task[1]- execution time
    # task[2]- period and deadline
    cnt=1
    while low<hyper :
        newList.append([low,task[1],task[2],i+1,cnt])
        low= low+task[2]
        cnt+=1
newList.sort()
print(newList)
heap=[]
for i in range(hyper):
    #pushing the tasks whose release time is <= the current time into
    #the heap so that tasks can be taken from the heap in order of priority
    while len(newList)>0 and newList[0][0]<= i:
        task= newList.pop(0)
        heapq.heappush(heap,[task[2],task[1],task[3],task[4],task[0]+task[2]])
        # period, execution time, task number, task instance, deadline

    #heap sorts the tasks prioritizing the period high-low
    if len(heap)>0:
        top= heapq.heappop(heap)
        # top]0]- period
        # top[1]- execution time
        # top[2]- task number
        # top[3]- task instance
        # top[4]- deadline

        #decrementing the execution time by 1- this task is being scheduled at current time
        top[1]=top[1]-1

        #if the execution time becomes 0, that instance is finished and can be removed, 
        #else push it back into the heap
        if top[1]>0: heapq.heappush(heap,top)
        possible=""

        #if deadline is before the current time, it is past deadline
        if top[4]<i+1: possible = " (Past Dealine)"

        print(str(i)+" - "+str(i+1)+":   Task "+ str(top[2]) +" - Instance "+str(top[3])+possible)
    else: print(str(i)+" - "+str(i+1)+":   Idle")

print("\nUnscheduled Tasks: ")
print(heap)
    
