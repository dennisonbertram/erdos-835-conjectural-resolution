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
struct M{int q,p,n;S v;uint64_t h;};
static uint64_t w(int r){uint64_t z=uint64_t(r)+0x9e3779b97f4a7c15ULL;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static uint64_t hv(const S&v){uint64_t h=0;for(auto[r,x]:v)h+=uint64_t(int64_t(x))*w(r);return h;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;}
static S neg(S v){for(auto&x:v)x.second=-x.second;return v;}
static bool sub(const S&a,const S&b,S&o){o.clear();size_t i=0,j=0;while(i<a.size()||j<b.size()){int r,x;if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){r=a[i].first;x=a[i++].second;}else if(i==a.size()||b[j].first<a[i].first){r=b[j].first;x=-b[j++].second;}else{r=a[i].first;x=a[i++].second-b[j++].second;}if(x < -1 || x > 1)return false;if(x)o.emplace_back(r,x);}return true;}
int main(int argc,char**argv){
 int qb=argc>2?std::atoi(argv[2]):0,qe=argc>3?std::atoi(argv[3]):228;std::ifstream in(argv[1]);int z;in>>z;std::vector<std::array<int,4>>tc(z);std::vector<std::vector<int>>g(228);for(int c=0;c<z;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::vector<M>m;std::array<std::array<std::vector<int>,2>,912>idx;std::unordered_map<uint64_t,std::vector<int>>by;std::vector<uint8_t>low(1<<24);for(int q=0;q<228;++q)for(int p:g[q])for(int n:g[q])if(p!=n){S v=vec(tc,{p},{n});if(v.empty()){std::cerr<<"zero single swap\n";return 4;}uint64_t h=hv(v);int k=m.size();m.push_back({q,p,n,v,h});by[h].push_back(k);low[h&((1<<24)-1)]=1;for(auto[r,x]:v)idx[r][x>0].push_back(k);}
 uint64_t configs=0,first=0,probes=0,lowhits=0,hashhits=0,checks=0;S residual;
 for(int q=qb;q<qe;++q){const auto&gq=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)for(int d=c+1;d<13;++d)for(int e=0;e<13;++e){if(e==a||e==b||e==c||e==d)continue;for(int f=e+1;f<13;++f){if(f==a||f==b||f==c||f==d)continue;for(int i=f+1;i<13;++i){if(i==a||i==b||i==c||i==d)continue;for(int j=i+1;j<13;++j){if(j==a||j==b||j==c||j==d)continue;++configs;std::vector<int>p{gq[a],gq[b],gq[c],gq[d]},n{gq[e],gq[f],gq[i],gq[j]};S target=neg(vec(tc,p,n));if(target.empty()){std::cerr<<"zero four-swap target\n";return 3;}int row=-1,sign=0,mag=-1;size_t size=0;for(auto[r,x]:target){int s=x>0,mm=std::abs(int(x));size_t zz=idx[r][s].size();if(mm>mag||(mm==mag&&zz<size)){row=r;sign=s;mag=mm;size=zz;}}for(int mi:idx[row][sign]){const M&a1=m[mi];if(a1.q==q)continue;++first;uint64_t rh=hv(target)-a1.h;++probes;if(!low[rh&((1<<24)-1)])continue;++lowhits;auto it=by.find(rh);if(it==by.end())continue;++hashhits;if(!sub(target,a1.v,residual))continue;for(int ni:it->second){++checks;const M&a2=m[ni];if(a2.v!=residual||a2.q==q||a2.q==a1.q)continue;std::cout<<"FOUND 4+1+1\nP";for(int x:p)std::cout<<' '<<x;std::cout<<' '<<a1.p<<' '<<a2.p<<"\nN";for(int x:n)std::cout<<' '<<x;std::cout<<' '<<a1.n<<' '<<a2.n<<"\nQ "<<q<<' '<<a1.q<<' '<<a2.q<<"\n";return 0;}}}}}}}
 std::cout<<"NONE q "<<qb<<':'<<qe<<" configs "<<configs<<" first "<<first<<" probes "<<probes<<" low_hits "<<lowhits<<" hash_hits "<<hashhits<<" exact_checks "<<checks<<"\n";
}
