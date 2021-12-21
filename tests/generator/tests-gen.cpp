#include <bits/stdc++.h>
#define file(name) freopen(name".in", "r", stdin); freopen(name".out", "w", stdout);
#define fast ios_base::sync_with_stdio(0); cin.tie(0);
#define x first
#define y second
#define pb push_back
#define mk make_pair
#define all(a) a.begin(), a.end()
#define len(a) (int)a.size()

using namespace std;

typedef long long ll;
typedef vector <int> vi;
typedef pair <int, int> pii;

int main(){
	srand(time(NULL));

	int n = 1000, m = 20000;
	
	for(int i = 0; i < m; i++){
		int a = rand() % n, b = rand() % n;

		cout << (i + 1) % (n + 1) << ',' << (i + 2) % (n + 1)  << ",R," << "R" << endl; 
	}
	
	
	return 0;
}
