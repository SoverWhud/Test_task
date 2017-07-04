#pragma once
#include <mutex>
#include <vector>

#include "array.h"

typedef unsigned int uint;
typedef unsigned char unchar;


class MyWork
{
public:
	//MyWork(); //Constructor
	//~MyWork(); //Deconstructor

	//Функции добавления объекта
	static void add_object(double* arr, int row_size, int column_size, int indent, int signal)
	{
		int row = row_size / 2;
		int col = column_size / 2;
		arr[row * indent + col] = signal;
	}

	double m1(const std::vector<ArrayDouble*>& vector_array) { if (_m1 <= 0) _m1 = m(vector_array, 1); return _m1; }

	double M2(const std::vector<ArrayDouble*>& vector_array)
	{
		if (_M2 <= 0)
			_M2 = m2(vector_array) - pow(m1(vector_array), 2);

		return _M2;
	}

	//Функции расчета коэффициента асимметрии
	double skewness(double* arr, int row_size, int column_size, int indent)
	{
		return M3(arr, row_size, column_size, indent) / sqrt(pow(M2(arr, row_size, column_size, indent), 3));
	}

	//Функции расчета коэффициента эксцесса
	double excess(double* arr, int row_size, int column_size, int indent)
	{
		return M4(arr, row_size, column_size, indent) / (pow(M2(arr, row_size, column_size, indent), 2)) - 3;
	}


	void empty_all()
	{
		_m1 = 0;
		_m2 = 0;
		_m3 = 0;
		_m4 = 0;

		_M2 = 0;
		_M3 = 0;
		_M4 = 0;
	}

private:
	double _m1{ 0.0 };
	double _m2{ 0.0 };
	double _m3{ 0.0 };
	double _m4{ 0.0 };
	
	double _M2{ 0.0 };
	double _M3{ 0.0 };
	double _M4{ 0.0 };

	//Функция расчета начального момента k - порядка
	double m(double* arr, int k, int row_size, int column_size, int indent);
	double m(const std::vector<ArrayDouble*>& vector_array, const int k);

	double m1(double* arr, int row_size, int column_size, int indent) { if (_m1 <= 0) _m1 = m(arr, 1, row_size, column_size, indent); return _m1; }

	double m2(double* arr, int row_size, int column_size, int indent) { if (_m2 <= 0) _m2 = m(arr, 2, row_size, column_size, indent); return _m2; }
	double m2(const std::vector<ArrayDouble*>& vector_array) { if (_m2 <= 0) _m2 = m(vector_array, 2); return _m2; }

	double m3(double* arr, int row_size, int column_size, int indent) { if (_m3 <= 0) _m3 = m(arr, 3, row_size, column_size, indent); return _m3; }
	double m4(double* arr, int row_size, int column_size, int indent) { if (_m4 <= 0) _m4 = m(arr, 4, row_size, column_size, indent); return _m4; }

	//Функции расчета центральных моментов
	double M2(double* arr, int row_size, int column_size, int indent)
	{
		if (_M2 <= 0)
			_M2 = m2(arr, row_size, column_size, indent) - pow(m1(arr, row_size, column_size, indent), 2);

		return _M2;
	}

	double M3(double* arr, int row_size, int column_size, int indent)
	{
		if (_M3 <= 0)
			_M3 = m3(arr, row_size, column_size, indent) - 3 * m1(arr, row_size, column_size, indent) * m2(arr, row_size, column_size, indent) + 2 * (pow(m1(arr, row_size, column_size, indent), 3));

		return _M3;
	}

	double M4(double* arr, int row_size, int column_size, int indent)
	{
		if (_M4 <= 0)
			_M4 = m4(arr, row_size, column_size, indent) - 4 * m3(arr, row_size, column_size, indent) * m1(arr, row_size, column_size, indent) +
			6 * m2(arr, row_size, column_size, indent) * (pow(m1(arr, row_size, column_size, indent), 2)) - 3 * (pow(m1(arr, row_size, column_size, indent), 4));

		return _M4;
	}
};
