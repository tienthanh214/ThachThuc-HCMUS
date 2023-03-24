#include <iostream>
#include <vector>

using namespace std;

#define HORIZONTAL 0
#define VERTICAL 1
#define MAIN_DIAGONAL 2
#define SUB_DIAGONAL 3

int check_symmetry(vector<vector<int>> map, int mode) {
    int M = map.size() - 1, N = map[0].size() - 1;
    bool is_horizontal = true;
    bool is_vertical = true;
    bool is_main_diagonnal = M != N;
    bool is_sub_diagonnal = M != N;
    for (int i = 1; i <= M; i++)
        for (int j = 1; j <= N; j++) {
            if (is_horizontal && map[i][j] != map[i][N + 1 - j])
                is_horizontal = false;
            if (is_vertical && map[i][j] != map[M + 1 - i][j])
                is_horizontal = false;
            if (is_main_diagonnal && map[i][j] != map[j][i])
                is_main_diagonnal = false;
            if (is_sub_diagonnal && map[i][j] != map[N + 1 - j][M + 1 - i])
                is_sub_diagonnal = false;
            if (is_horizontal + is_vertical + is_main_diagonnal + is_sub_diagonnal <= 1) {
                if (is_horizontal) return HORIZONTAL;
                if (is_vertical) return VERTICAL;
                if (is_main_diagonnal) return MAIN_DIAGONAL;
                if (is_sub_diagonnal) return SUB_DIAGONAL;
                return -1;
            }
        }
}

int main() {
}
