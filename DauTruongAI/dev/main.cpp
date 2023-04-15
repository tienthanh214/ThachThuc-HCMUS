#include <iostream>
#include <vector>
#include <fstream>
#include <random>
#include <queue>
#include <set>
#include <chrono>
#include <cstring>
#include <cassert>
#include <algorithm>

using namespace std;
/* --------- constant definition --------- */
const int MAX_N = 15 + 2;

const int HORIZONTAL = 0;
const int VERTICAL = 1;
const int MAIN_DIAGONAL = 2;
const int SUB_DIAGONAL = 3;

const int SHIELD = -1;
const int DANGEROUS = -2;
const int OUT_OF_MAP = -10;
const int MIN_SCORE_TO_WIN = 58;

const short INF = 0x3f3f;

const int dx[] = {-1, 1, 0, 0};
const int dy[] = {0, 0, -1, 1};

/*  for random feature  */
static std::mt19937_64 rng(
    std::chrono::system_clock::now().time_since_epoch().count());

/* for debug */
void print() {
    cerr << endl;
}
template<typename First, typename ... Strings>
void print(First arg, const Strings&... rest) {
    cerr << arg << " ";
    print(rest...);
}

// -------------------------------
struct MapInfo {
    int M;
    int N;
    int K;
    int max_K;
    int map[17][17]; // -1 : Shield, -2: Dangerous
    int symmetry_type;

    bool checkInside(int x, int y) {
        return 1 <= x && x <= M && 1 <= y && y <= N;
    }
};

int checkSymmetry(MapInfo &map_info) {
    int M = map_info.M, N = map_info.N;
    bool is_horizontal = true;
    bool is_vertical = true;
    bool is_main_diagonal = M == N;
    bool is_sub_diagonal = M == N;
    for (int i = 1; i <= M; i++)
        for (int j = 1; j <= N; j++) {
            if (is_horizontal && map_info.map[i][j] != map_info.map[i][N + 1 - j])
                is_horizontal = false;
            if (is_vertical && map_info.map[i][j] != map_info.map[M + 1 - i][j])
                is_vertical = false;
            if (is_main_diagonal && map_info.map[i][j] != map_info.map[j][i])
                is_main_diagonal = false;
            if (is_sub_diagonal && map_info.map[i][j] != map_info.map[N + 1 - j][M + 1 - i])
                is_sub_diagonal = false;
            if (is_horizontal + is_vertical + is_main_diagonal + is_sub_diagonal <= 1) {
                if (is_horizontal) return HORIZONTAL;
                if (is_vertical) return VERTICAL;
                if (is_main_diagonal) return MAIN_DIAGONAL;
                if (is_sub_diagonal) return SUB_DIAGONAL;
                return -1; // map isn't symmetric
            }
        }
    if (is_horizontal) return HORIZONTAL;
    if (is_vertical) return VERTICAL;
    if (is_main_diagonal) return MAIN_DIAGONAL;
    if (is_sub_diagonal) return SUB_DIAGONAL;
    return -2; // code bug (must never happen)
}


class BaseSolution {
public:
    virtual void run() = 0;
};

int main() {

    return 0;
}