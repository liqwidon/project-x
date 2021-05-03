#include "core.h"

void Genetic_algorithm::fill_data() {

    float stepx = (xmax-xmin)/population_count;//шаг по оси х
    float stepz = (zmax-zmin)/population_count;//шаг по оси y
    data.clear();
    res.clear();

    for (size_t idx = 0; idx < population_count; idx++) {

        data.push_back({xmin + stepx * idx, zmin + stepz * idx});
        res.push_back(function(data[idx][0],data[idx][1]));
    }
}

//возвращает значение искомой функции
float Genetic_algorithm::function(float x, float z) {

    return float(-(x*x+z*z));
    //return float(x/(x*x+2*z*z+1));
}

//убивает детей, которые не удовлетворяют условию
bool Genetic_algorithm::kill(vector<float> c1, vector<float> c2) {

    if (c1[0] > xmax || c1[0] < xmin || c1[1] > zmax || c1[1] < zmin || c2[0] > xmax || c2[0] < xmin || c2[1] > zmax || c2[1] < zmin)
        return true;
    else return false;
}

void Genetic_algorithm::tournament_selection() {

    vector<vector<float>> buff;
    vector<float> rb;

    while(buff.size() != population_count) {

        size_t t1 = rand() % data.size(),
                t2 = rand() % data.size();

        if (res[t1] > res[t2]) {

            buff.push_back(data[t1]);
            rb.push_back(res[t1]);

            swap(data[t1],data.back());
            swap(res[t1],res.back());
            data.pop_back();
            res.pop_back();
        }
        else {

            buff.push_back(data[t2]);
            rb.push_back(res[t2]);

            swap(data[t2],data.back());
            swap(res[t2],res.back());
            data.pop_back();
            res.pop_back();
        }
    }

    data = buff;
    res = rb;
}


void Genetic_algorithm::search_best() {

    vector<bool> color(data.size(),false);//закрашиваем тех, кого скрестили
    //используем случайный выбор для кроссинговера
    for (size_t k = 0; k < population_count; k++) {

        size_t j = rand() % population_count, i = rand() % population_count;

        if (color[i] == false) {

            vector<float> b1 = data[j], b2 = data[i];
            crossing_over(b1,b2);

            if (kill(b1,b2) == false) {

                data.push_back(b1);
                data.push_back(b2);
                res.push_back(function(b1[0],b1[1]));
                res.push_back(function(b2[0],b2[1]));
            }
            color[i] = true;
            color[j] = true;
        }
    }

    //после скрещивания надо провести отбор
    tournament_selection();
}

//мутация
float Genetic_algorithm::mutation(float c) {

    union {

        float in;
        unsigned long out;
    }data;

    data.in = c;

    bitset<sizeof(float) * CHAR_BIT> bits(data.out);

    float pred = rand() % 1000 / 1000;

    if (pred < mutat) {

        size_t idx = rand() % 31;
        (bits[idx] == 1) ? bits.set(idx,0) : bits.set(idx,1);
        data.out = bits.to_ulong();
    }

    return data.in;
}

void Genetic_algorithm::crossing_over(vector<float>& cop1, vector<float>& cop2) {

    for (size_t i=0;i<2;i++) {

        union {

            float in;
            unsigned long out;
        }data1;

        union {

            float in;
            unsigned long out;
        }data2;

        data1.in = cop1[i];


        data2.in = cop2[i];

        bitset<sizeof(float) * CHAR_BIT> bits1(data1.out), bits1_buff = bits1;

        bitset<sizeof(float) * CHAR_BIT> bits2(data2.out), bits2_buff = bits2;

        size_t flag = rand() % 31;
        for (size_t i = flag; i > 0; i--) {

            bits1_buff.set(i,bits2[i]);
            bits2_buff.set(i,bits1[i]);
        }

        data1.out = bits1_buff.to_ulong();
        data2.out = bits2_buff.to_ulong();

        cop1[i] = mutation(data1.in);
        cop2[i] = mutation(data2.in);
    }
}

vector<float> Genetic_algorithm::result()  {

    float x = 0, y = 0, result = INT_MIN;

    for(size_t i = 0; i < data.size(); i++) {

        if (res[i] > result) {

            x = data[i][0];
            y = data[i][1];
            result = res[i];
        }
    }

    return {x,y,result};
}
