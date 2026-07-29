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
struct M{int q;std::vector<int>p,n;S v;uint64_t h;};
static uint64_t w(int r){uint64_t z=uint64_t(r)+0x9e3779b97f4a7c15ULL;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;return z^(z>>31);}
static uint64_t hv(const S&v){uint64_t h=0;for(auto[r,x]:v)h+=uint64_t(int64_t(x))*w(r);return h;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){std::array<int8_t,912>c{};std::vector<int>t;for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;}
static S neg(S v){for(auto&x:v)x.second=-x.second;return v;}
static bool sub(const S&a,const S&b,int bound,S&o){o.clear();size_t i=0,j=0;while(i<a.size()||j<b.size()){int r,x;if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){r=a[i].first;x=a[i++].second;}else if(i==a.size()||b[j].first<a[i].first){r=b[j].first;x=-b[j++].second;}else{r=a[i].first;x=a[i++].second-b[j++].second;}if(x < -bound || x > bound)return false;if(x)o.emplace_back(r,x);}return true;}
static void output(const std::vector<int>&tp,const std::vector<int>&tn,const M&d,const M&s){std::cout<<"FOUND 3+2+1\nP";for(int x:tp)std::cout<<' '<<x;for(int x:d.p)std::cout<<' '<<x;for(int x:s.p)std::cout<<' '<<x;std::cout<<"\nN";for(int x:tn)std::cout<<' '<<x;for(int x:d.n)std::cout<<' '<<x;for(int x:s.n)std::cout<<' '<<x;std::cout<<"\n";}
int main(int argc,char**argv){
 int qb=argc>2?std::atoi(argv[2]):0,qe=argc>3?std::atoi(argv[3]):228;std::ifstream in(argv[1]);int z;in>>z;std::vector<std::array<int,4>>tc(z);std::vector<std::vector<int>>g(228);for(int c=0;c<z;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::vector<M>single,dbl;std::array<std::array<std::vector<int>,2>,912>si,di;std::unordered_map<uint64_t,std::vector<int>>sb,db;std::vector<uint8_t>slow(1<<24),dlow(1<<24);
 for(int q=0;q<228;++q)for(int p:g[q])for(int n:g[q])if(p!=n){S v=vec(tc,{p},{n});if(v.empty()){std::cerr<<"zero single swap\n";return 3;}uint64_t h=hv(v);int k=single.size();single.push_back({q,{p},{n},v,h});sb[h].push_back(k);slow[h&((1<<24)-1)]=1;for(auto[r,x]:v)si[r][x>0].push_back(k);}
 for(int q=0;q<228;++q){const auto&x=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=0;c<13;++c){if(c==a||c==b)continue;for(int d=c+1;d<13;++d){if(d==a||d==b)continue;std::vector<int>p{x[a],x[b]},n{x[c],x[d]};S v=vec(tc,p,n);if(v.empty()){std::cerr<<"zero double swap\n";return 4;}uint64_t h=hv(v);int k=dbl.size();dbl.push_back({q,p,n,v,h});db[h].push_back(k);dlow[h&((1<<24)-1)]=1;for(auto[r,y]:v)di[r][y>0].push_back(k);}}}
 uint64_t configs=0,sprobes=0,dprobes=0,slowhits=0,dlowhits=0,shash=0,dhash=0,checks=0;S residual;
 for(int q=qb;q<qe;++q){const auto&x=g[q];for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)for(int d=0;d<13;++d){if(d==a||d==b||d==c)continue;for(int e=d+1;e<13;++e){if(e==a||e==b||e==c)continue;for(int f=e+1;f<13;++f){if(f==a||f==b||f==c)continue;++configs;std::vector<int>tp{x[a],x[b],x[c]},tn{x[d],x[e],x[f]};S target=neg(vec(tc,tp,tn));if(target.empty()){std::cerr<<"zero triple-swap target\n";return 5;}uint64_t th=hv(target);int row=-1,sign=0,mag=-1;size_t cost=0;for(auto[r,y]:target){int ss=y>0,m=std::abs(int(y));size_t zc=si[r][ss].size()+di[r][ss].size();if(m>mag||(m==mag&&zc<cost)){row=r;sign=ss;mag=m;cost=zc;}}
  for(int ix:si[row][sign]){const M&s=single[ix];if(s.q==q)continue;++sprobes;uint64_t rh=th-s.h;if(!dlow[rh&((1<<24)-1)])continue;++dlowhits;auto it=db.find(rh);if(it==db.end())continue;++dhash;if(!sub(target,s.v,2,residual))continue;for(int j:it->second){++checks;const M&dd=dbl[j];if(dd.v!=residual||dd.q==q||dd.q==s.q)continue;output(tp,tn,dd,s);return 0;}}
  for(int ix:di[row][sign]){const M&dd=dbl[ix];if(dd.q==q)continue;++dprobes;uint64_t rh=th-dd.h;if(!slow[rh&((1<<24)-1)])continue;++slowhits;auto it=sb.find(rh);if(it==sb.end())continue;++shash;if(!sub(target,dd.v,1,residual))continue;for(int j:it->second){++checks;const M&s=single[j];if(s.v!=residual||s.q==q||s.q==dd.q)continue;output(tp,tn,dd,s);return 0;}}
 }}}}
 std::cout<<"NONE q "<<qb<<':'<<qe<<" configs "<<configs<<" single_probes "<<sprobes<<" double_probes "<<dprobes<<" single_low "<<slowhits<<" double_low "<<dlowhits<<" single_hash "<<shash<<" double_hash "<<dhash<<" exact_checks "<<checks<<"\n";
}
