// Matrix Multiplier

#include <iostream>
#include <vector>
using namespace std;

float dot_product(vector<float> vector_one,
                  vector<float> vector_two) {
  vector<float> elements;
  for (int i = 0; i < vector_one.size(); ++i) {
    elements.push_back(vector_one[i] * vector_two[i]);
  }

  float sum = 0;
  for (int i = 0; i < elements.size(); ++i) {
    sum += elements[i];
  }
  return sum;
}

vector< vector<float> > matrix_multiplication(
  vector< vector<float> > matrix1,
  vector< vector<float> > matrix2) {

  vector< vector<float> > multiplied;
  vector<float> row_multiplied;

  for (int rowA = 0; rowA < )
}


int main() {
  
}