male(jack).
male(oliver).
male(ali).
male(james).
male(simon).
male(harry).
female(helen).
female(sophie).
female(jess).
female(lily).
parent_of(jack, jess).
parent_of(jack, lily).
parent_of(helen, jess).
parent_of(helen, lily).
parent_of(oliver, james).
parent_of(sophie, james).
parent_of(jess, simon).
parent_of(ali, simon).
parent_of(lily, harry).
parent_of(james, harry).
therapist_of(dr_smith, simon).
therapist_of(dr_smith, lily).
therapist_of(dr_jones, james).
therapist_of(dr_jones, jess).
therapist_of(dr_clark, harry).
issue(simon, anxiety).
issue(lily, depression).
issue(james, stress).
issue(jess, grief).
issue(harry, trauma).
father_of(X, Y) :- male(X),parent_of(X, Y).
mother_of(X, Y) :- female(X),parent_of(X, Y).
grandfather_of(X, Y) :- male(X),parent_of(X, Z),parent_of(Z, Y).
grandmother_of(X, Y) :- female(X),parent_of(X, Z),parent_of(Z, Y).
is_therapist(X, Y) :- therapist_of(X, Y).
clients_of(Therapist, Clients) :- findall(Client,therapist_of(Therapist, Client), Clients).
deals_with(Client, Issue) :- issue(Client, Issue).
needs_help(Client) :- issue(Client, _).
find_therapist(Client, Therapist) :- therapist_of(Therapist, Client).
shared_therapist(Client1, Client2, Therapist) :- therapist_of(Therapist, Client1),therapist_of(Therapist, Client2).