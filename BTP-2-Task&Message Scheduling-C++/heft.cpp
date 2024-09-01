#include <bits/stdc++.h>
using namespace std;

void dfs_upward(vector<vector<int>> adj[],vector<float> &avg_comp_cost,vector<float> &upward,int i){
	if(upward[i]!=-1) return;
	float rank=0;
	for(auto it: adj[i]){
		dfs_upward(adj,avg_comp_cost,upward,it[0]);
		rank= max(rank,it[1]+upward[it[0]]);
	}
	upward[i]= rank+ avg_comp_cost[i];
}
void dfs_downward(vector<vector<int>> adj[],vector<float> &avg_comp_cost,vector<float> &downward,int i){
	if(downward[i]!=-1) return;
	float rank=0;
	for(auto it: adj[i]){
		dfs_downward(adj,avg_comp_cost,downward,it[0]);
		rank= max(rank,it[1]+downward[it[0]]+avg_comp_cost[it[0]]);
	}
	downward[i]= rank;
}

int main(){
	int q,v,e;
	//v tasks e edges
	cout<<"Enter num of processors(q), vertices(v), edges(e): \n";
	cin>>q>>v>>e;
	vector<float> avg_comp_cost(v+1);
	vector<vector<int>> adj[v+1],rev[v+1];
	cout<<"Enter average computation costs of v vertices: \n";
	for(int i=0;i<v;i++) cin>> avg_comp_cost[i+1];
	cout<<"Enter e edges (from to weight): \n";
	for(int i=0;i<e;i++){
		int a,b,c; cin>>a>>b>>c;
		adj[a].push_back({b,c});
		rev[b].push_back({a,c});
	}
	
	vector<int> entry, exit;
	for(int i=1;i<v+1;i++) if(adj[i].size()==0) exit.push_back(i);
	for(int i=1;i<v+1;i++) if(rev[i].size()==0) entry.push_back(i);
		
	vector<float> upward(v+1,-1), downward(v+1,-1);
	for(auto it: entry) dfs_upward(adj,avg_comp_cost,upward,it);
	for(auto it: exit) dfs_downward(rev,avg_comp_cost,downward,it);
	
	for(auto it:adj){
		for(auto itt: it){
			cout<<itt[0]<<itt[1]<<" ";
		}
		cout<<endl;
	}
	cout<<endl<<"Upward Rank: "<<endl;
	for(int i=1;i<v+1;i++) cout<<upward[i]<<endl;
	cout<<endl<<"Downward Rank: "<<endl;
	for(int i=1;i<v+1;i++) cout<<downward[i]<<endl;
	cout<<endl<<"Total Rank: "<<endl;
    for(int i=1;i<v+1;i++) cout<<upward[i]+downward[i]<<endl;
	return 0;
}