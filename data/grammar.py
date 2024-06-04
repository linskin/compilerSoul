grammar_str1 = ("Z ::= B e\n"
                "A ::= A e\n"
                "A ::= e\n"
                "B ::= C e\n"
                "B ::= A f\n"
                "C ::= C f\n"
                "D ::= f\n"
                "E ::= E\n")
grammar_str2 = ("E ::= E + T | T\n"
                "T ::= T * F | F\n"
                "F ::= ( E ) | i\n")
grammar_str3 = ("A ::= B a | C b | c\n"
                "B ::= d a | A e | f\n"
                "C ::= B g | h")
grammar_str4 = ("Ems ::= Ems + Tfs | Tfs\n"
                "Tfs ::= Tfs * F' | F'\n"
                "F' ::= ( Ems ) | iss\n")
grammar_str5 = ("Z ::= A b | c\n"
                "A ::= A a b | a\n"
                "b ::= c b D | d\n"
                "d ::= b D d | D\n")
grammar_str6 = ("Z ::= E + T\n"
                "E ::= E | S + F | T\n"
                "F ::= F | F P | P\n"
                "P ::= G\n"
                "G ::= G | G G | F\n"
                "T ::= T * i | i\n"
                "Q ::= E | E + F | T | S\n"
                "S ::= i\n")
grammar_str7 = ("S ::= Q c | R d | c\n"
                "Q ::= R b | S e | b\n"
                "R ::= S a | Q f | a")
grammar_str8 = ("Z ::= Z a | A a | B b\n"
                "A ::= B a | a\n"
                "B ::= A b | b")
grammar_str9 = ("group ::= ( ( expr ) ) * \n"
                "expr ::= factor_conn ( | factor_conn ) * \n"
                "factor_conn ::= factor | factor factor * \n"
                "factor ::= ( term | term ( * | + | ? ) ) * \n"
                "term ::= char | [ char - char ] | .")
grammar_str10 = ("E ::= T E'\n"
                 "E' ::= + T E' | ε\n"
                 "T ::= F T'\n"
                 "T' ::= * F T' | ε\n"
                 "F ::= ( E ) | i\n")
grammar_str11 = ("Z ::= E\n"
                 "E ::= T | E + T\n"
                "T ::= F | T * F\n"
                "F ::= ( E ) | i\n")