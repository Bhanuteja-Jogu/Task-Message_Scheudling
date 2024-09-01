#include <bits/stdc++.h>
using namespace std;
long long gcd(long long int a, long long int b)
{
    if (b == 0) return a;
 	return gcd(b, a % b);
}
long long lcm(int a, int b) { return (a / gcd(a, b)) * b; }

vector<int> distinctPrimeFactors(int N)
{
	vector<int> factors;
    if (N < 2) {
        return factors;
    }
    if (N == 2) {
    	factors.push_back(2);
    	return factors;
    }
 
    unordered_map<int, bool> visited;
    
    for (int i = 2; i * i <= N; i++) {
        while (N % i == 0) {
            if (!visited[i]) {
                factors.push_back(i);
                visited[i] = 1;
            }
            N /= i;
        }
    }
    if (N > 2)
        factors.push_back(N);
    return factors;
}

int main(){
	int n,Tss=12,Tsts,Nsts;
	cout<<"Enter no. of nodes: "<<endl;
	cin>> n;
	vector<vector<pair<int,int>>> signals(n);
	for(int i=0;i<n;i++){
		cout<<"Enter no. of signals in node "<< i+1<<endl;
		int k;cin>> k;
		cout<<"Enter size,periods of "<<k<<" signals"<<endl;
		for(int j=0;j<k;j++){
			int a,b;cin>>a>>b;
			signals[i].push_back({a,b});
			//Tss= gcd(Tss,b);
		}
	}
	// cout<<Tss<<endl;
	// !---Task-1---!
	// Iterate over size of Tsts over min to max
	// Tsts min= signal length Tsts max= length of longest message
	// Tss is fixed= lcm of all periods
	// Nsts is an integer. Tsts.Nsts= Tss
	Tsts= Tss/4;
	// !---Node-wise processes---!
	
	// !---Task-2---!
	// Pack the signals into messages
	// Signals with same periods packed into same message
	// Pack signals with same periods together
	// Pack into the message which is filled highest, if not possible spawn a new message
	vector<vector<int>> messages(n);
	for(int i=0;i<n;i++){
		multiset<pair<int,int>,greater<pair<int,int>>> arr;
		for(auto it: signals[i]){
			int s= it.first,p= it.second;
			if(arr.size()==0){
				arr.insert({s,p});
				continue;
			}
			auto itt=arr.begin();
			while(itt!=arr.end()){
				if(itt->second==p&& itt->first+s<= Tsts){
					arr.insert({s+itt->first,p});
					arr.erase(itt);
					break;
				}
				itt++;
			}
			if(itt==arr.end()) arr.insert({s,p});
		}
		for(auto it: arr){
			messages[i].push_back(it.second);
		}
	}
	for(auto it: messages){
		for(auto itt: it) cout<<itt<<" ";
		cout<<endl;
	}
	// !---Task-3---!
	// Construct  the schedule of messages in the flexray bus
	
	// Without Jitter
	// Schedule messages in FID'such that the allocation of FID's is minimized
	/* Algorithm-1:
	1) Start with an empty array which stores FID's with different periods
	2) Iterate over messages in ascending order of their periods
	3) For each message: Iterate over FID array in descending/ascending order of periods
	4) Assign FID which is available
	5) If not available, add a new FID with periodicity of its lowest prime factor
	
	- This greedy algorithm doesn't work
	- Lets assume there are 2, 3 groups available
	- Lets say we follow ascending order in step-3
	- Lets assume we have to fill messages with periods 6, 8
	- Going by ascending order of FID available first we fill up messages
	  with period 6 in the 2-group, then we don't have the choice but to
	  fill the next message with period 8 in 2-group itself
	  3-group is left unused which is certainly not optimal
	- And if we follow descending order in step-3
	- Similar case occurs for messages with period 6, 9 where 2 group goes unused
	- Hence, we need to use recursive approch testing all possible ways
	
	Algorithm-2:
	1) Start with an empty array which stores FID's with different periods
	2) Iterate over messages in possibility order
	Possibility order: For every periodicity of message, find the number of
	distinct prime factors and lets call them possibilities,
	Now sort the messages in the increasing order of possibilities
	3) For each message: Iterate over FID array in descending order of periods
	4) Assign FID which is available
	5) If not available, add a new FID with periodicity of its lowest prime factor
	
	- This algorithm also fails in following case
	2 3 7   m1(2 3 7) m2(7 11 13)
	Instead of considering all possibilities to sort we need to consider only
	those which are already available in the FID array so that there won't be 
	any need to spawn new slots
	
	Algorithm-3- Final ALgorithm:
	1) Start with an empty array which stores FID's with different periods
	2) Calculate Availability(A) for all messages and choose the message with
	lowest A at every iteration
	Availability order: For every periodicity of message, find the number of
	distinct prime factors and lets call them possibilities(P), let's call the
	number of P which are freely available in the FID array as Availability(A)
	Now choose the message with lowest A.
	3) For each message: Iterate over FID array in descending order of periods
	4) Assign FID which is available
	5) If not available, add a new FID with periodicity of its lowest prime factor
	
	Ai+1>= Ai
	Ai+1==0 => Ai=0 => Co-prime with all FID. Compulsory spawn
	Ai+1==1 => Ai=1,0 => Spawn compulsory required whichever order chosen
	Ai+1>1 => Ai= 0,1,2..Ai+1 -1 => Ai will consume 1 slot at max
	Ai+1= Ai+1 -1 
	Ai+1> 0
	Hence Ai+1 will always have a free slot.
	
	For with Jitter, We can use basic EDF or RM scheduling
	Just spawn a new FID whenever message exceeds its deadline.
	*/ 
	for(auto it: messages){
		vector<int> fid;
		unordered_map<int,int> availability;
		int Nsp=1;
		for(auto itt: it) Nsp= lcm(Nsp,itt);
		for(auto itt: it){
			if(availability[itt]==0){
				vector<int> factors= distinctPrimeFactors(itt);
				for(auto xt:factors){
					for(auto xtt: fid){
						if(xt==xtt){
							availability[itt]++;
							break;
						}
					}
				}
			}
		}
		
	}
	
	return 0;
}