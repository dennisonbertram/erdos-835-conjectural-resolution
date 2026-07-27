#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using S=std::vector<std::pair<int16_t,int8_t>>;
struct M{int q;S v;uint64_t h;};
static uint64_t weight(int r){uint64_t z=uint64_t(r)+0x9e3779b97f4a7c15ULL;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static uint64_t hashv(const S&v){uint64_t h=0;for(auto [r,x]:v)h+=uint64_t(int64_t(x))*weight(r);return h;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;}
static S neg(S v){for(auto&x:v)x.second=-x.second;return v;}
static bool sub(const S&a,const S&b,int bound,S&o){o.clear();size_t i=0,j=0;while(i<a.size()||j<b.size()){int r,x;if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){r=a[i].first;x=a[i++].second;}else if(i==a.size()||b[j].first<a[i].first){r=b[j].first;x=-b[j++].second;}else{r=a[i].first;x=a[i++].second-b[j++].second;}if(x < -bound || x > bound)return false;if(x)o.emplace_back(r,x);}return true;}
static std::pair<int,int> choose(const S&v,const std::array<std::array<std::vector<int>,2>,912>&idx){int row=-1,sign=0,mag=-1;size_t size=0;for(auto [r,x]:v){int s=x>0,m=std::abs(int(x));size_t z=idx[r][s].size();if(m>mag||(m==mag&&z<size)){row=r;sign=s;mag=m;size=z;}}return {row,sign};}
int main(int argc,char**argv){
 int qb=argc>2?std::atoi(argv[2]):0,qe=argc>3?std::atoi(argv[3]):228;
 std::ifstream in(argv[1]);int n;in>>n;std::vector<std::array<int,4>>tc(n);std::vector<std::vector<int>>g(228);for(int c=0;c<n;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::vector<M>moves;std::unordered_map<uint64_t,std::vector<int>>byhash;std::array<std::array<std::vector<int>,2>,912>idx;std::vector<uint8_t>low(1<<24);
 for(int q=0;q<228;++q)for(int p:g[q])for(int m:g[q])if(p!=m){S v=vec(tc,{p},{m});if(v.empty()){std::cerr<<"zero single swap\n";return 5;}uint64_t hv=hashv(v);int k=moves.size();moves.push_back({q,v,hv});byhash[hv].push_back(k);low[hv&((1<<24)-1)]=1;for(auto [r,x]:v)idx[r][x>0].push_back(k);}
 for(int i=0;i<int(moves.size());++i){S opposite=neg(moves[i].v);auto f=byhash.find(uint64_t(0)-moves[i].h);if(f==byhash.end())continue;for(int j:f->second)if(moves[j].q!=moves[i].q&&moves[j].v==opposite){std::cerr<<"cross-Q opposite single swaps\n";return 3;}}
 uint64_t configs=0,first_hits=0,probes=0,low_hits=0,hash_hits=0,exact_checks=0;S r1,r2;
 for(int q=qb;q<qe;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)for(int d=0;d<13;++d){if(d==a||d==b||d==c)continue;for(int e=d+1;e<13;++e){if(e==a||e==b||e==c)continue;for(int f=e+1;f<13;++f){if(f==a||f==b||f==c)continue;++configs;S target=neg(vec(tc,{h[a],h[b],h[c]},{h[d],h[e],h[f]}));if(target.empty()){std::cerr<<"zero triple-swap target\n";return 4;}auto [row1,sign1]=choose(target,idx);for(int i:idx[row1][sign1]){const M&m1=moves[i];if(m1.q==q||!sub(target,m1.v,2,r1))continue;++first_hits;if(r1.empty())continue;uint64_t h1=hashv(r1);auto [row2,sign2]=choose(r1,idx);for(int j:idx[row2][sign2]){const M&m2=moves[j];if(m2.q==q||m2.q==m1.q)continue;++probes;uint64_t hr=h1-m2.h;if(!low[hr&((1<<24)-1)])continue;++low_hits;auto z=byhash.find(hr);if(z==byhash.end())continue;++hash_hits;if(!sub(r1,m2.v,1,r2))continue;for(int k:z->second){++exact_checks;const M&m3=moves[k];if(m3.v!=r2||m3.q==q||m3.q==m1.q||m3.q==m2.q)continue;std::cout<<"FOUND\n";return 0;}}}}}}}
 std::cout<<"NONE q "<<qb<<':'<<qe<<" configs "<<configs<<" first "<<first_hits<<" probes "<<probes<<" low_hits "<<low_hits<<" hash_hits "<<hash_hits<<" exact_checks "<<exact_checks<<"\n";
}
