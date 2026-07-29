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
struct M{int q;S v;uint64_t h;};
static uint64_t weight(int r){uint64_t z=uint64_t(r)+0x9e3779b97f4a7c15ULL;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static uint64_t hashv(const S&v){uint64_t h=0;for(auto [r,x]:v)h+=uint64_t(int64_t(x))*weight(r);return h;}
static S diff(const std::vector<std::array<int,4>>&tc,int p,int n){std::array<int8_t,912>c{};for(int r:tc[p])++c[r];for(int r:tc[n])--c[r];S v;for(int r=0;r<912;++r)if(c[r])v.emplace_back(r,c[r]);return v;}
static S neg(S v){for(auto&x:v)x.second=-x.second;return v;}
static bool add(const S&a,const S&b,int bound,S&o){o.clear();size_t i=0,j=0;while(i<a.size()||j<b.size()){int r,x;if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){r=a[i].first;x=a[i++].second;}else if(i==a.size()||b[j].first<a[i].first){r=b[j].first;x=b[j++].second;}else{r=a[i].first;x=a[i++].second+b[j++].second;}if(x < -bound || x > bound)return false;if(x)o.emplace_back(r,x);}return true;}
static std::pair<int,int> choose(const S&v,const std::array<std::array<std::vector<int>,2>,912>&idx){int row=-1,sign=0,mag=-1;size_t size=0;for(auto [r,x]:v){int s=x<0,m=std::abs(int(x));size_t z=idx[r][s].size();if(m>mag||(m==mag&&z<size)){row=r;sign=s;mag=m;size=z;}}return {row,sign};}
int main(int argc,char**argv){
 int qb=argc>2?std::atoi(argv[2]):0,qe=argc>3?std::atoi(argv[3]):228;
 std::ifstream in(argv[1]);int n;in>>n;std::vector<std::array<int,4>>tc(n);std::vector<std::vector<int>>g(228);for(int c=0;c<n;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::vector<M>moves;std::vector<std::vector<int>>qm(228);std::unordered_map<uint64_t,std::vector<int>>by;std::array<std::array<std::vector<int>,2>,912>idx;std::vector<uint8_t>low(1<<24);
 for(int q=0;q<228;++q)for(int p:g[q])for(int m:g[q])if(p!=m){S v=diff(tc,p,m);uint64_t hv=hashv(v);int k=moves.size();moves.push_back({q,v,hv});qm[q].push_back(k);by[hv].push_back(k);low[hv&((1<<24)-1)]=1;for(auto [r,x]:v)idx[r][x>0].push_back(k);}
 uint64_t seconds=0,thirds=0,probes=0,lowhits=0,hashhits=0,checks=0;S s2,s3,s4;
 for(int q=qb;q<qe;++q)for(int i:qm[q]){const M&a=moves[i];auto [r1,z1]=choose(a.v,idx);for(int j:idx[r1][z1]){const M&b=moves[j];if(b.q<=q||!add(a.v,b.v,3,s2))continue;++seconds;if(s2.empty())continue;auto [r2,z2]=choose(s2,idx);for(int k:idx[r2][z2]){const M&c=moves[k];if(c.q<=q||c.q==b.q||!add(s2,c.v,2,s3))continue;++thirds;if(s3.empty())continue;uint64_t h3=hashv(s3);auto [r3,z3]=choose(s3,idx);for(int l:idx[r3][z3]){const M&d=moves[l];if(d.q<=q||d.q==b.q||d.q==c.q)continue;++probes;uint64_t hr=uint64_t(0)-h3-d.h;if(!low[hr&((1<<24)-1)])continue;++lowhits;auto f=by.find(hr);if(f==by.end())continue;++hashhits;if(!add(s3,d.v,1,s4))continue;S wanted=neg(s4);for(int eidx:f->second){++checks;const M&e=moves[eidx];if(e.v!=wanted||e.q<=q||e.q==b.q||e.q==c.q||e.q==d.q)continue;std::cout<<"FOUND\n";return 0;}}}}}
 std::cout<<"NONE q "<<qb<<':'<<qe<<" second "<<seconds<<" third "<<thirds<<" probes "<<probes<<" low_hits "<<lowhits<<" hash_hits "<<hashhits<<" exact_checks "<<checks<<"\n";
}
