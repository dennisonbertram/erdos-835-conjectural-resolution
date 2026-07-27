#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <utility>
#include <vector>
using S=std::vector<std::pair<int16_t,int8_t>>;
struct M{int q;std::array<int,4> cells;S v;uint64_t h;};
static uint64_t w(int r){uint64_t z=uint64_t(r)+0x9e3779b97f4a7c15ULL;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static uint64_t hv(const S&v){uint64_t h=0;for(auto[r,x]:v)h+=uint64_t(int64_t(x))*w(r);return h;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;}
static bool sumzero(const S&a,const S&b,const S&c){std::array<int8_t,912>x{};for(auto[r,z]:a)x[r]+=z;for(auto[r,z]:b)x[r]+=z;for(auto[r,z]:c)x[r]+=z;for(int z:x)if(z)return false;return true;}
int main(int argc,char**argv){
 int qb=argc>2?std::atoi(argv[2]):0,qe=argc>3?std::atoi(argv[3]):228;std::ifstream in(argv[1]);int z;in>>z;std::vector<std::array<int,4>>tc(z);std::vector<std::vector<int>>g(228);for(int c=0;c<z;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::vector<M>m;std::vector<std::vector<int>>qm(228);std::array<std::array<std::vector<int>,2>,912>idx;std::unordered_map<uint64_t,std::vector<int>>by;std::vector<uint8_t>low(1<<24);
 for(int q=0;q<228;++q){const auto&h=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=0;c<13;++c){if(c==a||c==b)continue;for(int d=c+1;d<13;++d){if(d==a||d==b)continue;S v=vec(tc,{h[a],h[b]},{h[c],h[d]});if(v.empty()){std::cerr<<"zero double swap\n";return 3;}uint64_t x=hv(v);int k=m.size();m.push_back({q,{h[a],h[b],h[c],h[d]},v,x});qm[q].push_back(k);by[x].push_back(k);low[x&((1<<24)-1)]=1;for(auto[r,y]:v)idx[r][y>0].push_back(k);}}}
 uint64_t outer=0,probes=0,lowhits=0,hashhits=0,checks=0;
 for(int q=qb;q<qe;++q)for(int ai:qm[q]){++outer;const M&a=m[ai];auto [row,x]=a.v.front();int sign=x<0;for(int bi:idx[row][sign]){const M&b=m[bi];if(b.q<=q)continue;++probes;uint64_t target=uint64_t(0)-a.h-b.h;if(!low[target&((1<<24)-1)])continue;++lowhits;auto f=by.find(target);if(f==by.end())continue;++hashhits;for(int ci:f->second){++checks;const M&c=m[ci];if(c.q<=q||c.q==b.q||!sumzero(a.v,b.v,c.v))continue;std::cout<<"FOUND 2+2+2 q "<<q<<' '<<b.q<<' '<<c.q<<"\nP "<<a.cells[0]<<' '<<a.cells[1]<<' '<<b.cells[0]<<' '<<b.cells[1]<<' '<<c.cells[0]<<' '<<c.cells[1]<<"\nN "<<a.cells[2]<<' '<<a.cells[3]<<' '<<b.cells[2]<<' '<<b.cells[3]<<' '<<c.cells[2]<<' '<<c.cells[3]<<"\n";return 0;}}}
 std::cout<<"NONE q "<<qb<<':'<<qe<<" outer "<<outer<<" probes "<<probes<<" low_hits "<<lowhits<<" hash_hits "<<hashhits<<" exact_checks "<<checks<<"\n";
}
