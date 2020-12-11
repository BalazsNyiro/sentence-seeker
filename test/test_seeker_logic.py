# -*- coding: utf-8 -*-
import unittest, util_test
import text, result_selectors
import os.path
import tokens

class SeekerLogicTests(util_test.SentenceSeekerTest):

    def test_is_operator(self):
        if self._test_exec("test_is_operator"):

            self.assertFalse(tokens.is_operator("Mother"))
            self.assertFalse(tokens.is_operator("and"))
            self.assertFalse(tokens.is_operator("Or"))

            # not operator, not string
            self.assertFalse(tokens.is_operator(["big", "AND", "car"]))

            self.assertTrue(tokens.is_operator("("))
            self.assertTrue(tokens.is_operator(")"))
            self.assertTrue(tokens.is_operator("AND"))
            self.assertTrue(tokens.is_operator("OR"))


    def test_token_split(self):
        if self._test_exec("test_token_split"):
            Query = "like 1945"
            Wanted = ["like", "AND", "1945"]
            self.assertEqual(tokens.token_split(Query), Wanted)

            Query = "(apple   house,mouse)"
            Wanted = ["(", "apple", "AND", "house", "AND", "mouse", ")"]
            self.assertEqual(tokens.token_split(Query), Wanted)

            Query = "(every OR special) AND (events OR (bird OR audience))"
            TokensDetected = tokens.token_split(Query)
            TokensWanted = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            self.assertEqual(TokensDetected, TokensWanted)

            Query = "birds (are OR  singing) AND (is)"
            TokensDetected = tokens.token_split(Query)
            TokensWanted = ["birds", "AND", "(", "are", "OR", "singing", ")", "AND", "(", "is", ")"]
            self.assertEqual(TokensDetected, TokensWanted)

    def test_token_split_and(self):
        if self._test_exec("test_token_split_and"):
            Query = "apple  house"
            Wanted = ["apple", "AND", "house"]
            TokensDetected = tokens.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

            Query = "(apple) (house)"
            Wanted = ["(", "apple", ")", "AND", "(", "house", ")"]
            TokensDetected = tokens.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

            Query = "(apple) house"
            Wanted = ["(", "apple", ")", "AND", "house"]
            TokensDetected = tokens.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

            Query = "apple (house)"
            Wanted = ["apple", "AND", "(", "house", ")"]
            TokensDetected = tokens.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

            Query = "apple (house) (mouse)"
            Wanted = ["apple", "AND", "(", "house", ")", "AND", "(", "mouse", ")"]
            TokensDetected = tokens.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

            Query = "apple ((house) (mouse))"
            Wanted = ["apple", "AND", "(", "(", "house", ")", "AND", "(", "mouse", ")", ")"]
            TokensDetected = tokens.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

    def test_token_group_finder(self):
        if self._test_exec("test_token_group_finder"):
            Tokens = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            TokenGroupsDetected = tokens.token_group_finder(Tokens)
            TokenGroupsWanted = [['every', 'OR', 'special'], 'AND', ['events', 'OR', ['bird', 'OR', 'audience']]]
            self.assertEqual(TokenGroupsDetected, TokenGroupsWanted)

def run_all_tests(Prg):
    SeekerLogicTests.Prg = Prg
    # I can't use self.Prg when I define class variable so I set FilePath from here
    SeekerLogicTests.FileNameBird = "bird.txt"
    SeekerLogicTests.FileBaseNameBirdWithoutExt = "test_document_bird"
    SeekerLogicTests.FilePathBird = os.path.join(Prg["DirDocuments"], SeekerLogicTests.FileNameBird)
    unittest.main(module="test_seeker_logic", verbosity=2, exit=False)

