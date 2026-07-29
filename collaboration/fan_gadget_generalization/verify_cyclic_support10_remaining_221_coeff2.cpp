#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using S=std::vector<std::pair<int16_t,int8_t>>;
struct M{int q;S v;};
static std::string key(const S&v){std::string s;for(auto [r,x]:v){s+=char(r&255);s+=char(r>>8);s+=char(x+4);}return s;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){
 std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}
 std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;
}
static S neg(S v){for(auto&x:v)x.second=-x.second;return v;}
static bool sub(const S&a,const S&b,S&o){o.clear();size_t i=0,j=0;while(i<a.size()||j<b.size()){int r,x;if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){r=a[i].first;x=a[i++].second;}else if(i==a.size()||b[j].first<a[i].first){r=b[j].first;x=-b[j++].second;}else{r=a[i].first;x=a[i++].second-b[j++].second;}if(x < -1 || x > 1)return false;if(x)o.emplace_back(r,x);}return true;}
static int slot(int x){return x==-2?0:x==-1?1:x==1?2:3;}
int main(int argc,char**argv){
 std::ifstream in(argv[1]);int n;in>>n;std::vector<std::array<int,4>>tc(n);std::vector<std::vector<int>>g(228);for(int c=0;c<n;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::unordered_map<std::string,int> singles;for(int q=0;q<228;++q)for(int p:g[q])for(int m:g[q])if(p!=m){S v=vec(tc,{p},{m});if(!singles.emplace(key(v),q).second)return 2;}
 std::vector<M>doubles;std::array<std::array<std::vector<int>,4>,912>idx;
 for(int q=0;q<228;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=0;c<13;++c){if(c==a||c==b)continue;for(int d=c+1;d<13;++d){if(d==a||d==b)continue;S v=vec(tc,{h[a],h[b]},{h[c],h[d]});int k=doubles.size();doubles.push_back({q,v});for(auto [r,x]:v)idx[r][slot(x)].push_back(k);}}}
 uint64_t outer=0,candidates=0,lookups=0;S residual;
 for(const M&a:doubles){int row=-1,t=0;for(auto [r,x]:a.v)if(std::abs(int(x))==2){row=r;t=-x;break;}if(row<0)continue;++outer;
  for(int coefficient:{t,t/2})for(int bi:idx[row][slot(coefficient)]){const M&b=doubles[bi];if(b.q==a.q)continue;++candidates;if(!sub(neg(a.v),b.v,residual))continue;++lookups;auto f=singles.find(key(residual));if(f!=singles.end()&&f->second!=a.q&&f->second!=b.q){std::cout<<"FOUND\n";return 0;}}
 }
 std::cout<<"NONE coeff2_double_swaps "<<outer<<" candidate_double_checks "<<candidates<<" exact_single_lookups "<<lookups<<"\n";
}
