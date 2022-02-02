library(pryr)

M = function(n) {k = 2^n; return(matrix(runif(k*k), nrow = k))}

for (n in 5:10) 
{
