#include <iostream>
#include <cmath>
#include <array>


long long PRNG(long long prev1, long long prev2, long long prev3, long long modulo,
         long long a, long long b, long long c){
             return (a * prev1 + b * prev2 + c * prev3) % modulo;
}


std::array <long long, 2> Period(long long a, long long b, long long c, long long seed1, long long seed2, long long seed3, long long modulo) {
    long long turtle, can;
    std::array <long long, 3> seed_turtle = {seed1, seed2, seed3};
    std::array <long long, 3> seed_can = {seed1, seed2, seed3};
    bool flag = false;
    long long i = 0;
    while (!flag){
        can = PRNG(seed_can[0], seed_can[1], seed_can[2], modulo, a, b, c);
        seed_can[2] = seed_can[1];
        seed_can[1] = seed_can[0];
        seed_can[0] = can;
        turtle = PRNG(seed_turtle[0], seed_turtle[1], seed_turtle[2], modulo, a, b, c);
        seed_turtle[2] = seed_turtle[1];
        seed_turtle[1] = seed_turtle[0];
        seed_turtle[0] = turtle;
        turtle = PRNG(seed_turtle[0], seed_turtle[1], seed_turtle[2], modulo, a, b, c);
        seed_turtle[2] = seed_turtle[1];
        seed_turtle[1] = seed_turtle[0];
        seed_turtle[0] = turtle;
        flag = seed_turtle == seed_can;
        ++i;
    }
    long long j = 0;
    flag = false;
    while (!flag){
        can = PRNG(seed_can[0], seed_can[1], seed_can[2], modulo, a, b, c);
        seed_can[2] = seed_can[1];
        seed_can[1] = seed_can[0];
        seed_can[0] = can;
        flag = seed_can == seed_turtle;
        ++j;
    }
    seed_turtle = {seed1, seed2, seed3};
    seed_can = {seed1, seed2, seed3};
    for (int i = 0; i < j; ++i) {
        can = PRNG(seed_can[0], seed_can[1], seed_can[2], modulo, a, b, c);
        seed_can[2] = seed_can[1];
        seed_can[1] = seed_can[0];
        seed_can[0] = can;
    }
    flag = seed_turtle == seed_can;
    i = 1;
    while (!flag){
        turtle = PRNG(seed_turtle[0], seed_turtle[1], seed_turtle[2], modulo, a, b, c);
        seed_turtle[2] = seed_turtle[1];
        seed_turtle[1] = seed_turtle[0];
        seed_turtle[0] = turtle;
        can = PRNG(seed_can[0], seed_can[1], seed_can[2], modulo, a, b, c);
        seed_can[2] = seed_can[1];
        seed_can[1] = seed_can[0];
        seed_can[0] = can;
        flag = seed_turtle == seed_can;
        ++i;
    }
    std::array <long long, 2> res = {i - 1, j};
    return res;
}


int main() {
    long long a, b, c, seed1, seed2, seed3, modulo, rnd, index;
    //std::cin >> a >> b >> c >> modulo >> seed1 >> seed2 >> seed3;

    a = 1000004;
    b = 696969;
    c = 159753;
    seed1 = 66666;
    seed2 = 1;
    seed3 = 2;
    modulo = 3;

    // a = 890;
    // b = 321;
    // c = 1238;
    // seed1 = 0;
    // seed2 = 2134;
    // seed3 = 756;
    // modulo = 2197;

    long long array[20];
    for (int i = 0; i < 20; i++){
        array[i] = 0;
    }
    std::array <long long, 2> perdiod =  Period(a, b, c, seed1, seed2, seed3, modulo);
    std::cout << "Preperiod = " << perdiod[0] << std::endl;
    std::cout << "Period = " << perdiod[1] << std::endl;
    index = std::trunc((double)seed1 / modulo * 100 / 5);
    ++array[index];
    index = std::trunc((double)seed2 / modulo * 100 / 5);
    ++array[index];
    index = std::trunc((double)seed3 / modulo * 100 / 5);
    ++array[index];
    for (int i = 0; i < 400; ++i){
        rnd = PRNG(seed1, seed2, seed3, modulo, a, b, c);
        seed1 = seed2;
        seed2 = seed3;
        seed3 = rnd;
        //
        // seed3 = seed2;
        // seed2 = seed1;
        // seed1 = rnd;
        //std::cout << (double)rnd / modulo << " " << std::ceil((double)rnd / modulo * 20) - (rnd != 0) << std::endl;
        index = std::trunc((double)rnd / modulo * 100 / 5);
        ++array[index];
    }
    double diff = 0;
    for (int i = 0; i < 20; ++i){
        diff += pow(array[i] - 20, 2) / 400;
    }
    std::cout << "Quality = " << diff << std::endl;
    return 0;
}
