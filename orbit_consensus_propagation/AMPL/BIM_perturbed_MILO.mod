
var x1 integer >= 0;
var x2 integer >= 0;

maximize profit: 12 * x1 + 9 * x2;

s.t. silicon: x1 <= 1000;
s.t. germanium: x2 <= 1500;
s.t. plastic: x1 + x2 <= 1750;
s.t. copper: 4.04 * x1 + 2.02 * x2 <= 4800;
