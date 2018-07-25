// Note: This code compiles, but does not output the correct results

#include <iostream>
#include <vector>
#include <string>
using namespace std;

vector<double> sense(vector<double> p, string Z, vector<string> world, double pHit, double pMiss) {
  vector<double> q;
  for (int i = 0; i < p.size(); ++i) {
    if (Z.compare(world[i]) == 0) {
      q.push_back(p[i] * pHit);
    } 
    else {
      q.push_back(p[i] * pMiss);
    }
  }

  int s = 0;
  for (int i = 0; i < q.size(); ++i) {
    s += q[i];
  }

  for (int i = 0; i < q.size(); ++i) {
    q[i] /= s;
  }

  return q;

}

vector<double> move(vector<double> p, int U, vector<string> world, double pExact, double pOvershoot, double pUndershoot) {
  vector<double> q;
  double s;
  for (int i = 0; i < p.size(); ++i) {
    s = pExact * p[(i-U) % p.size()];
    s += pOvershoot * p[(i-U-1) % p.size()];
    s += pUndershoot * p[(i-U+1) % p.size()];
    q.push_back(s);
  }

  return q;
}

int main() {
  vector<double> p(5, 0.2);

  vector<string> world;
  world.push_back("green");
  world.push_back("red");
  world.push_back("red");
  world.push_back("green");
  world.push_back("green");

  vector<string> measurements;
  measurements.push_back("red");
  measurements.push_back("green");

  vector<int> motions(2,1);

  double pHit = 0.6;
  double pMiss = 0.2;
  double pExact = 0.8;
  double pOvershoot = 0.1;
  double pUndershoot = 0.1;

  for (int k = 0; k < measurements.size(); ++k) {
    p = sense(p, measurements[k], world, pHit, pMiss);
    p = move(p, motions[k], world, pExact, pOvershoot, pUndershoot);
  }

  for (int i = 0; i < p.size(); ++i) {
    cout << p[i] << endl;
  }

  return 0;
}