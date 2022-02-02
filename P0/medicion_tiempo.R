library(pryr)

M = function(n) {k = 15^n; return(matrix(runif(k*k), nrow = k))}

for (n in 8:20) 
{
