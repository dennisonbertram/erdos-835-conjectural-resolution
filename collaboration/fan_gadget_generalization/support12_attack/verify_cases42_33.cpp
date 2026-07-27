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
struct R{int q;std::vector<int>p,n;};
static std::string key(const S&v,bool neg=false){std::string s;for(auto[r,x]:v){s+=char(r&255);s+=char(r>>8);s+=char((neg?-x:x)+6);}return s;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;}
static void found(const char*name,const R&a,const R&b){std::cout<<"FOUND "<<name<<"\nP";for(int x:a.p)std::cout<<' '<<x;for(int x:b.p)std::cout<<' '<<x;std::cout<<"\nN";for(int x:a.n)std::cout<<' '<<x;for(int x:b.n)std::cout<<' '<<x;std::cout<<"\nQ "<<a.q<<' '<<b.q<<"\n";}
int main(int argc,char**argv){
 (void)argc;
 std::ifstream in(argv[1]);int z;in>>z;std::vector<std::array<int,4>>tc(z);std::vector<std::vector<int>>g(228);for(int c=0;c<z;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::unordered_map<std::string,std::vector<R>>doubles;uint64_t dcount=0;
  for(int q=0;q<228;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=0;c<13;++c){if(c==a||c==b)continue;for(int d=c+1;d<13;++d){if(d==a||d==b)continue;++dcount;std::vector<int>p{h[a],h[b]},n{h[c],h[d]};doubles[key(vec(tc,p,n))].push_back(R{q,p,n});}}}
 uint64_t four=0,bounded=0;
 for(int q=0;q<228;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)for(int d=c+1;d<13;++d)
  for(int e=0;e<13;++e){if(e==a||e==b||e==c||e==d)continue;for(int f=e+1;f<13;++f){if(f==a||f==b||f==c||f==d)continue;for(int i=f+1;i<13;++i){if(i==a||i==b||i==c||i==d)continue;for(int j=i+1;j<13;++j){if(j==a||j==b||j==c||j==d)continue;++four;std::vector<int>p{h[a],h[b],h[c],h[d]},n{h[e],h[f],h[i],h[j]};S v=vec(tc,p,n);bool ok=true;for(auto[r,x]:v)if(std::abs(int(x))>2)ok=false;if(!ok)continue;++bounded;auto k=doubles.find(key(v,true));if(k!=doubles.end())for(const R&other:k->second)if(other.q!=q){found("4+2",R{q,p,n},other);return 0;}}}}}
 }
 std::unordered_map<std::string,std::vector<R>>triples;uint64_t triples_count=0;
 for(int q=0;q<228;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)for(int d=0;d<13;++d){if(d==a||d==b||d==c)continue;for(int e=d+1;e<13;++e){if(e==a||e==b||e==c)continue;for(int f=e+1;f<13;++f){if(f==a||f==b||f==c)continue;++triples_count;std::vector<int>p{h[a],h[b],h[c]},n{h[d],h[e],h[f]};S v=vec(tc,p,n);auto k=triples.find(key(v,true));if(k!=triples.end())for(const R&other:k->second)if(other.q!=q){found("3+3",R{q,p,n},other);return 0;}triples[key(v)].push_back(R{q,p,n});}}}}
 std::cout<<"NONE doubles "<<dcount<<" case42 "<<four<<" bounded "<<bounded<<" case33 "<<triples_count<<" vectors "<<triples.size()<<"\n";
}
