#ifndef CORE_H
#define CORE_H

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include <math.h>
#include <bitset>


using namespace std;


class Genetic_algorithm {
    float xmin;
    float xmax;
    float zmin;
    float zmax;

    float mutat;//вероятность мутации
    //int gener_count;//число поколений - сколько раз мы будем отсеивать детей
    int population_count;//население
    float prob;//вероятность скрещивания


    vector<vector<float>> data;//храним пары {x,y}
    vector<float> res;//храним результаты из функции

    //турнирная селекция
    void tournament_selection();

    //заполняет популяцию парами x,y;
    //заполняет вектор значениями функции от каждой пары x,y из data
    void fill_data();//(vector<vector<float>>& data, int pop,

    //значение функции
    float function(float x, float z);

    bool lam(int v, int u);

    bool kill(vector<float> c1, vector<float> c2);

    //кроссинговер
    void crossing_over(vector<float>& cop1, vector<float>& cop2);

    //мутация
    float mutation(float c);

    //по желанию
    /**
     * @brief inversion
     * @param c
     * @return
     */
    float inversion(float c);
public:

    //тут мы передадим первые данные и заполним массив data
    Genetic_algorithm(float xmin, float xmax, float zmin, float zmax, float m, int pop_c, float prob)
        : xmin(xmin), xmax(xmax), zmin(zmin), zmax(zmax), mutat(m), population_count(pop_c), prob(prob) {

        fill_data();
    }

    void search_best();//поиск родителей для скрещивания

    vector<float> result();
};

#endif // CORE_H
