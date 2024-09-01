import heapq
import math 

hyper1=1
hyper2=2
tasks1=[]
tasks2=[]
numTasks1= int(input("Enter number of tasks for processor 1: "))

# sum variable stores the utilization factor (U)
sum1=0
sum2=0

for i in range(numTasks1):
    task=[]
    #taking each task parameters as a string input
    task= list(int(x) for x in input("Enter release time, execution time, deadline, period,message num for Task "+str(i+1)+": ").split(" "))
    tasks1.append(task)
    #calculate hyperperiod
    hyper1= math.lcm(hyper1,task[3])
    #calculate sigma ei/pi
    sum1+= task[1]/task[3]

numTasks2= int(input("Enter number of tasks for processor 2: "))
for i in range(numTasks2):
    task=[]
    #taking each task parameters as a string input
    task= list(int(x) for x in input("Enter release time, execution time, deadline, period, message num for Task "+str(numTasks1+i+1)+": ").split(" "))
    tasks2.append(task)
    #calculate hyperperiod
    hyper2= math.lcm(hyper2,task[3])
    #calculate sigma ei/pi  
    sum2+= task[1]/task[3]

print("\nHyperperiod1 - "+ str(hyper1),end="\n\n")
print("\nHyperperiod2 - "+ str(hyper2),end="\n\n")
#print(tasks1)

utilization= 1 #utilization for non-RM schedules should be <= 1
print("Sum of Ci/Pi for processor 1: "+str(sum1)) 
print("Sum of Ci/Pi for processor 2: "+str(sum2)) 
print("Utilization: "+str(utilization))
if sum1> utilization or sum2>utilization: print("\n***EDF Scheduling is not possible within deadlines***\n")
else: print("\nEDF Schedule: \n")

newList1= []
newList2= []

for i in range(len(tasks1)):
    task= tasks1[i]
    low= task[0]
    # task[0]- release time
    # task[1]- execution time
    # task[2]- deadline
    # task[3]- period
    # task[4]- message num
    cnt=1
    while low<hyper1 :
        newList1.append([low,task[1],task[2],i+1,cnt,task[4]])
        low= low+task[3]
        cnt+=1

for i in range(len(tasks2)):
    task= tasks2[i]
    low= task[0]
    # task[0]- release time
    # task[1]- execution time
    # task[2]- deadline
    # task[3]- period
    # task[4]- message num
    cnt=1
    while low<hyper2 :
        newList2.append([low,task[1],task[2],numTasks1+i+1,cnt,task[4]])
        low= low+task[3]
        cnt+=1

newList1.sort()
newList2.sort()

print(newList1)
print(newList2)

heap1=[]
heap2=[]
hyper= max(hyper1,hyper2)
bus=[]
can=0
for i in range(hyper):
    #pushing the tasks whose release time is <= the current time into
    #the heap so that tasks1 can be taken from the heap1 in order of priority
    while len(newList1)>0 and newList1[0][0]<= i:
        task= newList1.pop(0)
        heapq.heappush(heap1,[task[2]+task[0],task[1],task[3],task[4],task[5]])
        # deadline, execution time, task number, instance, message num
    while len(newList2)>0 and newList2[0][0]<= i:
        task= newList2.pop(0)
        heapq.heappush(heap2,[task[2]+task[0],task[1],task[3],task[4],task[5]])

    #heap1 sorts the tasks1 prioritizing the deadline low- high
    if can==0 and len(bus)>0:
        can= bus.pop(0)
    if len(heap1)>0:
        top= heapq.heappop(heap1)
        # top]0]- deadline
        # top[1]- execution time
        # top[2]- task number
        # top[3]- task instance
        # top[4]- message num
        #decrementing the execution time by 1- this task is being scheduled at current time
        top[1]=top[1]-1

        #if the execution time becomes 0, that instance is  finished and can be removed, else push it back into the heap1
        if top[1]>0: 
            heapq.heappush(heap1,top)
        else:
            if top[4]>0: bus.append(top[4])
        possible=""
        #if deadline is before the current time, it is past deadline
        if top[0]<i+1: possible+= " (Past Dealine)"
        print(str(i)+" - "+str(i+1)+":  | Task "+ str(top[2]) +" - Instance "+str(top[3])+possible,end=" |     ")
    else: print(str(i)+" - "+str(i+1)+":  | Idle               ",end=" |     ")
    print(can,end="     | ")
    if len(heap2)>0:

        top= heapq.heappop(heap2)
        temp=[]
        while top[4]>0 and can!=top[4]:
            temp.append(top)
            top= heapq.heappop(heap2)
        while len(temp)!=0:
            heapq.heappush(heap2,temp.pop(0))
        # top]0]- deadline
        # top[1]- execution time
        # top[2]- task number
        # top[3]- task instance
        # top[4]- message num
        #decrementing the execution time by 1- this task is being scheduled at current time
        top[1]=top[1]-1

        #if the execution time becomes 0, that instance is finished and can be removed, else push it back into the heap1
        if top[1]>0: heapq.heappush(heap2,top)
        if top[4]>0: can=0
        possible=""
        #if deadline is before the current time, it is past deadline
        if top[0]<i+1: possible+= " (Past Dealine)"
        print(" Task "+ str(top[2]) +" - Instance "+str(top[3])+possible,end=" |\n")
    else: print(" Idle              ",end=" |\n") 
print("\nUnscheduled Tasks: ")
print(heap1)