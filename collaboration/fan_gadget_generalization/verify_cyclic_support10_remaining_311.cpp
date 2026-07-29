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
struct M{int q,p,n;S v;};
static std::string key(const S&v){std::string s;for(auto [r,x]:v){s+=char(r&255);s+=char(r>>8);s+=char(x+4);}return s;}
static S vec(const std::vector<std::array<int,4>>&tc,const std::vector<int>&p,const std::vector<int>&n){
 std::array<int8_t,912> c{};std::vector<int> t;
 for(int x:p)for(int r:tc[x]){if(!c[r])t.push_back(r);++c[r];}
 for(int x:n)for(int r:tc[x]){if(!c[r])t.push_back(r);--c[r];}
 std::sort(t.begin(),t.end());t.erase(std::unique(t.begin(),t.end()),t.end());S v;for(int r:t)if(c[r])v.emplace_back(r,c[r]);return v;
}
static S neg(S v){for(auto&x:v)x.second=-x.second;return v;}
static bool sub(const S&a,const S&b,S&o){
 o.clear();size_t i=0,j=0;while(i<a.size()||j<b.size()){int r,x;
  if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){r=a[i].first;x=a[i++].second;}
  else if(i==a.size()||b[j].first<a[i].first){r=b[j].first;x=-b[j++].second;}
  else{r=a[i].first;x=a[i++].second-b[j++].second;}
  if(x < -1 || x > 1)return false;if(x)o.emplace_back(r,x);
 }return true;
}
int main(int argc,char**argv){
 int qstart=argc>2?std::atoi(argv[2]):0,qend=argc>3?std::atoi(argv[3]):228;
 std::ifstream in(argv[1]);int n;in>>n;std::vector<std::array<int,4>>tc(n);std::vector<std::vector<int>>g(228);
 for(int c=0;c<n;++c){int q;in>>q>>tc[c][0]>>tc[c][1]>>tc[c][2]>>tc[c][3];g[q].push_back(c);}
 std::vector<M> moves;std::unordered_map<std::string,int> by;std::array<std::array<std::vector<int>,2>,912> idx;
 for(int q=0;q<228;++q)for(int p:g[q])for(int m:g[q])if(p!=m){S v=vec(tc,{p},{m});int k=moves.size();moves.push_back({q,p,m,v});if(!by.emplace(key(v),k).second)return 2;for(auto [r,x]:v)idx[r][x>0].push_back(k);}
 uint64_t configs=0,lookups=0;S residual;
 for(int q=qstart;q<qend;++q){const auto&h=g[q];
  for(int pa=0;pa<13;++pa)for(int pb=pa+1;pb<13;++pb)for(int pc=pb+1;pc<13;++pc)
  for(int na=0;na<13;++na){if(na==pa||na==pb||na==pc)continue;
   for(int nb=na+1;nb<13;++nb){if(nb==pa||nb==pb||nb==pc)continue;
    for(int nc=nb+1;nc<13;++nc){if(nc==pa||nc==pb||nc==pc)continue;++configs;
     S target=neg(vec(tc,{h[pa],h[pb],h[pc]},{h[na],h[nb],h[nc]}));
     int row=-1,sign=0,mag=-1;size_t size=0;
     for(auto [r,x]:target){int s=x>0,m=std::abs(int(x));size_t z=idx[r][s].size();if(m>mag||(m==mag&&z<size)){row=r;sign=s;mag=m;size=z;}}
     if(row<0)return 3;
     for(int mi:idx[row][sign]){const M&a=moves[mi];if(a.q==q||!sub(target,a.v,residual))continue;++lookups;auto f=by.find(key(residual));if(f==by.end())continue;const M&b=moves[f->second];if(b.q==q||b.q==a.q)continue;
      std::cout<<"FOUND\nP "<<h[pa]<<' '<<h[pb]<<' '<<h[pc]<<' '<<a.p<<' '<<b.p<<"\nN "<<h[na]<<' '<<h[nb]<<' '<<h[nc]<<' '<<a.n<<' '<<b.n<<"\n";return 0;
     }
    }
   }
  }
  if(q%16==0)std::cerr<<"q "<<q<<"\n";
 }
 std::cout<<"NONE configurations "<<configs<<" lookups "<<lookups<<"\n";
}
