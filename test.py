import unittest
from parser import parser

class TestParser(unittest.TestCase):
    
    def test_parser_give_join_sql1(self):
        sql = """
        SELECT 
            t1.field1,
            t2.field2
        FROM table1 t1
        JOIN table2 AS t2
        ON 
            t1.field3 = t2.field4
        """
        (tables, fields, identifier) = parser(sql)
        
        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0], "table1")
        self.assertEqual(tables[1], "table2")
        self.assertEqual(fields["table1"], ["field1", "field3"])
        self.assertEqual(fields["table2"], ["field2", "field4"])
        self.assertEqual(identifier, [])
    
    def test_parser_give_join_sql2(self):
        sql = """
        SELECT t1.field1, t2.* FROM t1 JOIN t2 USING(field3)
        """
        (tables, fields, identifier) = parser(sql)

        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0], "t1")
        self.assertEqual(tables[1], "t2")
        self.assertEqual(fields["t1"], ["field1", "field3"])
        self.assertEqual(fields["t2"], ["*", "field3"])
        self.assertEqual(identifier, [])

    def test_parser_give_join_sql3(self):
        sql = """
        SELECT field1, field2 FROM t1, t2 WHERE field1 = 'ab' AND field3 = 'cd'
        """ 
        (tables, fields, identifier) = parser(sql)

        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0], "t1")
        self.assertEqual(tables[1], "t2")
        self.assertEqual(len(fields), 0)
        self.assertEqual(identifier, ["field1", "field2", "field3"])

if __name__ == '__main__':
    unittest.main()
