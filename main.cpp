// Daniel Phan
// Player Name random stat creator
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

struct Athlete {
    string name;
    int points;
    int assists;
    int rebounds;
};

void displayStats(const Athlete& player) {
    cout << "Player: " << player.name << endl;
    cout << "Points: " << player.points << endl;
    cout << "Assists: " << player.assists << endl;
    cout << "Rebounds: " << player.rebounds << endl;
}

int main() {
    srand(time(0));
    Athlete player;
    cout << "Enter player name: ";
    getline(cin, player.name);
    player.points = rand() % 41;     // 0-40
    player.assists = rand() % 11;    // 0-10
    player.rebounds = rand() % 21;   // 0-20
    displayStats(player);
    return 0;
}
