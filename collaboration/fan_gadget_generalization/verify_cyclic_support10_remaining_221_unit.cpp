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
struct M{int q;S v;};
struct Qs{int a=-1,b=-1,c=-1;};
static std::string key(const S&v){std::string s;for(auto [r,x]:v){s+=char(r&255);s+=char(r>>8);s+=char(x+3);}return s;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){
 std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}
 std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;
}
static bool target(const S&a,const S&s,S&b){
 b.clear();size_t i=0,j=0;while(i<a.size()||j<s.size()){int r,x;if(j==s.size()||(i<a.size()&&a[i].first<s[j].first)){r=a[i].first;x=-a[i++].second;}else if(i==a.size()||s[j].first<a[i].first){r=s[j].first;x=-s[j++].second;}else{r=a[i].first;x=-a[i++].second-s[j++].second;}if(x < -1 || x > 1)return false;if(x)b.emplace_back(r,x);}return b.size()<=16;
}
int main(int argc,char**argv){
 int begin=argc>2?std::atoi(argv[2]):0,end=argc>3?std::atoi(argv[3]):35568;
 std::ifstream in(argv[1]);int n;in>>n;std::vector<std::array<int,4>>tc(n);std::vector<std::vector<int>>g(228);for(int c=0;c<n;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::vector<M>singles;for(int q=0;q<228;++q)for(int p:g[q])for(int m:g[q])if(p!=m){S v=vec(tc,{p},{m});if(v.size()!=6&&v.size()!=8)return 4;singles.push_back({q,v});}
 std::vector<M>doubles;std::unordered_map<std::string,Qs>by;std::array<std::array<std::vector<int>,2>,912>post;
 for(int q=0;q<228;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=0;c<13;++c){if(c==a||c==b)continue;for(int d=c+1;d<13;++d){if(d==a||d==b)continue;S v=vec(tc,{h[a],h[b]},{h[c],h[d]});bool unit=true;for(auto [r,x]:v)if(std::abs(int(x))!=1)unit=false;if(!unit)continue;if(v.size()!=10&&v.size()!=12&&v.size()!=14&&v.size()!=16)return 5;int k=doubles.size();doubles.push_back({q,v});Qs&z=by[key(v)];if(z.a<0)z.a=q;else if(z.a!=q&&z.b<0)z.b=q;else if(z.a!=q&&z.b!=q&&z.c<0)z.c=q;for(auto [r,x]:v)post[r][x>0].push_back(k);}}}
 std::vector<uint8_t>count(doubles.size());std::vector<int>touched;S bvec;uint64_t posting_hits=0,candidates=0,lookups=0,zero_threshold=0;
 end=std::min(end,int(singles.size()));
 for(int si=begin;si<end;++si){const M&s=singles[si];touched.clear();
  for(auto [r,x]:s.v)for(int di:post[r][x<0]){++posting_hits;if(!count[di])touched.push_back(di);++count[di];}
  for(int di:touched){const M&a=doubles[di];int threshold=(int(a.v.size())+int(s.v.size())-16+1)/2;if(count[di]>=threshold&&a.q!=s.q){++candidates;if(target(a.v,s.v,bvec)){++lookups;auto f=by.find(key(bvec));if(f!=by.end()){const Qs&q=f->second;if((q.a!=a.q&&q.a!=s.q)||(q.b>=0&&q.b!=a.q&&q.b!=s.q)||(q.c>=0&&q.c!=a.q&&q.c!=s.q)){std::cout<<"FOUND\n";return 0;}}}}count[di]=0;}
  for(int di=0;di<int(doubles.size());++di){const M&a=doubles[di];if(a.v.size()+s.v.size()>16||a.q==s.q)continue;++zero_threshold;++candidates;if(target(a.v,s.v,bvec)){++lookups;auto f=by.find(key(bvec));if(f!=by.end()){const Qs&q=f->second;if((q.a!=a.q&&q.a!=s.q)||(q.b>=0&&q.b!=a.q&&q.b!=s.q)||(q.c>=0&&q.c!=a.q&&q.c!=s.q)){std::cout<<"FOUND\n";return 0;}}}}
 }
 std::cout<<"NONE singles "<<begin<<':'<<end<<" unit_doubles "<<doubles.size()<<" posting_hits "<<posting_hits<<" candidates "<<candidates<<" exact_lookups "<<lookups<<" zero_threshold "<<zero_threshold<<"\n";
}
