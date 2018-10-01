'''
– std::cout 
– std::cin 
– std::cerr 
– std::clog 

– std::itoa: convert integer to a string
– std::atoi: convert string to integer
– std::atof convert string to double

typedef unsigned int Counter;

enum PositionType { Equity = 1 , Bond = 2, Option = 3 };
PositionType posType = Equity;

if (posType == Equity){
    cout << "processing equity position" << endl; 
} else if (posType == Bond){
    cout << "processing bond position" << endl; 
} else if (posType == Option){
    cout << "processing option position" << endl; 
} else {
    cout << "unexpected position type" << endl; 
}

switch (posType){
case Equity:
cout << "processing equity position" << endl;
case Bond:
cout << "processing bond position" << endl;
case Option:
cout << "processing option position" << endl;
default:
cout << "unexpected position type" << endl;
}

std::string class
length() 
substr()
at() instead of []

Loops:
for (unsigned int i = 1; i < 10; i++){ 
    std::cout << i << std::endl;
}

unsigned int i = 1; 
while (i < 10){
    std::cout << i << std::endl;
    i++; 
}

reading and writing files:
std::string fname = "test.txt"; 
std::ifstream file ( fname ); 
std::string line;
while (getline(file, line)){
    std::cout << line; 
}
file.close();

std::string fname = "test.txt"; 
std::ofstream file (fname);
file << "SPY" << ", " << "QQQ" << std::endl; 
file.close();

passing by const reference.

array:
int intArr [] = {};
int intArr [10];

new and delete:
int main(int argc, const char * argv[]) { 
    std::vector<int>* vecIntPtr(new std::vector<int>());
    vecIntPtr->push_back(0.0); 
    vecIntPtr->push_back(5.0);
    delete vecIntPtr;
    return 0.0; }

std::vectors(multi-dimensional)
push back() and at()
begin() and end() (iterator)
std::vector<int> vecInt(5, 100); 
int tmp = vecInt.at(10);
vecInt.push_back(200);

std::maps
insert() at()
begin() and end() (interator)

'''

