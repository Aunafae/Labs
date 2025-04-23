import importlib.util
import json
from pathlib import Path


class TestDriver:
    def __init__(self, module_path, test_file):
        self.module_path = module_path
        self.test_file = test_file

    def load_module(self, module_name):
        spec = importlib.util.spec_from_file_location(module_name, self.module_path / f"{module_name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_tests(self):
        with open(self.test_file, 'r') as file:
            tests = json.load(file)
        
        results = []
        for i, test in enumerate(tests, start=1):
            try:
                module = self.load_module(test['module'])
                func = getattr(module, test['name'], None)
                
                arr = test['arr'][0]
                k = test['k'][0]
                n = test['n'][0]

                result = func(arr, n, k)
                expected_result = test['expected_result']
                status = 'success' if result == expected_result else 'failed'
                message = '' if status == 'success' else f"Expected {expected_result}, got {result}"

                results.append({
                    'test_number': i,
                    'received_result': result,
                    'expected_result': expected_result,
                    'status': status,
                    'message': message
                })
            
            except Exception as e:
                received_message = str(e)
                expected_message = test.get('expected_result', '')
                status = 'success' if received_message == expected_message else 'failed'

                results.append({
                    'test_number': i,
                    'received_result': received_message,
                    'expected_result': expected_message,
                    'status': status,
                    'message': '' if status == 'success' else f"Expected {expected_message}, got {received_message}"
                })
        
        return results

    def generate_report(self, results):
        for result in results:
            report = "\n"
            report += f"\nTest #{result['test_number']}: {'Success' if result['status'] == 'success' else 'Failed'}" 
            report += f"\n\tReceived Result: {result['received_result']}" 
            report += f"\n\tExpected Result: {result['expected_result']}"  
            report += f"\n\tMessage: {result['message']}" if result['message'] else ""
            print(report)


if __name__ == "__main__":
    module_path = Path("test_modules")
    test_file = "tests.json"

    driver = TestDriver(module_path, test_file)
    results = driver.run_tests()
    driver.generate_report(results)