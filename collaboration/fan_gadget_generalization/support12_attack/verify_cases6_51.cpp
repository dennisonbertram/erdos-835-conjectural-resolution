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
struct Qs{int a=-1,b=-1;};
static std::string key(const S&v,bool n=false){std::string s;for(auto [r,x]:v){s+=char(r&255);s+=char(r>>8);s+=char((n?-x:x)+7);}return s;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;}
static std::string sig(const std::vector<std::array<int,4>>&tc,const std::vector<int>&cells){std::vector<int>r;for(int c:cells)for(int x:tc[c])r.push_back(x);std::sort(r.begin(),r.end());std::string s;for(int x:r){s+=char(x&255);s+=char(x>>8);}return s;}
static bool disjoint(const std::vector<int>&a,const std::vector<int>&b){for(int x:a)for(int y:b)if(x==y)return false;return true;}
static void output(const char*name,int q,const std::vector<int>&p,const std::vector<int>&n){std::cout<<"FOUND "<<name<<" q "<<q<<"\nP";for(int x:p)std::cout<<' '<<x;std::cout<<"\nN";for(int x:n)std::cout<<' '<<x;std::cout<<"\n";}
int main(int argc,char**argv){
 (void)argc;
 std::ifstream in(argv[1]);int n;in>>n;std::vector<std::array<int,4>>tc(n);std::vector<std::vector<int>>g(228);for(int c=0;c<n;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 uint64_t six=0,collisions=0;
 for(int q=0;q<228;++q){std::unordered_map<std::string,std::vector<std::vector<int>>>seen;const auto&h=g[q];
  for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)for(int d=c+1;d<13;++d)for(int e=d+1;e<13;++e)for(int f=e+1;f<13;++f){++six;std::vector<int>x{h[a],h[b],h[c],h[d],h[e],h[f]};auto&old=seen[sig(tc,x)];for(const auto&y:old){++collisions;if(disjoint(x,y)){output("6",q,y,x);return 0;}}old.push_back(x);}
 }
 std::unordered_map<std::string,std::vector<int>>single;
 for(int q=0;q<228;++q)for(int p:g[q])for(int m:g[q])if(p!=m)single[key(vec(tc,{p},{m}))].push_back(q);
 uint64_t fivepairs=0,fivebounded=0;
  for(int q=0;q<228;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)for(int d=c+1;d<13;++d)for(int e=d+1;e<13;++e)
  for(int f=0;f<13;++f){if(f==a||f==b||f==c||f==d||f==e)continue;for(int i=f+1;i<13;++i){if(i==a||i==b||i==c||i==d||i==e)continue;for(int j=i+1;j<13;++j){if(j==a||j==b||j==c||j==d||j==e)continue;for(int k=j+1;k<13;++k){if(k==a||k==b||k==c||k==d||k==e)continue;for(int l=k+1;l<13;++l){if(l==a||l==b||l==c||l==d||l==e)continue;++fivepairs;std::vector<int>p{h[a],h[b],h[c],h[d],h[e]},m{h[f],h[i],h[j],h[k],h[l]};S v=vec(tc,p,m);bool unit=true;for(auto[r,x]:v)if(std::abs(int(x))>1)unit=false;if(!unit)continue;++fivebounded;auto z=single.find(key(v,true));if(z!=single.end())for(int other:z->second)if(other!=q){output("5+1",q,p,m);return 0;}}}}}}
 }
 std::cout<<"NONE case6 subsets "<<six<<" collisions "<<collisions<<" case51 configs "<<fivepairs<<" bounded "<<fivebounded<<"\n";
}
