import unittest

# util_test: utils for testing

class SentenceSeekerTest(unittest.TestCase):
    TestsExecutedOnly = []

    def _test_exec(self, TestCaseName):
        if not self.TestsExecutedOnly: # if emtpy, test can be executed
            return True
        # if TexecutedOnly has element, exec the test if it's in Executedlist
        if TestCaseName in self.TestsExecutedOnly:
            return True
        else:
            print("\n\nTest temporarily not executed: " + TestCaseName)
            return False

    def setUp(self):
        print("\nTESTING: setUp")
        self.Prg["TestExecution"] = True

    # https://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method/39606065#39606065
    def tearDown(self):
        print("\nTESTING: tearDown")
        self.Prg["TestExecution"] = False

        def list2reason(exc_list):
            if exc_list and exc_list[-1][0] is self:
                return exc_list[-1][1]

        Result = self.defaultTestResult()  # these 2 methods have no side effects
        self._feedErrorsToResult(Result, self._outcome.errors)
        Error = list2reason(Result.errors)
        Failure = list2reason(Result.failures)
        Ok = not Error and not Failure
        self.Prg["TestResults"].append({"status_ok": Ok, "Error": Error, "Failure": Failure})


def result_all(Prg):
    TitlePrinted = False

    for TestResult in Prg["TestResults"]:
        if not TestResult["status_ok"]:
            if not TitlePrinted:
                TitlePrinted = True
                print("=== TestResults: ===")
            print(TestResult)
