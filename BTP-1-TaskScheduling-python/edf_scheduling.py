import heapq
import math 

hyper=1
tasks=[]
numTasks= int(input("Enter number of tasks: "))

# sum variable stores the utilization factor (U)
sum=0

for i in range(numTasks):
    task=[]
    #taking each task parameters as a string input
    task= list(int(x) for x in input("Enter release time, execution time, deadline, period for Task "+str(i+1)+": ").split(" "))
    tasks.append(task)
    #calculate hyperperiod
    hyper= math.lcm(hyper,task[3])
    #calculate sigma ei/pi
    sum+= task[1]/task[3]


print("\nHyperperiod - "+ str(hyper),end="\n\n")
#print(tasks)

utilization= 1 #utilization for non-RM schedules should be <= 1
print("Sum of Ci/Pi: "+str(sum))
print("Utilization: "+str(utilization))
if sum> utilization: print("\n***EDF Scheduling is not possible within deadlines***\n")
else: print("\nEDF Schedule: \n")
newList= []

for i in range(len(tasks)):
    task= tasks[i]
    low= task[0]
    # task[0]- release time
    # task[1]- execution time
    # task[2]- deadline
    # task[3]- period
    cnt=1
    while low<hyper :
        newList.append([low,task[1],task[2],i+1,cnt])
        low= low+task[3]
        cnt+=1
newList.sort()
print(newList)
heap=[]
for i in range(hyper):
    #pushing the tasks whose release time is <= the current time into
    #the heap so that tasks can be taken from the heap in order of priority
    while len(newList)>0 and newList[0][0]<= i:
        task= newList.pop(0)
        heapq.heappush(heap,[task[2]+task[0],task[1],task[3],task[4]])
        # deadline, execution time, task number, instance

    #heap sorts the tasks prioritizing the deadline low- high
    if len(heap)>0:
        top= heapq.heappop(heap)
        # top]0]- deadline
        # top[1]- execution time
        # top[2]- task number
        # top[3]- task instance

        #decrementing the execution time by 1- this task is being scheduled at current time
        top[1]=top[1]-1

        #if the execution time becomes 0, that instance is finished and can be removed, else push it back into the heap
        if top[1]>0: heapq.heappush(heap,top)

        possible=""
        #if deadline is before the current time, it is past deadline
        if top[0]<i+1: possible+= " (Past Dealine)"
        print(str(i)+" - "+str(i+1)+":   Task "+ str(top[2]) +" - Instance "+str(top[3])+possible)
    else: print(str(i)+" - "+str(i+1)+":   Idle") 
    
print("\nUnscheduled Tasks: ")
print(heap)