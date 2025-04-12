#include "pch.h"
#include "CppUnitTest.h"
#include "../QualityAndTesting 5 Lab/QualityAndTesting 5 Lab.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTest
{
	TEST_CLASS(UnitTest)
	{
	public:
		
		TEST_METHOD(TestN0)
		{
			int k = 6;
            int n = 0;
			int* arr = nullptr;

            string expected = "Неправильные исходные данные";
			string result;

			try {
				countTransmitters(arr, n, k);
			}
			catch (exception e) {
				result = e.what();
			}

            Assert::AreEqual(expected, result);
		}

		TEST_METHOD(TestK0)
		{
			int k = 0;
			int n = 5;
			int arr[5] = { 3, 1, 4, 6, 2 };

			string expected = "Неправильные исходные данные";
			string result;

			try {
				countTransmitters(arr, n, k);
			}
			catch (exception e) {
				result = e.what();
			}

			Assert::AreEqual(expected, result);
		}

		TEST_METHOD(TestExistXNonPositive)
		{
			int k = 6;
			int n = 5;
			int arr[5] = { 3, -1, 4, 0, 2 };

			string expected = "Неправильные исходные данные";
			string result;

			try {
				countTransmitters(arr, n, k);
			}
			catch (exception e) {
				result = e.what();
			}

			Assert::AreEqual(expected, result);
		}

		TEST_METHOD(TestTwoHousesInRow)
		{
			int k = 4;
			int n = 3;
			int arr[3] = { 19, 23, 24  };

			int expected = 1;
			int result = countTransmitters(arr, n, k);

			Assert::AreEqual(expected, result);
		}

		TEST_METHOD(TestNoTwoHousesInRow)
		{
			int k = 7;
			int n = 2;
			int arr[3] = { 1, 9 };

			int expected = 2;
			int result = countTransmitters(arr, n, k);

			Assert::AreEqual(expected, result);
		}
	};
}
